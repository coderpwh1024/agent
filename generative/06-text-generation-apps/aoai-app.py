from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint=""
deployment=" "
apiKey=" "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview",
)


prompt="""从前有一个"""

messages = [{"role": "user", "content": prompt}]
completion = client.chat.completions.create(model=deployment, messages=messages)

print("打印结果为:")
print("\n")
print(completion.choices[0].message.content)
