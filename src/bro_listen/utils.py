"""utils module"""
import argparse
import os
from pathlib import Path

import toml

from bro_listen.voice import VoiceAPI


def get_config_path() -> Path:
    """
    Finds configuration file path.
    If file under path "$HOME/.config/bro_listen/config.toml" is not found,
    function tries second possible location which is the package installation directory.
    If also this file cannot be found, `AttributeError` is raised.
    """
    default_config_file: Path = Path(os.path.dirname(__file__)) / "config.toml"
    user_config_file: Path = Path.home() / ".config" / "bro_listen" / "config.toml"
    if not user_config_file.exists():
        if not default_config_file.exists():
            raise AttributeError(
                f"Cannot find config file. Neither {user_config_file} "
                "nor {default_config_file} exists."
            )
        return default_config_file
    return user_config_file


def get_args() -> argparse.Namespace:
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument("-c", "--config", type=str, help="path to config file")

    return parser.parse_args()


class Config:  # pylint: disable=R0903
    """
    Parses config file.
    """

    def __init__(self, config_path: str) -> None:
        config_data: dict = toml.load(config_path)
        self.voice_api: VoiceAPI = VoiceAPI(
            config_data.get("voice_api", VoiceAPI.VOSK.value)
        )
        self.language: str = config_data.get("language", "en-us")
        self.openai_api_key: str = config_data.get("openai_api_key", None)
        self.enable_audio_response: bool = config_data.get(
            "enable_audio_response", False
        )
        self.device_id: str = config_data.get("device_id", None)
