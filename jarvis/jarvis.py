#!/usr/bin/env python3

import argparse
import json
import queue
import sys
import sounddevice as sd
import openai
import os
import pyttsx3

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-a", "--audio", action='store_true',
    help="Enable audio response")
args = parser.parse_args(remaining)

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    print("To use copilot please set the OPENAI_API_KEY environment variable")
    print("You can get an API key from https://beta.openai.com/account/api-keys")
    print("To set the environment variable, run:")
    print("export OPENAI_API_KEY=<your key>")
    sys.exit(1)
    
def chat_request(prompt):
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
    response = strip_all_whitespaces_from(response.choices)[0]
    return response

def strip_all_whitespaces_from(choices):
    return [choice.text.strip() for choice in choices]

try:
    audio = args.audio
    device_info = sd.query_devices(args.device, "input")
    samplerate = int(device_info["default_samplerate"])
    model = Model(lang="en-us")

    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, samplerate)
        print("ok, please give me the command:")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                prompt = json.loads(rec.Result()).get("text", None)
                if prompt:
                    print(prompt)
                    print("cool, here is chatgpt response:")
                    response = chat_request(prompt)
                    print(response)
                    if audio:
                        pyttsx3.speak(response)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))