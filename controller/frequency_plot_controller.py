import numpy as np
import pyqtgraph as pg

class FrequencyPlotController:
    def __init__(self, main):
        self.main = main
        
    def plot_frequency_domain(self, y_signal_data):
        # Get data from the displayed signal
        signal = np.array(y_signal_data)
        sampling_rate = self.main.displayed_signal.sampling_freq
        number_of_samples = len(signal)
        
        # Calculate FFT
        fft_data = np.fft.fft(signal)
        X_mag = np.abs(fft_data)
        freqs = np.fft.fftfreq(number_of_samples, 1/sampling_rate)
        # freqs = np.fft.fftshift(freqs)

        # Keep only positive frequencies
        positive_freq_indices = freqs >= 0
        X_mag_positive = X_mag[positive_freq_indices]
        freqs_positive = freqs[positive_freq_indices]

        # Clear previous plot
        self.main.frequency_domain_plot.clear()
        
        # Plot magnitude spectrum
        self.main.frequency_domain_plot.plot(freqs_positive, X_mag_positive, pen='r')
        # self.main.frequency_domain_plot.plot(f[np.argmax(X_mag)], np.max(X_mag), symbol='x', symbolPen='y')
        
        # Set labels
        self.main.frequency_domain_plot.setLabel('bottom', 'Frequency (Hz)')
        self.main.frequency_domain_plot.setLabel('left', 'Magnitude')


