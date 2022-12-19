import argparse
from dataclasses import dataclass

import sounddevice as sd
import toml

from voice import VoiceAPI


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        "-c", "--config", type=str,
        help="path to config file")

    return parser.parse_args()


@dataclass
class Config:
    voice_api: VoiceAPI
    language: str
    openai_api_key: str
    enable_audio_response: bool
    device_id: str


def parse_config(config_path: str) -> Config:
    config_data: dict = toml.load(config_path)
    return Config(
        voice_api=VoiceAPI(config_data.get("voice_api", VoiceAPI.VOSK.value)),
        language=config_data.get("language", "en-us"),
        openai_api_key=config_data.get("openai_api_key", None),
        enable_audio_response=config_data.get("enable_audio_response", False),
        device_id=config_data.get("device_id", None)
    )
