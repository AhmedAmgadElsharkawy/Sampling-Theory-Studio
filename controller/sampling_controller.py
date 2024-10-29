import pyqtgraph as pg
import numpy as np
class SamplingController:
    def __init__(self,main):
        self.main = main

    def change_SNR(self, value):
        self.main.displayed_signal.change_snr(value)

        self.change_sampling_freq(self.main.displayed_signal.sampling_freq)
    
    def change_sampling_freq(self, value):
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
        else :
            interpolate = self.main.displayed_signal.whittaker_shannon_interpolation(self.main.displayed_signal.x_data, y_values_sampled, x_values, 1 / self.main.displayed_signal.sampling_freq)
        error = np.array(self.main.displayed_signal.y_data) - interpolate
        self.main.error_signal_plot.plot(self.main.displayed_signal.x_data, error, pen="r", name="Error Signal")
        self.main.error_signal_plot.setYRange(-2, 2)
        self.main.reconstructed_signal_plot.plot(self.main.displayed_signal.x_data, interpolate, pen="r", name="Reconstructed Signal")
        self.main.original_signal_plot.plot(self.main.displayed_signal.x_data, self.main.displayed_signal.y_data, pen='r', name="Original Signal")

    def change_reconstruction_method(self):
        """Function to be triggered when the combo box selection changes."""
        selected_option = self.main.reconstruction_combo.currentText()  # Get the selected text
        self.main.interpolation_method = selected_option
        self.change_sampling_freq(self.main.displayed_signal.sampling_freq)

    def clear_plots(self):
        self.main.original_signal_plot.clear()
        self.main.reconstructed_signal_plot.clear()
        self.main.error_signal_plot.clear()
        self.main.frequency_domain_plot.clear()
        self.main.displayed_signal = None

    