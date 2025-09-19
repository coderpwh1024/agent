from IPython.core.debugger import prompt
from grpc.framework.interfaces.base.utilities import completion
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from torch.ao.quantization import per_channel_weight_observer_range_neg_127_to_127

load_dotenv()

endpoint = ""
deployment = " "
apiKey = " "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview",
)

deployment = ""

prompt = """Complete the following:Once upon a time there was a"""

messages = [{"role": "user", "content": prompt}]
completion = client.chat.completions.create(model=deployment, messages=messages)

print("打印结果为:")
print("\n")
print(completion.choices[0].message.content)
