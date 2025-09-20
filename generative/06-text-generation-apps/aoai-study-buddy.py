from openai import AzureOpenAI
import os
from dotenv import  load_dotenv

load_dotenv()


endpoint=""
deployment=" "
apiKey=" "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)

question=input("Ask your questions on python language to your study buddy:")
prompt=f"""
You are an expert on the python language.

Whenever certain questions are asked,you need to provide response in below format.

- Concept
- Example code showing the concept implementation
- explanation of the example and how the concept is done for the user to understand better.

Provide answer for the question: {question}
"""

messages=[{"role":"user","content":prompt}]

completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    temperature=0.1,
    max_tokens=1024
)
print("结果为:")
print("\n")
print(completion.choices[0].message.content)

