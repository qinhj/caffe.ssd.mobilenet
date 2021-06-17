# !/bin/bash
set -e # -xe

# =============================================================================
# This file is used to create the lmdb files.
# =============================================================================

caffe_dir=$HOME/desktop/caffe
bash_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir=$bash_dir/..

# update the following vars if necessary
data_dir=$root_dir/data
if [ ! -d $data_dir ]; then
    echo "$data_dir not exist!"
    exit
fi
out_dir_lmdb=$root_dir/output
out_dir_link=$root_dir

## user settings
redo=1
mapfile=$data_dir/labelmap.prototxt
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
  ## remove exist softlink
  rm -rf $out_dir_link/$subset"_"$db

  python $caffe_dir/scripts/create_annoset.py \
    --anno-type=$anno_type \
    --label-type=$label_type \
    --label-map-file=$mapfile \
    --min-dim=$min_dim --max-dim=$max_dim \
    --resize-width=$width --resize-height=$height \
    --check-label $extra_cmd \
    $data_dir \
    $out_dir_lmdb/$subset.txt \
    $out_dir_lmdb/$subset"_"$db \
    $out_dir_link
done
