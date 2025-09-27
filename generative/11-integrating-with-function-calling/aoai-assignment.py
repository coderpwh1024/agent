from IPython.core.debugger import prompt
from matplotlib.style.core import available

student_1_description = "Emily Johnson is a sophomore majoring in computer science at Duke University. She has a 3.7 GPA. Emily is an active member of the university's Chess Club and Debate Team. She hopes to pursue a career in software engineering after graduating."

student_2_description = "Michael Lee is a sophomore majoring in computer science at Stanford University. He has a 3.8 GPA. Michael is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after finishing his studies."

# 提示词1

prompt1 = f'''
Please extract the following information from the given text and return it as a JSON object:

name
major
school
grades
club

This is the body of text to extract the information from:
{student_1_description}
'''

# 提示词2

prompt2 = f'''
Please extract the following information from the given text and return it as a JSON object:

name
major
school
grades
club

This is the body of text to extract the information from:
{student_2_description}
'''

import os
import json
from openai import AzureOpenAI

endpoint=" "
deployment=" "
apiKey=" "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)

openai_response1 = client.chat.completions.create(
    model=deployment,
    messages=[{"role": "user", "content": prompt1}]
)

print(openai_response1.choices[0].message.content)
print("\n")

openai_response2 = client.chat.completions.create(
    model=deployment,
    messages=[{"role": "user", "content": prompt2}]
)
print(openai_response2.choices[0].message.content)
print("\n")

print("===============================================================================================================")

# 带有markdown语法的json解析异常

# json_response1 = json.loads(openai_response1.choices[0].message.content)
# json_response2 = json.loads(openai_response2.choices[0].message.content)
# print(json_response1)
# print("\n")
# print(json_response2)


messages = [{"role": "user", "content": "Find me a good course for a beginner student to learn Azure ."}]

functions = [
    {
        "name": "search_courses",
        "description": "Retrieves courses from the search index based on the parameters provided",
        "parameters": {
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "description": "The role of the learner (i.e. developer, data scientist, student, etc.)"
                },
                "product": {
                    "type": "string",
                    "description": "The product that the lesson is covering (i.e. Azure, Power BI, etc.)"
                },
                "level": {
                    "type": "string",
                    "description": "The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"
                }
            },
            "required": [
                "role"
            ]
        }
    }
]

response = client.chat.completions.create(model=deployment,
                                          messages=messages,
                                          functions=functions,
                                          function_call="auto")

# 打印请求函数的结果
print(response.choices[0].message)
response_message = response.choices[0].message

import requests


# 搜索课程 函数
def search_curses(role, product, level):
    url = "https://learn.microsoft.com/api/catalog/"
    params = {
        "role": role,
        "product": product,
        "level": level
    }
    response = requests.get(url, params=params)
    modules = requests.json()["modules"]
    results = []
    for module in modules[:5]:
        title = module["title"]
        url = module["url"]
        results.append({"title": title, "url": url})
    return str(results)


# 解析函数

if response_message.function_call.name:
    print("Function call 函数为:")
    print(response_message.function_call.name)
    print("\n")

    function_name = response_message.function_call.name

    available_functions = {
        "search_courses": search_curses,
    }
    function_to_call = available_functions[function_name]

    function_args = json.loads(response_message.function_call.arguments)
    print("函数参数部分为:")
    print(function_args)
    function_response = function_to_call(**function_args)

    print("函数输出部分为:")
    print("\n")
    print(function_response)
    print("\n")
    print(type(function_response))

    messages.append(
        {
            "role": response_message.role,
            "content": None,
            "function_call": {
                "name": function_name,
                "arguments": response_message.function_call.arguments
            }
        }
    )
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response
        }
    )

print("Messages in next request:")
print(messages)
print()

# 第二次请求大模型
second_response = client.chat.completions.create(
    messages=messages,
    model=deployment,
    function_call="auto",
    functions=functions,
    temperature=0
)

print(second_response.choices[0].message)
