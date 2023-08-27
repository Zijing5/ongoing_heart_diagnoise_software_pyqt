'''
author: Zoe Wu
project: pyqtproject
data: 2023-08-22

Enjoy!
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget,\
    QBoxLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QStackedLayout
from PyQt5.QtGui import QIcon
from page1 import MyWindow1
from page2 import MyWindow2
from page3 import MyWindow3
import page3,page2,page1_2

if __name__ == '__main__':
    app = QApplication(sys.argv)

    MainWindow1 = MyWindow1()
    MainWindow2 = MyWindow2()
    MainWindow1.show()
    # 在按下界面1的按钮后，界面2显示并且界面1关闭
    MainWindow1.btn1next.clicked.connect(MainWindow1.close)
    MainWindow1.btn1next.clicked.connect(MainWindow2.show)

    MainWindow2.btn2next.clicked.connect(MainWindow2.close)
    MainWindow3 = MyWindow3()
    MainWindow2.btn2next.clicked.connect(MainWindow3.show)

    MainWindow3.btn3next.clicked.connect(MainWindow3.close)
    app.exec_()