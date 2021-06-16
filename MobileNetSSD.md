## Prepare Env ##
See [ssd/SSD.md](https://github.com/qinhj/caffe.ssd/blob/master/SSD.md) for more.

## Quick Test ##
```
$ source env.rc

## download pretrained MobileNetSSD caffe model
https://drive.google.com/open?id=0B3gersZ2cHIxVFI1Rjd5aDgwOG8 // mobilenet_iter_73000.caffemodel
https://drive.google.com/open?id=0B3gersZ2cHIxRm5PMWRoTkdHdHc // MobileNetSSD_deploy.caffemodel

## smoke detect (with pretrained caffe model)
$ python detect.py --pycaffe $CAFFE_ROOT/python --model deploy.prototxt --weights mobilenet_ssd.caffemodel --images images

## smoke merge (bn -> conv)
$ python tools/merge_bn.py --pycaffe $CAFFE_ROOT/python --model deploy.prototxt --weights mobilenet_ssd.caffemodel --model_out out.prototxt --weights_out out.caffemodel
```

## Quick Data ##
```
$ source env.rc

## create your dataset or extract some classes from voc dataset by voc_extract.py
## see https://github.com/qinhj/caffe.ssd/blob/master/scripts/voc_extract.py
$ python voc_extract.py --dataset $HOME/data --classes cat,dog,person

## create label list and lmdb(one can also use ssd official shell scripts)
$ vi tools/create_list.sh
$ vi tools/create_data.sh
$ bash tools/create_list.sh // generate train/val/test.txt
$ bash tools/create_data.sh

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
$ bash train.sh
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

## Reference ##
[Caffe Lesson5: blas && boost::thread](https://blog.csdn.net/baobei0112/article/details/47616451)  
[Train MobileNet-SSD](https://www.yuque.com/yahei/hey-yahei/train_mssd)