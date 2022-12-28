# hey jarvis 🤖
Tool that allows for voice interaction with OpenAI chat without need to type long, detailed requests. <br>
It's an terminal application that captures audio from microphone and queries chat with transcripted message.

<p align="center">
  <img src="https://github.com/mikkac/hey_jarvis/blob/master/demo/jarvis_demo.gif" alt="animated" />
</p>


---
**Note:** Currently `text-davinci-003` model is used as a chat backend. Unfortunately API for chatGPT is not yet provided by OpenAI.


## Installation

`poetry` is required to install the package from the source code. You can get it [here](https://python-poetry.org/docs/)

Once `poetry` is enabled in the system, to install the project and its dependencies, execute following command:

```bash
$ git clone https://github.com/mikkac/hey_jarvis.git && cd hey_jarvis && poetry install
```

## Configuration

After installation, configuration file has to be provided.
Default location used by the application is `$HOME/.config/hey_jarvis/config.toml`. <br>
One can use the default [configuration file](https://github.com/mikkac/hey_jarvis/blob/master/src/hey_jarvis/config.toml). The only thing that needs to be provided is OpenAI API key that can be generated [here](https://beta.openai.com/account/api-keys).

### Configuration details

Application supports several configuration parameters.
* `voice_api` - Voice recognition API. Currently only `"vosk"` is supported, but it's planned to also enable usage of [Google Speech-To-Text](https://cloud.google.com/speech-to-text) and [Azure Speech to text](https://azure.microsoft.com/en-us/products/cognitive-services/speech-to-text/).
* `language` - language used by `voice_api`. Currently available languages are listed in [Vosk's documentation](https://github.com/alphacep/vosk-api).
* `enable_audio_response` - chat's responses are only written to console by default. However, it's possible to vocalize them by setting this parameter to `true`.
* `device_id` - ID of recording device. It should be commented out or completely removed from configuration if default device shall be used.

## Usage

Once configuration file has been provided, start the application with command:
```bash
$ poetry run hey_jarvis
```
or

```bash
$ poetry shell
$ hey_jarvis
```

## License

This project is licensed under the LICENSE file that [can be found here](https://github.com/mikkac/hey_jarvis/blob/master/LICENSE.md)