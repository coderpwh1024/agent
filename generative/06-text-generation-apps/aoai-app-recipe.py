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


no_recipes = input("No of recipes (for example ,5:")

ingredients = input("List of ingredients (for example, chicken,potatoes,and carrots:")

filter = input("Filter (for exmaple,vegetarian,vegan,or gluten-free:")

prompt = f"""Show me {no_recipes} recipes for a dish with the following ingredients:{ingredients} . Per recipe,list all the ingredients used,no {filter}:"""

messages = [{"role": "user", "content": prompt}]

completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    temperature=0.1,
    max_tokens=1024
)

print("Recipes:")
print(completion.choices[0].message.content)

old_prompt_result= completion.choices[0].message.content
prompt_shopping = "Produce a shopping list, and please don't include ingredients that I already have at home: "
new_prompt = f"Given ingredients at home {ingredients} and these generated recipes: {old_prompt_result}, {prompt_shopping}"

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



