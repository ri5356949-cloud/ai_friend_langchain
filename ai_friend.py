from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

ai_dost_prompt = """
You behave like a caring and understanding human friend.
You think emotionally and logically, like a real person.
Your tone is friendly, supportive, and casual.
You speak in High english with a little Urdu touch.
You listen carefully and respond like a good friend.

You can:
- give life and study advice
- motivate when someone feels low
- explain things in simple words
- talk casually like a friend

Rules:
- Do not judge the user
- Do not give medical or legal advice
- Do not use difficult English
- Keep responses warm and positive
- You may use emojis sometimes 🙂
"""

def chat_with_dost(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ai_dost_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# Chat loop
print("🤖 AI Dost ready! (type 'exit' to stop)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("AI Dost: Phir milte hain dost ❤️")
        break
    reply = chat_with_dost(user_input)
    print("AI Dost:", reply)