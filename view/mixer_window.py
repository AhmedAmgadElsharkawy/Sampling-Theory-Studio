import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QApplication,QLineEdit,QLabel,QScrollArea,QPushButton
)
import pyqtgraph as pg

from controller.mixer_controller import MixerController
from model.signal_model import Signal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QDialog





class MixerWindow(QDialog):
    def __init__(self,main):
        super().__init__()
        self.main = main
        self.mixed_signal = Signal()
        self.components_list = []
        self.setWindowTitle('Signals Mixer')
        self.setGeometry(300, 200, 800, 600)
        self.is_dark_mode = True
        # self.main_widget = QWidget(self)
        # self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self)


        self.mix_output_signal_plot = pg.PlotWidget()
        self.mix_output_signal_plot.showGrid(x=True, y=True)  # Enable grid for both x and y axes
        self.mix_output_signal_curve = self.mix_output_signal_plot.plot(pen = 'r')

        
        self.props_and_components_and_buttons_container_widget = QWidget()
        self.props_and_components_and_buttons_container_layout = QHBoxLayout()
        self.props_and_components_and_buttons_container_widget.setLayout(self.props_and_components_and_buttons_container_layout)

        self.props_and_components_container_widget = QWidget()
        self.props_and_components_container_widget.setFixedWidth(600)
        self.props_and_components_container_widget.setFixedHeight(250) 
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
        self.frequency_input_field.setValidator(QDoubleValidator())
        self.frequency_prop_container_layout.addWidget(self.frequency_input_field_label)
        self.frequency_prop_container_layout.addStretch()
        self.frequency_prop_container_layout.addWidget(self.frequency_input_field)

        self.amplitude_prop_container_widget = QWidget()
        self.amplitude_prop_container_layout = QHBoxLayout()
        self.amplitude_prop_container_widget.setLayout(self.amplitude_prop_container_layout)
        self.amplitude_input_field_label = QLabel("Amplitude")
        self.amplitude_input_field = QLineEdit()
        self.amplitude_input_field.setValidator(QDoubleValidator())
        self.amplitude_prop_container_layout.addWidget(self.amplitude_input_field_label)
        self.amplitude_prop_container_layout.addStretch()
        self.amplitude_prop_container_layout.addWidget(self.amplitude_input_field)

        self.phase_shift_prop_container_widget = QWidget()
        self.phase_shift_prop_container_layout = QHBoxLayout()
        self.phase_shift_prop_container_widget.setLayout(self.phase_shift_prop_container_layout)
        self.phase_shift_input_field_label = QLabel("Phase Shift")
        self.phase_shift_input_field = QLineEdit()
        self.phase_shift_input_field.setValidator(QDoubleValidator())
        self.phase_shift_prop_container_layout.addWidget(self.phase_shift_input_field_label)
        self.phase_shift_prop_container_layout.addStretch()
        self.phase_shift_prop_container_layout.addWidget(self.phase_shift_input_field)
        
        self.add_component_button_layout = QHBoxLayout()
        self.add_component_button = QPushButton("Add Component")
        self.add_component_button.setEnabled(False)
        self.add_component_button_layout.addStretch()
        self.add_component_button_layout.addWidget(self.add_component_button)
        self.add_component_button.setStyleSheet("padding:3px 8px")
        
        self.props_layout.addWidget(self.amplitude_prop_container_widget)
        self.props_layout.addWidget(self.frequency_prop_container_widget)
        self.props_layout.addWidget(self.phase_shift_prop_container_widget)
        self.props_layout.addStretch()
        self.props_layout.addLayout(self.add_component_button_layout)

        self.amplitude_input_field.textChanged.connect(self.enable_disable_add_component_button)
        self.frequency_input_field.textChanged.connect(self.enable_disable_add_component_button)
        self.phase_shift_input_field.textChanged.connect(self.enable_disable_add_component_button)

        self.components_widget = QWidget()
        self.components_layout = QVBoxLayout()
        self.components_widget.setLayout(self.components_layout)

        self.components_label = QLabel("Components")
        self.components_scroll_area = QScrollArea()
        self.components_scroll_area.setWidgetResizable(True)
        self.components_list_widget = QWidget()
        self.components_list_layout = QVBoxLayout()
        self.components_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.components_list_layout.setSpacing(0)
        self.components_list_widget.setLayout(self.components_list_layout)
        self.components_scroll_area.setWidget(self.components_list_widget)

        self.components_layout.addWidget(self.components_label)
        self.components_layout.addWidget(self.components_scroll_area)


        
        self.buttons_container_widget = QWidget()
        self.buttons_container_layout = QVBoxLayout()
        self.buttons_container_widget.setLayout(self.buttons_container_layout)
        self.buttons_container_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.add_signal_button = QPushButton("Add Signal")
        self.add_signal_button.setDisabled(True)
        self.export_button = QPushButton("Export")
        self.export_button.setEnabled(False)
        self.cancel_push_button = QPushButton("Cancel")
        self.buttons_container_layout.addWidget(self.add_signal_button)
        self.buttons_container_layout.addWidget(self.export_button)
        self.buttons_container_layout.addWidget(self.cancel_push_button)
        

        


        self.props_and_components_container_layout.addWidget(self.props_widget)
        self.props_and_components_container_layout.addWidget(self.components_widget)

        
        self.props_and_components_and_buttons_container_layout.addWidget(self.props_and_components_container_widget)
        self.props_and_components_and_buttons_container_layout.addStretch()
        self.props_and_components_and_buttons_container_layout.addWidget(self.buttons_container_widget)
        self.main_layout.addWidget(self.mix_output_signal_plot)
        self.main_layout.addWidget(self.props_and_components_and_buttons_container_widget)
        

        self.mixer_controller = MixerController(self,main)
        

    def enable_disable_add_component_button(self):
        if self.frequency_input_field.text() == "" or self.amplitude_input_field.text() == "" or self.phase_shift_input_field.text() == "":
            self.add_component_button.setEnabled(False)
        else:
            self.add_component_button.setEnabled(True)

