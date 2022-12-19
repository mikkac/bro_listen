#!/usr/bin/env python3

import argparse
import os
import sys

import pyttsx3
from rich.console import Console

from voice import VoiceRecognizer, VoskVoiceRecognizer
from chat import init_chat_api, request_chat_response
from utils import get_args


def main(args: argparse.Namespace) -> None:
    init_chat_api(os.environ.get("OPENAI_API_KEY"))

    voice_recognizer: VoiceRecognizer = VoskVoiceRecognizer(
        language="en-us", device=args.device)

    console = Console()
    with console.status("[bold green]Listening...") as status:
        for prompt in voice_recognizer.listen():
            status.stop()
            console.print(f'[bold green]Prompt:[/bold green]\n{prompt}\n')
            with console.status("[bold blue]Waiting for response...", spinner="point", spinner_style="blue"):
                response = request_chat_response(prompt)

            console.print(f'[bold blue]Response:[/bold blue]\n{response}\n')
            status.start()


if __name__ == "__main__":
    try:
        main(get_args())
    except KeyboardInterrupt:
        print("\nDone")
        sys.exit(0)
    except Exception as e:
        print(type(e).__name__ + ": " + str(e))
        sys.exit(1)
