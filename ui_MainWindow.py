# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\QtApp\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(955, 539)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setAutoFillBackground(False)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitterH = QtWidgets.QSplitter(self.centralWidget)
        self.splitterH.setOrientation(QtCore.Qt.Horizontal)
        self.splitterH.setChildrenCollapsible(True)
        self.splitterH.setObjectName("splitterH")
        self.treeFiles = QtWidgets.QTreeWidget(self.splitterH)
        self.treeFiles.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeFiles.sizePolicy().hasHeightForWidth())
        self.treeFiles.setSizePolicy(sizePolicy)
        self.treeFiles.setColumnCount(2)
        self.treeFiles.setObjectName("treeFiles")
        self.treeFiles.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.treeFiles.headerItem().setFont(0, font)
        self.treeFiles.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.treeFiles.headerItem().setFont(1, font)
        self.treeFiles.header().setDefaultSectionSize(150)
        self.scrollArea = QtWidgets.QScrollArea(self.splitterH)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(200, 0))
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 751, 420))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labPicture = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labPicture.setAlignment(QtCore.Qt.AlignCenter)
        self.labPicture.setObjectName("labPicture")
        self.verticalLayout.addWidget(self.labPicture)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.splitterH)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setIconSize(QtCore.QSize(50, 50))
        self.mainToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actOpen.setIcon(icon)
        self.actOpen.setObjectName("actOpen")
        self.actZoomIn = QtWidgets.QAction(MainWindow)
        self.actZoomIn.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icons/zoomin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actZoomIn.setIcon(icon1)
        self.actZoomIn.setObjectName("actZoomIn")
        self.actZoomOut = QtWidgets.QAction(MainWindow)
        self.actZoomOut.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icons/zoomout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actZoomOut.setIcon(icon2)
        self.actZoomOut.setObjectName("actZoomOut")
        self.actZoomRealSize = QtWidgets.QAction(MainWindow)
        self.actZoomRealSize.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/icons/realsize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actZoomRealSize.setIcon(icon3)
        self.actZoomRealSize.setObjectName("actZoomRealSize")
        self.actZoomFitW = QtWidgets.QAction(MainWindow)
        self.actZoomFitW.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/icons/fitwidth.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actZoomFitW.setIcon(icon4)
        self.actZoomFitW.setObjectName("actZoomFitW")
        self.actZoomFitH = QtWidgets.QAction(MainWindow)
        self.actZoomFitH.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/icons/fitheight.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actZoomFitH.setIcon(icon5)
        self.actZoomFitH.setObjectName("actZoomFitH")
        self.actDetect = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/icons/detect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actDetect.setIcon(icon6)
        self.actDetect.setObjectName("actDetect")
        self.actBox = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/icons/hidebox.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actBox.setIcon(icon7)
        self.actBox.setObjectName("actBox")
        self.actDetectThis = QtWidgets.QAction(MainWindow)
        self.actDetectThis.setIcon(icon6)
        self.actDetectThis.setObjectName("actDetectThis")
        self.mainToolBar.addAction(self.actOpen)
        self.mainToolBar.addAction(self.actDetect)
        self.mainToolBar.addAction(self.actDetectThis)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actZoomIn)
        self.mainToolBar.addAction(self.actZoomOut)
        self.mainToolBar.addAction(self.actZoomRealSize)
        self.mainToolBar.addAction(self.actZoomFitW)
        self.mainToolBar.addAction(self.actZoomFitH)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actBox)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Demo3_9  QTreeWidget，QDockWidget"))
        self.treeFiles.headerItem().setText(0, _translate("MainWindow", "CT"))
        self.treeFiles.headerItem().setText(1, _translate("MainWindow", "检测结果"))
        self.actOpen.setText(_translate("MainWindow", "打开"))
        self.actOpen.setToolTip(_translate("MainWindow", "打开患者文件夹"))
        self.actOpen.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actZoomIn.setText(_translate("MainWindow", "放大"))
        self.actZoomIn.setToolTip(_translate("MainWindow", "放大图像"))
        self.actZoomIn.setShortcut(_translate("MainWindow", "Ctrl++"))
        self.actZoomOut.setText(_translate("MainWindow", "缩小"))
        self.actZoomOut.setToolTip(_translate("MainWindow", "缩小图像"))
        self.actZoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.actZoomRealSize.setText(_translate("MainWindow", "原始大小"))
        self.actZoomRealSize.setToolTip(_translate("MainWindow", "显示原始大小"))
        self.actZoomFitW.setText(_translate("MainWindow", "适合宽度"))
        self.actZoomFitW.setToolTip(_translate("MainWindow", "适合宽度显示"))
        self.actZoomFitW.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actZoomFitH.setText(_translate("MainWindow", "适合高度"))
        self.actZoomFitH.setToolTip(_translate("MainWindow", "适合高度显示"))
        self.actZoomFitH.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actDetect.setText(_translate("MainWindow", "检测所有"))
        self.actDetect.setToolTip(_translate("MainWindow", "检测所有CT"))
        self.actBox.setText(_translate("MainWindow", "隐藏Box"))
        self.actBox.setToolTip(_translate("MainWindow", "隐藏检测框"))
        self.actDetectThis.setText(_translate("MainWindow", "检测此CT"))
        self.actDetectThis.setToolTip(_translate("MainWindow", "检测此张CT"))
import res_rc
