import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSlider, QPushButton, QComboBox, QFrame, QGroupBox,QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import pyqtgraph as pg

from model.signal_model import Signal

from controller.error_plot_controller import ErrorPlotController
from controller.frequency_plot_controller import  FrequencyPlotController
from controller.sampling_controller import SamplingController
from controller.load_signal_controller import LoadSignalController


# temporary hard coded signal data
from data.temporary_signal import (hard_coded_x_data , hard_coded_y_data)

from view.mixer_window import MixerWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals_list = []
        self.displayed_signal = Signal()
        self.interpolation_method = "Whittaker-Shannon"

        # # Set temporary hard coded signal data
        # self.displayed_signal.x_data = hard_coded_x_data
        # self.displayed_signal.y_data = hard_coded_y_data
        # self.displayed_signal.max_frequency = 62
        # self.displayed_signal.original_y = hard_coded_y_data
        
        self.setWindowTitle('Sampling Theory Studio')
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon("icon.png"))
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.frequency_plot_controller = FrequencyPlotController(self)
        self.sampling_controller = SamplingController(self)

        self.create_signal_display()
        self.create_control_panel()

        self.main_layout.addLayout(self.graph_layout, 4)
        self.main_layout.addLayout(self.control_layout, 1)

        self.error_plot_controller = ErrorPlotController(self)
        self.load_signal_controller = LoadSignalController(self)
        self.signal_mixer_button.clicked.connect(self.open_mixer_window)
        
        




    def open_mixer_window(self):
        self.mixer_window = MixerWindow(self)
        self.mixer_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.mixer_window.show()

    def open_mixer_window(self):
        self.mixer_window = MixerWindow(self)
        self.mixer_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.mixer_window.show()

    def create_signal_display(self):
        self.graph_layout = QVBoxLayout()
        self.graph_layout.setSpacing(0)

        self.original_signal_plot = pg.PlotWidget(title="Original Signnal")
        self.reconstructed_signal_plot =pg.PlotWidget(title="Reconstructed Signal")
        self.error_signal_plot = pg.PlotWidget(title="Error Signal")
        self.frequency_domain_plot = pg.PlotWidget(title="Frequency Domain")

        self.original_signal_plot.showGrid(x=True, y=True)
        self.reconstructed_signal_plot.showGrid(x=True, y=True)
        self.error_signal_plot.showGrid(x=True, y=True)
        self.frequency_domain_plot.showGrid(x=True, y=True)

        self.graph_layout.addWidget(self.original_signal_plot)
        self.graph_layout.addWidget(self.reconstructed_signal_plot)
        self.graph_layout.addWidget(self.error_signal_plot)
        self.graph_layout.addWidget(self.frequency_domain_plot)

    def create_control_panel(self):
        self.control_layout = QVBoxLayout()
        self.control_group = QGroupBox("Controls")
        self.control_group.setStyleSheet(
            "background-color: #2B2B2B; border: 2px solid #A0A0A0; padding: 10px;"
        )
        self.control_group_layout = QVBoxLayout(self.control_group)
        font = QFont("Arial", 10, QFont.Weight.Bold)

        self.sampling_freq_group = QGroupBox()
        self.sampling_freq_group.setStyleSheet("border: none; padding: 5px;")
        self.sampling_freq_layout = QVBoxLayout(self.sampling_freq_group)
        self.sampling_freq_label = QLabel("Sampling Frequency (Hz): 1")
        self.sampling_freq_label.setFont(font)
        self.sampling_freq_label.setStyleSheet("color: white;")
        self.sampling_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.sampling_freq_slider.setRange(1, 400)
        self.sampling_freq_slider.setValue(0)
        self.sampling_freq_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.sampling_freq_layout.addWidget(self.sampling_freq_label)
        self.sampling_freq_layout.addWidget(self.sampling_freq_slider)

        self.snr_group = QGroupBox()
        self.snr_group.setStyleSheet("border: none; padding: 5px;")
        self.snr_layout = QVBoxLayout(self.snr_group)
        self.snr_label = QLabel("Signal-to-Noise Ratio (dB): 100")
        self.snr_label.setFont(font)
        self.snr_label.setStyleSheet("color: white;")
        self.snr_slider = QSlider(Qt.Orientation.Horizontal)
        self.snr_slider.setRange(1, 100)
        self.snr_slider.setValue(100)
        self.snr_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.snr_layout.addWidget(self.snr_label)
        self.snr_layout.addWidget(self.snr_slider)

        self.reconstruction_method_group = QGroupBox("Reconstruction Method")
        self.reconstruction_method_group.setStyleSheet(
            "border: 2px solid #A0A0A0; padding: 5px; color: white;"
        )
        self.reconstruction_method_layout = QVBoxLayout(self.reconstruction_method_group)
        self.reconstruction_combo = QComboBox()
        self.reconstruction_combo.addItems(["Whittaker-Shannon", "Linear", "CubicSpline"])
        
        self.reconstruction_combo.currentIndexChanged.connect(self.sampling_controller.change_reconstruction_method)
        
        self.reconstruction_method_layout.addWidget(self.reconstruction_combo)
        
        
        self.load_signal_button = QPushButton("Load Signal")
        self.load_signal_button.setFont(font)
        self.load_signal_button.setStyleSheet("""
            QPushButton {
                background-color: #A5D6A7;
                color: black;
                padding: 10px 20px;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #81C784;
            }
        """)

        self.signal_mixer_button = QPushButton("Signal Mixer")
        self.signal_mixer_button.setFont(font)
        self.signal_mixer_button.setStyleSheet("""
            QPushButton {
                background-color: #A5D6A7;
                color: black;
                padding: 10px 20px;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #81C784;
            }
        """)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.load_signal_button)
        self.button_layout.addWidget(self.signal_mixer_button)

        # self.placeholder_box = QFrame()
        # self.placeholder_box.setFrameShape(QFrame.Shape.Box)
        # self.placeholder_box.setFrameShadow(QFrame.Shadow.Raised)
        # self.placeholder_box.setStyleSheet("border: 2px solid white;")
        # self.placeholder_box.setFixedHeight(380)

        # self.signal_layout = QHBoxLayout()
        # self.signal_1_label = QLabel("Signal 1")
        # self.signal_1_label.setFont(font)
        # self.signal_1_label.setStyleSheet("color: white; background: transparent; border: none;")

        # self.eye_button = QPushButton()
        # self.eye_button.setIcon(QIcon("eye.png"))
        # self.eye_button.setFixedSize(40, 40)
        # self.eye_button.setStyleSheet("""
        #     QPushButton {
        #         border: none;
        #         background: transparent;
        #     }
        #     QPushButton:hover {
        #         background-color: rgba(255, 255, 255, 0.2);
        #     }
        # """)

        # self.trash_button = QPushButton()
        # self.trash_button.setIcon(QIcon("trash.png"))
        # self.trash_button.setFixedSize(40, 40)
        # self.trash_button.setStyleSheet("""
        #     QPushButton {
        #         border: none;
        #         background: transparent;
        #     }
        #     QPushButton:hover {
        #         background-color: rgba(255, 255, 255, 0.2);
        #     }
        # """)

        # self.signal_layout.addWidget(self.signal_1_label)
        # self.signal_layout.addWidget(self.eye_button)
        # self.signal_layout.addWidget(self.trash_button)


        # self.placeholder_layout.setAlignment(self.signal_layout, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.signals_scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget_layout = QVBoxLayout()
        self.scroll_area_widget.setLayout(self.scroll_area_widget_layout)
        self.signals_scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area_widget.setStyleSheet("border:none;""padding:0px;""margin:0px")
        self.signals_scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.sampling_freq_slider.valueChanged.connect(self.change_sampling_freq)
        self.snr_slider.valueChanged.connect(self.handle_snr_change)

        self.control_group_layout.addWidget(self.sampling_freq_group)
        self.control_group_layout.addWidget(self.snr_group)
        self.control_group_layout.addWidget(self.reconstruction_method_group)
        self.control_group_layout.addLayout(self.button_layout)
        self.control_group_layout.addWidget(self.signals_scroll_area)

        self.control_layout.addWidget(self.control_group)

    def update_label(self, label, value):
        label.setText(f"{label.text().split(':')[0]}: {value}")

    def change_sampling_freq(self, value):
        # Call the method in SamplingController
        self.sampling_freq_label.setText(f"{self.sampling_freq_label.text().split(':')[0]}: {value}")
        self.sampling_controller.change_sampling_freq(value)

    def handle_snr_change(self, value):
        # Call the method in SamplingController
        self.snr_label.setText(f"{self.snr_label.text().split(':')[0]}: {value}")
        self.sampling_controller.change_SNR(value)
