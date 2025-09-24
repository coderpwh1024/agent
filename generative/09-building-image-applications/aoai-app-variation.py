from openai import  AzureOpenAI
import  os
import requests
from PIL import Image
import  dotenv
import  json


dotenv.load_dotenv()


endpoint=" "
deployment=" "
apiKey=" "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview",
)


