"""chat module"""
import openai


class Chat:  # pylint: disable=R0903
    """
    Class that interfaces OpenAI API. It initializes the SDK and allows user to send prompts.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the OpenAI SDK with `api_key`.
        One can obtain an API key via https://beta.openai.com/account/api-keys.
        Note: If `api_key` is empty, `AttributeError` will be raised.
        """
        openai.api_key = api_key
        if not openai.api_key:
            raise AttributeError(
                '"openai_api_key" cannot be empty. Please provide a valid API key. '
                "One can be generated via https://beta.openai.com/account/api-keys"
            )

    def ask(self, prompt: str) -> str:
        """
        Sends request to OpenAI API and returns response as string.
        """
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
        response = Chat._strip_all_whitespaces_from(response.choices)[0]
        return response

    @staticmethod
    def _strip_all_whitespaces_from(choices: dict) -> list:
        """
        Removes all whitespace from a dict of choices
        """
        return [choice.text.strip() for choice in choices]
