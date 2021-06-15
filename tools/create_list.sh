# !/bin/bash
set -e # -xe

# =============================================================================
# @Brief:   This file is used to create the list of train and test files for
#           training/testing procedures. They map each image to its label file.
# @Outputs: trainval.txt, test.txt and test_name_size.txt .
# @Note:    1) The outputs can be shared by all classes;
# =============================================================================

bash_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir=${bash_dir}/..
# update the 'data_root_dir' if necessary
data_root_dir=${root_dir}/data
if [ ! -d ${data_root_dir} ]; then
    echo "${data_root_dir} not exist!"
    exit
fi

output_dir=${root_dir}/output
rm -rf ${output_dir}
[ ! -d ${output_dir} ] && mkdir -p ${output_dir}
echo "output_dir: "${output_dir}

# outputs
dst_all_tmp=${output_dir}"/all_tmp.txt"
dst_file_trainval=${output_dir}"/trainval.txt"
dst_file_test=${output_dir}"/test.txt"
dst_file_test_name_size=${output_dir}"/test_name_size.txt"

# check images and labels
if [ $(ls ${data_root_dir}/Images | wc -l) != $(ls ${data_root_dir}/Labels | wc -l) ]; then
    echo "Images and Labels not equal count. Images and Labels must be same count!"
    exit
fi

cd ${data_root_dir} && find . -name "*.jpg" | sort > ${dst_file_trainval}
cd ${data_root_dir} && find . -name "*.xml" | sort > ${dst_file_test}
# combine images and labels
paste -d' ' ${dst_file_trainval} ${dst_file_test} > ${dst_file_test_name_size}

# random shuffle the lines in all images
awk 'BEGIN{srand()}{b[rand()NR]=$0}END{for(x in b)print b[x]}' ${dst_file_test_name_size} > ${dst_all_tmp}

# split all by two part: trainval and test(default is 0.8=4/5)
cnt=$(cat ${dst_all_tmp} | wc -l)
cnt_trainval=$((cnt*4/5))
awk 'FNR<="'$cnt_trainval'"' ${dst_all_tmp} > ${dst_file_trainval}
awk 'FNR>"'$cnt_trainval'"' ${dst_all_tmp} > ${dst_file_test}

# generate test_name_size.txt
rm -rf ${dst_file_test_name_size}
while read line; do
    line=${line%% *}
	size=`identify ${data_root_dir}/${line} | cut -d ' ' -f 3 | sed -e "s/x/ /" | sed -r 's/([^ ]+) (.*)/\2 \1/'`
	name=$(basename ${line})
    name=${name%%.*}
	echo ${name}" "${size} >> ${dst_file_test_name_size}
done < ${dst_file_test}

#ln -sf ${data_root_dir}/Images ${output_dir}/
#ln -sf ${data_root_dir}/Labels ${output_dir}/
#ln -sf ${data_root_dir}/labelmap.prototxt ${output_dir}/
cp -rf ${data_root_dir}/* ${output_dir}/

rm -f ${dst_all_tmp}
echo "Done!"
