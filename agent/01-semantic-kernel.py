import os
from typing import Annotated
import os
from typing import Annotated
import asyncio
from openai import AsyncOpenAI

from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from sqlalchemy.sql.functions import random


class DestinationsPlugin:
    """"一份随机的度假目的地列表."""

    def __init__(self):
        self.destinations = [
            "Barcelona, Spain",
            "Paris, France",
            "Berlin, Germany",
            "Tokyo, Japan",
            "Sydney, Australia",
            "New York, USA",
            "Cairo, Egypt",
            "Cape Town, South Africa",
            "Rio de Janeiro, Brazil",
            "Bali, Indonesia"
        ]

        self.last_destination = None

    @kernel_function(description="提供一个随机的度假目的地")
    def get_random_destination(self) -> Annotated[str, "返回一个随机的度假目的地"]:
        available_destinations = self.destinations.copy()
        if self.last_destination in available_destinations:
            available_destinations.remove(self.last_destination)

        destination = random.choice(available_destinations)

        self.last_destination = destination
        return destination


load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com/",
)

# Create an AI Service that will be used by the `ChatCompletionAgent`
chat_completion_service = OpenAIChatCompletion(
    ai_model_id="gpt-4o-mini",
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