import json
import os
from dotenv import load_dotenv
from IPython.display import display, HTML
from typing import Annotated
import asyncio
from openai import AsyncAzureOpenAI

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import FunctionCallContent, FunctionResultContent, StreamingTextContent
from semantic_kernel.functions import kernel_function

apiKey = ""
endpoint = " "
open_ai_version = "2024-08-01-preview"
azure_deployment = " "


# 插件定义
class DestinationsPlugin:
    """度假地点清单"""

    @kernel_function(description="提供一个随机的度假目的地")
    def get_destinatios(self) -> Annotated[str, "返回一个随机的度假目的地"]:
        return """
                西班牙，巴塞罗那
                法国，巴黎
                德国，柏林
                日本，东京
                美国，纽约
                """

    @kernel_function(description="返回所有可用的度假目的地")
    def get_available_destinations(self,destination:Annotated[str,"检查可用的地点"]) -> Annotated[str, "返回所有可用的度假目的地"]:
        return """
                巴塞罗那 - 不可用
                巴黎 - 可用
                柏林 - 可用
                东京 - 不可用
                纽约 - 可用
                """

load_dotenv()

# 客户端
client = AsyncAzureOpenAI(
    api_key=apiKey,
    azure_endpoint=endpoint,
    api_version=open_ai_version,
)

# chat
chat_completion_service = OpenAIChatCompletion(
    ai_model_id=azure_deployment,
    async_client=client,
)

agent = ChatCompletionAgent(
    service=chat_completion_service,
    name="TravelAgent",
    instructions="您是一位智能助手，能帮助客户规划随机度假目的地的旅行行程",
    plugins=[DestinationsPlugin()],
)

user_inputs = [
    "有哪些可用的目的地？",
    "巴塞罗那可用吗？",
    "有没有不在欧洲的可用度假目的地？",
]

async def main():
    thread: ChatHistoryAgentThread | None = None

    for user_input in user_inputs:
        html_output = (
            f"<div style='margin-bottom:10px'>"
            f"<div style='font-weight:bold'>User:</div>"
            f"<div style='margin-left:20px'>{user_input}</div></div>"
        )

        agent_name = None
        full_response: list[str] = []
        function_calls: list[str] = []

        # Buffer to reconstruct streaming function call
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

                    # Accumulate arguments (streamed in chunks)
                    if isinstance(item.arguments, str):
                        argument_buffer += item.arguments
                elif isinstance(item, FunctionResultContent):
                    # Finalize any pending function call before showing result
                    if current_function_name:
                        formatted_args = argument_buffer.strip()
                        try:
                            parsed_args = json.loads(formatted_args)
                            formatted_args = json.dumps(parsed_args)
                        except Exception:
                            pass  # leave as raw string

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

        display(HTML(html_output).data)

if __name__ == "__main__":
    asyncio.run(main())














