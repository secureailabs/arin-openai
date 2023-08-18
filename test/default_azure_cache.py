import json

from arin_core_azure.env_tools import get_string_from_env

from arin_openai.client_openai import ClientOpenai

messages = []
messages.append(
    {"role": "system", "content": "You are a intelligent assistant."},
)
messages.append(
    {"role": "user", "content": "this is a test"},
)
engine_name = get_string_from_env("OPENAI_ENGINE_NAME")
client = ClientOpenai.from_default_azure(engine_name, do_cache=True)
print(client.engine_name)
chat = client.chat_completion_messages(messages)
reply = chat["choices"][0]["message"]["content"]
print(f"ChatGPT: {reply}")
