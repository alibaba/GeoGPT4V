work_dir=''
cd $work_dir
INPUT_FILE=''
OUTPUT_FILE=''
THRESHOLD=0.9

python ./pipline/filter.py \
    --input_file $INPUT_FILE \
    --output_file $OUTPUT_FILE \
    --threshold $THRESHOLD \