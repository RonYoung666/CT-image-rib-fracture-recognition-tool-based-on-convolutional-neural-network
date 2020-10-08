##-*- coding: utf-8 -*-

import sys, os, time, re
from enum import Enum   ##枚举类型
from functools import partial

from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QLabel, QProgressBar, QFileDialog, QDockWidget, QProgressDialog, QAction
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QDir, QFileInfo, QSize, QThread, QObject
from PyQt5.QtGui import QIcon, QImage, QPixmap, qGray, QPalette, QBrush

from ui_MainWindow import Ui_MainWindow
from detector import Detector

from PIL import Image
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import cv2

import random
import time

import label_map_util
import visualization_utils as vis_util

class TreeItemType(Enum):    ##节点类型枚举类型
   itemPatient = 1001    #顶层节点
   itemType = 1002  #组节点 
   itemFile = 1003  #CT文件节点


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.curPixmap=QPixmap()   #图片
        self.pixRatio=1            #显示比例
        self.itemFlags=(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  #节点标志


        self.ui.mainToolBar.setIconSize(QSize(40, 40))    ##设置工具栏图标大小
        self.ui.mainToolBar.setFixedHeight(70)    ##设置工具栏高度
        self.setCentralWidget(self.ui.splitterH)    ##使splitter充满工作区
        #self.setCentralWidget(self.ui.scrollArea)

        self.setWindowTitle("CT Rib Fracture Detector")
        self.showMaximized()    ##全屏显示

        ##设置背景颜色
        self.setStyleSheet("#MainWindow{background-color:white}")

        ##设置图片区初始颜色
        pe = QPalette()
        pe.setColor(QPalette.Background, Qt.white)
        self.ui.labPicture.setAutoFillBackground(True)
        self.ui.labPicture.setPalette(pe)

        ##检测框显隐按钮属性
        self.iconHideBox = QIcon()
        self.iconHideBox.addPixmap(QPixmap(":/images/icons/hidebox.png"), QIcon.Normal, QIcon.Off)
        self.iconShowBox = QIcon()
        self.iconShowBox.addPixmap(QPixmap(":/images/icons/showbox.png"), QIcon.Normal, QIcon.Off)
        self.actBoxFlag = 0    ##0:隐藏Box  1:显示Box

        self.ui.actBox.setEnabled(True)
        self.ui.actBox.setVisible(False)

        ##在工具栏上添加QLabel和QProgressBar
        self.lab1 = QLabel(self)
        self.lab1.setMinimumWidth(50)
        self.actLab1 = self.ui.mainToolBar.addWidget(self.lab1)
        self.actLab1.setVisible(False)

        self.prg = QProgressBar(self)
        self.prg.setMinimumWidth(100)
        self.prg.setMaximumWidth(300)
        self.actPrg = self.ui.mainToolBar.addWidget(self.prg)
        self.actPrg.setVisible(False)
        

        self.lab2 = QLabel(self)
        self.lab2.setMinimumWidth(300)
        self.actLab2 = self.ui.mainToolBar.addWidget(self.lab2)
        self.actLab2.setVisible(False)

        self.numTotal = 0
        self.numLoad = 0

        ##失效检测按钮
        self.ui.actDetect.setEnabled(False)
        self.ui.actDetectThis.setEnabled(False)

        ##设置树的宽度
        self.ui.treeFiles.setColumnWidth(0, 220)
        self.ui.treeFiles.setColumnWidth(1, 40)


##  =================自定义功能函数================================
    ##显示已检测的图片
    def __displayDetectedImage(self, item):
        dcmFileName = item.data(0, Qt.UserRole)
        self.ui.statusBar.showMessage(dcmFileName)

        #预处理
        dcmFile = pydicom.read_file(dcmFileName)
        origin = dcmFile.pixel_array # type:numpy.ndarray

        intercept = dcmFile.RescaleIntercept
        slope = dcmFile.RescaleSlope
        origin = origin * slope + intercept
        origin[origin < -100] = -100 # 去除低亮部分
        origin[origin > 750] = 750 # 去除高亮部分

        # 归一化到0-255
        origin = cv2.normalize(origin, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC3) 
        image_np = np.expand_dims(origin,-1) # 将origin增加一个维度
        image_np = np.repeat(image_np,3,2) # 将二维矩阵重复三次

        #plt.imsave("output/undetected.jpg", image_np)

        NUM_CLASSES = 6
        PATH_TO_LABELS = 'label_map.pbtxt'
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        result = item.data(1, Qt.UserRole)
        boxes = result[1]
        scores = result[2]
        classes = result[3]
        
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            boxes,
            classes,
            scores,
            category_index,
            use_normalized_coordinates=True,
            line_thickness=1)

        #plt.imsave("output/detected.jpg", image_np)
        image = QImage(image_np, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)  

        self.curPixmap = QPixmap(image)
        self.on_actZoomFitH_triggered()

        self.ui.actZoomIn.setEnabled(True)
        self.ui.actZoomOut.setEnabled(True)
        self.ui.actZoomRealSize.setEnabled(True)
        self.ui.actZoomFitW.setEnabled(True)
        self.ui.actZoomFitH.setEnabled(True)


    ##显示图片
    def __displayImage(self, item):
        dcmFileName = item.data(0, Qt.UserRole)
        self.ui.statusBar.showMessage(dcmFileName)

        #预处理
        dcmFile = pydicom.read_file(dcmFileName)
        origin = dcmFile.pixel_array # type:numpy.ndarray

        intercept = dcmFile.RescaleIntercept
        slope = dcmFile.RescaleSlope
        origin = origin * slope + intercept
        origin[origin < -100] = -100 # 去除低亮部分
        origin[origin > 750] = 750 # 去除高亮部分

        # 归一化到0-255
        #origin = cv2.normalize(origin, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC3) 
        origin = cv2.normalize(origin, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1) 
        #rgb = np.expand_dims(origin,-1) # 将origin增加一个维度
        #rgb = np.repeat(rgb,3,2) # 将二维矩阵重复三次

        image = QImage(origin[:], origin.shape[1], origin.shape[0], origin.shape[1], QImage.Format_Indexed8)  
        self.curPixmap = QPixmap(image)
        self.on_actZoomFitH_triggered()

        self.ui.actZoomIn.setEnabled(True)
        self.ui.actZoomOut.setEnabled(True)
        self.ui.actZoomRealSize.setEnabled(True)
        self.ui.actZoomFitW.setEnabled(True)
        self.ui.actZoomFitH.setEnabled(True)


