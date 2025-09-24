import dotenv
from openai import AzureOpenAI
import os
import  requests
from PIL import  Image
import  json

dotenv.load_dotenv()

# gpt-40 暂时不支持图片生成等

endpoint=" "
deployment=" "
apiKey=" "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview",
)

try:
    result = client.images.generate(
        model=deployment,
        prompt="""小兔子骑在马背上，举着棒棒糖，置身于一片雾蒙蒙的、长满洋水仙的草甸上。它说着 你好 """,
        size="1024*1024",
        n=1
    )
    generation_response=json.loads(result.model_dump_json())
    image_dir=os.path.join(os.curdir,'images')

    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    image_path=os.path.join(image_dir,'generated-image.png')

    images_url=generation_response['data'][0]['url']
    generated_image=requests.get(images_url).content
    with open(image_path,'wb') as image_file:
        image_file.write(generated_image)

    image=Image.open(image_path)
    image.show()

finally:
    print("完成!")


