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
You are going to play as a historical character {persona}. 

Whenever certain questions are asked, you need to remember facts about the timelines and incidents and respond the accurate answer only. Don't create content yourself. If you don't know something, tell that you don't remember.

Provide answer for the question: {question}
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

