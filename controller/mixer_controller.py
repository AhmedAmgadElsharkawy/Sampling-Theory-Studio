import os
import numpy as np
import pandas as pd
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
        self.mixer_window.export_button.clicked.connect(self.export_signal_to_csv_file)
        

    def get_unique_filename(self,filename):
        base, ext = os.path.splitext(filename)  # Split filename into base and extension
        counter = 1
        while os.path.exists(filename):
            filename = f"{base}_{counter}{ext}"  # Create new filename
            counter += 1
        return filename

    def export_signal_to_csv_file(self):
        df = pd.DataFrame({
            'Elapsed Time': self.mixer_window.mixed_signal.x_data,
            'II': self.mixer_window.mixed_signal.y_data,
            'MAX FREQUENCY': self.mixer_window.mixed_signal.max_frequency
        })

        filename = self.get_unique_filename("data/mixer_signals/mixed_signal.csv")
        df.to_csv(filename, index=False)
        

    def add_signal(self):
        self.main.load_signal_controller.add_signal_to_signals_scroll_area(f"custom_signal_{self.main.scroll_area_widget_layout.count()}",self.mixed_signal)
        self.close_mixer()
        
    def close_mixer(self):
        self.mixer_window.accept() 

    def add_component(self):
        maximum_freq_changed = False
        component = Component(frequency=float(self.mixer_window.frequency_input_field.text())
                              ,amplitude=float(self.mixer_window.amplitude_input_field.text()),
                              phase_shift=float(self.mixer_window.phase_shift_input_field.text()))
        if self.mixed_signal.max_frequency == None:
            self.mixed_signal.max_frequency = component.frequency
            self.mixed_signal.min_frequency = component.frequency
        else:
            if component.frequency > self.mixed_signal.max_frequency:
                maximum_freq_changed = True
                self.mixed_signal.max_frequency = component.frequency
            if component.frequency < self.mixed_signal.min_frequency:
                self.mixed_signal.min_frequency = component.frequency


        component.x_data = np.arange(0, 4, 1 / (20 * self.mixed_signal.max_frequency))
        component.y_data = component.amplitude * np.sin(2 * np.pi * component.frequency * component.x_data + component.phase_shift * np.pi /180)
        self.mixed_signal.x_data = component.x_data
        if(len(self.mixed_signal.y_data) == 0):
            self.mixed_signal.y_data = component.y_data.copy()
        elif maximum_freq_changed == False:
            self.mixed_signal.y_data += component.y_data
        else :
            for curr_component in self.mixed_signal.components:
                curr_component.x_data = component.x_data.copy()
                curr_component.y_data = curr_component.amplitude * np.sin(2 * np.pi * curr_component.frequency * curr_component.x_data + curr_component.phase_shift * np.pi /180)
            maximum_freq_changed = False
            self.mixed_signal.y_data = component.y_data.copy()
            for curr_component in self.mixed_signal.components:
                self.mixed_signal.y_data += curr_component.y_data
        self.mixed_signal.original_y = self.mixed_signal.y_data.copy()

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
       if(self.mixer_window.components_list_layout.count()):
           self.mixer_window.add_signal_button.setEnabled(True)
           self.mixer_window.export_button.setEnabled(True)


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
            self.mixer_window.mixed_signal.max_frequency = 0
            self.mixer_window.add_signal_button.setEnabled(False)
            self.mixer_window.export_button.setEnabled(False)
            # self.mixer_window.mixed_signal = None
        
        elif self.component.frequency == self.mixer_window.mixed_signal.max_frequency:
            self.mixer_window.mixed_signal.y_data -= self.component.y_data
            self.mixer_window.mixed_signal.max_frequency = 0
            for cur_component in self.mixer_window.mixed_signal.components:
                self.mixer_window.mixed_signal.max_frequency = max(self.mixer_window.mixed_signal.max_frequency,cur_component.frequency)
            
            self.mixer_window.mixed_signal.x_data = np.arange(0, 1, 1 / (30 * self.mixer_window.mixed_signal.max_frequency))
            for cur_component in self.mixer_window.mixed_signal.components:
                cur_component.x_data = self.mixer_window.mixed_signal.x_data.copy()
                cur_component.y_data = cur_component.amplitude * np.sin(2 * np.pi * cur_component.frequency * cur_component.x_data + cur_component.phase_shift * np.pi /180)
            self.mixer_window.mixed_signal.y_data = [0]*len(self.mixer_window.mixed_signal.x_data)
            for curr_component in self.mixer_window.mixed_signal.components:
                self.mixer_window.mixed_signal.y_data += curr_component.y_data
            self.mixer_window.mixed_signal.original_y = self.mixer_window.mixed_signal.y_data.copy()
                
        else:
            self.mixer_window.mixed_signal.y_data -= self.component.y_data

        self.mixer_window.mixer_controller.draw_mixed_signal()
        self.mixer_window.components_list_layout.removeWidget(self)
        self.deleteLater()


        
        

        

    

    