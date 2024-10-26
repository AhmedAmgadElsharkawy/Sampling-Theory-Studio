import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
)
import pyqtgraph as pg

from controller.error_plot_controller import ErrorPlotController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = []
        self.selected_signal = 0
        self.reconstructed_signal = None
        self.setWindowTitle('Sampling Theory Studio')
        self.setGeometry(100, 100, 1400, 900)
        self.is_dark_mode = True
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.graph1 =  pg.PlotWidget()
        self.graph2 =  pg.PlotWidget()
        self.graph3 =  pg.PlotWidget()
        self.graph4 =  pg.PlotWidget()

        self.main_layout.addWidget(self.graph1)
        self.main_layout.addWidget(self.graph2)
        self.main_layout.addWidget(self.graph3)
        self.main_layout.addWidget(self.graph4)

        error_plot_controlelr = ErrorPlotController(self)


   

