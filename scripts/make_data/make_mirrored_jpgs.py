#coding=utf-8
import os
import shutil
from PIL import Image

inpath = "D:/CTrfd/TensorFlow/data/jpgs/"
outpath = "D:/CTrfd/TensorFlow/data/mrdjpgs/"
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
    jpg_list = os.listdir(inpath + patient)
    for jpg in jpg_list:
        im = Image.open(inpath + patient + '/' + jpg)
        mirroredim = im.transpose(Image.FLIP_LEFT_RIGHT)
        mirroredim.save(outpath + patient + '/mrd' + jpg)
