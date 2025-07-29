import json
import os
import random
import asyncio
from typing import Annotated
from dotenv import load_dotenv
from IPython.display import display, HTML
from openai import AsyncOpenAI
from openai import AsyncOpenAI, AsyncAzureOpenAI
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import FunctionCallContent, FunctionResultContent, StreamingTextContent
from semantic_kernel.functions import kernel_function
from torchgen.api.native import arguments

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


client = AsyncAzureOpenAI(
    api_key=apiKey,
    azure_endpoint=endpoint,
    api_version=open_ai_version,
)

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

user_inputs = [
    "为旅行安排一个随机目的地",
    "我不喜欢那个目的地。再给我计划另一个假期"
]


async def main():
    thread: ChatHistoryAgentThread | None = None

    for user_input in user_inputs:
        html_output = (
            f"<div style='margin-bottom:10px'>"
            f"<div style='font-weight:bold'>User:</div>"
            f"<div style='margin-left:20px'>{user_input}</div>"
        )
        agent_name = None
        full_response: list[str] = []
        function_calls: list[str] = []

        current_function_name = None
        argument_buffer = ""

        async for response in agent.invoke_stream(
                messages=user_input,
                thread=thread,
        ):
            thread = response.thread
            agent_name = response.name
            content_items = list(response.items)

            for item in content_items:
                if isinstance(item, FunctionCallContent):
                    if item.function_name:
                        current_function_name = item.function_name

                    if instance(item.arguments, str):
                        argument_buffer += item.arguments
                elif isinstance(item, FunctionResultContent):
                    if current_function_name:
                        formatted_args = argument_buffer.strip()
                        try:
                            parsed_args = json.loads(formatted_args)
                            formatted_args = json.dumps(parsed_args)
                        except Exception:
                            pass

                        function_calls.append(f"Calling function: {current_function_name}({formatted_args})")
                        current_function_name = None
                        argument_buffer = ""

                    function_calls.append(f"\nFunction Result:\n\n{item.result}")
                elif isinstance(item, StreamingTextContent) and item.text:
                    full_response.append(item.text)

    if function_calls:
        html_output += (
            "<div style='margin-bottom:10px'>"
            "<details>"
            "<summary style='cursor:pointer; font-weight:bold; color:#0066cc;'>Function Calls (click to expand)</summary>"
            "<div style='margin:10px; padding:10px; background-color:#f8f8f8; "
            "border:1px solid #ddd; border-radius:4px; white-space:pre-wrap; font-size:14px; color:#333;'>"
            f"{chr(10).join(function_calls)}"
            "</div></details></div>"
        )

    html_output += (
        "<div style='margin-bottom:20px'>"
        f"<div style='font-weight:bold'>{agent_name or 'Assistant'}:</div>"
        f"<div style='margin-left:20px; white-space:pre-wrap'>{''.join(full_response)}</div></div><hr>"
    )

    display(HTML(html_output))


if __name__ == "__main__":
    asyncio.run(main())




