work_dir=''
cd $work_dir
API_KEY=''
GEN_NUM=3
MAX_RETRY_NUM=5
MP_NUM=4
INSTRUCTION_FILE=''
OUTPUT_FILE=''
CODE_DIR=''
IMAGE_DIR=''
DATASET='geo3k' #geoqa geo3k unigeo_proving

python ./pipline/gen_image_mp.py \
    --instruction_file $INSTRUCTION_FILE \
    --output_file $OUTPUT_FILE \
    --api_key $API_KEY \
    --gen_num $GEN_NUM \
    --dataset $DATASET \
    --max_retry_num $MAX_RETRY_NUM \
    --mp_num $MP_NUM \
    --code_dir $CODE_DIR \
    --image_dir $IMAGE_DIR \