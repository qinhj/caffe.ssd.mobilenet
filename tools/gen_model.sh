#!/bin/bash
set -e # -xe

# =============================================================================
# This file is used to generate the prototxt files.
# =============================================================================

bash_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir=${bash_dir}/..
# update the following vars if necessary
prototxt_dir=${root_dir}/prototxt
output_dir=${root_dir}/output

if [ ! -d ${prototxt_dir} ]; then
    echo "${prototxt_dir} not exist!"
    exit
fi
[ ! -d ${output_dir} ] && mkdir -p ${output_dir}

generate_prototxt() {
    fin=$1
    fout=${fin%_*}.prototxt
    cp ${prototxt_dir}/${fin} ${output_dir}/${fout}
    sed -i "s/cls6x/${cls_num6}/g" ${output_dir}/${fout}
    sed -i "s/cls3x/${cls_num3}/g" ${output_dir}/${fout}
    sed -i "s/cls1x/${cls_num}/g" ${output_dir}/${fout}
}

show_usage() {
	echo "Usage: $0 <CLASSNUM>"
    echo "Options:"
    echo "  <CLASSNUM>  label numbers, e.g. 21 for voc and 80 for coco"
    echo "Example:"
    echo "  $0 21"
}

# check classnum
if test -z $1; then
    show_usage
	exit 1
fi
echo $1 | grep '^[0-9]*$' >/dev/null 2>&1
if [ $? != 0 ];then
    show_usage
	exit 1
fi

cls_num=$1
cls_num3=$(expr $1 \* 3)
cls_num6=$(expr $1 \* 6)

generate_prototxt MobileNetSSD_train_template.prototxt
generate_prototxt MobileNetSSD_test_template.prototxt
#generate_prototxt MobileNetSSD_deploy_bn_template.prototxt
generate_prototxt MobileNetSSD_deploy_template.prototxt
