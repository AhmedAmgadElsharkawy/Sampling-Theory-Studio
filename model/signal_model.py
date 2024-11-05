import numpy as np
from diffpy.utils.parsers.resample import wsinterp
from scipy.interpolate import CubicSpline
import random
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
        noisy_signal = y.copy()
        maxi = -1000
        for i in range(len(self.y_data)):
            maxi = max(maxi, abs(noisy_signal[i]))

        for i in range(len(self.y_data)):
            if (self.SNR != 100):
                rand = random.uniform(-1, 1) 
                noisy_signal[i] += (rand * (maxi * (1 / self.SNR)))
        return noisy_signal
    
    def whittaker_shannon_interpolation(self, x, y_sampled, x_sampled, T=1):
        x = np.asarray(x)
        y_sampled = np.asarray(y_sampled)
        x_sampled = np.asarray(x_sampled)

        # Calculate the sinc matrix
        sinc_matrix = np.sinc((x - x_sampled[:, None]) / T)

        # Perform the interpolation
        y_new = np.dot(y_sampled, sinc_matrix)

        return y_new
    
    def linear_interpolation(self, x, y_sampled, x_sampled):
        """Perform linear interpolation to estimate y values at x_new based on sampled x and y."""
        x = np.asarray(x)
        y_sampled = np.asarray(y_sampled)
        x_sampled = np.asarray(x_sampled)

        # Perform linear interpolation using numpy's interp function
        y_new = np.interp(x, x_sampled, y_sampled)

        return y_new
    
    def spline_interpolation(self, x, y_sampled, x_sampled):
        """Perform cubic spline interpolation to estimate y values at x_new based on sampled x and y."""
        x = np.asarray(x)
        y_sampled = np.asarray(y_sampled)
        x_sampled = np.asarray(x_sampled)

        # Create a cubic spline interpolation function
        cs = CubicSpline(x_sampled, y_sampled)

        # Evaluate the spline at the new x values
        y_new = cs(x)

        return y_new

    def zero_order_hold_interpolation(self, x, y_sampled, x_sampled):
        x = np.asarray(x)
        x_sampled = np.asarray(x_sampled)
        y_sampled = np.asarray(y_sampled)

        # Initialize output array
        y_new = np.zeros_like(x)

        # Perform Zero-Order Hold
        for i in range(len(x_sampled) - 1):
            # Find indices where x_full is between x_sampled[i] and x_sampled[i+1]
            indices = (x >= x_sampled[i]) & (x < x_sampled[i + 1])
            y_new[indices] = y_sampled[i]

        # Handle the last segment
        y_new[x >= x_sampled[-1]] = y_sampled[-1]

        return y_new
    
    def first_order_hold_interpolation(self, x, y_sampled, x_sampled):
        x = np.asarray(x)
        x_sampled = np.asarray(x_sampled)
        y_sampled = np.asarray(y_sampled)

        # Initialize output array
        y_new = np.zeros_like(x)

        # Perform First-Order Hold
        for i in range(len(x_sampled) - 1):
            # Find indices where x_full is between x_sampled[i] and x_sampled[i+1]
            indices = (x >= x_sampled[i]) & (x < x_sampled[i + 1])
            if np.any(indices):
                # Linear interpolation formula
                y_new[indices] = y_sampled[i] + (y_sampled[i + 1] - y_sampled[i]) * \
                                 (x[indices] - x_sampled[i]) / (x_sampled[i + 1] - x_sampled[i])

        # Handle the last segment
        y_new[x >= x_sampled[-1]] = y_sampled[-1]

        return y_new