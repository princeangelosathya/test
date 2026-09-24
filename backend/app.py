"""Chat API: question -> (MCP get_schema) -> LLM writes SQL -> (MCP run_sql) -> LLM answers."""
import asyncio
import os
import sys

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
from llm import ANSWER_SYSTEM, ask_llm, sql_prompt  # noqa: E402

app = Flask(__name__)

SERVER = StdioServerParameters(
    command=sys.executable,
    args=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")],
    env=dict(os.environ),
)


async def call_tool(name: str, args: dict) -> str:
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, args)
    text = result.content[0].text
    if result.isError:
        raise RuntimeError(text)
    return text


@app.route("/health")
def health():
    try:
        schema = asyncio.run(call_tool("get_schema", {}))
        return jsonify({"status": "ok", "schema": schema})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data["question"]

        schema = asyncio.run(call_tool("get_schema", {}))
        sql = ask_llm(sql_prompt(schema), question)
        rows = asyncio.run(call_tool("run_sql", {"query": sql}))
        answer = ask_llm(ANSWER_SYSTEM, f"Question: {question}\nQuery result: {rows}")

        return jsonify({"answer": rows, "sql": sql})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
