from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = " "
deployment = " "
apiKey = " "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)

question = input("Ask your questions on python language to your study buddy:")

prompt = f"""
您是一位Python语言专家。

当被问及特定问题时，您需要按照以下格式进行回答：

- 概念
- 展示概念实现的示例代码
- 对示例的讲解及概念实现方式的说明，帮助用户更好地理解

请针对以下问题提供答案：{question}
"""

messages = [{"role": "user", "content": prompt}]

completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    temperature=0.1,
    max_tokens=1024
)
print("结果为:")
print("\n")
print(completion.choices[0].message.content)
