#coding=utf-8
import os
import shutil
from xml.etree.ElementTree import parse, Element

inpath = "D:/CTrfd/TensorFlow/data/xmls/"
outpath = "D:/CTrfd/TensorFlow/data/mrdxmls/"
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
    xml_list = os.listdir(inpath + patient)
    for xml in xml_list:
        doc = parse(inpath + patient + '/' + xml)
        root = doc.getroot()

        fname = root.find("filename")
        fname.text = "mrd" + os.path.splitext(fname.text)[0] + ".jpg"
        # print(fname.text)

        obj_list = root.iter('object')
        for obj in obj_list:
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin')
            xmax = bndbox.find('xmax')
            xmint = xmin.text
            xmaxt = xmax.text
            xmax.text = str(512 - int(xmint))
            xmin.text = str(512 - int(xmaxt))

        doc.write(outpath + patient + '/mrd' + xml)
