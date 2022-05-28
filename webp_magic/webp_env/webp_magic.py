"""
设置根目录，选择文件夹，批量转换为webp
"""


import os
import sys
import sqlite3
from glob import glob
from PySide2 import QtGui, QtWidgets, QtCore
# from PySide2.QtCore import QDir, QTimer, QSize
# from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from webp_magic_ui import Ui_MainWindow
from webptools import cwebp
from pillow import image
from pathlib import Path

# pass input_image(.jpeg,.pnp .....) path ,
# output_image(give path where to save and image file name with .webp file type extension)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pwd = os.getcwd()
        self.conn = sqlite3.connect('webp_magic.db')
        self.initialize_config()

    def window_init(self):
        self.pushButton.setText("选择转换目录")
        self.pushButton_2.setText("设置默认目录")
        self.pushButton_3.setText("WebP 批量转换")
        # 设置控件属性
        self.pushButton.clicked.connect(self.open_dir)
        self.pushButton_2.clicked.connect(self.set_root)
        self.pushButton_3.clicked.connect(self.transfer_webp)

    def open_dir(self):
        file_directory = QFileDialog.getExistingDirectory(QMainWindow(), "选择文件夹", self.pwd)
        self.pwd = file_directory
        self.statusbar.showMessage("打开路径！{}".format(self.pwd))

    def initialize_config(self):
        self.create_config_table_if_not_exite()
        cursor = self.conn.cursor()
        cursor.execute('select path from webp_config')
        self.pwd = cursor.fetchone()[0]
        self.statusbar.showMessage("默认目录初始化：{}".format(self.pwd))

    def set_root(self):
        cursor = self.conn.cursor()
        sql = 'insert or replace into webp_config (id, path) values (0, "{}");'.format(self.pwd)
        cursor.execute(sql)
        self.conn.commit()
        window.statusbar.showMessage("默认目录设置成功")

    def transfer_webp(self):
        image_paths = glob(os.path.join(self.pwd, '/*.jpg')) + glob(self.pwd + '/*.png')
        for image_path in image_paths:
            try:
                output_image = image_path.replace('.jpg', '.webp').replace('.png', '.webp')
                cwebp(input_image=image_path, output_image=output_image, option="-q 80", logging="-v")
                window.statusbar.showMessage("恭喜聪明婷婷 WebP文件转换成功！")
            except:
                window.statusbar.showMessage("无法转换文件：{}".format(image_path))

    def create_config_table_if_not_exite(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS webp_config (id integer primary key, path text);')
        self.conn.commit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.window_init()
    window.show()
    sys.exit(app.exec_())
