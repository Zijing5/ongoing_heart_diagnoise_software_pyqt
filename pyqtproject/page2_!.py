'''
author: Zoe Wu
project: pyqtproject
data: 2023-08-21
Enjoy!
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget,\
    QBoxLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QFileDialog,QSizePolicy
from PyQt5.QtGui import QIcon,QPixmap,QDrag,QFont
from PyQt5.QtCore import QPoint,QRect,QSize
import os
import PyQt5
class MyWindow2(QWidget):
    # 为了后续更好封装 创建自己的类

    def __init__(self):
        super().__init__()
        # self.setAcceptDrops(True)
        self.btn1 = QPushButton('仓库')
        self.btn2 = QPushButton('工作间')
        self.btn2next = QPushButton('下一步')
        self.box = None
        self.target_folder_ware = 'save/warehouse'
        self.target_folder_work = 'save/workroom'
        self.init_ui()
        self.init_action()
        self.standard_cut()

    def init_ui(self):
        self.setWindowTitle('切片选择')
        # 设置大小
        self.resize(600,600)

        # 窗口居中
        cp = QDesktopWidget().availableGeometry().center()
        x = cp.x()
        y = cp.y()
        _, _, width, height = self.frameGeometry().getRect()
        self.move(int(x - width / 2), int(y - height / 2))


        # 布局
        font = QFont()
        font.setPointSize(16)  # 设置字体大小为16
        layout1 = QHBoxLayout()  # 创建布局器
        warehouse = QLabel('WAREHOUSE')
        workroom = QLabel('WORKROOM')
        self.box1 = QGroupBox()
        self.box1.setAcceptDrops(True)
        self.box1.dragEnterEvent = self.dragEnterEvent
        self.box1.dropEvent = self.dropEvent
        self.layout1 = QVBoxLayout()


        # self.layout1.addStretch(1)
        self.layout1.addWidget(warehouse)
        # self.layout1.addStretch(1)
        self.layout1.addWidget(self.btn1)
        # self.layout1.addStretch(1)

        self.box1.setLayout(self.layout1)


        self.box2 = QGroupBox()
        self.box2.setAcceptDrops(True)
        self.box2.dragEnterEvent = self.dragEnterEvent
        self.box2.dropEvent = self.dropEvent

        self.layout2 = QVBoxLayout()
        # self.layout2.addStretch()
        self.layout2.addWidget(workroom)
        # self.layout2.addStretch()
        self.layout2.addWidget(self.btn2)
        # self.layout2.addStretch()
        self.box2.setLayout(self.layout2)


        self.layout3 = QHBoxLayout()  # 创建布局器
        # self.layout3.addStretch()
        self.layout3.addWidget(self.box1)
        # self.layout3.addStretch()
        self.layout3.addWidget(self.box2)
        # self.layout3.addStretch()

        self.layout = QVBoxLayout()
        # self.layout.addStretch()
        self.layout.addLayout(self.layout3)
        # self.layout.addStretch()
        self.btn2next.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.btn2next.setMinimumSize(QSize(200, 20))
        self.btn2next.setMaximumSize(QSize(500, 100))
        self.layout.addWidget(self.btn2next,alignment=PyQt5.QtCore.Qt.AlignmentFlag.AlignHCenter)
        # self.layout.addStretch()


        # 当前窗口使用该布局器
        self.setLayout(self.layout)

    def init_action(self):
        self.btn1.clicked.connect(self.btn1_press_clicked)
        self.btn2.clicked.connect(self.btn2_press_clicked)

    def btn1_press_clicked(self):
        # 一旦按下，开启仓库
        current_path = os.path.join(os.getcwd(),'save//warehouse')
        print(current_path)
        os.startfile(current_path)
        # selected_folder = QFileDialog.getOpenFileName(self,'仓库',current_path)
        # if selected_folder:
        #     self.source_folder = selected_folder

    def btn2_press_clicked(self):
        # 一旦按下，开启工作间
        current_path = os.path.join(os.getcwd(), 'save//workroom')
        print(current_path)
        os.startfile(current_path)
        # selected_folder = QFileDialog.getOpenFileName(self,'工作间（标准切面）', current_path)
        # if selected_folder:
        #     self.source_folder = selected_folder

    def standard_cut(self):
        pass
        #todo#自动判断标准切面并存储到workroom里面

    def dragEnterEvent(self, event):
        # 存在路径且本地
        print('drag enter event called')
        if self.box1.underMouse():
            self.box = 1
        if self.box2.underMouse():
            self.box = 2
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].isLocalFile():
            event.acceptProposedAction()

    def dropEvent(self, event):
        print('drop event called')
        # if hasattr(self, 'source_folder'):
        if True:
            # 源地址
            file_path = event.mimeData().urls()[0].toLocalFile()
            if 'workroom' in file_path:
                if self.is_inside_box(self.box1, event.pos()):
                    target_folder = self.target_folder_ware
                else:
                    target_folder = 0
            if 'warehouse' in file_path:
                if self.is_inside_box(self.box2, event.pos()):
                    target_folder = self.target_folder_work
                else:
                    target_folder = 0

            if target_folder:
                file_name = os.path.basename(file_path)
                target_path = os.path.join(target_folder, file_name)
                if os.path.exists(file_path):
                    os.rename(file_path, target_path)
                    event.acceptProposedAction()
                    self.update_image(target_path)


    def update_image(self, image_path):
        pass
        # pixmap = QPixmap(image_path)
        # self.image_label.setPixmap(pixmap)

    def is_inside_box(self, box, position):
        if self.box == 1:
            position = position + self.box1.geometry().topLeft() # 事件发生控件box
        elif self.box == 2:
            position = position + self.box2.geometry().topLeft() # 事件发生控件box
        else:
            return
        rect = box.geometry() # 窗口坐标
        # print(rect,'contains',position)
        return rect.contains(position)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow2()
    w.show()
    app.exec_()