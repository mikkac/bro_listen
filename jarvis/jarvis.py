#!/usr/bin/env python3

import argparse
import os
import sys

from colored import fg, attr
import pyttsx3

from voice import VoiceRecognizer, VoskVoiceRecognizer
from chat import init_chat_api, request_chat_response
from utils import get_args


def main(args: argparse.Namespace) -> None:
    init_chat_api(os.environ.get("OPENAI_API_KEY"))

    voice_recognizer: VoiceRecognizer = VoskVoiceRecognizer(
        language="en-us", device=args.device)

    print('-' * 80)
    print(f'{attr("bold")}Waiting for command.. {attr("reset")}')
    print('-' * 80)
    for prompt in voice_recognizer.listen():
        print(f'{fg("green")}{attr("bold")}Prompt:{attr("reset")}\n{prompt}\n')

        response = request_chat_response(prompt)

        print(f'{fg("blue")}{attr("bold")}Response:{attr("reset")}\n{response}\n')

        print('-' * 80)
        print(f'{attr("bold")}Waiting for command...{attr("reset")}')
        print('-' * 80)
        # if audio:
        # pyttsx3.speak(response)


if __name__ == "__main__":
    try:
        main(get_args())
    except KeyboardInterrupt:
        print("\nDone")
        sys.exit(0)
    except Exception as e:
        print(type(e).__name__ + ": " + str(e))
        sys.exit(1)
