from view.mixer_window import MixerWindow
class MixerController:
    def __init__(self,main):
        self.main = main
        self.main.signal_mixer_button.clicked.connect(self.open_mixer_window)

    def open_mixer_window(self):
        self.main.mixer_window = MixerWindow()
        self.main.mixer_window.show()

    