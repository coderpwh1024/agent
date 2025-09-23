import  os
from openai import  AzureOpenAI
import  numpy as np
from dotenv import  load_dotenv

endpoint = " "
deployment = " "
apiKey = " "

# 构建azure open client 客户端
client=AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)



