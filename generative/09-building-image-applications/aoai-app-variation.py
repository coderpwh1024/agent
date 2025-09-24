from langgraph.pregel.io import single
from openai import AzureOpenAI
import os
import requests
from PIL import Image
import dotenv
import json

dotenv.load_dotenv()

endpoint = " "
deployment = " "
apiKey = " "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview",
)

# 获取图片
image_dir = os.path.join(os.curdir, 'images')

image_path = os.path.join(image_dir, 'generated-image.png')
print("图片路径为:", image_path)
print("\n")
image = Image.open(image_path)
image.show()

try:
    print("LOG creating variation")
    result = client.images.create_variation(
        image=open(image_path, "rb"),
        n=1,
        size="1024*1024"
    )
    client.images.create_variation()
    response = json.loads(result.model_dump_json())

    image_path = os.path.join(image_dir, 'generated_variation.png')

    image_url = response['data'][0]['url']

    print("LOG downloading image")
    generated_image = requests.get(image_url).content
    with open(image_path, 'wb') as image_file:
        image_file.write(generated_image)

        image = Image.open(image_path)
        image.show()

finally:
    print("completed!")
