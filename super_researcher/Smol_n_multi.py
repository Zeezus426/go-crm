import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv
from autogen_ext_mcp.tools import get_tools_from_mcp_server
load_dotenv()


async def main():
    serp = os.getenv("SERPER_API_KEY")
    fire = os.getenv("FIRE")

    serper = StdioServerParameters(
        command="npx",  # Using uvx ensures dependencies are available
        args = ["-y", "serper-search-scrape-mcp-server"],
        env={"SERPER_API_KEY": str(serp)},
    )

    duck = StdioServerParameters(
        command="uvx",
        args = ["mcp-duckduckgo-search-server"],
    )

    firecrawl = StdioServerParameters(
        command='npx',
        args=["-y", "firecrawl-mcp"],
        env={"FIRECRAWL_API_KEY": str(fire)},
    )

    # Initialize the model client.
    model_client = OpenAIChatCompletionClient(
        model="qwen3-4b-instruct-2507",
        base_url="http://127.0.0.1:1234/v1",
        api_key="sk-xxxx",
        model_info={
        "vision": True,
        "function_calling": True,
        "json_output": False,
        "family": ModelFamily.UNKNOWN,
        "structured_output": False,
    },
    )

    serpy = await get_tools_from_mcp_server(serper)
    ducky = await get_tools_from_mcp_server(duck)
    firey = await get_tools_from_mcp_server(firecrawl)

    # Create the primary agent.
    primary_agent = AssistantAgent(
        "Research_1",
        model_client=model_client,
        system_message="You are a Research ai",
    )

    # Create the critic agent.
    secondary_agent = AssistantAgent(
        "Research_2",
        model_client=model_client,
        system_message="You are a Research ai",
    )

    tertiary = AssistantAgent(
        "critic_agent",
        model_client=model_client,
        system_message="You are a critic AI, your job is to review the work of another AI and provide feedback. If the work meets the required standards, respond with 'APPROVE'. If it does not meet the standards, provide constructive criticism and suggest improvements.",
    )

    # Define a termination condition that stops the task if the critic approves.
    text_termination = TextMentionTermination("APPROVE")

    # Create a team with the primary and critic agents.
    team = RoundRobinGroupChat([primary_agent, secondary_agent], termination_condition=text_termination)

    result = asyncio.run(team.run(task="""Agregate me data on the top hospitals, aged care units, telehealth services in Australia that are in need of medical supplies.
    Search linkedIn, company websites, news articles, and any other relevant sources. """))
    print(result)


