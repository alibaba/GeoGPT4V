work_dir=''
cd $work_dir
API_KEY=''
GEN_NUM=1
MAX_RETRY_NUM=5
MP_NUM=3
QUESTION_FILE=''
OUTPUT_FILE=''
DATASET='geo3k' #geoqa geo3k unigeo_proving
MODEL='gpt4v'

python ./pipline/gen_instruction_mp.py \
    --question $QUESTION_FILE \
    --output_file $OUTPUT_FILE \
    --api_key $API_KEY \
    --gen_num $GEN_NUM \
    --max_retry_num $MAX_RETRY_NUM \
    --dataset $DATASET \
    --mp_num $MP_NUM \
    --model $MODEL \
