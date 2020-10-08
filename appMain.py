##  GUI应用程序主程序入口

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from myMainWindow import MyMainWindow
import ctypes
    
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

app = QApplication(sys.argv)    #创建GUI应用程序
icon = QIcon(":/images/icons/app.png")
app.setWindowIcon(icon)

mainform = MyMainWindow()        #创建主窗体
mainform.show()                 #显示主窗体

sys.exit(app.exec_()) 
