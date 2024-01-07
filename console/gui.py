from PyQt6 import QtWidgets
from ui.UI_MainWindow import Ui_main_window

class MainWindow(QtWidgets.QMainWindow, Ui_main_window):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()

app.exec()