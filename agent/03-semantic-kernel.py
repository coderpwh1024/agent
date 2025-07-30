import json
import os
from typing import Annotated
from dotenv import load_dotenv
import asyncio
from IPython.display import display, HTML
from lazy_object_proxy.utils import await_
from openai import AsyncOpenAI, AsyncAzureOpenAI

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import FunctionCallContent, FunctionResultContent, StreamingTextContent
from semantic_kernel.functions import kernel_function

import random


apiKey = ""
endpoint = ""
open_ai_version = "2024-08-01-preview"
azure_deployment = ""


class DestinationsPlugin:
    """一份随机的度假目的地列表"""

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
        available_destinations = self.destinations.copy()
        if self.last_destination and len(available_destinations) > 1:
            available_destinations.remove(self.last_destination)

        destination = random.choice(available_destinations)

        self.last_destination = destination

        return destination

client=AsyncAzureOpenAI(
    api_key=apiKey,
    azure_endpoint=endpoint,
    api_version=open_ai_version,
)

chat_completion_service = OpenAIChatCompletion(
    ai_model_id=azure_deployment,
    async_client=client,
)


AGENT_INSTRUCTIONS = """你是一位乐于助人的AI助手，可以帮助客户规划假期行程。

重要提示：当用户指定目的地时，始终为该地点进行规划。仅当用户未表明偏好时，才建议随机目的地。

对话开始时，请用以下信息介绍自己：
"你好！我是你的旅行助手 TravelAgent。我可以帮助你规划假期并为你推荐有趣的目的地。以下是一些你可以询问我的事情：
1. 为某个特定地点规划一日游
2. 推荐一个随机的度假目的地
3. 寻找具有特定特色（海滩、山脉、历史遗迹等）的目的地
4. 如果你不喜欢我的第一个建议，规划一个替代行程

今天你想让我帮你规划什么样的旅行呢？"

始终优先考虑用户的偏好。如果他们提到特定目的地，如“巴厘岛”或“巴黎”，请将你的规划重点放在该地点上，而不是建议其他替代方案。
"""

agent = ChatCompletionAgent(
    service=chat_completion_service,
    plugins=[DestinationsPlugin()],
    name="TravelAgent",
    instructions=AGENT_INSTRUCTIONS,
)

user_inputs = [
    "给我计划一个一日游",
    "我不喜欢那个目的地。给我计划另一个假期"
]

async  def main():
  thread: ChatHistoryAgentThread|None=None

  for user_input in user_inputs:
      html_output = (
          f"<div style='margin-bottom:10px'>"
          f"<div style='font-weight:bold'>User:</div>"
          f"<div style='margin-left:20px'>{user_input}</div>"
          f"</div>"
      )

      agent_name = None
      full_response: list[str] = []
      function_calls: list[str] = []

      current_function_name = None
      argument_buffer = ""

      async  for response in agent.invoke_stream(
          messages=user_input,
          thread=thread,
      ):
          thread = response.thread
          agent_name = response.name
          content_items = list(response.items)

          for item in content_items:
             if isinstance(item,FunctionCallContent):
                 if item.function_name:
                     current_function_name = item.function_name

                 if isinstance(item.arguments,str):
                     argument_buffer += item.arguments

             elif  isinstance(item,FunctionResultContent):
                 if current_function_name:
                     formatted_args = argument_buffer.strip()
                     try:
                         parsed_args = json.loads(formatted_args)
                         formatted_args = json.dumps(parsed_args)
                     except Exception:
                         pass

                     function_calls.append(f"Calling function: {current_function_name}({formatted_args})")
                     current_function_name=None
                     argument_buffer=""

                 function_calls.append(f"\n Function Result:\n\n{item.result}")
             elif isinstance(item,StreamingTextContent) and item.text:
                 full_response.append(item.text)

          if function_calls:
              html_output+=(
                  "<div style='margin-bottom:10px'>"
                  "<details>"
                  "<summary style='cursor:pointer; font-weight:bold; color:#0066cc;'>Function Calls (click to expand)</summary>"
                  "<div style='margin:10px; padding:10px; background-color:#f8f8f8; "
                  "border:1px solid #ddd; border-radius:4px; white-space:pre-wrap; font-size:14px; color:#333;'>"
                  f"{chr(10).join(function_calls)}"
                  "</div></details></div>"
              )

          html_output+=(
              "<div style='margin-bottom:20px'>"
              f"<div style='font-weight:bold'>{agent_name or 'Assistant'}:</div>"
              f"<div style='margin-left:20px; white-space:pre-wrap'>{''.join(full_response)}</div></div><hr>"
          )

          display(HTML(html_output))

if __name__ == "__main__":
    asyncio.run(main())
















