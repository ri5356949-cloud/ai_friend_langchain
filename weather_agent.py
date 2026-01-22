import json
from dotenv import load_dotenv
from openai import OpenAI
import requests
load_dotenv()
client = OpenAI()

# ---------------- TOOL ----------------
def get_weather(city: str):
    print("🔧 Tool Called: get_weather", city)

    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return "Unable to fetch weather data"

     

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Get the current weather for a given city"
    },   
}



# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are a helpful AI assistant that follows a ReAct pattern.

Steps:
1. plan   → decide what to do
2. action → call a tool
3. observe → analyze tool result
4. output → final answer to user

Rules:
- Respond ONLY in valid JSON
- Perform ONE step at a time
- Use the exact JSON format

JSON format:
{
  "step": "plan | action | observe | output",
  "content": "string (for plan/output)",
  "function": "tool name (only for action)",
  "input": "tool input (only for action)",
  "output": "tool result (only for observe)"
}

Available tool:
- get_weather(city: string)
- add(x: number, y: number)
"""

messages = [
    {"role": "system", "content": system_prompt}
]


while True:
    user_query = input("User > ")
    messages.append({"role": "user", "content": user_query})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    assistant_message = response.choices[0].message.content
    print("🤖 Assistant >", assistant_message)

    try:
        assistant_json = json.loads(assistant_message)
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON response")
        break

    step = assistant_json.get("step")

    if step == "plan":
        messages.append({"role": "assistant", "content": assistant_message})

    elif step == "action":
        function_name = assistant_json.get("function")
        function_input = assistant_json.get("input")

        if function_name in available_tools:
            tool_fn = available_tools[function_name]["fn"]
            tool_result = tool_fn(function_input)
        else:
            tool_result = f"Error: Unknown tool '{function_name}'"

        observe_message = {
            "step": "observe",
            "output": tool_result
        }
        messages.append({"role": "assistant", "content": json.dumps(observe_message)})

    elif step == "observe":
        messages.append({"role": "assistant", "content": assistant_message})

    elif step == "output":
        print("✅ Final Output >", assistant_json.get("content"))
        break

    else:
        print("❌ Error: Unknown step")
        break