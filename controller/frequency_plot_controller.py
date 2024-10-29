import numpy as np
import pyqtgraph as pg

class FrequencyPlotController:
    def __init__(self, main):
        self.main = main
        
    def plot_frequency_domain(self):
        # Get data from the displayed signal
        signal = np.array(self.main.displayed_signal.y_data)
        sampling_rate = self.main.displayed_signal.sampling_freq * 2
        number_of_samples = len(signal)
        
        # Calculate FFT
        fft_data = np.fft.fftshift(np.fft.fft(signal))
        X_mag = np.abs(fft_data)
        f = np.linspace(sampling_rate/-2, sampling_rate/2, number_of_samples)

        # Clear previous plot
        self.main.frequency_domain_plot.clear()
        
        # Add Nyquist frequency markers
        nyquist = sampling_rate/2
        self.main.frequency_domain_plot.addLine(x=nyquist, pen='r')
        self.main.frequency_domain_plot.addLine(x=-nyquist, pen='r')
        
        # Plot magnitude spectrum
        self.main.frequency_domain_plot.plot(f, X_mag, pen='b')
        self.main.frequency_domain_plot.plot(f[np.argmax(X_mag)], np.max(X_mag), symbol='x', symbolPen='y')
        
        # Set labels
        self.main.frequency_domain_plot.setLabel('bottom', 'Frequency (Hz)')
        self.main.frequency_domain_plot.setLabel('left', 'Magnitude')