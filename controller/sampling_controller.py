import pyqtgraph as pg
import numpy as np
class SamplingController:
    def __init__(self,main):
        self.main = main

    def change_SNR(self, value):
        self.main.displayed_signal.change_snr(value)

        self.change_sampling_freq_and_plot_all_signals(self.main.displayed_signal.sampling_freq)
    
    def change_sampling_freq_and_plot_all_signals(self, value):
        self.main.displayed_signal.change_sampling_freq(value)
        
        self.main.original_signal_plot.clear()
        self.main.error_signal_plot.clear()
        self.main.reconstructed_signal_plot.clear()
        # Plot the original signal
        sampled_points = self.main.displayed_signal.sampled_points
        x_values, y_values_sampled = zip(*sampled_points)
        sample_markers = pg.ScatterPlotItem(
                x=x_values,
                y=y_values_sampled,
                pen=None,
                symbol="x",
                symbolPen="b",
                name="sample_markers",
            )
        self.main.original_signal_plot.addItem(sample_markers)
        if self.main.interpolation_method == "CubicSpline":
            interpolate = self.main.displayed_signal.spline_interpolation(self.main.displayed_signal.x_data, y_values_sampled, x_values)
        elif self.main.interpolation_method == "Linear":
            interpolate = self.main.displayed_signal.linear_interpolation(self.main.displayed_signal.x_data, y_values_sampled, x_values)
        elif self.main.interpolation_method == "Zero-Order-Hold":
            interpolate = self.main.displayed_signal.zero_order_hold_interpolation(self.main.displayed_signal.x_data, y_values_sampled, x_values)
        elif self.main.interpolation_method == "First-Order-Hold":
            interpolate = self.main.displayed_signal.first_order_hold_interpolation(self.main.displayed_signal.x_data, y_values_sampled, x_values)
        else :
            interpolate = self.main.displayed_signal.whittaker_shannon_interpolation(self.main.displayed_signal.x_data, y_values_sampled, x_values, 1 / self.main.displayed_signal.sampling_freq)
        error = np.array(self.main.displayed_signal.y_data) - interpolate
        self.main.original_signal_plot.plot(self.main.displayed_signal.x_data, self.main.displayed_signal.y_data, pen='r', name="Original Signal")
        self.main.error_signal_plot.plot(self.main.displayed_signal.x_data, error, pen="r", name="Error Signal")
        self.main.error_signal_plot.setYRange(-2, 2)
        self.main.frequency_plot_controller.plot_frequency_domain(y_values_sampled, x_values)
        self.main.reconstructed_signal_plot.plot(self.main.displayed_signal.x_data, interpolate, pen="r", name="Reconstructed Signal")
        signal_min = 1000
        signal_max = -1000
        interpolate_min = 1000
        interpolate_max = -1000
        error_min = 1000
        error_max = -1000
        for i in range(len(self.main.displayed_signal.y_data)):
            signal_max = max(signal_max, self.main.displayed_signal.y_data[i])
            signal_min = min(signal_min, self.main.displayed_signal.y_data[i])
            interpolate_max = max(interpolate_max, interpolate[i])
            interpolate_min = min(interpolate_min, interpolate[i])
            error_max = max(error_max, error[i])
            error_min= min(error_min, error[i])

        self.main.original_signal_plot.setLimits(xMin=self.main.displayed_signal.x_data[0], xMax=self.main.displayed_signal.x_data[-1], yMin = signal_min, yMax = signal_max)
        self.main.reconstructed_signal_plot.setLimits(xMin=self.main.displayed_signal.x_data[0], xMax=self.main.displayed_signal.x_data[-1], yMin = interpolate_min, yMax = interpolate_max)
        self.main.error_signal_plot.setLimits(xMin=self.main.displayed_signal.x_data[0], xMax=self.main.displayed_signal.x_data[-1], yMin = error_min, yMax = error_max)

        self.main.original_signal_plot.setYRange(signal_min, signal_max)
        self.main.reconstructed_signal_plot.setYRange(interpolate_min, interpolate_max)
        self.main.error_signal_plot.setYRange(error_min, error_max)

    def change_reconstruction_method(self):
        """Function to be triggered when the combo box selection changes."""
        selected_option = self.main.reconstruction_combo.currentText()  # Get the selected text
        self.main.interpolation_method = selected_option
        self.change_sampling_freq_and_plot_all_signals(self.main.displayed_signal.sampling_freq)

    def clear_plots(self):
        self.main.original_signal_plot.clear()
        self.main.reconstructed_signal_plot.clear()
        self.main.error_signal_plot.clear()
        self.main.frequency_domain_plot.clear()
        self.main.displayed_signal = None

    