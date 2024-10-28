import pyqtgraph as pg
class SamplingController:
    def __init__(self,main):
        self.main = main

    def change_SNR(self, value):
        self.main.displayed_signal.change_snr(value)
        
        self.main.original_signal_plot.clear()
        # Plot the original signal
        self.main.original_signal_plot.plot(self.main.displayed_signal.x_data, self.main.displayed_signal.y_data, pen='r', name="Original Signal")
    
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
        self.main.reconstructed_signal_plot.plot(x_values, y_values_sampled, pen="r", name="Reconstructed Signal")
        self.main.original_signal_plot.plot(self.main.displayed_signal.x_data, self.main.displayed_signal.y_data, pen='r', name="Original Signal")