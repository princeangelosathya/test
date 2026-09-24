"""MCP server: gives the chat API two tools, get_schema and run_sql."""
import json
import os

import pymysql
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("ecommerce-db")


def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        cursorclass=pymysql.cursors.DictCursor,
    )


@mcp.tool()
def get_schema() -> str:
    """Return every table and its columns for the ecommerce database."""
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT table_name AS t, column_name AS c, data_type AS d "
            "FROM information_schema.columns WHERE table_schema = DATABASE() "
            "ORDER BY table_name, ordinal_position"
        )
        rows = cur.fetchall()
    conn.close()
    tables = {}
    for r in rows:
        tables.setdefault(r["t"], []).append(f'{r["c"]} ({r["d"]})')
    return "\n".join(f"{t}: {', '.join(cols)}" for t, cols in tables.items())


@mcp.tool()
def run_sql(query: str) -> str:
    """Run a SQL query and return the rows as JSON."""
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    conn.close()
    return json.dumps(rows, default=str)


if __name__ == "__main__":
    mcp.run()
