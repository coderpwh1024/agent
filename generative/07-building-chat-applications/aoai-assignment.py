import os
from os import times

from openai import AzureOpenAI
import numpy as np
from dotenv import load_dotenv
from qdrant_client.http import model

endpoint = ""
deployment = " "
apiKey = " "

# 构建azure open client 客户端
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)


text_prompt = "牛津逗号应该一直使用吗？";


begin = times()

response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "你是一个智能小助手"},
        {"role": "user", "content": text_prompt}
    ]
)

end = times()
print("大模型处理时间: %.2f 秒" % (end[0] - begin[0]))
print("大模型返回结果为:\n")
print(response.choices[0].message.content)
