"""voice module"""
import json
import queue
import sys
from abc import abstractmethod
from enum import Enum
from typing import Any, Generator, Union

import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel


class VoiceAPI(Enum):
    """
    Available voice APIs.
    Note: Currently only VOSK is supported.
    """

    VOSK = "vosk"
    GOOGLE = "google"  # currently not supported
    AZURE = "azure"  # currently not supported


class VoiceRecognizer:  # pylint: disable=R0903
    """
    Interface for voice recognition functionality.
    """

    @abstractmethod
    def listen(self) -> Generator[str, None, None]:
        """
        Listen for voice prompts, transcripts them and returns for further processing.
        """


class VoskVoiceRecognizer(VoiceRecognizer):
    """
    Recognizes voice using VOSK SDK
    """

    data_queue: queue.Queue[Any] = queue.Queue()

    def __init__(self, language: str = "en-us", device: Union[str, int] = None):
        device_info: dict = sd.query_devices(device, "input")
        self.device: Union[str, int] = device
        self.samplerate: int = int(device_info["default_samplerate"])

        SetLogLevel(-1)
        self.model: Model = Model(lang=language)

    def listen(self) -> Generator[str, None, None]:
        """
        See `VoiceRecognizer.listen`
        Note: This method is blocking
        """
        with sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,
            device=self.device,
            dtype="int16",
            channels=1,
            callback=VoskVoiceRecognizer.callback,
        ):
            rec = KaldiRecognizer(self.model, self.samplerate)
            while True:
                data = self.data_queue.get()
                if rec.AcceptWaveform(data):
                    prompt = json.loads(rec.Result()).get("text", None)
                    if prompt:
                        yield prompt

    @staticmethod
    def callback(indata, _1, _2, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        VoskVoiceRecognizer.data_queue.put(bytes(indata))
