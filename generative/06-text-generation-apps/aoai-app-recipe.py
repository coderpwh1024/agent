from openai import  AzureOpenAI
import os
from dotenv import  load_dotenv

client = AzureOpenAI(

    azure_endpoint="",
    azure_deployment="",
    api_key="",
    api_version="2024-08-01-preview",
)

deployment =""

no_recipes = input("No of recipes (for example ,5:")

ingredients = input("List of ingredients (for example, chicken,potatoes,and carrots:")

filter =input("Filter (for exmaple,vegetarian,vegan,or gluten-free:")

