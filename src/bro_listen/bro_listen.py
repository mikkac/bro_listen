#!/usr/bin/env python3
"""main module"""

import argparse
import sys

import pyttsx3
from rich.console import Console
from rich.panel import Panel

from bro_listen.chat import Chat
from bro_listen.utils import Config, get_args, get_config_path
from bro_listen.voice import (
    VoiceAPI,
    VoiceRecognizer,
    VoskVoiceRecognizer,
)


def main(config: Config, console: Console) -> None:  # pylint: disable=W0621
    """
    Main function that orchestrates chatting with OpenAI based on prompts given with oral prompts.
    """
    chat: Chat = Chat(config.openai_api_key)

    if config.voice_api == VoiceAPI.VOSK:
        voice_recognizer: VoiceRecognizer = VoskVoiceRecognizer(
            language=config.language, device=config.device_id
        )
    else:
        raise AttributeError(
            '"voice_api" different than "vosk" is currently not supported :('
        )

    if config.enable_audio_response:
        engine = pyttsx3.init()

    with console.status("[bold green]Listening...") as status:
        for prompt in voice_recognizer.listen():
            status.stop()
            console.print(Panel(f"[bold green]You:[/bold green] {prompt}"))
            with console.status(
                "[bold blue]Waiting for response...",
                spinner="point",
                spinner_style="blue",
            ):
                response = chat.ask(prompt)
                console.print(Panel(f"[bold blue]bro:[/bold blue] {response}"))
            if config.enable_audio_response:
                with console.status(
                    "[bold yellow]Speaking 🔊", spinner="point", spinner_style="yellow"
                ):
                    engine.say(response)
                    engine.runAndWait()

            status.start()


def run() -> None:
    """
    Runs bro_listen tool.
    """
    console: Console = Console()
    try:
        cmd_args: argparse.Namespace = get_args()
        if not cmd_args.config:
            cmd_args.config = get_config_path()
        config: Config = Config(cmd_args.config)
        main(config, console)
    except KeyboardInterrupt:
        console.print("[bold yellow]Bye![/bold yellow]")
        sys.exit(0)
    except AttributeError as error:
        console.print(f"[bold red]{error}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    run()
