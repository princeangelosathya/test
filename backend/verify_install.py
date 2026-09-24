"""Confirms everything is installed. Run automatically at the end of setup."""
import asyncio
import importlib.util
import os
import sys

MODS = ["flask", "pymysql", "cryptography", "dotenv", "anthropic", "mcp"]
missing = [m for m in MODS if importlib.util.find_spec(m) is None]
if missing:
    print("MISSING PACKAGES:", ", ".join(missing))
    sys.exit(1)

from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

here = os.path.dirname(os.path.abspath(__file__))


async def main():
    params = StdioServerParameters(command=sys.executable, args=[os.path.join(here, "mcp_server.py")])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = [t.name for t in (await s.list_tools()).tools]
            assert "get_schema" in tools and "run_sql" in tools, tools


asyncio.run(main())
print("Backend install OK (packages present, MCP server starts)")
