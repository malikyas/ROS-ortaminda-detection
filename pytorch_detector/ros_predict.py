#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import torch
from torchvision import transforms
from torch.autograd import Variable
import cv2
import matplotlib.pyplot as plt
import rospy
from cv_bridge import CvBridge, CvBridgeError
import sys
from sensor_msgs.msg import Image
import numpy as np


class detector():
    def __init__(self):
        self.node_name = 'detector'
        rospy.init_node(self.node_name)

        self.loader = transforms.Compose([transforms.ToTensor()])

        self.bridge = CvBridge()
        
        rospy.Subscriber("/mybot/camera1/image_raw", Image, self.ros_to_cv, queue_size = 1)
        
        rospy.loginfo("Image alındı.")


    def img_loader(self, cv_image):
        #img = cv_image.convert('RGB')
        img = cv_image
        img = self.loader(img).float()
        img = Variable(img, requires_grad=True)
        return img.cuda()
    
    def predictor(self, cv_image):
        model = torch.load('/home/m3/catkin_ws/src/detectors/pytorch_detector/network')
        model.eval()
        img_arr = self.img_loader(cv_image)
        with torch.no_grad():
            pred = model([img_arr])
        return pred
    
    def drawBbox(self, cv_image):
        boxes_np = np.array(self.predictor(cv_image)[0]['boxes'].cpu())
        threshold = 0.8
        iter_num = len(boxes_np)
        for i in range(iter_num):
            tl =  (boxes_np[i][0], boxes_np[i][1])
            br = (boxes_np[i][2], boxes_np[i][3])
            if self.predictor(cv_image)[0]['scores'][i] > threshold:
                cv_image = cv2.rectangle(cv_image, tl, br, (0,0,255), 2)       
        return cv_image

    def drawMask(self, cv_image):
        h = cv_image.shape[0]
        w = cv_image.shape[1]
        mask_acc = np.zeros([h,w])
        for i in range(len(self.predictor(cv_image)[0]['masks'])):
            mask_acc += np.array(self.predictor(cv_image)[0]['masks'][i].cpu()).reshape(h,w)
        return mask_acc

    def ros_to_cv(self, ros_image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(ros_image, 'bgr8')
        
        except CvBridgeError as error:
            print(error)
                       
        #output = self.drawBbox(cv_image)
        output = self.drawMask(cv_image)
    
        cv2.imshow('output', output)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
           rospy.signal_shutdown('Kapanıyor')
    

def main(args):
    try:
        detector()
        rospy.spin()
    except KeyboardInterrupt:
        print('Kapanıyor')
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

            
