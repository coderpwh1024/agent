import os
import json
import requests
import asyncio
from accelerate.commands.config.update import description
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials import AzureKeyCredential
from autogen_core import CancellationToken
from autogen_core.tools import FunctionTool
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from typing import Any, Callable, Set, Dict, List, Optional


apiKey =""
endpoint = ""
open_ai_version = "2024-08-01-preview"
deployment = " "

client = AzureAIChatCompletionClient(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    credential=AzureKeyCredential(apiKey),
    model_info={
        "json_output": True,
        "function_calling": True,
        "vision": True,
        "family": "unknown"
    }
)


async def run_client():
    result = await   client.create([UserMessage(content="What is the capital of France?", source="user")])
    print(result)


def vacation_destinations(city: str) -> tuple[str, str]:
    """
    Checks if a specific vacation destination is available

    Args:
        city (str): Name of the city to check

    Returns:
        tuple: Contains city name and availability status ('Available' or 'Unavailable')
    """
    descriptions = {
        "Barcelona": "Available",
        "Tokyo": "Unavailable",
        "Cape Town": "Available",
        "Vancouver": "Available",
        "Dubai": "Unavailable",
    }

    if city in descriptions:
        return city, descriptions[city]
    else:
        return city, "City not found"


# tool
get_vacations = FunctionTool(
    vacation_destinations, description="Search for vacation destinations and if they are available or not."
)

agent = AssistantAgent(
    name="assistant",
    model_client=client,
    tools=[get_vacations],
    system_message="You are a helpful assistant that helps users find vacation destinations and their availability.",
    reflect_on_tool_use=True,
)


async def assistant_run() -> None:
    response = await  agent.on_messages(
        [TextMessage(content="I would like to take a trip to Tokyo", source="user")],
        cancellation_token=CancellationToken(),
    )
    print(response.inner_messages)
    print(response.chat_message)


if __name__ == "__main__":
    asyncio.run(assistant_run())
