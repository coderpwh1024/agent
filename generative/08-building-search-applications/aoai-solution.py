import os
import pandas as pd
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
from qdrant_client.http import model

load_dotenv()

endpoint = " "
deployment = " "
apiKey = " "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)

# embedding 模型
model = 'text-embedding-3-large'
SIMILARITIES_RESULTS_THRESHOLD = 0.75
DATASET_NAME = "../embedding_index_3m.json"



# 加载JSON 数据
def load_dataset(source:str)->pd.core.frame.DataFrame:
    pd_vectors = pd.read_json(source)
    return  pd_vectors.drop(columns=["text"],errors="ignore").fillna("")


# 余弦相似度
def cosine_similarity(a,b):
    if len(a)>len(b):
        b=np.pad(b,(0,len(a)-len(b)),'constant')
    elif len(b)>len(a):
        a=np.pad(a,(0,len(b)-len(a)),'constant')
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
