import os

from arin_openai.client_openai import ClientOpenai

messages = []
messages.append(
    {"role": "system", "content": "You are a intelligent assistant."},
)
messages.append(
    {"role": "user", "content": "this is a test"},
)

client = ClientOpenai.from_default_openai()
call_dict = {}
call_dict["api_base"] = client.api_base
call_dict["api_key"] = client.api_key
call_dict["api_type"] = client.api_type
call_dict["messages"] = messages
call_dict["model"] = "gpt-3.5-turbo"
call_dict["temperature"] = 0.7


chat = client.chat_completion(call_dict)
reply = chat["choices"][0]["message"]["content"]
print(f"ChatGPT: {reply}")
