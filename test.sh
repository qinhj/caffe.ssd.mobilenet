#!/bin/bash
set -e # -xe
source env.rc

SOLVER="solver_test.prototxt"
WEIGHT=$(ls -t snapshot/*.caffemodel | head -n 1) # "mobilenet_iter_73000.caffemodel"

if test -z $WEIGHT; then
	exit 1
fi
$CAFFE_ROOT/build/tools/caffe train -solver=$SOLVER -weights=$WEIGHT -gpu 0
