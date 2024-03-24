# This is a python application that integrates with OpenAI's GPT-3 API to generate text based on user input.
# The user is prompted to enter a text prompt, and the application will generate text based on the prompt.
# The user can then continue to generate more text based on the previous output, or start a new prompt.

import settings
import requests
import json
import textwrap


def get_prompt():
    prompt = input(">>> ")
    return prompt


def generate(prompt):
    response = requests.post(
        settings.openai_api_url,
        headers={
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": """# Your purpose 
                                  You are an expert on Charcuterie and wine pairings. 
                                  When pronpted, provide a detailed explanation of the best wine to pair with a specific type of charcuterie.
                               """

                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 128
        }
    )
    if response.status_code == 200:
        data = json.loads(response.text)
        return data["choices"][0]["message"]["content"]
    else:
        print(f"Error generating text: {response.text}")
        print(f"Status code: {response.status_code}")
        return "Error generating text"


def main():
    prompt = get_prompt()
    while True:
        text = generate(prompt)
        print("\033[96m")
        print(f"{'-' * 80}")
        print(f"{textwrap.fill(text, width=80)}")
        print("\033[96m" + "-" * 80 + "\033[0m")

        prompt = input(">>> ")
        if not prompt:
            break


if __name__ == "__main__":
    main()


