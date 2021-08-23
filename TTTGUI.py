import sys
from PyQt5.QtWidgets import *
from menu import DlgMain


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg_main = DlgMain()
    dlg_main.show()
    sys.exit(app.exec_())