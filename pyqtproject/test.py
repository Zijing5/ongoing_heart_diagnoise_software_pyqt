'''
author: Zoe Wu
project: pyqtproject
data: 2023-08-21

Enjoy!
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget,\
    QBoxLayout
from PyQt5.QtGui import QIcon

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # sys.argv 运行程序时传递的参数，为列表

    w = QWidget()  # 一个框架
    w.setWindowTitle('先心病诊断')

    # 按钮
    btn1 = QPushButton('视频',w)
    btn2 = QPushButton('图像',w)
    btn1.setGeometry(200,400,100,50)
    btn2.setGeometry(200,200,100,50)
    # btn1.setParent(w)
    # btn2.setParent(w)

    # 标签
    label1 = QLabel('先心病诊断',w)
    label1.setGeometry(100,100,100,50)

    # 编辑
    edit = QLineEdit(w)
    edit.setPlaceholderText("输入")
    edit.setGeometry(150,100,200,20)

    # 图标
    w.setWindowIcon(QIcon('../HIT.png'))

    w.resize(600,600)
    # w.move(0,0)

    # 窗口居中
    cp = QDesktopWidget().availableGeometry().center()
    x = cp.x()
    y = cp.y()
    _,_,width,height = w.frameGeometry().getRect()
    w.move(int(x-width/2),int(y-height/2))

    w.show()

    app.exec_() # 若缺失 程序一闪而过