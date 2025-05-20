import openai
import json
import re
import datetime
from agent.tools import search_documents
from agent.tool_schema import tool_schema

# Point to Ollama
openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"  # Required dummy

# 🔧 Fixes datetime serialization issues
def clean_dates_for_json(records):
    for record in records:
        for key, value in record.items():
            if isinstance(value, (datetime.date, datetime.datetime)):
                record[key] = str(value)
    return records

async def agent_chat(user_query: str):
    print("\n📨 User Query:", user_query)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a strict and factual assistant. You MUST use the available tools to answer questions that involve factual data, recent updates, or specific government documents. "
                "Never rely on your own memory or training data for such queries. If a user asks about energy policies, agency documents, regulations, reports, or updates, always call the appropriate tool. "
                "Only respond directly if the question is purely general or conversational. Otherwise, invoke the tool first."
             
            )
        },
        {"role": "user", "content": user_query}
    ]

    print("🧠 Sending initial message to LLM...")
    response = await openai.ChatCompletion.acreate(
        model="mistral",
        messages=messages,
        tools=tool_schema,
        tool_choice="auto"
    )

    message = response["choices"][0]["message"]
    print("📥 Initial LLM response:\n", json.dumps(message, indent=2))

    # ✅ CASE 1: Tool call received
    if message.get("tool_calls"):
        print("✅ Tool call detected!")

        for tool_call in message["tool_calls"]:
            fn_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])

            print(f"🔧 Calling tool: {fn_name} with arguments: {args}")
            if fn_name == "search_documents":
                results = await search_documents(**args)

                if not results:
                    print("❗ WARNING: Tool result was empty — no matching data found in the database.")
                    return "⚠️ No relevant documents were found in the database for your request. Please try with different keywords or agency."

                # 🔄 Fix date serialization
                results = clean_dates_for_json(results)

                print("📦 Tool result:\n", json.dumps(results, indent=2))

                follow_up = [
                    *messages,
                    message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": fn_name,
                        "content": json.dumps(results)
                    }
                ]

                print("🔁 Sending tool result back to LLM...")
                final_response = await openai.ChatCompletion.acreate(
                    model="mistral",
                    messages=follow_up
                )

                print("✅ Final LLM answer:\n", final_response["choices"][0]["message"]["content"])
                return final_response["choices"][0]["message"]["content"]

    # ✅ CASE 2: No tool call — fallback
    print("⚠️ No tool call detected. Returning message directly...")
    return message["content"]
