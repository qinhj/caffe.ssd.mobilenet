"""
MobileNet-SSD detection demo

@Author:    qinhongjie@imilab.com
@Data:      2021/05/25

Usage:
$ python detect.py --pycaffe $HOME/desktop/caffe/python --model deploy.prototxt --weights mobilenet_ssd.caffemodel --images images
"""

import argparse
import sys, os
import numpy as np
import cv2

## default settings
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_PYCAFFE = os.path.join(DIR_ROOT, "../../python")

## default voc 21 class labels
CLASSES = (
    'background',
    'aeroplane', 'bicycle', 'bird', 'boat', 'bottle',       # 01-05
    'bus', 'car', 'cat', 'chair', 'cow',                    # 06-10
    'diningtable', 'dog', 'horse', 'motorbike', 'person',   # 11-15
    'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'    # 16-20
)


def preprocess(src, shape=None):
    img = cv2.resize(src, (300,300))
    img = img - 127.5
    img = img * 0.007843
    return img


def postprocess(img, out):   
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0,0,:,3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0,0,:,1]
    conf = out['detection_out'][0,0,:,2]
    return (box.astype(np.int32), conf, cls)


def detect(imgfile):
    origimg = cv2.imread(imgfile)
    img = preprocess(origimg)
    
    img = img.astype(np.float32)
    img = img.transpose((2, 0, 1))

    net.blobs['data'].data[...] = img
    out = net.forward()  
    box, conf, cls = postprocess(origimg, out)

    print("img: %s" % (imgfile))
    for i in range(len(box)):
       p1 = (box[i][0], box[i][1])
       p2 = (box[i][2], box[i][3])
       cv2.rectangle(origimg, p1, p2, (0,255,0))
       p3 = (max(p1[0], 15), max(p1[1], 15))
       title = "%s:%.2f" % (CLASSES[int(cls[i])], conf[i])
       cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (0, 255, 0), 1)
       print("obj[%02d] %s: %.2f" % (i, CLASSES[int(cls[i])], conf[i]))
    cv2.imshow("SSD", origimg)
    print("----------------------------")

    k = cv2.waitKey(0) & 0xff
    ## Exit if ESC pressed
    return False if 27 == k else True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pycaffe', type=str, default=DIR_PYCAFFE, help='pycaffe path')
    parser.add_argument('--model', type=str, default='deploy.prototxt', help='network description file')
    parser.add_argument('--weights', type=str, default='mobilenet_iter_73000.caffemodel', help='model weights path')
    parser.add_argument('--images', type=str, default='images', help='test images folder path')
    args = parser.parse_args()

    ## check input args
    if not os.path.exists(args.model):
        sys.exit("proto file not found: %s" % args.model)
    if not os.path.exists(args.weights):
        sys.exit("caffe model not found: %s" % args.weights)

    sys.path.append(args.pycaffe)
    import caffe

    ## load caffe model
    net = caffe.Net(args.model, args.weights, caffe.TEST)

    for img in os.listdir(args.images):
        if img.endswith(".jpg"):
            if not detect(os.path.join(args.images, img)):
                sys.exit("receive ESC and quit")
