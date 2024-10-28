import numpy as np
class Signal:
    def __init__(self):
        self.x_data = []
        self.y_data = []
        self.original_y = []
        self.components = []
        self.noise_samples = []
        self.max_frequency = None
        self.min_frequenncy = None
        self.SNR = 0

    def change_snr(self, new_snr):
        self.SNR = new_snr
        self.y_data = self.apply_noise(self.original_y)

    def create_noise(self):
        self.noise_samples.clear()
        temp_signal = np.array(self.y_data.copy())
        signal_power = temp_signal**2
        signal_average_power = np.mean(signal_power)
        noise_power = signal_average_power / self.SNR
        noise = np.random.normal(0, np.sqrt(noise_power), len(temp_signal))
        self.noise_samples.append(noise)
        return self.noise_samples

    def apply_noise(self, y):
        noisy = self.create_noise()
        noisy_signal = y.copy()
        for noise in noisy:
            noisy_signal += noise
        return noisy_signal
        
        
    