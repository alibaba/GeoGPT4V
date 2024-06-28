# GeoGPT4V: Towards Geometric Multi-modal Large Language Models with Geometric Image Generation

This repository contains the code and data for the paper titled "GeoGPT4V: Towards Geometric Multi-modal Large Language Models with Geometric Image Generation".

## Contents

* [Install](#Install)
* [Usage](#Usage)
* [Train](#Train)
* [Dataset](#Dataset)
* [Model](#Model)



## Install

1. Clone this repository.

2. Install Package.

   ```shell
   conda create -n geogpt4v python=3.10 -y
   conda activate geogpt4v
   pip install -r requirements.txt
   ```

3. Install Wolfarm engine. Please follow its [offical tutorial](https://support.wolfram.com/45743).

## Usage

### Data Preparation

1. Download following open-source datasets or use your own datasets:

   1. [Geometry3K](https://lupantech.github.io/inter-gps/)
   2. [GeoQA](https://github.com/chen-judge/GeoQA)
   3. [UniGeo](https://github.com/chen-judge/UniGeo)

2. Transform the dataset into the following format and save it as a jsonline file:

   ```
   # multi-choice quetion example
   {"id": 1, "question": "For the pair of similar figures, find the area of the green figure.", "choices": ["20.4", "28.6", "56.0", "78.4"], "answer": "D", "image": "image path"}
   
   # open-ending quetsion example
   {"id": 2, "question": "Prove that △ABC is congruent to △DEF.", "answer": "Because AB = DE, BC = EF, and ∠ABC is equal to ∠DEF, △ABC is congruent to △DEF.", "image": "image path"}
   ```

3. [optional] If you are using your own dataset, please modify the function 'construct_prompt'  in './pipeline/gen_instruction_mp.py'.

### Data Generation

Run the scripts in the following order, remember to modify the dataset path and API key in the scripts.

1. sh scripts/gen_instruction_gpt4v_mp.sh
2. sh scripts/gen_image_mp.sh
3. sh scripts/rerank_gp4v_mp.sh
4. sh scripts/filter.sh

## Train

You can use following models' offical training code or use your own code. You can run scripts/convert_format.sh to transform the GeoGPT4V dataset into the required format for model training.

1. [LLaVA](https://github.com/haotian-liu/LLaVA)
2. [ShareGPT4V](https://sharegpt4v.github.io/)
3. [InternVL-Chat](https://github.com/OpenGVLab/InternVL)

## Dataset

You can download the datasets from the following links.

| Dataset      | Link                                                   | Note                                                         |
| ------------ | ------------------------------------------------------ | ------------------------------------------------------------ |
| GeoGPT4V-1.0 | https://huggingface.co/datasets/caishihao/GeoGPT4V-1.0 | The dataset we used in the paper.                            |
| GeoGPT4V-1.1 | https://huggingface.co/datasets/caishihao/GeoGPT4V-1.1 | The dataset after applying the rule-based (image size) filtering. |

## Model

You can download the models from the following links.

| Model                                | Link                                                        |
| ------------------------------------ | ----------------------------------------------------------- |
| LLaVA-1.5-7B-GeoGPT4V                | https://huggingface.co/caishihao/GeoGPT4V-LLaVA-1.5-7B-v1   |
| LLaVA-1.5-13B-GeoGPT4V               | https://huggingface.co/caishihao/GeoGPT4V-LLaVA-1.5-13B-v1  |
| ShareGPT4V-7B-GeoGPT4V               | https://huggingface.co/caishihao/GeoGPT4V-ShareGPT4V-7B-v1  |
| ShareGPT4V-1.5-13B-GeoGPT4V          | https://huggingface.co/caishihao/GeoGPT4V-ShareGPT4V-13B-v1 |
| InternVL-Chat-V1.2-Plus-40B-GeoGPT4V | https://huggingface.co/Rosiness/GeoGPT4V-InternVL-Chat-40B  |



