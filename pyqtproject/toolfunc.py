'''
author: Zoe Wu
project: pyqtproject
data: 2023-08-27

Enjoy!
'''
# 地址内最大结尾数值,输出新文件开始idx
import os

#
def nextidx(path):
    print(os.path.exists(path),'???')
    filenames = os.listdir(path)
    print(filenames[:3])
    if filenames:
        print('?')
        idx = max([int(file.split('_')[-1].split('.')[0]) for file in filenames])
    else:
        idx = -1
    print(idx,'it is')
    return idx+1

def clear_file(path):
#   清空文件夹内文件
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # 删除文件