##  ===========connectSlotsByName() 自动连接的槽函数=================        
    @pyqtSlot()
    def on_actOpen_triggered(self):
        ##返回的文件夹路径
        path = QFileDialog.getExistingDirectory()
        if(path == ""):
            return

        ##生成进度条组件
        self.numTotal = len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))])    ##文件总数
        self.numLoad = 0    ##已加载数
        self.lab1.setText(" 加载中")
        self.prg.setRange(0, self.numTotal)
        self.prg.setValue(0)
        self.lab2.setText(" 剩余文件：" + str(self.numTotal - self.numLoad))
        self.actLab1.setVisible(True)
        self.actPrg.setVisible(True)
        self.actLab2.setVisible(True)

        print("From mainThread: ", QThread.currentThreadId())

        ##建立工作线程
        workThread = QThread(parent=self)

        openDir= OpenDir(path, self.itemFlags)
        openDir.moveToThread(workThread)
        openDir.dirError.connect(self.do_dirError)
        openDir.newDcmFile.connect(self.do_newDcmFile)
        openDir.openFinished.connect(self.do_openFinished)
        openDir.openFinished.connect(workThread.quit)
        workThread.started.connect(lambda:openDir.run(self.ui.treeFiles))

        workThread.start()


    def do_dirError(self):
        self.lab2.setText("不是患者文件夹，请重新选择！")

    def do_newDcmFile(self):
        self.numLoad = self.numLoad + 1
        self.prg.setValue(self.numLoad)
        self.lab2.setText(" 剩余文件：" + str(self.numTotal - self.numLoad))

    def do_openFinished(self):
        self.actLab1.setVisible(False)
        self.actPrg.setVisible(False)
        self.actLab2.setVisible(False)

        self.ui.actDetect.setEnabled(True)


    ##检测所有按钮触发
    @pyqtSlot()
    def on_actDetect_triggered(self):
        self.ui.actDetect.setEnabled(False)
        self.ui.actOpen.setEnabled(False)
        topItem = self.ui.treeFiles.topLevelItem(0)

        ##显示进度条组件
        self.numTotal = 0
        for i in range(topItem.childCount()):
            self.numTotal = self.numTotal + topItem.child(i).childCount()
        self.numLoad = 0    ##已加载数
        self.lab1.setText(" 检测中")
        self.prg.setRange(0, self.numTotal)
        self.prg.setValue(0)
        self.lab2.setText(" 剩余文件：" + str(self.numTotal - self.numLoad))
        self.actLab1.setVisible(True)
        self.actPrg.setVisible(True)
        self.actLab2.setVisible(True)

        #print("From mainThread: ", QThread.currentThreadId())

        ##建立工作线程
        workThread = QThread(parent=self)

        self.detectTreeFiles = DetectTreeFiles(self.ui.treeFiles)
        self.detectTreeFiles.moveToThread(workThread)
        self.detectTreeFiles.detecting.connect(self.do_detecting)
        self.detectTreeFiles.gotResult.connect(self.do_gotResult)
        self.detectTreeFiles.gotAllResult.connect(self.do_gotAllResult)
        self.detectTreeFiles.gotAllResult.connect(workThread.quit)
        workThread.started.connect(self.detectTreeFiles.run)

        workThread.start()


    ##正检测在某节点
    def do_detecting(self, index):
        i = index[0]
        j = index[1]
        item = self.ui.treeFiles.topLevelItem(0).child(i).child(j)
        item.setText(1, "检测中...")
        item.setTextAlignment(1, Qt.AlignCenter)


    ##得到检测结果
    def do_gotResult(self, result):
        i = result[4]
        j = result[5]
        del result[5]
        del result[4]
        item = self.ui.treeFiles.topLevelItem(0).child(i).child(j)

        classes = result[3]
        brush = QBrush(Qt.SolidPattern)
        if 5.0 in classes:
            item.setText(1, "骨质异常")
            brush.setColor(Qt.GlobalColor.cyan)
        elif 3.0 in classes or 4.0 in classes:
            item.setText(1, "骨折")
            brush.setColor(Qt.GlobalColor.red)
        elif 6.0 in classes:
            item.setText(1, "发育异变")
            brush.setColor(Qt.GlobalColor.yellow)
        else:
            item.setText(1, "正常")
            brush.setColor(Qt.GlobalColor.white)
        item.setBackground(1, brush)
        item.setTextAlignment(1, Qt.AlignCenter)
        item.setData(1, Qt.UserRole, result)

        ##进度条
        self.numLoad = self.numLoad + 1
        self.prg.setValue(self.numLoad)
        self.lab2.setText(" 剩余文件：" + str(self.numTotal - self.numLoad))


    def do_gotAllResult(self):
        ##隐藏进度条
        self.actLab1.setVisible(False)
        self.actPrg.setVisible(False)
        self.actLab2.setVisible(False)

        self.ui.actOpen.setEnabled(True)


    ##检测当前按钮触发
    @pyqtSlot()
    def on_actDetectThis_triggered(self):
        self.ui.actOpen.setEnabled(False)
        self.ui.actDetect.setEnabled(False)
        self.ui.actDetectThis.setEnabled(False)

        print("From mainThread: ", QThread.currentThreadId())

        ##建立工作线程
        workThread = QThread(parent=self)

        detectThis = DetectThis()
        detectThis.moveToThread(workThread)
        detectThis.gotThisResult.connect(self.do_gotThisResult)
        detectThis.gotThisResult.connect(workThread.quit)
        #workThread.started.connect(lambda:detectThis.run(item))
        workThread.started.connect(partial(detectThis.run, self.ui.treeFiles.currentItem()))

        workThread.start()

        item = self.ui.treeFiles.currentItem()
        item.setText(1, "检测中...")
        item.setTextAlignment(1, Qt.AlignCenter)


    ##得到当前检测结果
    def do_gotThisResult(self):
        self.ui.actOpen.setEnabled(True)
        self.ui.actDetect.setEnabled(True)


    ##检测框显隐按钮触发
    @pyqtSlot()
    def on_actBox_triggered(self):
        if self.actBoxFlag == 0:    ##隐藏
            self.__displayImage(self.ui.treeFiles.currentItem())
            self.actBoxFlag = 1
            self.ui.actBox.setIcon(self.iconShowBox)
            self.ui.actBox.setText("显示Box")
            self.ui.actBox.setToolTip("显示检测框")

        else:    ##显示
            self.__displayDetectedImage(self.ui.treeFiles.currentItem())
            self.actBoxFlag = 0
            self.ui.actBox.setIcon(self.iconHideBox)
            self.ui.actBox.setText("隐藏Box")
            self.ui.actBox.setToolTip("隐藏检测框")


    ##当前选中节点改变
    def on_treeFiles_currentItemChanged(self, current, previous):
        if (current == None or current == previous):
            self.ui.actBox.setVisible(False)
            return
        nodeType = current.type()

        if nodeType == TreeItemType.itemFile.value:
            detected = current.data(1, Qt.UserRole)[0]
            if detected:
                self.__displayDetectedImage(current)    ##显示已检测图片
                self.actBoxFlag = 0
                self.ui.actBox.setIcon(self.iconHideBox)
                self.ui.actBox.setText("隐藏Box")
                self.ui.actBox.setToolTip("隐藏检测框")
                self.ui.actBox.setVisible(True)
                self.ui.actDetectThis.setEnabled(False)
            else:
                self.__displayImage(current)    ##显示图片
                self.ui.actBox.setVisible(False)
                self.ui.actDetectThis.setEnabled(True)
            return

        self.ui.actDetectThis.setEnabled(False)

        if nodeType == TreeItemType.itemType.value:
            current.setExpanded(True)

        self.ui.actBox.setVisible(False)

        self.ui.actZoomIn.setEnabled(False)
        self.ui.actZoomOut.setEnabled(False)
        self.ui.actZoomRealSize.setEnabled(False)
        self.ui.actZoomFitW.setEnabled(False)
        self.ui.actZoomFitH.setEnabled(False)


    @pyqtSlot()  ##适应高度显示图片
    def on_actZoomFitH_triggered(self): 
        H=self.ui.scrollArea.height() #得到scrollArea的高度
        realH=self.curPixmap.height() #原始图片的实际高度
        self.pixRatio=float(H)/realH  #当前显示比例，必须转换为浮点数
        pix=self.curPixmap.scaledToHeight(H-30) #图片缩放到指定高度
        self.ui.labPicture.setPixmap(pix)         #设置Label的PixMap

    @pyqtSlot()  ##适应宽度显示
    def on_actZoomFitW_triggered(self): 
        W=self.ui.scrollArea.width()-20
        realW=self.curPixmap.width() 
        self.pixRatio=float(W)/realW
        pix=self.curPixmap.scaledToWidth(W-30) 
        self.ui.labPicture.setPixmap(pix)         #设置Label的PixMap

    @pyqtSlot()    ##实际大小
    def on_actZoomRealSize_triggered(self): 
        self.pixRatio=1  #恢复显示比例为1
        self.ui.labPicture.setPixmap(self.curPixmap)

    @pyqtSlot()  ##放大显示
    def on_actZoomIn_triggered(self):  
        self.pixRatio=self.pixRatio*1.2
        W=self.pixRatio*self.curPixmap.width()
        H=self.pixRatio*self.curPixmap.height()
        pix=self.curPixmap.scaled(W,H)  #图片缩放到指定高度和宽度，保持长宽比例
        self.ui.labPicture.setPixmap(pix)

    @pyqtSlot() ##缩小显示
    def on_actZoomOut_triggered(self): 
        self.pixRatio=self.pixRatio*0.8
        W=self.pixRatio*self.curPixmap.width()
        H=self.pixRatio*self.curPixmap.height()
        pix=self.curPixmap.scaled(W,H)     #图片缩放到指定高度和宽度，保持长宽比例
        self.ui.labPicture.setPixmap(pix)


