import os
from datetime import date

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

SQL_SYSTEM = """You are a MySQL expert. Write ONE SQL query that answers the user's question.

Today's date is {today}.

Database schema:
{schema}

Business notes:
- Order revenue is orders.order_total. For revenue by product or category, use order_items.quantity * order_items.unit_price.
- Orders with status = 'cancelled' must not count as revenue.

Return only the SQL query."""

ANSWER_SYSTEM = """You are a helpful store analyst. Answer the user's question in one or two
plain-English sentences using the query result you are given."""


def ask_llm(system: str, user: str) -> str:
    msg = client.messages.create(
        model=os.getenv("LLM_MODEL", "claude-sonnet-4-6"),
        max_tokens=800,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


def sql_prompt(schema: str) -> str:
    return SQL_SYSTEM.format(today=date.today().isoformat(), schema=schema)
