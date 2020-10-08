#coding=utf-8
import os
from PIL import Image
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import cv2

def main():
    inpath = "E:/学习/8毕业设计/CT图像处理/CTdata/"
    outpath = "D:/CTrfd/TensorFlow/data/alljpgs/"

    patient_list = os.listdir(inpath)

    # 新建患者文件夹
    for patient in patient_list:
        new_folder = outpath + patient
        exist = os.path.exists(new_folder)
        if not exist: # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(new_folder) # makedirs 创建文件时如果路径不存在会创建这个路径
            print("create " + new_folder)
        else:
            print(new_folder + " is exist")

    for patient in patient_list:
        print(patient)
        dcm_list = os.listdir(inpath + patient);
        for dcm in dcm_list:
            #print(patient + '/' + dcm)
            if os.path.isdir(inpath + patient + '/' + dcm): # 跳过文件夹
                continue
            if os.path.splitext(dcm)[-1] != ".dcm": # 跳过非dcm文件
                continue
            dcm_file = pydicom.read_file(inpath + patient + '/' +dcm)
            if dcm_file.SeriesDescription == "Dose Record":
                continue
            origin = dcm_file.pixel_array # type:numpy.ndarray
            origin[origin < 1000] = 1000 # 去除低亮部分
            origin[origin > 3000] = 3000 # 去除高亮部分
            rgb = np.expand_dims(origin,-1) # 将origin增加一个维度
            rgb = np.repeat(rgb,3,2) # 将二维矩阵重复三次
            # 归一化到0-255
            rgb = cv2.normalize(rgb, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC3) 
            plt.imsave(outpath + patient + '/' + dcm + ".jpg",rgb)

if __name__ == "__main__":
    main()

