![interface](https://github.com/RonYoung666/CTRibFractureRecognition/blob/master/interface.png)
# 基于 ResNet50 的 CT 图像肋骨骨折识别工具

一个用来识别 CT 图像(DICOM)中肋骨骨折的 Windows 桌面工具，识别部分使用了 ResNet50 网络，调用了 TensorFlow 的 [Object Detection API](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/)，桌面程序部分使用 [PyQt5](https://doc.qt.io/qtforpython/) 编写而成。

本工具的特点是能够批量导入一位患者的所有 CT 图像并按照切片类型进行分类排序，并且能够进行批量检测与查看。

本工具对于大家有如下 3 个用途：

1. 直接拿来检测 CT 图像中的肋骨骨折
2. 替换 CNN 部分为你自己的神经网络用来检测 CT 图像中的其他病灶
3. 替换输入部分和 CNN 部分用来检测普通图像中的目标物体


## 安装

1. 下载源代码
2. 本工具使用了下面的依赖，使用前请先检查依赖是否已全部安装好

|Package              |Version
|-------------------- |-----------
|dicom                |0.9.9.post1
|lxml                 |4.3.4
|matplotlib           |3.1.3
|numpy                |1.16.4+mkl
|object-detection     |0.1
|opencv-python        |4.2.0.32
|pandas               |0.25.0
|Pillow               |5.4.1
|pydicom              |1.4.2
|PyQt5                |5.13.0
|tensorboard          |1.13.0
|tensorflow-estimator |1.13.0
|tensorflow-gpu       |1.13.2

## 使用方法

### 直接拿来检测 CT 图像中的肋骨骨折

1. 进入 Windows 控制台
2. 进入项目文件夹，并运行 python appMain.py
3. 点击 “打开”, 选择患者的 DICOM 文件夹
4. 点击 “检测此CT” 可以检测单张 CT
5. 点击 “检测所有” 可以批量顺序检测所有 CT

### 替换 CNN 部分为你自己的神经网络用来检测 CT 图像中的其他病灶

参考 TensorFlow [Object Detection API](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/) 教程构建自己的神经网络，将 trained_module3270/frozen_inference_graph.pb 文件替换为自己训练好的模型。

参考教程训练模型的过程中需要一些脚本，我也已经上传到了库中，详情见 scripts 文件夹。

由于 DICOM 文件的特殊性，转换为普通图片还需要进行一些转换操作，scripts/make_data 文件夹中的脚本是我自己写的，具体用途如下：

|脚本名                |用途
|--------------------- |-----------
|dcm2jpg.py            |将 DICOM 文件转换为 JPEG 文件
|make_mirrored_jpgs.py |镜像翻转图片来增加数据量
|make_mirrored_xmls.py |镜像翻转标定框
|split.py              |划分训练集和测试集


### 替换输入部分和 CNN 部分用来检测普通图像中的目标物体

替换 CNN 部分方法同上，替换输入部分需要自己仔细修改一些源码，本工具中进行了许多针对 CT 图像的操作，修改为针对普通图像的操作即可。

对 PyQt5 不熟悉的朋友可以参考书籍[《Python Qt GUI 与数据可视化编程》](https://www.epubit.com/bookDetails?id=UB6c7836a7146b7)，本工具的桌面软件部分基本是参考此书写的，在此对作者表示感谢！
