from arin_openai.client_openai import ClientOpenai

messages = []
messages.append(
    {"role": "system", "content": "You are a intelligent assistant."},
)
messages.append(
    {"role": "user", "content": "this is a test"},
)

account_id = "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/arin-openai-canada-east-group/providers/Microsoft.CognitiveServices/accounts/arin-openai-canada-east"
engine_name = "gpt-35-turbo"
client = ClientOpenai.from_account_id_azure(account_id, engine_name)

# call_dict["temperature"] = 0.7


chat = client.chat_completion_messages(messages, temperature=0.7, max_tokens=150)
reply = chat["choices"][0]["message"]["content"]
print(f"ChatGPT: {reply}")
