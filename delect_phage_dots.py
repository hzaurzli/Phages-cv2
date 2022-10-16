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
        self.setGeometry(600,100,1125,600)
        self.lbl=QLabel("",self)
        # self.pm=QPixmap()
        # self.lbl.setPixmap(self.pm)
        self.lbl.resize(500,500)
        self.lbl.move(50,30)
        self.lbl.setScaledContents(True)

        self.lbl2 = QLabel("", self)
        self.lbl2.resize(500, 500)
        self.lbl2.move(570, 30)
        self.lbl2.setScaledContents(True)


        #移除按钮
        btn1=QPushButton("remove figure",self)
        btn1.clicked.connect(self.myRemovePic)
        btn1.move(120,550)
        #增加按钮
        btn2=QPushButton("add figure",self)
        btn2.clicked.connect(self.myAddPic)
        btn2.move(25,550)

        btn3 = QPushButton("counting", self)
        btn3.clicked.connect(lambda: self.counting(openfile_name)) # 信号函数传参
        btn3.move(270, 550)
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
        params.maxThreshold = 200
        params.thresholdStep = 5.5

        params.filterByColor = True
        # params.blobColor = 0
        params.blobColor = 0

        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 5000

        params.filterByCircularity = True
        params.minCircularity = 0.3

        params.filterByConvexity = True
        params.minConvexity = 0.6

        params.filterByInertia = True
        params.minInertiaRatio = 0.6

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(gauss)

        im_with_keypoints = cv2.drawKeypoints(img0, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        x_coordinate = []
        for (x, y) in keypoints[0].convert(keypoints):
            x_coordinate.append(x)

        x_coordinate.sort()
        print("共检测出%d个斑点" % len(x_coordinate))
        cv2.imwrite(os.path.dirname(file) + '/tmp.jpg', im_with_keypoints)
        self.lbl2.setPixmap(QPixmap(os.path.dirname(file) + '/tmp.jpg'))

        QMessageBox.information(self, "Dots", "Dots number is %d" % len(x_coordinate), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)


if __name__=="__main__":
    app=QApplication(sys.argv)
    mc=MyClass()
    app.exec_()