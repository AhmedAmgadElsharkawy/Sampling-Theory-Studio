import os
import pandas as pd
from PyQt6.QtWidgets import QFileDialog,QLabel,QPushButton,QHBoxLayout,QWidget,QScrollArea
from PyQt6.QtGui import QIcon,QFont
from model.signal_model import Signal
from PyQt6.QtCore import Qt


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
        data = pd.read_csv(file_path).iloc[:,0:2]
        self.x = data.iloc[:,0]
        self.y = data.iloc[:,1]
        signal = Signal()
        signal.x_data = data.iloc[:,0]
        signal.y_data = data.iloc[:,1]
        # self.main.signals_list.append(signal)
        signalName = os.path.splitext(os.path.basename(file_path))[0]
        self.add_signal_to_signals_scroll_area(signal_name = signalName,signal = signal)
    
    def add_signal_to_signals_scroll_area(self,signal_name,signal):
        signal_item = SignalItem(self.main,signal,signal_name)
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

        self.eye_button = QPushButton()
        if(self.main.scroll_area_widget_layout.count() == 0):
            self.eye_button.setIcon(QIcon("assets/icons/show.svg"))
        else:
            self.eye_button.setIcon(QIcon("assets/icons/hide.svg"))
        self.eye_button.setFixedSize(30, 30)
        self.eye_button.setStyleSheet("""
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
        self.signal_layout.addWidget(self.eye_button)
        self.signal_layout.addWidget(self.trash_button)

        


        
        
    