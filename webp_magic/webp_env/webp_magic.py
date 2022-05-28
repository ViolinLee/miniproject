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
from PIL import Image
from pathlib import Path
import traceback

# pass input_image(.jpeg,.pnp .....) path ,
# output_image(give path where to save and image file name with .webp file type extension)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pwd = os.getcwd()  # 防止表无数据
        self.quality = 50  # 防止表无数据
        self.QualitySliderBar.setValue(self.quality)
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
        self.QualitySliderBar.valueChanged[int].connect(self.changeValue)
        self.checkBox.stateChanged.connect(self.checkBoxChange)
        self.checkBox.toggle()

    def checkBoxChange(self, state):
        if state == QtCore.Qt.Checked:
            self.checked = True
        else:
            self.checked = False
        # print(self.checked)

    def changeValue(self, value):
        self.quality = value
        cursor = self.conn.cursor()
        sql = 'insert or replace into webp_config (id, quality) values (0, {});'.format(self.quality)
        cursor.execute(sql)
        self.conn.commit()
        self.statusbar.showMessage("设置图片压缩质量：{}%".format(self.quality))

    def open_dir(self):
        file_directory = QFileDialog.getExistingDirectory(QMainWindow(), "选择文件夹", self.pwd)
        self.pwd = file_directory
        self.statusbar.showMessage("打开路径！{}".format(self.pwd))

    def initialize_config(self):
        self.create_config_table_if_not_exite()
        cursor = self.conn.cursor()
        cursor.execute('select path, quality from webp_config')
        config = cursor.fetchone()
        if config is None:
            pass
        else:
            self.pwd = config[0] if config[0] is not None else os.getcwd()
            self.quality = config[1]
            self.QualitySliderBar.setValue(self.quality)
            self.statusbar.showMessage("默认目录初始化：{}  图片压缩质量：{}%".format(self.pwd, self.quality))

    def set_root(self):
        if os.path.exists(self.pwd):
            cursor = self.conn.cursor()
            sql = 'insert or replace into webp_config (id, path, quality) values (0, "{}", 50);'.format(self.pwd)
            cursor.execute(sql)
            self.conn.commit()
            self.statusbar.showMessage("默认目录设置成功")
        else:
            self.statusbar.showMessage("默认目录设置失败")

    def transfer_webp(self):
        if self.checked:
            webp_path = os.path.join(self.pwd, 'webp')
            if not os.path.exists(webp_path):
                os.mkdir(webp_path)
            else:
                pass
        else:
            webp_path = self.pwd
        # print(webp_path)

        image_paths = glob(self.pwd + '/*.jpg') + glob(self.pwd + '/*.png')
        for image_path in image_paths:
            try:
                image_name = image_path.split('\\')[-1]
                image_name = image_name.replace('.jpg', '.webp').replace('.png', '.webp')
                output_image = os.path.join(webp_path, image_name)
                # print(output_image)

                """
                cwebp(input_image=image_path, output_image=output_image, option="-q 80", logging="-v")
                """
                source = Path(image_path)
                destination = output_image  # source.with_suffix(".webp")
                image = Image.open(source)  # Open image
                image.save(destination, format="webp", quality=self.quality)  # Convert image to webp
                self.statusbar.showMessage("恭喜聪明婷婷 WebP文件转换成功！")
            except:
                traceback.print_exc()
                self.statusbar.showMessage("无法转换文件：{}".format(image_path))

    def create_config_table_if_not_exite(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS webp_config (id integer primary key, path text, quality integer);')
        self.conn.commit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.window_init()
    window.show()
    sys.exit(app.exec_())
