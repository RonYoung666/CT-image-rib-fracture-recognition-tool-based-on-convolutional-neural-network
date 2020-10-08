# -*- coding: utf-8 -*-
import numpy as np
import os
import tensorflow as tf
import cv2
import pydicom
import label_map_util

MODEL_NAME = 'trained_module3270'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = 'label_map.pbtxt'
NUM_CLASSES = 6

class Detector():
    def __init__(self, parent=None):
        # Load a (frozen) Tensorflow model into memory.
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        # Loading label map
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(
            label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)
        
        self.count = 0

        self.detection_graph.as_default()
        self.sess = tf.compat.v1.Session(graph=self.detection_graph)



    def dcm2numpyArray(self, dcmFileName):
        dcmFile = pydicom.read_file(dcmFileName)
        origin = dcmFile.pixel_array # type:numpy.ndarray
        origin[origin < 1000] = 1000 # 去除低亮部分
        origin[origin > 3000] = 3000 # 去除高亮部分
        # 归一化到0-255
        origin = cv2.normalize(origin, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC3) 
        rgb = np.expand_dims(origin,-1) # 将origin增加一个维度
        rgb = np.repeat(rgb,3,2) # 将二维矩阵重复三次
        #print(type(rgb))
        return rgb

    def detect(self, dcmFileName):
        print("detecting ",dcmFileName)

        image_np = self.dcm2numpyArray(dcmFileName)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Extract image tensor
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Extract detection boxes
        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Extract detection scores
        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        # Extract detection classes
        classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        # Extract number of detectionsd
        num_detections = self.detection_graph.get_tensor_by_name(
            'num_detections:0')
        # Actual detection.
        (boxes, scores, classes, num_detections) = self.sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        boxes = np.squeeze(boxes)
        classes = np.squeeze(classes).astype(np.int32)
        scores = np.squeeze(scores)

        ##去除置信率低于95%的
        for i in range(boxes.shape[0]):
            if scores[i] < 0.95:
                break
        boxes = boxes[0:i]
        classes = classes[0:i]
        scores = scores[0:i]

        ##去除negative的
        i = 0
        while i < boxes.shape[0]:
            if classes[i] == 1 or classes[i] == 2:
                boxes = np.delete(boxes, i, axis=0)
                classes = np.delete(classes, i, axis=0)
                scores = np.delete(scores, i, axis=0)
                continue
            i = i + 1

        result = [boxes, scores, classes]

        '''
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            boxes,
            classes,
            scores,
            self.category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=None,
            line_thickness=1)

        # Display output
        plt.imsave("output/" + str(self.count) + ".jpg", image_np)
        self.count = self.count + 1
        '''

        print("\nresult:")
        print("num:", boxes.shape[0])
        print("boxes\n: ", boxes)
        print("scores\n: ", scores)
        print("classes\n: ", classes)
        print("\n\n")

        return result


if __name__ == "__main__":
    detector = Detector()
    path = "E:/学习/8毕业设计/CT图像处理/CTdata/2Test/"
    dcmList = os.listdir(path)    ##文件列表
    for dcm in dcmList:
        dcmFileName = path + dcm
        if os.path.isdir(dcmFileName):
            continue
        if os.path.splitext(dcm)[-1] != ".dcm": # 跳过非dcm文件
            continue
        result = detector.detect(dcmFileName)
        boxes = result[0]
        scores = result[1]
        classes = result[2]
        print("\n\nin detector")
        print("boxes.shape: ", boxes.shape)
        print("boxes.shape[0]: ", boxes.shape[0])
        print("boxes: ", boxes)
        print("scores.shape: ", scores.shape)
        print("scores[0]: ", scores[0])
        print("scores: ", scores)
        print("classes.shape: ", classes.shape)
        print("classes: ", classes)
        '''
        if 6.0 in result[2][0]:
            print("6.0 in")
        if 5.0 in result[2][0]:
            print("5.0 in")
        if 4.0 in result[2][0]:
            print("4.0 in")
        if 3.0 in result[2][0]:
            print("3.0 in")
        if 2.0 in result[2][0]:
            print("2.0 in")
        if 1.0 in result[2][0]:
            print("1.0 in")
        '''
