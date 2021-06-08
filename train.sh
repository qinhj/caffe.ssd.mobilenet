#!/bin/bash
set -e # -xe
source env.rc

SOLVER="solver_train.prototxt"
WEIGHT="" # "mobilenet_iter_73000.caffemodel"

mkdir -p snapshot
$CAFFE_ROOT/build/tools/caffe train -solver=$SOLVER -weights=$WEIGHT -gpu 0
