import math
from datasets import Dataset
from sentence_transformers import (
    InputExample,
    SentenceTransformer,
    losses,
    models,
)
from sentence_transformers.datasets import NoDuplicatesDataLoader
from sentence_transformers.evaluation import TranslationEvaluator, InformationRetrievalEvaluator
from Cache import CachedMultipleNegativesRankingLoss
from tqdm import tqdm 

# Training parameters
model_name = "me5-large"
train_batch_size = 960
max_seq_length = 512
num_epochs = 15
data_path = "./data/final_data_27_01_24.jsonl"
test_path = './data/evaluation.jsonl'

# Use Huggingface/transformers model (like BERT, RoBERTa, XLNet, XLM-R) for mapping tokens to embeddings
word_embedding_model = models.Transformer(model_name, max_seq_length=max_seq_length)

# Apply mean pooling to get one fixed sized sentence vector
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

################# Read the train corpus  #################
train = Dataset.from_json(data_path)
train_samples = []
for row in train:
    anchor = row["passage"]
    pos = row["positive"]
    neg = row["negative"]
    train_samples.append(InputExample(texts=[anchor, pos, neg]))

test = Dataset.from_json(test_path)

query = {}
positive = test['positive']
for i in tqdm(range(len(positive))):
    query['q'+str(i)] = positive[i]

context = {}
anchor = test['anchor']
for i in tqdm(range(len(anchor))):
    context['c'+str(i)] = anchor[i]

relevant = {}
for i in tqdm(range(len(anchor))):
    relevant['q'+str(i)] = set(['c'+str(i)])


evaluator = InformationRetrievalEvaluator(queries=query,corpus=context, relevant_docs=relevant,batch_size=64, show_progress_bar=True)

# evaluator = TranslationEvaluator(test['positive'],test['anchor'], batch_size=64, show_progress_bar=False)

train_dataloader = NoDuplicatesDataLoader(train_samples, batch_size=train_batch_size)
train_loss = CachedMultipleNegativesRankingLoss(model=model, mini_batch_size=96)
# train_loss = losses.ContrastiveLoss(model, margin=0.2)

warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.05)

# Train the model
# model.fit(
#     train_objectives=[(train_dataloader, train_loss)],
#     epochs=num_epochs,
#     warmup_steps=warmup_steps,
#     optimizer_params={"lr": 5e-6},
#     checkpoint_path="model_26_01_24",
#     output_path='result',
#     show_progress_bar=True,
#     use_amp=False,  # Set to True, if your GPU supports FP16 cores
#     checkpoint_save_steps=500,
#     checkpoint_save_total_limit=10,
#     evaluator = evaluator,
#     evaluation_steps = 20,
# )

model.evaluate(evaluator=evaluator, output_path='result')
