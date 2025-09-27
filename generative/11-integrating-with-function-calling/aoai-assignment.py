from IPython.core.debugger import prompt

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
from dotenv import load_dotenv

endpoint = " "
deployment = " "
apiKey = " "

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

print("======================================================")

# 带有markdown语法的json解析异常

# json_response1 = json.loads(openai_response1.choices[0].message.content)
# json_response2 = json.loads(openai_response2.choices[0].message.content)
# print(json_response1)
# print("\n")
# print(json_response2)


messages = [{"role": "user", "content": "Find me a good course for a beginner student to learn Azure ."}]

functions=[
    {
        "name":"search_courses",
        "description":"Retrieves course from the search index based on the parameters provided",
        "parameters":{
            "role":{
                "type":"string",
                "description":"The role of the learner (i.e. developer, data scientist, student, etc.)"
            },
            "product":{
                "type":"string",
                "description":"The product that the lesson is covering (i.e. Azure, Power BI, etc.)"
            },
            "level":{
                "type":"string",
                "description":"The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"

            }
        },
        "required":["role"]
    }
]

reponse = client.chat.completions.create(
    model=deployment,
    messages=messages,
    functions=functions,
    function_call="auto"
)
print(reponse.choices[0].message)







