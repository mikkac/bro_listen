#!/usr/bin/env python3

import argparse
import sys

import pyttsx3
from rich.console import Console
from rich.panel import Panel

from chat import init_chat_api, request_chat_response
from utils import get_args, Config
from voice import VoiceRecognizer, VoskVoiceRecognizer, VoiceAPI


def main(config: Config, console: Console) -> None:
    init_chat_api(config.openai_api_key)

    if config.voice_api == VoiceAPI.VOSK:
        voice_recognizer: VoiceRecognizer = VoskVoiceRecognizer(
            language=config.language, device=config.device_id)
    else:
        raise AttributeError(
            "\"voice_api\" different than \"vosk\" is currently not supported :(")

    if config.enable_audio_response:
        engine = pyttsx3.init()

    with console.status("[bold green]Listening...") as status:
        for prompt in voice_recognizer.listen():
            status.stop()
            console.print(Panel(f'[bold green]You:[/bold green] {prompt}'))
            with console.status("[bold blue]Waiting for response...", spinner="point", spinner_style="blue"):
                response = request_chat_response(prompt)
                console.print(
                    Panel(f'[bold blue]jarvis:[/bold blue] {response}'))
            if config.enable_audio_response:
                with console.status("[bold yellow]Speaking 🔊", spinner="point", spinner_style="yellow"):
                    engine.say(response)
                    engine.runAndWait()

            status.start()


if __name__ == "__main__":
    console: Console = Console()
    try:
        cmd_args: argparse.Namespace = get_args()
        if not cmd_args.config:
            from pathlib import Path
            cmd_args.config: Path = Path.home() / ".config" / "jarvis.toml"
        config: Config = Config(cmd_args.config)
        main(config, console)
    except KeyboardInterrupt:
        console.print("[bold yellow]Bye![/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]{type(e).__name__}: {e}[/bold red]")
        sys.exit(1)
