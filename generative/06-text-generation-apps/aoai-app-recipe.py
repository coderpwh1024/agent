from openai import AzureOpenAI
import os
from dotenv import load_dotenv

endpoint=""
deployment=" "
apiKey=" "


client = AzureOpenAI(

    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    api_version="2024-08-01-preview",
)


no_recipes = input("食谱数量(例如，5:")


ingredients = input("输入的食材(例如，鸡肉，土豆，胡萝卜:")


filter=input("过滤器(例如，素食，素食， celiac:")



prompt = f"""根据以下食材：{ingredients}，向我展示{no_recipes}道菜的食谱。每道食谱请列出所使用的全部食材，不要包含{filter}："""


messages = [{"role": "user", "content": prompt}]

completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    temperature=0.1,
    max_tokens=1024
)

print("食谱为:")
print(completion.choices[0].message.content)

old_prompt_result= completion.choices[0].message.content
prompt_shopping = "请生成一个购物清单，请不要包含我在家有的食材："
new_prompt = f"根据家中已有的食材{ingredients}以及这些生成的食谱：{old_prompt_result}，{prompt_shopping}"


messages=[{"role":"user","content":new_prompt}]
completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    temperature=0.1,
    max_tokens=1024
)
print("\n")
print("============================shipping list===============")
print(completion.choices[0].message.content)



