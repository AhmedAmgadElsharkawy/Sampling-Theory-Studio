import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import Qt


class FrequencyPlotController:
    def __init__(self, main):
        self.main = main
        
        
    def plot_frequency_domain(self, y_signal_data, x_signal_data):
        # Get data from the displayed signal
        signal_amplitude_original = np.array(self.main.displayed_signal.y_data)
        signal_amplitude_original = signal_amplitude_original - np.mean(signal_amplitude_original)
        sampling_rate = self.main.displayed_signal.sampling_freq
        twice_max_frequency = 20 * self.main.displayed_signal.max_frequency
        number_of_samples = len(signal_amplitude_original)
        
        
        # Calculate FFT for the original signal
        fft_data_original = np.fft.fft(signal_amplitude_original)
        amplitude_axis_original = np.abs(fft_data_original)
        amplitude_axis_original = np.fft.fftshift(amplitude_axis_original)
        freqs_axis_original = np.fft.fftfreq(len(fft_data_original), 1 / twice_max_frequency)
        freqs_axis_original = np.fft.fftshift(freqs_axis_original)
        
        # Clear previous plot
        self.main.frequency_domain_plot.clear()

        # Create a PlotDataItem for the original signal
        plt = pg.PlotDataItem(freqs_axis_original, amplitude_axis_original, pen='r')
        self.main.frequency_domain_plot.addItem(plt)

        # Create PlotDataItems for repeated signals
        for i in [-2, -1, 1, 2]:
            shifted_freqs = freqs_axis_original + (i *  sampling_rate)
            plt = pg.PlotDataItem(shifted_freqs, amplitude_axis_original, pen='b')
            self.main.frequency_domain_plot.addItem(plt)


        # Set fixed view range to show overlapping
        freq_y_min = number_of_samples
        freq_y_max = -number_of_samples

        for i in range(len(freqs_axis_original)):
            freq_y_min = min(freq_y_min, amplitude_axis_original[i])
            freq_y_max = max(freq_y_max, amplitude_axis_original[i])
            freq_range = 10 * sampling_rate
            self.main.frequency_domain_plot.setLimits(xMin=min(freqs_axis_original), xMax=max(freqs_axis_original), yMin=freq_y_min, yMax=freq_y_max)
            
        # Set plot ranges 
        self.main.frequency_domain_plot.setXRange(-freq_range, freq_range)
        self.main.frequency_domain_plot.setYRange(0, np.max(amplitude_axis_original)) 
        
        # Set labels
        self.main.frequency_domain_plot.setLabel('bottom', 'Frequency (Hz)')
        self.main.frequency_domain_plot.setLabel('left', 'Magnitude')

