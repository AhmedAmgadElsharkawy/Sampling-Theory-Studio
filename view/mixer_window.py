import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QApplication,QLineEdit,QLabel
)
import pyqtgraph as pg

# from controller.mixer_controller import MixerController
from model.signal_model import Signal



class MixerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mixed_signal = Signal()
        self.setWindowTitle('Signals Mixer')
        self.setGeometry(100, 100, 1400, 900)
        self.is_dark_mode = True
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.mix_output_signal_plot = pg.PlotWidget()
        self.mix_output_signal_curve = self.mix_output_signal_plot.plot(pen = 'r')
        
        self.props_and_components_container_widget = QWidget()
        self.props_and_components_container_layout = QHBoxLayout()
        self.props_and_components_container_widget.setLayout(self.props_and_components_container_layout)
        
        self.props_widget = QWidget()
        self.props_layout = QVBoxLayout()
        self.props_widget.setLayout(self.props_layout)
        
        self.frequency_prop_container_widget = QWidget()
        self.frequency_prop_container_layout = QHBoxLayout()
        self.frequency_prop_container_widget.setLayout(self.frequency_prop_container_layout)
        self.frequency_input_field_label = QLabel("Frequency")
        self.frequency_input_field = QLineEdit()
        self.frequency_prop_container_layout.addWidget(self.frequency_input_field_label)
        self.frequency_prop_container_layout.addWidget(self.frequency_input_field)

        self.amplitude_prop_container_widget = QWidget()
        self.amplitude_prop_container_layout = QHBoxLayout()
        self.amplitude_prop_container_widget.setLayout(self.amplitude_prop_container_layout)
        self.amplitude_input_field_label = QLabel("Amplitude")
        self.amplitude_input_field = QLineEdit()
        self.amplitude_prop_container_layout.addWidget(self.amplitude_input_field_label)
        self.amplitude_prop_container_layout.addWidget(self.amplitude_input_field)

        self.phase_shift_prop_container_widget = QWidget()
        self.phase_shift_prop_container_layout = QHBoxLayout()
        self.phase_shift_prop_container_widget.setLayout(self.phase_shift_prop_container_layout)
        self.phase_shift_input_field_label = QLabel("Phase")
        self.phase_shift_input_field = QLineEdit()
        self.phase_shift_prop_container_layout.addWidget(self.phase_shift_input_field_label)
        self.phase_shift_prop_container_layout.addWidget(self.phase_shift_input_field)
        
        self.props_layout.addWidget(self.amplitude_prop_container_widget)
        self.props_layout.addWidget(self.frequency_prop_container_widget)
        self.props_layout.addWidget(self.phase_shift_prop_container_widget)


        
        




        self.components_widget = QWidget()
        self.components_layout = QVBoxLayout()
        self.components_widget.setLayout(self.components_layout)

        self.components_label = QLabel("Components")
        self.components_list_widget = QWidget()
        self.components_list_layout = QVBoxLayout()
        self.components_list_widget.setLayout(self.components_list_layout)

        self.components_layout.addWidget(self.components_label)
        self.components_layout.addWidget(self.components_list_widget)


        






        self.props_and_components_container_layout.addWidget(self.props_widget)
        self.props_and_components_container_layout.addWidget(self.components_widget)


        self.main_layout.addWidget(self.mix_output_signal_plot)
        self.main_layout.addWidget(self.props_and_components_container_widget)
        

        # self.mixer_controller = MixerController(self)

        

        



