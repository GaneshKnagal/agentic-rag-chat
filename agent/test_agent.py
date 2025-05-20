import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio
from agent.llm_agent import agent_chat

if __name__ == "__main__":
    query = "executive orders about security"
    result = asyncio.run(agent_chat(query))
    print("\n🤖 Agent Reply:\n", result)
