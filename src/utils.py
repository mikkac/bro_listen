import argparse

import toml
from voice import VoiceAPI


def get_args() -> argparse.Namespace:
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        "-c", "--config", type=str,
        help="path to config file")

    return parser.parse_args()


class Config:
    """
    Parses config file.
    """

    def __init__(self, config_path: str) -> None:
        config_data: dict = toml.load(config_path)
        self.voice_api: VoiceAPI = VoiceAPI(
            config_data.get("voice_api", VoiceAPI.VOSK.value))
        self.language: str = config_data.get("language", "en-us")
        self.openai_api_key: str = config_data.get("openai_api_key", None)
        self.enable_audio_response: bool = config_data.get(
            "enable_audio_response", False)
        self.device_id: str = config_data.get("device_id", None)
