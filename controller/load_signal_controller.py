import os
import pandas as pd
from PyQt6.QtWidgets import QFileDialog,QLabel,QPushButton,QHBoxLayout,QWidget,QScrollArea
from PyQt6.QtGui import QIcon,QFont
from model.signal_model import Signal
from PyQt6.QtCore import Qt
import math


class LoadSignalController:
    def __init__(self,main):
        self.main = main
        self.main.load_signal_button.clicked.connect(self.browse_file)

    def browse_file(self):
        file_dialog = QFileDialog(self.main)
        file_path, _ = file_dialog.getOpenFileName(self.main, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.add_signal(file_path)

    def add_signal(self, file_path):
        if not file_path:
            pass
        data = pd.read_csv(file_path).iloc[:,:]
        signal = Signal()
        signal.x_data = list(data.iloc[:1000,0])
        signal.y_data = list(data.iloc[:1000,1])
        signal.original_y = list(data.iloc[:1000,1])
        signal.max_frequency = float(data.iloc[0,2])
        signalName = os.path.splitext(os.path.basename(file_path))[0]
        self.add_signal_to_signals_scroll_area(signal_name = signalName,signal = signal)
    
    def add_signal_to_signals_scroll_area(self,signal_name,signal):
        signal_item = SignalItem(self.main,signal,signal_name)
        if(self.main.scroll_area_widget_layout.count() == 0):
            signal_item.show_signal()
        self.main.scroll_area_widget_layout.addWidget(signal_item)

        
      


class SignalItem(QWidget):
    def __init__(self,main,signal,signal_name):
        super().__init__()
        self.main = main
        self.signal = signal
        self.signal_name = signal_name
        font = QFont("Arial", 10, QFont.Weight.Bold)
        self.signal_layout = QHBoxLayout()
        self.setLayout(self.signal_layout)
        self.signal_label = QLabel(self.signal_name)
        self.signal_label.setFont(font)
        self.signal_label.setStyleSheet("color: white; background: transparent; border: none;")

        self.eye_button_show = QPushButton()
        self.eye_button_hide = QPushButton()
        self.eye_button_show.setIcon(QIcon("assets/icons/hide.svg"))
        self.eye_button_hide.setIcon(QIcon("assets/icons/show.svg"))
        self.eye_button_show.setFixedSize(30, 30)
        self.eye_button_hide.setFixedSize(30, 30)
        self.eye_button_show.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.eye_button_hide.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        self.trash_button = QPushButton()
        self.trash_button.setIcon(QIcon("assets/icons/delete.svg"))
        self.trash_button.setFixedSize(30, 30)
        self.trash_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        self.signal_layout.addWidget(self.signal_label)
        self.signal_layout.addStretch()
        self.signal_layout.addWidget(self.eye_button_show)
        self.signal_layout.addWidget(self.eye_button_hide)
        self.eye_button_show.setVisible(False)
        self.signal_layout.addWidget(self.trash_button)

        self.eye_button_hide.clicked.connect(self.show_signal)
        self.trash_button.clicked.connect(self.delete_signal)

    def show_signal(self):
        self.hide_signals()
        self.eye_button_hide.setVisible(False)
        self.eye_button_show.setVisible(True)
        self.main.displayed_signal = self.signal
        self.main.displayed_signal.sample_signal()
        self.main.sampling_controller.change_sampling_freq(1)
        self.main.sampling_freq_slider.setEnabled(True)
        self.main.sampling_freq_slider.setRange(1, int(math.ceil(4 * self.main.displayed_signal.max_frequency)))
        self.main.sampling_freq_slider.setValue(1)
        self.main.nyquist_rate_slider.setEnabled(True)
        self.main.nyquist_rate_slider.setValue(0)
        self.main.snr_slider.setEnabled(True)
        self.main.reconstruction_combo.setEnabled(True)

    def hide_signals(self):
        for i in range(self.main.scroll_area_widget_layout.count()):
            signalItem = self.main.scroll_area_widget_layout.itemAt(i).widget()
            signalItem.eye_button_hide.setVisible(True)
            signalItem.eye_button_show.setVisible(False)

    def delete_signal(self):
        self.main.sampling_controller.clear_plots()
        self.main.scroll_area_widget_layout.removeWidget(self)
        if(self.main.scroll_area_widget_layout.count() == 0):
            self.main.displayed_signal = None
            self.main.sampling_freq_slider.setEnabled(False)
            self.main.snr_slider.setEnabled(False)
            self.main.reconstruction_combo.setEnabled(False)
        else:
            self.main.scroll_area_widget_layout.itemAt(0).widget().show_signal()
        self.deleteLater()
            
        


        
        
    