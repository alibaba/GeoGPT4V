work_dir=''
cd $work_dir
INPUT_FILE=''
OUTPUT_FILE=''
MODEL='' #llava sharegpt4v internvl_chat

python ./utils/convert_format.py \
    --input_file $INPUT_FILE \
    --output_file $OUTPUT_FILE \
    --model $MODEL \