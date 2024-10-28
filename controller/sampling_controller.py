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
        interpolate = self.main.displayed_signal.lagrange_interpolation(self.main.displayed_signal.x_data, y_values_sampled, x_values)
        self.main.reconstructed_signal_plot.plot(self.main.displayed_signal.x_data, interpolate, pen="r", name="Reconstructed Signal")
        self.main.original_signal_plot.plot(self.main.displayed_signal.x_data, self.main.displayed_signal.y_data, pen='r', name="Original Signal")