##打开患者文件夹
class OpenDir(QObject):
    dirError = pyqtSignal()
    newDcmFile = pyqtSignal()
    openFinished = pyqtSignal()
    def __init__(self, path, itemFlags, parent=None):
        super().__init__(parent)
        self.path = path
        self.itemFlags = itemFlags

    def run(self, treeFiles):
        print("From workThread: ", QThread.currentThreadId())

        dcmList = os.listdir(self.path)    ##文件列表

        ##添加根节点
        for dcm in dcmList:
            dcmFile = self.path + '/' + dcm
            if os.path.isdir(dcmFile):
                continue
            if os.path.splitext(dcm)[-1] != ".dcm": # 跳过非dcm文件
                continue
            sliceFile = pydicom.read_file(dcmFile)
            patientName = str(sliceFile.PatientName)
            break
        else:
            self.dirError.emit()
            return
        treeFiles.clear()
        icon = QIcon(":/images/icons/patient.png")
        topItem = TreeWidgetItem(TreeItemType.itemPatient.value)
        topItem.setIcon(0, icon)
        topItem.setText(0, patientName)
        topItem.setFlags(self.itemFlags)
        topItem.setData(0, Qt.UserRole, "")
        topItem.setExpanded(True)
        topItem.setDisabled(False)
        treeFiles.addTopLevelItem(topItem)

        ##遍历患者文件夹
        for dcm in dcmList:
            #dcmFile = os.path.join(path, dcm)
            dcmFile = self.path + '/' + dcm

            if os.path.isdir(dcmFile):
                continue

            self.newDcmFile.emit()

            if os.path.splitext(dcm)[-1] != ".dcm": # 跳过非dcm文件
                continue

            sliceFile = pydicom.read_file(dcmFile)
            seriesDescription = str(sliceFile.SeriesDescription)

            ##只加载切片文件
            match = re.match(r"(.*?)mm(.*?)", seriesDescription, re.M | re.I)
            if not match:
                continue

            ##添加Type节点
            #exist = treeFiles.findItems(seriesDescription, Qt.MatchExactly | Qt.MatchRecursive)
            #if exist:
            #else:
            typeNum = os.path.splitext(dcmFile)[-2]
            typeNum = os.path.splitext(typeNum)[-2]
            typeNum = os.path.splitext(typeNum)[-1]
            typeNum = typeNum[1:]
            for i in range(topItem.childCount()):
                item = topItem.child(i)
                if item.data(0, Qt.UserRole) == typeNum:
                    parentItem = item
                    break
            else:
                icon = QIcon(":/images/icons/type.png")
                #item = QTreeWidgetItem(TreeItemType.itemType.value)
                item = TreeWidgetItem(TreeItemType.itemType.value)
                item.setIcon(0, icon)
                item.setText(0, seriesDescription)
                item.setFlags(self.itemFlags)
                item.setData(0, Qt.UserRole, typeNum)
                topItem.addChild(item)
                parentItem = item

            ##添加节点
            icon = QIcon(":/images/icons/file.png")
            #item = QTreeWidgetItem(TreeItemType.itemFile.value)
            item = TreeWidgetItem(TreeItemType.itemFile.value)
            item.setIcon(0, icon)
            item.setText(0, dcm)
            item.setFlags(self.itemFlags)
            item.setData(0, Qt.UserRole, dcmFile)

            result = [False]
            item.setData(1, Qt.UserRole, result)

            parentItem.addChild(item)

        ##对节点排序
        for i in range(topItem.childCount()):
            item = topItem.child(i)
            item.sortChildren(0, Qt.SortOrder.AscendingOrder)
        #topItem.sortChildren(0, Qt.SortOrder.AscendingOrder)
        topItem.setExpanded(True)

        self.openFinished.emit()


