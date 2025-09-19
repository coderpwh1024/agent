from openai import AzureOpenAI
import os
from dotenv import load_dotenv


endpoint=""
deployment=" "
apiKey=" "


client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)


persona = input("Tell me the historical character I want to be:")
question = input("Ask your question about the historical character:")


prompt=f"""
你将扮演一位历史人物{persona}。

当被问到特定问题时，你需要根据时间线和事件的确切事实进行回答，仅提供准确答案。不要自行编造内容。若不了解某些信息，请直接表示不记得。

请回答以下问题：{question}
"""

messages =[{"role":"user","content":prompt}]

completion=client.chat.completions.create(
    model=deployment,
    messages=messages,
    temperature=0.1,
    max_tokens=1024
)


print("结果为:")
print("\n")
print(completion.choices[0].message.content)

