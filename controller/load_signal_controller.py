from PyQt6.QtWidgets import QFileDialog
from model.signal_model import Signal
import pandas as pd



class LoadSignalController:
    def __init__(self,main):
        self.main = main
        self.main.load_signal_button.clicked.connect(self.browse_file)

    def browse_file(self):
        file_dialog = QFileDialog(self.main)
        file_path, _ = file_dialog.getOpenFileName(self.main, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.add_signal(file_path)

    def add_signal(self, file_path):
        if not file_path:
            pass
        data = pd.read_csv(file_path).iloc[:,0:2]
        self.x = data.iloc[:,0]
        self.y = data.iloc[:,1]
        signal = Signal()
        signal.x_data = data.iloc[:,0]
        signal.y_data = data.iloc[:,1]
        self.main.signals_list.append(signal)
        
        
    