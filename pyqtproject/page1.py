'''
author: Zoe Wu
project: pyqtproject
data: 2023-08-21

Enjoy!
'''
import sys
import time
import toolfunc
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget,\
    QVBoxLayout, QHBoxLayout, QFileDialog, QSizePolicy, QTextEdit
from PyQt5.QtGui import QIcon,QImage,QFont
from PyQt5.QtCore import  QStandardPaths,QSize, QThread,pyqtSignal, QCoreApplication
import cv2 as cv
import os
import PyQt5

class MyThread(QThread):
    loading_signal0 = pyqtSignal(str)
    loading_signal1 = pyqtSignal(str)
    loading_signal2 = pyqtSignal(list)
    def __init__(self):
        super(MyThread, self).__init__()

    def fromvideo(self, video_path):
        print('here and',video_path)
        frame_count = 0 #todo #读取目录 从下一个序号开始
        video_capture = cv.VideoCapture(video_path)
        idx0 = toolfunc.nextidx("save/warehouse")
        print(idx0,'idx0')
        while True:
            self.loading_signal0.emit(str(frame_count+idx0))
            ret, frame = video_capture.read()  # 读取视频的下一帧图像
            print('{}'.format(frame_count+idx0))
            if not ret:
                break  # 如果无法读取帧，则结束循环
            # frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            save_path = os.path.join("save/warehouse", "img_{}.png".format(frame_count+idx0))  # 构建图像的保存路径和名称
            cv.imwrite(save_path, frame)  # 保存图像
            frame_count += 1
        # 释放视频捕获对象
        video_capture.release()
        # self.text.append('加载完成')

    def fromimage(self, image_paths):
        print('here?')
        idx0 = toolfunc.nextidx("save/warehouse")
        print(idx0)
        for idx, image_path in enumerate(image_paths):
            self.loading_signal0.emit(str(idx+idx0))
            img = cv.imread(image_path)  # 读取图片
            print('img')
            save_path = os.path.join("save/warehouse", "img_{:02d}.png".format(idx+idx0))  # 根据索引编号保存图片
            cv.imwrite(save_path, img)  # 保存图片

    def run(self):
        while True:
            print('线程执行中')
            time.sleep(1)


class MyWindow1(QWidget):

    def __init__(self):
        super().__init__()
        # 设置大小
        self.btn1 = QPushButton('视频')
        self.btn2 = QPushButton('图片')
        self.btn1next = QPushButton('下一步')
        self.video_capture = None
        self.init_ui()
        self.init_action()
        self.destroyed.connect(self.cleanup)

    def init_ui(self):
        self.setWindowTitle('上传')
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
        # layout1.addStretch()
        self.btn1.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.btn2.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.btn1.setMinimumSize(QSize(25, 50))
        self.btn1.setMaximumSize(QSize(260, 500))
        self.btn2.setMinimumSize(QSize(25, 50))
        self.btn2.setMaximumSize(QSize(260, 500))
        layout1.addWidget(self.btn1)
        layout1.addWidget(self.btn2)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)  # 设置为只读，以便只显示文本而不允许编辑
        # text.setStyleSheet("background-color: gray;")  # 设置灰色背景
        layout.addWidget(self.text)
        self.text.setMaximumSize(QSize(560, 200))
        self.text.setMaximumSize(QSize(560, 100))

        self.btn1next.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.btn1next.setMinimumSize(QSize(200, 20))
        self.btn1next.setMaximumSize(QSize(500, 100))

        self.btn1next.setFont(font)  # 将新字体应用到按钮
        self.btn1.setFont(font)  # 将新字体应用到按钮
        self.btn2.setFont(font)  # 将新字体应用到按钮
        layout.addWidget(self.btn1next,alignment=PyQt5.QtCore.Qt.AlignmentFlag.AlignHCenter)

        # 当前窗口使用该布局器
        self.setLayout(layout)
    def init_action(self):
        self.btn1.clicked.connect(self.upload_video)
        self.btn2.clicked.connect(self.upload_pic)
        self.mythread = MyThread()
        self.mythread.loading_signal1.connect(self.mythread.fromvideo)
        self.mythread.loading_signal2.connect(self.mythread.fromimage)
        self.mythread.loading_signal0.connect(self.update_text)
        self.mythread.start()

    def upload_video(self):
        # 视频路径
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)  # 获取用户的桌面路径
        # desktop_path = r" E:\MrMa\QTProject\pyqt\file"
        file_dialog = QFileDialog()
        file_dialog.setDirectory(desktop_path)
        video_path, _ = file_dialog.getOpenFileName(self, "Select Video File", "",
                                                    "Video Files (*.mp4 *.avi *.mkv *.wmv)")

        if video_path:
            save_folder = "save/warehouse"  # 存储文件夹路径
            save_folder1 = "save/workroom"  # 存储文件夹路径
            # 创建存储文件夹（如果不存在）
            # flag=0
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            if not os.path.exists(save_folder1):
                os.makedirs(save_folder1)


            print(video_path,'this is video path')
            self.mythread.loading_signal1.emit(video_path)

        # E:\MrMa\QTProject\pyqt\file


    def upload_pic(self):
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        # desktop_path = r" E:\MrMa\QTProject\pyqt\file"
        file_dialog = QFileDialog()
        file_dialog.setDirectory(desktop_path)
        image_paths, _ = file_dialog.getOpenFileNames(self, "Select Image File", "",
                                                    "Image Files (*.jpg *.png *.bmp)")
        if image_paths:
            save_folder1 = "save/workroom"  # 存储文件夹路径
            save_folder = "save/warehouse"  # 存储文件夹路径
            # 创建存储文件夹（如果不存在）
            if not os.path.exists(save_folder1):
                os.makedirs(save_folder1)
                # 清空文件夹 #todo##如果点击清空按钮才清空仓库
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)


            self.mythread.loading_signal2.emit(image_paths)




    def update_text(self, t):
        self.text.append('loading img_{} ...'.format(t))
        QCoreApplication.processEvents()  # 触发界面更新

    def cleanup(self):
        if self.video_capture is not None:
            self.video_capture.release()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow1()
    w.show()

    app.exec_()