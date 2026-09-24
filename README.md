# Store Chat: Fix It Challenge (90 minutes)

A chat app that answers questions about an online store's database.
The code is complete, but it has bugs. Find them and fix them.

Everything is already installed in this workspace. Do not install anything.

## Start
1. Open `backend/.env` in the editor and fill in the values from your desk card.
2. Open a terminal (Terminal menu, New Terminal) and run: `bash run.sh`
3. Open the **Ports** tab at the bottom, and click the globe icon next to **Chat UI (5173)**.

After you edit a backend file, press Ctrl+C in the terminal and run `bash run.sh` again.
Frontend edits appear automatically.

## How it fits together
React page -> Flask API (`backend/app.py`) -> MCP server (`backend/mcp_server.py`) -> MySQL
The LLM (`backend/llm.py`) writes the SQL and turns the result into a sentence.

## Tips
- Add `/health` to the end of your Chat UI address to test the database connection.
- Read the terminal output and the browser console (F12). The errors tell you where to look.
- Fix one thing at a time and test after each fix.
- Goal: the chat answers store questions correctly and refuses to change data.
