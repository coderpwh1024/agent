import os
from typing import Annotated
import os
from typing import Annotated
import asyncio
from openai import AsyncOpenAI, AsyncAzureOpenAI
import random
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function



apiKey = " "
endpoint = ""
open_ai_version = "2024-08-01-preview"
azure_deployment = ""



class DestinationsPlugin:
    """"一份随机的度假目的地列表."""

    def __init__(self):
        self.destinations = [
            "巴塞罗那, 西班牙",
            "巴黎, 法国",
            "柏林, 德国",
            "东京, 日本",
            "悉尼, 澳大利亚",
            "纽约, 美国",
            "开罗, 埃及",
            "开普敦, 南非",
            "里约热内卢, 巴西",
            "巴厘岛, 印度尼西亚"
        ]

        self.last_destination = None

    @kernel_function(description="提供一个随机的度假目的地")
    def get_random_destination(self) -> Annotated[str, "返回一个随机的度假目的地"]:
        # Get available destinations (excluding last one if possible)
        available_destinations = self.destinations.copy()
        if self.last_destination and len(available_destinations) > 1:
            available_destinations.remove(self.last_destination)

        destination = random.choice(available_destinations)

        self.last_destination = destination

        return destination


load_dotenv()

client = AsyncAzureOpenAI(
    api_key=apiKey,
    azure_endpoint=endpoint,
    api_version=open_ai_version,
)


# Create an AI Service that will be used by the `ChatCompletionAgent`
chat_completion_service = OpenAIChatCompletion(
    ai_model_id=azure_deployment,
    async_client=client,
)

agent = ChatCompletionAgent(
    service=chat_completion_service,
    plugins=[DestinationsPlugin()],
    name="TravelAgent",
    instructions="您是一位智能助手，能帮助客户规划随机度假目的地的旅行行程"
)


async def main():
    thread: ChatHistoryAgentThread | None = None

    user_inputs = [
        "为我安排一次旅行",
    ]

    for user_input in user_inputs:
        print(f"# User:{user_input}\n")
        first_chunk = True
        async for reponse in agent.invoke_stream(
                message=user_input, thread=thread,
        ):
            if first_chunk:
                print(f"#{reponse.name}:", end="", flush=True)
                first_chunk = False
            print(f"{reponse}", end="", flush=True)
            thread = reponse.thread
        print()

    await thread.delete() if thread else None


if __name__ == "__main__":
    asyncio.run(main())