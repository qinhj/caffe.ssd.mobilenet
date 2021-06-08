# !/bin/bash
set -e # -xe

# =============================================================================
# This file is used to create the lmdb files.
# =============================================================================

bash_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir=${bash_dir}/..
# update the following vars if necessary
data_root_dir=${root_dir}/output
caffe_root_dir=$HOME/desktop/caffe
if [ ! -d ${data_root_dir} ]; then
    echo "${data_root_dir} not exist!"
    exit
fi

#cd $root_dir

## user settings
redo=1
dataset_name="Main" # This will be directory holding train and test LMDBs
mapfile=$data_root_dir/labelmap.prototxt
anno_type="detection"
db="lmdb"
min_dim=0
max_dim=0
width=0
height=0

label_type="xml"

extra_cmd="--encode-type=jpg --encoded"

if [ $redo ]; then
  extra_cmd="$extra_cmd --redo"
fi

for subset in test trainval; do
  python $caffe_root_dir/scripts/create_annoset.py \
    --anno-type=$anno_type \
    --label-type=$label_type \
    --label-map-file=$mapfile \
    --min-dim=$min_dim \
    --max-dim=$max_dim \
    --resize-width=$width \
    --resize-height=$height \
    --check-label \
    $extra_cmd \
    $data_root_dir \
    $data_root_dir/$subset.txt \
    $data_root_dir/$dataset_name/$db/$dataset_name"_"$subset"_"$db \
    examples/$dataset_name
done
