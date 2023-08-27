'''
author: Zoe Wu
project: pyqtproject
data: 2023-08-21

Enjoy!
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget,\
    QBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon,QImage
from PyQt5.QtCore import  QStandardPaths
import cv2 as cv
import os

class MyWindow1(QWidget):
    # 为了后续更好封装 创建自己的类

    def __init__(self):
        # 一定要调用父类的init方法，因为里面有很多对UI的初始化操作
        super().__init__()
        # 设置大小
        self.btn1 = QPushButton('视频')
        self.btn2 = QPushButton('图片')
        self.btn1next = QPushButton('下一步')
        self.video_label = QLabel()
        self.init_ui()
        self.init_action()

    def init_ui(self):
        self.setWindowTitle('上传')
        self.resize(600,600)
        # 窗口居中
        cp = QDesktopWidget().availableGeometry().center()
        x = cp.x()
        y = cp.y()
        _, _, width, height = self.frameGeometry().getRect()
        self.move(int(x - width / 2), int(y - height / 2))


        # 垂直布局
        layout = QVBoxLayout()  # 创建布局器
        layout.addStretch()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.video_label)
        layout.addStretch()
        layout.addWidget(self.btn1next)
        # 当前窗口使用该布局器
        self.setLayout(layout)
    def init_action(self):
        self.btn1.clicked.connect(self.upload_video)
        self.btn2.clicked.connect(self.upload_pic)


    def video2img(self):

        if self.video_capture.isOpened():
            frame_count = 0  # 计数器，用于给每一帧图像编号
            # 创建存储文件夹（如果不存在）
            save_folder = "save/warehouse"
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            self.video_label.setText("processing")
            while True:

                ret, frame = self.video_capture.read()  # 读帧
                if not ret:
                    break  # 无法读取帧,结束循环

                frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # BGR——>RGB
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)  # 创建一个 QImage 对象

                save_path = os.path.join(save_folder, "img_{}.png".format(frame_count))  # 构建图像的保存路径和名称
                q_image.save(save_path)  # 保存图像

                frame_count += 1

            self.video_label.setText("All frames saved successfully")  # 在界面上显示成功消息
        else:
            self.video_label.setText("Error opening video file")  # 如果无法打开视频文件，则显示错误消息
    def upload_video(self):

        # 视频路径
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)  # 获取用户的桌面路径
        file_dialog = QFileDialog()
        file_dialog.setDirectory(desktop_path)
        video_path, _ = file_dialog.getOpenFileName(self, "Select Video File", "",
                                                    "Video Files (*.mp4 *.avi *.mkv)")

        if video_path:
            # 若存在 则释放对象
            if self.video_capture is not None:
                self.video_capture.release()
            # 不存在，读取
            self.video_capture = cv.VideoCapture(video_path)
            print('here')
        self.video2img()




    def upload_pic(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow1()
    w.show()

    app.exec_()