import os
from os import times

from openai import AzureOpenAI
import numpy as np
from dotenv import load_dotenv
from qdrant_client.http import model

endpoint=" "
deployment=" "
apiKey=" "

# 构建azure open client 客户端
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)

text_prompt = "牛津逗号应该一直使用吗？";

# prompt = "Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. By contrast, humans can generally perform a new language task from only a few examples or from simple instructions - something that current NLP systems still largely struggle to do. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art fine-tuning approaches.\n\ntl;dr"

prompt = """
最近的研究表明，在对大型文本语料库进行预训练后再针对特定任务进行微调，能够在许多自然语言处理任务和基准测试中实现显著提升。尽管这种方法在架构上通常与任务无关，但仍需要数千或数万个示例的特定任务微调数据集。
相比之下，人类通常只需几个示例或简单指令就能完成新的语言任务——而这仍然是当前自然语言处理系统难以企及的能力。
本文证明，扩大语言模型规模能显著提升任务无关的少样本学习性能，有时甚至能够与先前需要微调的最先进方法相媲美。
简要总结：大规模语言模型通过少样本学习即可达到与传统微调方法相当的性能。
"""

begin = times()

response = client.chat.completions.create(
    model=deployment,
    messages=[
        # {"role": "system", "content": "你是一个智能小助手"},
        {"role": "system", "content": prompt},
        {"role": "user", "content": text_prompt}
    ]
)

end = times()
print("大模型处理时间: %.2f 秒" % (end[0] - begin[0]))
print("大模型返回结果为:\n")
print(response.choices[0].message.content)

print("---------------------------------------------------------------------------------------")



# 余弦相似度
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


text = "the quick brown for jumped over the lazy dog"
model = "text-embedding-3-large"

emb = client.embeddings.create(input='[text]', model=model).data[0].embedding
print( emb)
print("---------------------------------------------------------------------------------------")

# compare several words
automobile_embedding  = client.embeddings.create(input='automobile', model=model).data[0].embedding
vehicle_embedding     = client.embeddings.create(input='vehicle', model=model).data[0].embedding
dinosaur_embedding    = client.embeddings.create(input='dinosaur', model=model).data[0].embedding
stick_embedding       = client.embeddings.create(input='stick', model=model).data[0].embedding

print(cosine_similarity(automobile_embedding, vehicle_embedding))
print(cosine_similarity(automobile_embedding, dinosaur_embedding))
print(cosine_similarity(automobile_embedding, stick_embedding))
print("\n")
print("===============================embedding======================================")