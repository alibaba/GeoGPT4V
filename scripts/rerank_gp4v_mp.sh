work_dir=''
cd $work_dir
API_KEY=''
GEN_NUM=1
MAX_RETRY_NUM=5
MP_NUM=2
INSTRUCTION_FILE=''
OUTPUT_FILE=''
MODEL='gpt4v'

python ./pipline/rerank_mp.py \
    --instruction_file $INSTRUCTION_FILE \
    --output_file $OUTPUT_FILE \
    --api_key $API_KEY \
    --gen_num $GEN_NUM \
    --mp_num $MP_NUM \
    --max_retry_num $MAX_RETRY_NUM \
    --model $MODEL \
