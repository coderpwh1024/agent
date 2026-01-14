import os
from openai import AzureOpenAI

# 不自定义http_client，让库使用默认配置
endpoint = ""
subscription_key = ""

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-08-01-preview",
    timeout=60.0,  # 设置超时
    max_retries=3  # 设置重试次数
)

try:
    response = client.chat.completions.create(
        model="Server",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "如何快速上手python"},
        ]
    )
    print("请求结果为:", response.choices[0].message.content)
except Exception as e:
    print(f"请求失败: {e}")