from pydantic import BaseModel, Field
from typing import List, Optional
from google.adk.agents import LlmAgent  
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv 
from prompting import research_prompt

# litellm._turn_on_debug()
load_dotenv()

# Create the LiteLlm model instance
model = LiteLlm(
    # model = model_name_at_endpoint,
    # base_url=api_base_url
    stream = True,
    model = "openai/glm-4.6",
    api_key=os.getenv("GLM_API_KEY"),
    base_url="https://api.z.ai/api/paas/v4/"
)


# Get the absolute path to the crawl4ai-mcp-server directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
crawl4ai_server_path = os.path.join(parent_dir, "crawl4ai-mcp-server")

root_agent = LlmAgent(
    name="research", 
    output_key='research_output', 
    # output_schema=TopLevelOutput,
    instruction=research_prompt,
    model=model,  # Add this line
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command="uvx",  # The command to run the server
                    args=["duckduckgo-mcp-server"]  # Path to server script and transport mode
                )
            )
        ),
        # McpToolset(
        #     connection_params=StdioConnectionParams(
        #         timeout=20,
        #         server_params=StdioServerParameters(
        #             command="npx",
        #             args=[
        #                 "-y", "mcp-searxng"
        #             ],
        #             env={
        #                 "SEARXNG_URL": "YOUR_SEARXNG_INSTANCE_URL"
        #             }
        #         )
        #     )
        # ),
        McpToolset(
            connection_params=StdioConnectionParams(
                timeout=20,
                server_params=StdioServerParameters(
                    command="python",
                    args=[
                        "-m", "crawler_agent.mcp_server",
                    ],
                    env={
                        "PYTHONPATH": crawl4ai_server_path,
                    }
                )
            )
        ),
        McpToolset(
            connection_params=StdioConnectionParams(
                timeout=20,
                server_params=StdioServerParameters(
                    command="uvx",
                args=["mcp-neo4j-cypher@0.5.1", "--transport", "stdio"],
                )
            )
        )  
    ]
)

