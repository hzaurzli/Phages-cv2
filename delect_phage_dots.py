import sys,os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
import pandas as pd


class Dialog(QtWidgets.QDialog):
    """对QDialog类重写，实现一些功能"""

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        if os.path.exists(os.path.dirname(openfile_name) + '/tmp.jpg') == True:
            os.remove(os.path.dirname(openfile_name) + '/tmp.jpg')


class MyClass(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("By Small runze")
        self.setGeometry(600,100,1125,800)
        self.lbl=QLabel("",self)
        self.lbl.resize(500,500)
        self.lbl.move(50,30)
        self.lbl.setScaledContents(True)

        self.lbl2 = QLabel("", self)
        self.lbl2.resize(500, 500)
        self.lbl2.move(570, 30)
        self.lbl2.setScaledContents(True)

        # 添加文本标签
        self.label = QLabel("", self)
        self.label.move(25, 558)
        self.label.setFont(QtGui.QFont("Roman times", 15))
        self.label.setText("ThresholdStep:")
        # 添加设置一个文本框
        self.text = QtWidgets.QLineEdit("", self)
        # 调整文本框的位置大小
        self.text.setGeometry(QtCore.QRect(180, 555, 180, 30))
        self.text.setPlaceholderText("  5.5; step length")

        # 添加文本标签
        self.label2 = QLabel("", self)
        self.label2.move(400, 558)
        self.label2.setFont(QtGui.QFont("Roman times", 15))
        self.label2.setText("MinCircularity:")
        # 添加设置一个文本框
        self.text2 = QtWidgets.QLineEdit("", self)
        # 调整文本框的位置大小
        self.text2.setGeometry(QtCore.QRect(570, 555, 180, 30))
        self.text2.setPlaceholderText("  0.3; range 0-1")


        # 添加文本标签
        self.label3 = QLabel("", self)
        self.label3.move(25, 638)
        self.label3.setFont(QtGui.QFont("Roman times", 15))
        self.label3.setText("MinConvexity:")
        # 添加设置一个文本框
        self.text3 = QtWidgets.QLineEdit("", self)
        # 调整文本框的位置大小
        self.text3.setGeometry(QtCore.QRect(180, 635, 180, 30))
        self.text3.setPlaceholderText("  0.6; range 0-1")

        # 添加文本标签
        self.label4 = QLabel("", self)
        self.label4.move(400, 638)
        self.label4.setFont(QtGui.QFont("Roman times", 15))
        self.label4.setText("MinInertiaRatio:")
        # 添加设置一个文本框
        self.text4 = QtWidgets.QLineEdit("", self)
        # 调整文本框的位置大小
        self.text4.setGeometry(QtCore.QRect(570, 635, 180, 30))
        self.text4.setPlaceholderText("  0.6; range 0-1")

        # 添加文本标签
        self.label5 = QLabel("", self)
        self.label5.move(800, 558)
        self.label5.setFont(QtGui.QFont("Roman times", 15))
        self.label5.setText("BlobColor:")
        # 添加设置一个文本框
        self.text5 = QtWidgets.QLineEdit("", self)
        # 调整文本框的位置大小
        self.text5.setGeometry(QtCore.QRect(920, 555, 130, 30))
        self.text5.setPlaceholderText("  0; range 0-255")

        # 添加文本标签
        self.label6 = QLabel("", self)
        self.label6.move(800, 638)
        self.label6.setFont(QtGui.QFont("Roman times", 15))
        self.label6.setText("MinArea:")
        # 添加设置一个文本框
        self.text6 = QtWidgets.QLineEdit("", self)
        # 调整文本框的位置大小
        self.text6.setGeometry(QtCore.QRect(920, 635, 130, 30))
        self.text6.setPlaceholderText("  100; range > 0")


        # 添加文本标签
        self.label7 = QLabel("", self)
        self.label7.move(800, 718)
        self.label7.setFont(QtGui.QFont("Roman times", 15))
        self.label7.setText("MaxArea:")
        # 添加设置一个文本框
        self.text7 = QtWidgets.QLineEdit("", self)
        # 调整文本框的位置大小
        self.text7.setGeometry(QtCore.QRect(920, 715, 130, 30))
        self.text7.setPlaceholderText("  5000; range > 0")


        #移除按钮
        btn1 = QPushButton("Remove figure",self)
        btn1.setGeometry(150, 750, 100, 30)
        btn1.setFont(QtGui.QFont("", 10))
        btn1.clicked.connect(self.myRemovePic)

        #增加按钮
        btn2 = QPushButton("Add figure",self)
        btn2.setGeometry(25, 750, 100, 30)
        btn2.clicked.connect(self.myAddPic)
        btn2.setFont(QtGui.QFont("", 10))

        btn3 = QPushButton("Counting", self)
        btn3.setGeometry(350, 750, 100, 30)
        btn3.setFont(QtGui.QFont("", 10))
        btn3.clicked.connect(lambda: self.counting(openfile_name))  # 信号函数传参

        self.show()

    def myRemovePic(self):
        self.lbl.setPixmap(QPixmap(""))
        self.lbl2.setPixmap(QPixmap(""))
        if os.path.exists(os.path.dirname(openfile_name) + '/tmp.jpg') == True:
            os.remove(os.path.dirname(openfile_name) + '/tmp.jpg')


    def myAddPic(self):
        global openfile_name
        openfile_name = QFileDialog.getOpenFileName(self, 'choose figures', '')[0]
        print(openfile_name)
        self.lbl.setPixmap(QPixmap(openfile_name))


    def counting(self,file):

        def cv_show_image(name, img):
            cv2.namedWindow(name, 0)
            cv2.imshow(name, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        img0 = cv2.imread(openfile_name)
        gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
        gauss = cv2.GaussianBlur(gray, (9, 9), 0)

        params = cv2.SimpleBlobDetector_Params()
        # parameter
        params.minThreshold = 100
        params.maxThreshold = 255
        try:
            params.thresholdStep = float(self.text.text())
        except:
            params.thresholdStep = 5.5

        params.filterByColor = True
        # params.blobColor = 0
        try:
            params.blobColor = float(self.text5.text())
        except:
            params.blobColor = 0


        params.filterByArea = True
        try:
            params.minArea = float(self.text6.text())
        except:
            params.minArea = 100
        try:
            params.maxArea = float(self.text7.text())
        except:
            params.maxArea = 5000


        params.filterByCircularity = True
        try:
            params.minCircularity = float(self.text2.text())
        except:
            params.minCircularity = 0.3

        params.filterByConvexity = True
        try:
            params.minConvexity = float(self.text3.text())
        except:
            params.minConvexity = 0.6

        params.filterByInertia = True
        try:
            params.minInertiaRatio = float(self.text4.text())
        except:
            params.minInertiaRatio = 0.6

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(gauss)

        im_with_keypoints = cv2.drawKeypoints(img0, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        try:
            x_coordinate = []
            for (x, y) in keypoints[0].convert(keypoints):
                x_coordinate.append(x)

            x_coordinate.sort()
            print("共检测出%d个斑点" % len(x_coordinate))
            cv2.imwrite(os.path.dirname(file) + '/tmp.jpg', im_with_keypoints)
            self.lbl2.setPixmap(QPixmap(os.path.dirname(file) + '/tmp.jpg'))

            QMessageBox.information(self, "Dots", "Dots number is %d" % len(x_coordinate), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        except:
            QMessageBox.critical(self, "Critical", "Please adjust the resolution", QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)


if __name__=="__main__":
    app=QApplication(sys.argv)
    mc=MyClass()
    app.exec_()