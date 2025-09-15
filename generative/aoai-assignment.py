import os
from http.client import responses
from importlib import import_module

from langchain.chat_loaders.facebook_messenger import import_lookup
from lib2to3.btm_utils import tokens

import tiktoken
from prompt_toolkit import prompt

text = f"""
Jupiter is the fifth planet from the Sun and the \
largest in the Solar System. It is a gas giant with \
a mass one-thousandth that of the Sun, but two-and-a-half \
times that of all the other planets in the Solar System combined. \
Jupiter is one of the brightest objects visible to the naked eye \
in the night sky, and has been known to ancient civilizations since \
before recorded history. It is named after the Roman god Jupiter.[19] \
When viewed from Earth, Jupiter can be bright enough for its reflected \
light to cast visible shadows,[20] and is on average the third-brightest \
natural object in the night sky after the Moon and Venus.
"""

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

tokens = encoding.encode(text)
print(tokens)

[encoding.decode_single_token_bytes(token) for token in tokens]

from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key="",
    api_version="",
)

deployment = "";


#    大模型请求函数
def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}],
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        temperature=0,
        max_tokens=1024
    )

    return response.choices[0].message.content


text = f"""
oh say can you see 
"""

prompt = f"""
```{text}```
"""

response = get_completion(prompt)
print(response)

text=f"""
generate a lesson plan on the Martian War of 2076
"""

prompt=f"""
```{text}```
"""

response=get_completion(prompt)
print(response)


