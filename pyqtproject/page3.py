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
import PyQt5.QtCore


class Window1(QWidget):
    def __init__(self):
        super().__init__()
        QLabel('这是第一个工作间页面',self)


class Window2(QWidget):
    def __init__(self):
        super().__init__()
        self.l = QLabel('这是诊断算法页面',self)
        self.b1 = QPushButton('xxx1算法',self)
        self.b2 = QPushButton('xxx2算法',self)
        self.b3 = QPushButton('xxx3算法',self)
        self.b4 = QPushButton('xxx4算法',self)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.l)
        layout.addStretch()
        layout.addWidget(self.b1)
        layout.addStretch()
        layout.addWidget(self.b2)
        layout.addStretch()
        layout.addWidget(self.b3)
        layout.addStretch()
        layout.addWidget(self.b4)
        self.setLayout(layout)



class Window3(QWidget):
    def __init__(self):
        super().__init__()
        QLabel('这是诊断结果页面',self)


class MyWindow3(QWidget):
    def __init__(self):
        # 一定要调用父类的init方法，因为里面有很多对UI的初始化操作
        super().__init__()
        self.create_stacked_layout()
        self.init_ui()
    def create_stacked_layout(self):
        # self. 则该变量可以在整个类中调用
        self.stacked_layout = QStackedLayout()
        page1 = Window1()
        page2 = Window2()
        page3 = Window3()
        self.stacked_layout.addWidget(page1)
        self.stacked_layout.addWidget(page2)
        self.stacked_layout.addWidget(page3)

    def init_ui(self):
        self.setWindowTitle('诊断')
        # 设置大小
        self.resize(600,600)
        # 窗口居中
        cp = QDesktopWidget().availableGeometry().center()
        x = cp.x()
        y = cp.y()
        _, _, width, height = self.frameGeometry().getRect()
        self.move(int(x - width / 2), int(y - height / 2))

        btn1 = QPushButton('工作间')
        btn2 = QPushButton('诊断算法')
        btn3 = QPushButton('诊断结果')
        self.btn3next = QPushButton('结束诊断')
        btn1.clicked.connect(self.btn1_press_clicked)
        btn2.clicked.connect(self.btn2_press_clicked)
        btn3.clicked.connect(self.btn3_press_clicked)
        # self.btn3next.clicked.connect(self.btn_press4_clicked)

        # 创建一个Widget用于显示具体内容
        widget = QWidget()
        widget.setLayout(self.stacked_layout)
        widget.setStyleSheet('background-color:grey;')

        layoutbtn = QVBoxLayout()
        layoutbtn.addStretch()
        layoutbtn.addWidget(btn1)
        layoutbtn.addWidget(btn2)
        layoutbtn.addWidget(btn3)
        layoutbtn.addStretch(1)
        layoutbtn.addWidget(self.btn3next)
        layoutbtn.addStretch()

        layout = QHBoxLayout()
        layout.addLayout(layoutbtn)
        layout.addWidget(widget)

        self.setLayout(layout)

    def btn1_press_clicked(self):
        self.stacked_layout.setCurrentIndex(0)
    def btn2_press_clicked(self):
        self.stacked_layout.setCurrentIndex(1)
    def btn3_press_clicked(self):
        self.stacked_layout.setCurrentIndex(2)
    def btn3next_press_clicked(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow3()
    w.show()

    app.exec_()