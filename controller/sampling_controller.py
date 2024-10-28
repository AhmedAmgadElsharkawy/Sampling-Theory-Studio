class SamplingController:
    def __init__(self,main):
        self.main = main

    def changeSNR(self, value):
        self.main.displayed_signal.change_snr(value)
        
        self.main.original_signal_plot.clear()
        # Plot the original signal
        self.main.original_signal_plot.plot(self.main.displayed_signal.x_data, self.main.displayed_signal.y_data, pen='r', name="Original Signal")