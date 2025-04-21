import sys
#import qdarktheme 
#from PyQt5.QtWidgets import  QStyleFactory 
from login_2 import LoginWindow   
from PyQt5.QtWidgets import QApplication 

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    app.setStyle("Fusion")
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_()) 