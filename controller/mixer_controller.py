import numpy as np
from model.component_model import Component

class MixerController:
    def __init__(self,mixer_window):
        self.mixer_window = mixer_window
        self.mixed_signal = mixer_window.mixed_signal
        self.mixer_window.add_component_button.clicked.connect(self.add_component)

    def add_component(self):
        print(float(self.mixer_window.frequency_input_field.text()))
        print(float(self.mixer_window.amplitude_input_field.text()))
        print(float(self.mixer_window.phase_shift_input_field.text()))
        component = Component(frequency=float(self.mixer_window.frequency_input_field.text())
                              ,amplitude=float(self.mixer_window.amplitude_input_field.text()),
                              phase_shift=float(self.mixer_window.phase_shift_input_field.text()))
        print("component",component.amplitude,component.frequency,component.phase_shift)
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
        self.mixer_window.components_list.append(component)
        self.mixed_signal.x_data = component.x_data
        if(len(self.mixed_signal.y_data) == 0):
            self.mixed_signal.y_data = component.y_data
        else:
            self.mixed_signal.y_data += component.y_data

        self.draw_mixed_signal()

    def draw_mixed_signal(self):
        self.mixer_window.mix_output_signal_plot.clear()
        self.mixer_window.mix_output_signal_curve.setData(self.mixed_signal.x_data,self.mixed_signal.y_data)
        self.mixer_window.mix_output_signal_plot.addItem(self.mixer_window.mix_output_signal_curve)
        

        

    

    