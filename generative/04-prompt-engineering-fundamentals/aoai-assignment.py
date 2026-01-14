import os

import tiktoken



text=f"""
木星是太阳系中距离太阳第五近的行星，也是太阳系中体积最大的行星。作为一颗气态巨行星，木星的质量仅为太阳的千分之一，但却是太阳系中所有其他行星质量总和的两倍半。木星是夜空中肉眼可见的最明亮天体之一，在有历史记载之前就已被古代文明所知晓。其名称源于罗马神话中的朱庇特[19]。从地球观测时，木星的亮度足以让其反射的光投射出可见的阴影[20]，是继月球和金星之后，夜空中平均亮度第三的自然天体。
"""


encoding = tiktoken.encoding_for_model("gpt-4o")

tokens = encoding.encode(text)
print(tokens)

[encoding.decode_single_token_bytes(token) for token in tokens]

from openai import AzureOpenAI
from dotenv import load_dotenv



load_dotenv()

client = AzureOpenAI(
    api_key='1DmwJTq4xKOzqz9D1uZILiyjSI3rjF9SWho5zyGqUI68Gv7kPia7JQQJ99AKACLArgHXJ3w3AAAAACOGwDD5', # this is also the default, it can be omitted
    api_version='2024-08-01-preview',
    azure_endpoint='https://tangi-m42ecc94-southcentralus.cognitiveservices.azure.com'
)



#    大模型请求函数
def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        #  TODO
        model='Server',
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
        max_tokens=1024
    )
    return response.choices[0].message.content


text = f"""
额, 你可看见吗
"""

prompt = f"""
```{text}```
"""

response = get_completion(prompt)
print(response)

text = f"""
生成一份关于2076年火星战争的教案
"""

prompt = f"""
```{text}```
"""

response = get_completion(prompt)
print(response)


text=f"""
木星是太阳系中距离太阳第五近的行星，也是太阳系中最大的行星。它是一颗气态巨行星，质量仅为太阳的千分之一，但却是太阳系中所有其他行星总质量的两倍半。木星是夜空中肉眼可见的最明亮天体之一，在有历史记载之前就已被古代文明所知。它的名字来源于罗马神话中的朱庇特神[19]。从地球观测时，木星的亮度足以让其反射的光投射出可见的阴影[20]，是继月球和金星之后，夜空中平均亮度第三的自然天体。
"""

prompt = f"""
将提供给你的内容总结成适合二年级小朋友理解的版本。
```{text}```
"""

response = get_completion(prompt)
print(response)


response = client.chat.completions.create(
    #  TODO
    model='',
    messages=[
        {"role":"system","content":"You are a sarcastic assistant."},
        {"role":"user","content":"Who won the world series in 2020?"},
        {"role":"assistant","content":"Who do you think won? The Los Angeles Dogers of course."},
        {"role":"user","content":"Where was it played?"}
    ],
)

print(response.choices[0].message.content)


