import numpy as np
from model.component_model import Component
from PyQt6.QtWidgets import QWidget,QHBoxLayout,QLabel,QPushButton
from PyQt6.QtGui import QIcon

from controller.load_signal_controller import LoadSignalController


class MixerController:
    def __init__(self,mixer_window,main):
        self.main = main
        self.mixer_window = mixer_window
        self.mixed_signal = mixer_window.mixed_signal
        self.mixer_window.add_component_button.clicked.connect(self.add_component)
        self.mixer_window.add_signal_button.clicked.connect(self.add_signal)
        self.mixer_window.cancel_push_button.clicked.connect(self.close_mixer)
        

    def add_signal(self):
        self.main.load_signal_controller.add_signal_to_signals_scroll_area(f"custom_signal_{self.main.scroll_area_widget_layout.count()}",self.mixed_signal)
        self.close_mixer()
        
    def close_mixer(self):
        self.mixer_window.accept() 

    def add_component(self):
        component = Component(frequency=float(self.mixer_window.frequency_input_field.text())
                              ,amplitude=float(self.mixer_window.amplitude_input_field.text()),
                              phase_shift=float(self.mixer_window.phase_shift_input_field.text()))
        if self.mixed_signal.max_frequency == None:
            self.mixed_signal.max_frequency = component.frequency
            self.mixed_signal.min_frequency = component.frequency
        else:
            if component.frequency > self.mixed_signal.max_frequency:
                self.mixed_signal.max_frequency = component.frequency
            if component.frequency < self.mixed_signal.min_frequency:
                self.mixed_signal.min_frequency = component.frequency


        component.x_data = np.arange(0, 20, 0.02)
        component.y_data = component.amplitude * np.sin(2 * np.pi * component.frequency * component.x_data + component.phase_shift * np.pi /180)
        self.mixed_signal.x_data = component.x_data
        if(len(self.mixed_signal.y_data) == 0):
            self.mixed_signal.y_data = component.y_data
        else:
            self.mixed_signal.y_data += component.y_data
        self.mixed_signal.original_y  = self.mixed_signal.y_data.copy()

        self.mixer_window.mixed_signal.components.append(component)

        self.draw_mixed_signal()
        self.add_component_item(component=component)
    

    def draw_mixed_signal(self):
        self.mixer_window.mix_output_signal_plot.clear()
        self.mixer_window.mix_output_signal_curve.setData(self.mixed_signal.x_data,self.mixed_signal.y_data)
        self.mixer_window.mix_output_signal_plot.addItem(self.mixer_window.mix_output_signal_curve)

    def add_component_item(self,component):
       component_item = ComponentItem(self.mixer_window,component) 
       self.mixer_window.components_list_layout.addWidget(component_item)


class ComponentItem(QWidget):
    def __init__(self,mixer_window,component):
        super().__init__()
        self.mixer_window = mixer_window
        self.component = component

        self.component_item_layout = QHBoxLayout()
        self.setLayout(self.component_item_layout)
        self.component_name_label = QLabel(f"compnent{self.mixer_window.components_list_layout.count()} ({self.component.amplitude}, {self.component.frequency}, {self.component.phase_shift})")
        self.trash_button = QPushButton()
        self.trash_button.setIcon(QIcon("assets/icons/delete.svg"))
        self.trash_button.setFixedSize(15, 15)
        self.component_item_layout.addWidget(self.component_name_label)
        self.component_item_layout.addStretch()
        self.component_item_layout.addWidget(self.trash_button)

        self.trash_button.clicked.connect(self.delete_component_item)

    def delete_component_item(self):
        self.mixer_window.mixed_signal.components.remove(self.component)
        if(len(self.mixer_window.mixed_signal.components) == 0):
            self.mixer_window.mixed_signal.x_data = []
            self.mixer_window.mixed_signal.y_data = []
            # self.mixer_window.mixed_signal = None
        else:
            self.mixer_window.mixed_signal.y_data -= self.component.y_data

        self.mixer_window.mixer_controller.draw_mixed_signal()
        self.mixer_window.components_list_layout.removeWidget(self)
        self.deleteLater()


        
        

        

    

    