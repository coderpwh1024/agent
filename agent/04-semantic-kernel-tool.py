import json
import os
from dotenv import load_dotenv
from IPython.display import display, HTML
from typing import Annotated
from openai import AsyncOpenAI

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import FunctionCallContent, FunctionResultContent, StreamingTextContent
from semantic_kernel.functions import kernel_function


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