##检测所有
class DetectTreeFiles(QObject):
    detecting = pyqtSignal(list)
    gotResult = pyqtSignal(list)
    gotAllResult = pyqtSignal()
    def __init__(self, treeFiles, parent=None):
        super().__init__(parent)
        self.treeFiles = treeFiles

    def run(self):
        #print("From workThread: ", QThread.currentThreadId())
        detector = Detector()
        topItem = self.treeFiles.topLevelItem(0)
        for i in range(topItem.childCount()):
            typeItem = topItem.child(i)
            for j in range(typeItem.childCount()):
                item = typeItem.child(j)
                detected = item.data(1, Qt.UserRole)[0]
                if detected:
                    continue
                self.detecting.emit([i, j])

                dcmFileName = item.data(0, Qt.UserRole)
                result = detector.detect(dcmFileName)
                result.insert(0, True)
                result.append(i)
                result.append(j)

                self.gotResult.emit(result)
        self.gotAllResult.emit()

            
##检测当前
class DetectThis(QObject):
    gotThisResult = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self, item):
        print("From workThread: ", QThread.currentThreadId())
        detector = Detector()
        detected = item.data(1, Qt.UserRole)[0]
        if detected:
            return
        dcmFileName = item.data(0, Qt.UserRole)
        result = detector.detect(dcmFileName)
        result.insert(0, True)

        classes = result[3]
        brush = QBrush(Qt.SolidPattern)
        if 5.0 in classes:
            item.setText(1, "骨质异常")
            brush.setColor(Qt.GlobalColor.cyan)
        elif 3.0 in classes or 4.0 in classes:
            item.setText(1, "骨折")
            brush.setColor(Qt.GlobalColor.red)
        elif 6.0 in classes:
            item.setText(1, "发育异变")
            brush.setColor(Qt.GlobalColor.yellow)
        else:
            item.setText(1, "正常")
            brush.setColor(Qt.GlobalColor.white)
        item.setBackground(1, brush)
        item.setTextAlignment(1, Qt.AlignCenter)
        item.setData(1, Qt.UserRole, result)

        self.gotThisResult.emit()

            
##重写排序的比较方式
class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        QTreeWidgetItem.__init__(self, parent)

    def __lt__(self, otherItem):
        column = self.treeWidget().sortColumn()

        selfText = self.text(column)
        #print(selfText)
        selfText0 = os.path.splitext(selfText)[-2]
        selfTextNum = os.path.splitext(selfText0)[-1]
        selfNum = int(selfTextNum[1:])

        otherText = otherItem.text(column)
        otherText0 = os.path.splitext(otherText)[-2]
        otherTextNum = os.path.splitext(otherText0)[-1]
        otherNum = int(otherTextNum[1:])

        #if selfNum == otherNum

        try:
            return selfNum < otherNum
        except ValueError:
            return self.text(column) < otherItem.text(column)
