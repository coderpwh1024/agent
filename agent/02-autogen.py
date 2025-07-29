import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage

apiKey = ""
endpoint = ""
open_ai_version = "2024-08-01-preview"
deployment = ""

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


asyncio.run(run_client())

agent = AssistantAgent(
    name="assistant",
    model_client=client,
    tools=[],
    system_message="你是一位策划精彩假期行程的旅行代理",
)

from IPython.display import display, HTML


async def assistant_run():
    user_query = "Plan me a great sunny vacation";
    html_output = "<div style='margin-bottom:10px'>"
    html_output += "<div style='font-weight:bold'>User:</div>"
    html_output += f"<div style='margin-left:20px'>{user_query}</div>"
    html_output += "</div>"

    response = await agent.on_messages([TextMessage(content=user_query, source="user")],
                                       cancellation_token=CancellationToken(),
                                       )

    html_output += "<div style='margin-bottom:20px'>"
    html_output += "<div style='font-weight:bold'>Assistant:</div>"
    html_output += f"<div style='margin-left:20px; white-space:pre-wrap'>{response.chat_message.content}</div>"
    html_output += "</div>"

    display(HTML(html_output))


async def main():
    await assistant_run()


if __name__ == "__main__":
    asyncio.run(main())
