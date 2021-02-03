from function import window
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=window()
    win.show()
    sys.exit(app.exec_())
