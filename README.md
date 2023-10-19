# SynTOD

This is code for the paper "SynTOD: An Augmented Synthetic Response Approach for Robust End-to-end Task-Oriented Dialogue System"


## Checkout source code and data from github repository
To download [data.zip](link) properly, git lfs(Large File Storage) extension must be installed.
```
git lfs install
git lfs pull
git checkout -f HEAD
```
## Environment setting

Our python version is 3.6.9.

The package can be installed by running the following command.

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Download preprocessed data

For the experiments, we use MultiWOZ2.1 and MultiWOZ2.2.
You can download at [MultiWOZ](link)

We use the preprocessing scripts implemented by [Zhang et al., 2020](https://arxiv.org/abs/1911.10484). Please refer to [here](https://github.com/thu-spmi/damd-multiwoz/blob/master/data/multi-woz/README.md) for the details.

## Download pre-trained models
- T5-small (https://huggingface.co/t5-small)
- PPTOD-small (https://github.com/awslabs/pptod)
## Training

Our implementation supports a single GPU with 2 phases training. Please use smaller batch sizes if out-of-memory error raises.

First, we train model with original data by following script (please refer to `config.py` to see the detailed configs):
```
CUDA_VISIBLE_DEVICES="0" python main.py -run_type train -model_dir ckpt2.1/t5-small -backbone t5-small -version 2.1
```

The next step, the best checkpoint is ultilized to generate synthetic data:
```
CUDA_VISIBLE_DEVICES="0" python main.py -run_type predict -ckpt ckpt2.1/t5-small/ckpt-epoch4 -batch_size 64 -pred_data_type test -output out.json -version 2.1
```
After that, combine systhetic data with original data: 
```
python data/merge.py 
```

Finally, set `ADD_SYNTHETIC_DATA = True` in `quick_config.py`  ,
train model with synthetic data and original data:

```
CUDA_VISIBLE_DEVICES="0" python main.py -run_type train -model_dir ckpt2.1/t5-small-synthetic -backbone t5-small -version 2.1
```

The checkpoints will be saved at the end of each epoch (the default training epoch is set to 10).

## Inference

```
python main.py -run_type predict -ckpt $CHECKPOINT -output $MODEL_OUTPUT -batch_size $BATCH_SIZE
```

All checkpoints are saved in ```$MODEL_DIR``` with names such as 'ckpt-epoch10-step7053'.

The result file (```$MODEL_OUTPUT```) will be saved in the checkpoint directory.

To reduce inference time, it is recommended to set large ```$BATCH_SIZE```. In our experiemnts, it is set to 16 for inference.

You can download our trained model [here](https://drive.google.com/file/d/1azIdWPgJKa3PTBFE8lZ1B02bfgguKS2u/view?usp=sharing).

## Acknowledgements
Our code hugely based on (https://github.com/bepoetree/MTTOD) for "Improving End-to-End Task-Oriented Dialogue System with A Simple Auxiliary Task" and
(https://github.com/Tomiinek/MultiWOZ_Evaluation) for evaluation.
