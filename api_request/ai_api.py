import requests
from utility.setting import Setting
import json

config = Setting()
config.setting_var()

def build_payload_prompt(existing_payload=None, prompt=None, operating_system="Windows"):
    return (
        "You are a penetration testing assistant.\n"
        "Your task is to return a Python payload suitable for use with `exec()`.\n\n"
        f"{'Modify the following payload:\n' + existing_payload + '\n' if existing_payload else ''}"
        f"{'Use this prompt for guidance:\n' + prompt + '\n' if prompt else ''}"
        f"{'Generate a random useful payload if no prompt or base is provided.' if not existing_payload and not prompt else ''}"
        f"Operating System: {operating_system}\n\n"
        "provide multiple lines of code if necessary, give multiple commands if needed, and give multiple examples(more than 6).\n"
        "do not use ; or any other separator in the payload.\n"
        "The payload should be a valid Python code that can be executed with `exec()`.\n"
        "The payload should not contain any comments or explanations.\n"
        "The payload should be suitable for a penetration testing scenario.\n"
        "The payload should be concise and to the point.\n"
    )

def ai_response(existing_payload=None, prompt=None):
    content = build_payload_prompt(existing_payload, prompt)

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config.API_KEY_AI}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://example.com",  # Optional
                "X-Title": "PentestTool",               # Optional
            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [
                    {"role": "user", "content": content}
                ]
            })
        )

        data = response.json()

        # Pretty-print response (for debug)
        # print("[RAW RESPONSE]")
        # print(json.dumps(data, indent=4))

        # Print only the AI payload result
        print("\n[AI PAYLOAD RESPONSE]")
        print(data["choices"][0]["message"]["content"])

    except Exception as e:
        print(f"Error occurred: {e}")

# Examples:
ai_response(existing_payload="", prompt="Modify the payload to use a different command.")
print('--' * 50)
ai_response(prompt="Create a payload that uploads a file to a remote server.")
print('--' * 50)
ai_response()  # Random payload
