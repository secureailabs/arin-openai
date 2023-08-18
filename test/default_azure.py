import json

from arin_openai.client_openai import ClientOpenai

# openai.api_key = os.environ["OPENAI_API_KEY"]
messages = []
messages.append(
    {"role": "system", "content": "You are a intelligent assistant."},
)
messages.append(
    {"role": "user", "content": "this is a test"},
)


client = ClientOpenai.from_default_azure("gpt-35-turbo")
print(client.engine_name)
chat = client.chat_completion_messages(messages)
reply = chat["choices"][0]["message"]["content"]
print(f"ChatGPT: {reply}")
