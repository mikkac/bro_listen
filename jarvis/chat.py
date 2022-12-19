import sys
import os
from typing import Optional

import openai


def init_chat_api(api_key: Optional[str]) -> None:
    openai.api_key = api_key
    if not openai.api_key:
        raise AttributeError(
            "\"openai_api_key\" cannot be empty. Please provide a valid API key. One can be generated via https://beta.openai.com/account/api-keys")


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
