import asyncio
import json
import os
import re
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

def load_mcp_config(path="config.json"):
    
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    def substitute(match):
        var = match.group(1)
        value = os.environ.get(var)
        if value is None:
            raise RuntimeError(f"config.json references ${{{var}}}, but it isn't set in your .env")
        return value

    resolved = re.sub(r"\$\{([A-Z0-9_]+)\}", substitute, raw)
    return json.loads(resolved).get("mcpServers", {})

class MCPManager:

    def __init__(self):
        self.stack = AsyncExitStack()
        self.openai_tools = []          
        self.tool_to_session = {}       

    async def connect_all(self, servers: dict):
        for name, cfg in servers.items():
            try:
                read, write, _ = await self.stack.enter_async_context(
                    streamablehttp_client(cfg["url"], headers=cfg.get("headers"))
                )
                session = await self.stack.enter_async_context(ClientSession(read, write))
                await session.initialize()

                tools = await session.list_tools()
                for tool in tools.tools:
                    self.tool_to_session[tool.name] = session
                    self.openai_tools.append({
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema,
                        },
                    })
                print(f"[System Log] -> Connected MCP '{name}': {len(tools.tools)} tools loaded.")
            except Exception as e:
                print(f"[System Warning] -> Failed to connect to MCP '{name}': {e}")

    async def call_tool(self, name: str, args: dict) -> str:
        result = await self.tool_to_session[name].call_tool(name, args)
        return result.content[0].text if result.content else ""

    async def aclose(self):
        await self.stack.aclose()