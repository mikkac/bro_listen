#!/usr/bin/env python3

from abc import abstractmethod
import json
import queue
import sys
import sounddevice as sd
from typing import Union
from vosk import Model, KaldiRecognizer, SetLogLevel


class VoiceRecognizer:
    @abstractmethod
    def listen(self) -> None:
        pass


class VoskVoiceRecognizer(VoiceRecognizer):
    data_queue: queue.Queue() = queue.Queue()

    def __init__(self, language: str = "en-us", device: Union[str, int] = None):
        device_info: dict = sd.query_devices(device, "input")
        self.device: Union[str, int] = device
        self.samplerate: int = int(device_info["default_samplerate"])
        
        SetLogLevel(-1)
        self.model: Model = Model(lang=language)

    def listen(self):
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=self.device,
                               dtype="int16", channels=1, callback=VoskVoiceRecognizer.callback):
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
