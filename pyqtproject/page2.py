'''
author: Zoe Wu
project: pyqtproject
data: 2023-08-21
Enjoy!
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget,\
    QBoxLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QFileDialog,QSizePolicy,QGridLayout
from PyQt5.QtGui import QIcon,QPixmap,QDrag,QFont
from PyQt5.QtCore import QPoint,QRect,QSize
import os
import PyQt5
import re
class MyWindow2(QWidget):
    # 为了后续更好封装 创建自己的类

    def __init__(self):
        super().__init__()
        # self.setAcceptDrops(True)
        self.btn1 = QPushButton('仓库')
        self.btn2 = QPushButton('工作间')
        self.nextpage1 = QPushButton('下一页')
        self.nextpage2 = QPushButton('下一页')
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
        # warehouse = QLabel('WAREHOUSE')
        # workroom = QLabel('WORKROOM')
        self.box1 = QGroupBox()
        self.box1.setAcceptDrops(True)
        self.box1.dragEnterEvent = self.dragEnterEvent
        self.box1.dropEvent = self.dropEvent
        self.layout1 = QVBoxLayout()
        self.grid_layout1 = QGridLayout()
        self.init_images_to_grid(self.box1, self.grid_layout1, "save//warehouse")


        # self.layout1.addStretch(1)
        self.layout1.addLayout(self.grid_layout1)
        # self.layout1.addStretch(1)
        self.layout1.addWidget(self.nextpage1)
        self.layout1.addWidget(self.btn1)
        # self.layout1.addStretch(1)

        self.box1.setLayout(self.layout1)


        self.box2 = QGroupBox()
        self.box2.setAcceptDrops(True)
        self.box2.dragEnterEvent = self.dragEnterEvent
        self.box2.dropEvent = self.dropEvent
        self.grid_layout2 = QGridLayout()
        self.init_images_to_grid(self.box2, self.grid_layout2, "save//workroom")

        self.layout2 = QVBoxLayout()
        # self.layout2.addStretch()
        self.layout2.addLayout(self.grid_layout2)
        self.layout2.addWidget(self.nextpage2)
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

    def init_images_to_grid(self, grid_box, grid_layout, folder_path):
        # Load images from folder and populate the grid layout
        images = self.load_images_from_folder(folder_path)
        # print(images[:5])
        images = sorted(images, key=lambda item: int(item.split('_')[-1].split('.')[0]))
        # print(images[:5]
        row, col = 0, 0
        grid_columns = 2 # 四宫格
        print(grid_box.geometry())
        cell_width = min(grid_box.geometry().width(),grid_box.geometry().height())//grid_columns
        image_names = []  # 存储图片名称的列表

        for image_path in images:
            print(image_path)
            image_name = os.path.basename(image_path)  # 获取图片的文件名
            image_names.append(image_name)  # 将图片名称添加到列表中
            pixmap = QPixmap(image_path)
            aspect_ratio = pixmap.width() / pixmap.height()
            scaled_width = cell_width
            scaled_height = int(scaled_width / aspect_ratio)
            label = QLabel()
            label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            label.setScaledContents(True)
            # label.setPixmap(pixmap)
            # print('1',pixmap.size())
            # print(scaled_height,scaled_width)
            scaled = pixmap.scaled(scaled_width, scaled_height, \
                                          PyQt5.QtCore.Qt.KeepAspectRatio, PyQt5.QtCore.Qt.SmoothTransformation)
            # print('2',scaled.size())
            label.setPixmap(scaled)

            name_label = QLabel(image_name)  # 创建一个显示图片名称的标签
            name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)  # 居中对齐
            name_label.setWordWrap(True)  # 自动换行
            vbox = QVBoxLayout()  # 垂直布局，用于放置图片和名称标签
            vbox.addWidget(label)
            vbox.addWidget(name_label)
            widget = QWidget()  # 创建一个容器小部件，将垂直布局放置其中
            widget.setLayout(vbox)
            grid_layout.addWidget(widget, row, col)
            # label.setAlignment(PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)  # 设置图片对齐方式
            # label.setGeometry(col * cell_width, row * cell_width, cell_width, cell_width)  # 设置图片位置和大小
            col += 1
            if col >= 2:
                col = 0
                row += 1
            if row>=2:
                break

    def load_images_to_grid(self, grid_box, grid_layout, images):
        # 点击下一页按钮后触发 这里的Images是排序后的图片路径
        # Load images from folder and populate the grid layout
        row, col = 0, 0
        grid_columns = 2 # 四宫格
        cell_width = min(grid_box.geometry().width(),grid_box.geometry().height())//grid_columns
        # 获取目前区域内最后一张图片的编号 寻找下一张图片序号 并继续更新
        # idx = idx_get()
        image_names = []
        # 删除之前所有小控件
        for i in reversed(range(grid_layout.count())):
            item = grid_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        if len(images)>0:
            for image_path in images:
                print(image_path)
                image_name = os.path.basename(image_path)  # 获取图片的文件名
                image_names.append(image_name)  # 将图片名称添加到列表中
                pixmap = QPixmap(image_path)
                aspect_ratio = pixmap.width() / pixmap.height()
                scaled_width = min(cell_width,250)
                scaled_height = int(scaled_width / aspect_ratio)
                label = QLabel()
                label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                label.setScaledContents(True)
                # label.setPixmap(pixmap)
                # print('1',pixmap.size())
                # print(scaled_height,scaled_width)
                scaled = pixmap.scaled(scaled_width, scaled_height, \
                                              PyQt5.QtCore.Qt.KeepAspectRatio, PyQt5.QtCore.Qt.SmoothTransformation)

                print('2',scaled.size())
                label.setPixmap(scaled)

                name_label = QLabel(image_name)  # 创建一个显示图片名称的标签
                name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)  # 居中对齐
                name_label.setWordWrap(True)  # 自动换行
                vbox = QVBoxLayout()  # 垂直布局，用于放置图片和名称标签
                vbox.addWidget(label)
                vbox.addWidget(name_label)
                widget = QWidget()  # 创建一个容器小部件，将垂直布局放置其中
                widget.setLayout(vbox)
                grid_layout.addWidget(widget, row, col)
                # label.setAlignment(PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)  # 设置图片对齐方式
                # label.setGeometry(col * cell_width, row * cell_width, cell_width, cell_width)  # 设置图片位置和大小
                col += 1
                if col >= 2:
                    col = 0
                    row += 1
                if row>=2:
                    break
    # def deleteVBoxLayout(grid_layout):
    #     pixmap = QPixmap()
    #     label = QLabel()
    #     label.setPixmap(pixmap)
    #     name_label = QLabel('')  # 创建一个显示图片名称的标签
    #     name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)  # 居中对齐
    #     name_label.setWordWrap(True)  # 自动换行
    #     vbox = QVBoxLayout()  # 垂直布局，用于放置图片和名称标签
    #     vbox.addWidget(label)
    #     vbox.addWidget(name_label)
    #     widget = QWidget()  # 创建一个容器小部件，将垂直布局放置其中
    #     widget.setLayout(vbox)
    #     grid_layout.addWidget(widget)

    def idx_get(self,grid_layout):
        # 返回图片的名称 输入是网格布局
        label_texts = []
        for i in range(grid_layout.count()):
            print(i)
            widget = grid_layout.itemAt(i)
            if widget is not None:
                widget = widget.widget()
                if isinstance(widget, QWidget):
                    labels = widget.findChildren(QLabel)  # 查找 QWidget 下的所有 QLabel
                    for label in labels:
                        label_texts.append(label.text())
        label_texts = [text for text in label_texts if text.strip()]
        # print('上四张图片',label_texts)
        return label_texts

    # def next4get(self, label_texts, path):
    #     # 得到目前展示的四张图片名 并在地址中寻找接下来四个文件名
    #     max_numbers = [int(item.split('_')[-1].split('.')[0]) for item in label_texts]
    #     maxidx = max(max_numbers)
    #     # print('前四章图片最大',maxidx)
    #     filenames = os.listdir(path)
    #     # matching_files = [filename for filename in filenames if filename.endswith('.png')]
    #
    #     matching_numbers = [int(item.split('_')[-1].split('.')[0]) for item in filenames]
    #     matching_numbers.sort()
    #     # print('已排序',matching_numbers[:5])
    #
    #     greater_numbers = [num for num in matching_numbers if num > maxidx]
    #     # print('比较大小',greater_numbers[:4])
    #     if len(greater_numbers) == 0:
    #         # print(greater_numbers,'??')
    #         greater_numbers = matching_numbers
    #     if len(greater_numbers) >= 4:
    #         result_files = []
    #         for num in greater_numbers[:4]:
    #             print(num)
    #             matching_file = next((file for file in filenames \
    #                                   if re.search(r'\d+', file) \
    #                                   and int(re.search(r'\d+', file).group()) == num), None)
    #             # print('筛选结果',matching_file)
    #             if matching_file:
    #                 result_files.append(matching_file)
    #     if len(greater_numbers) < 4 and len(greater_numbers) > 0:
    #         result_files = []
    #         for num in greater_numbers:
    #             matching_file = next((file for file in filenames if str(num) in file), None)
    #             if matching_file:
    #                 result_files.append(matching_file)
    #
    #     return result_files

    #todo#改进:导入新的视频和图片时采取增加而不是覆盖的方式；但是首次打开文件需要清空之前的文件。 解决
    #todo#解决bug:两库图片名称一致的情况下，无法转移
    #todo#解决bug:图片转移时，有展示，无库存，不可更新；无展示，有库存，不可更新；无展示，无库存，不可更新。只有有展示，有库存才更新。解决
    #todo#重新设计图片存储方式，使得一边实现图片的转移，一边进行图片的依次展示。
    #######重新设计图片存储方式#######
    #方法1: 图片均以img0,1,2,3...命名，会导致的问题是，两库图片名称一致的情况下，无法转移。
    #       ------> imgwork0,1,2...; imgware0,1,2... 此时图片还不能判断疾病呢，这样命名没错。
    #方法2: 图片根据结尾序号0，1，2，3...依次更新，从头至尾。会导致另一边转移的新图片难以加入展示的序列。
    #       ------> 转移后立即按最大序号递增重命名。
    #方法3: 图片转移后，展示的图片不更新。
    #       ------> 转移后立即进行展示更新

    #######图片转移后展示的问题解决#######
    # nextpage1_press_clicked 链接更新下一页
    #         label_texts = self.idx_get(self.grid_layout1) # 无展示，为空，有展示，为列表
    #         name = self.next4get(label_texts, path='save//warehouse')
    #         label_texts得到后面<=4个展示图片，或者没有图片; !label_texts从头开始选取<=4个图片展示，或者没有图片
    #         如果没有图片，则返回空列表
    #         dir = [os.path.join('save//warehouse',i) for i in name] #找到图片地址并加载
    #         self.load_images_to_grid(self.box1, self.grid_layout1, dir)


    def next4get(self,label_texts, path):
        filenames = os.listdir(path)
        # matching_files = [filename for filename in filenames if filename.endswith('.png')]
        matching_numbers = [int(item.split('_')[-1].split('.')[0]) for item in filenames] # 库内
        print('这个空间没东西',matching_numbers)
        matching_numbers.sort()
        print('success sort')
        if len(matching_numbers) == 0:
            result_files = []
        else:
            if label_texts:
                # 得到目前展示的四张图片名 并在地址中寻找接下来四个文件名
                max_numbers = [int(item.split('_')[-1].split('.')[0]) for item in label_texts]
                maxidx = max(max_numbers)
                print(maxidx)
                # print('前四章图片最大',maxidx)
                # print('已排序',matching_numbers[:5])
                greater_numbers = [num for num in matching_numbers if num > maxidx]
                # print('比较大小',greater_numbers[:4])
                if len(greater_numbers)==0:
                    # print(greater_numbers,'??')
                    greater_numbers = matching_numbers
                if len(greater_numbers) >=4 :
                    result_files = []
                    for num in greater_numbers[:4]:
                        print(num)
                        matching_file = next((file for file in filenames \
                                              if re.search(r'\d+', file) \
                                              and int(re.search(r'\d+', file).group()) == num), None)
                        # print('筛选结果',matching_file)
                        if matching_file:
                            result_files.append(matching_file)
                if len(greater_numbers) < 4 and len(greater_numbers)>0 :
                    result_files = []
                    for num in greater_numbers:
                        matching_file = next((file for file in filenames if str(num) in file), None)
                        if matching_file:
                            result_files.append(matching_file)
            else:
                result_files = []
                # 目前没有展示 但是仓库里有东西，可能是新添加的
                if len(matching_numbers) >= 4:
                    print('目前没有展示 但是仓库里有东西，可能是新添加的>=4')
                    result_files = matching_numbers[:4].copy()
                    for num in result_files:
                        matching_file = next((file for file in filenames if str(num) in file), None)
                        # print('筛选结果',matching_file)
                        if matching_file:
                            result_files.append(matching_file)
                    print(result_files)
                else:
                    print('目前没有展示 但是仓库里有东西，可能是新添加的<4')
                    print( matching_numbers)
                    # result_files = matching_numbers.copy()
                    for num in matching_numbers:
                        print(num)
                        matching_file = next((file for file in filenames if str(num) in file), None)
                        print('??')
                        if matching_file:
                            result_files.append(matching_file)
                    print(result_files)
        return result_files



    def load_images_from_folder(self, folder_path):
        image_paths = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(folder_path, filename)
                image_paths.append(image_path)
        return image_paths
        # 文件夹中导入图片路径并作为列表输出
        # return ["path_to_image1", "path_to_image2", "path_to_image3", ...]

    def load_next_page(self):
        # Clear the current grid layout and load images for the next page
        for i in reversed(range(self.grid_layout2.count())):
            self.grid_layout2.itemAt(i).widget().setParent(None)
        self.load_images_to_grid(self.grid_layout2, "path_to_next_page_images_folder")


    def init_action(self):
        self.btn1.clicked.connect(self.btn1_press_clicked)
        self.btn2.clicked.connect(self.btn2_press_clicked)
        self.nextpage2.clicked.connect(self.nextpage2_press_clicked)
        self.nextpage1.clicked.connect(self.nextpage1_press_clicked)

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

    def nextpage2_press_clicked(self):
        label_texts = self.idx_get(self.grid_layout2)
        name = self.next4get(label_texts, path='save//workroom')
        print(name)
        dir = [os.path.join("save//workroom",i) for i in name]
        print(dir)
        self.load_images_to_grid(self.box2, self.grid_layout2, dir)

    def nextpage1_press_clicked(self):
        label_texts = self.idx_get(self.grid_layout1)
        name = self.next4get(label_texts, path='save//warehouse')
        dir = [os.path.join('save//warehouse',i) for i in name]
        self.load_images_to_grid(self.box1, self.grid_layout1, dir)

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