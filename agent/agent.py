from swarm import Swarm, Agent
from notion_utils import get_notion_page
from file_utils import read_file, write_file, read_dir
from openai import OpenAI
import os


client = Swarm(OpenAI())

def notion_handoff():
    return notion_agent

def file_handoff():
    return file_agent

notion_agent = Agent(
    name="Notion Agent",
    # model="gemini-1.5-pro",
    instructions="You are a Notion API Agent. You get database items from notion and return them in a way which can be processed by other agents.",
    # parallel_tool_calls=False,
    functions=[get_notion_page, notion_handoff, file_handoff],
)

file_agent = Agent(
    name="File Agent",
    # model="gemini-1.5-pro",
    instructions="You are a File Agent. You Read and Write files and directories",
    # parallel_tool_calls=False,
    functions=[read_file, write_file, read_dir, notion_handoff, file_handoff],
)

with open("instructions.md") as f:
    instructions = f.read()

agent_b = Agent(
    name="Agent B",
    # model="gemini-1.5-pro",
    instructions=f"You are a documentation writer. You are to write documentation in the ./example directory only. Here is the format you should write the documentation in: {instructions}",
    # parallel_tool_calls=False,
    functions=[notion_handoff, file_handoff],
)

databaseid = os.getenv("NOTION_DATABASE_ID")
response = client.run(
    agent=agent_b,
    messages=[{"role": "user", "content": f"Can you turn the notion databaseid {databaseid} into documentation? You should get the notion database and then write it to the ./example directory. You should keep the notion cursor and keep calling it until you get no response. Here are the instructions for the documentation: {instructions}"}],
)

print(response.messages[-1]["content"])