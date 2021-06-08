## Prepare Env ##
```
$ CAFFE_ROOT=$HOME/desktop/caffe
$ ...

* See ssd/SSD.md for more.
```

## Quick Test ##
```
## download pretrained MobileNetSSD caffe model
https://drive.google.com/open?id=0B3gersZ2cHIxVFI1Rjd5aDgwOG8 // mobilenet_iter_73000.caffemodel
https://drive.google.com/open?id=0B3gersZ2cHIxRm5PMWRoTkdHdHc // MobileNetSSD_deploy.caffemodel

## smoke detect (with pretrained caffe model)
$ python detect.py --pycaffe $HOME/desktop/caffe/python --model deploy.prototxt --weights mobilenet_ssd.caffemodel --images images

## smoke merge (bn -> conv)
$ python tools/merge_bn.py --pycaffe $CAFFE_ROOT/python --model deploy.prototxt --weights mobilenet_ssd.caffemodel --model_out out.prototxt --weights_out out.caffemodel
```

## Quick Data ##
```
## create label list and dataset
$ vi tools/create_list.sh
$ vi tools/create_data.sh
$ tools/create_list.sh // generate train/val/test.txt
$ export PYTHONPATH=$CAFFE_ROOT/python:$PYTHONPATH && bash tools/create_data.sh

## outputs:
.
├── examples
│   └── Main
│       ├── Main_test_lmdb -> xxx/tools/../output/Main/lmdb/Main_test_lmdb
│       └── Main_trainval_lmdb -> xxx/tools/../output/Main/lmdb/Main_trainval_lmdb
├── output
│   ├── Images
│   ├── labelmap.prototxt
│   ├── Labels
│   ├── Main
│   │   └── lmdb
│   │       ├── Main_test_lmdb
│   │       └── Main_trainval_lmdb
│   ├── test_name_size.txt
│   ├── test.txt
│   └── trainval.txt
```

## Quick Train ##
```
$ mv examples/Main/Main_trainval_lmdb trainval_lmdb
$ mv examples/Main/Main_test_lmdb test_lmdb

## train own mobilenet-ssd
$ CLASSNUM=21
$ tools/gen_model.sh $CLASSNUM
$ train.sh
```

## Model Info (Caffe) ##
```
=====================================================
(*) mobilenet_ssd // support: multi resolution, but ...
=====================================================
input: 4( 1 3 300 300)  // nchw
...
->  mbox_loc:           4( 1 7668 1 1)  7668 = 1917 * 4, 4 = sizeof(float)
->  mbox_conf_flatten:  4( 1 40257 1 1) 40257 = 1917 * 21, 21 = voc_class_num
->  mbox_priorbox:      4( 1 2 7668 1)  7668 = 1917 * 4, 4 = ?; 2 = ?
output: 4( 1 100 6 1)   // post processed results, 100: max detected objects, 6: label, score, lt(x,y), rb(x,y)
-----------------------------------------------------
input: 4( 1 3 640 360)  // nchw
...
->  mbox_loc:           4( 1 18792 1 1) 18792 = 4698 * 4, 4 = sizeof(float)
->  mbox_conf_flatten:  4( 1 98658 1 1) 98658 = 4698 * 21, 21 = voc_class_num
->  mbox_priorbox:      4( 1 2 18792 1) 18792 = 4698 * 4, 4 = ?; 2 = ?
output: 4( 1 100 6 1)   // post processed results, 100: max detected objects, 6: label, score, lt(x,y), rb(x,y)
-----------------------------------------------------
resolution:         300x300     640x360
-----------------------------------------------------
strides:    /2      150x150     320x180
            /4       75x75      160x90
            /8       38x38       80x45
-----------------------------------------------------
conv11      /16     (19x19)x3   (40x23)x3
conv13      /32     (10x10)x6   (20x12)x6
conv14_2    /64       (5x5)x6    (10x6)x6
conv15_2    /128      (3x3)x6     (5x3)x6
conv16_2    /256      (2x2)x6     (3x2)x6
conv17_2    /512      (1x1)x6     (2x1)x6
-----------------------------------------------------
mbox                = 1917      = 4698
```

## Caffe FAQ ##
```
1. fatal error: hdf5.h missing
$ pkg-config hdf5 --libs --cflags
-I/usr/include/hdf5/serial -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5
line92: INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/
line93: LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial
```

## Reference ##
[Caffe Lesson5: blas && boost::thread](https://blog.csdn.net/baobei0112/article/details/47616451)  
[Train MobileNet-SSD](https://www.yuque.com/yahei/hey-yahei/train_mssd)