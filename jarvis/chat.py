import sys
import os
from typing import Optional

import openai


def init_chat_api(api_key: Optional[str]) -> None:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if openai.api_key is None:
        print("To use copilot please set the OPENAI_API_KEY environment variable")
        print("You can get an API key from https://beta.openai.com/account/api-keys")
        print("To set the environment variable, run:")
        print("export OPENAI_API_KEY=<your key>")
        sys.exit(1)


def request_chat_response(prompt: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stop=["`"],
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
    )
    response = _strip_all_whitespaces_from(response.choices)[0]
    return response


def _strip_all_whitespaces_from(choices: dict) -> list:
    return [choice.text.strip() for choice in choices]
