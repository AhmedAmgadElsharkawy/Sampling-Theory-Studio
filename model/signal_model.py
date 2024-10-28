import numpy as np
from diffpy.utils.parsers.resample import wsinterp
class Signal:
    def __init__(self):
        self.x_data = []
        self.y_data = []
        self.original_y = []
        self.components = []
        self.noise_samples = []
        self.sampled_points = []
        self.max_frequency = None
        self.min_frequenncy = None
        self.SNR = 0
        self.sampling_freq = 1

    def get_impulse_train(self):
        impulse_train = np.arange(0, self.x_data[-1], (1 / self.sampling_freq))
        impulse_train = np.around(impulse_train, 3)
        return impulse_train

    def sample_signal(self):
        impulse_train = self.get_impulse_train()
        y_values_sampled = np.zeros(len(impulse_train))
        y_values_sampled = wsinterp(impulse_train, self.x_data, self.y_data)
        self.sampled_points = list(zip(impulse_train, y_values_sampled))

    def change_sampling_freq(self, new_sampling_freq):
        self.sampling_freq = new_sampling_freq
        self.sample_signal()

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
    
    def whittaker_shannon_interpolation(self, x, y, x_new, T=1):
        x = np.asarray(x)
        y = np.asarray(y)
        x_new = np.asarray(x_new)

        # Calculate the sinc matrix
        sinc_matrix = np.sinc((x - x_new[:, None]) / T)

        # Perform the interpolation
        y_new = np.dot(y, sinc_matrix)

        return y_new