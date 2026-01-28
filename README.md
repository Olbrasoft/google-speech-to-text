# Google Speech-to-Text

Python library for speech recognition using Google's free Chromium Speech API.

**No API key required!** Uses the same API that powers speech recognition in Chrome browser.

## Features

- Free speech-to-text transcription
- Support for 100+ languages
- Simple Python API and CLI
- Accepts any audio format (via ffmpeg)
- High accuracy (powered by Google)

## Installation

```bash
pip install google-speech-to-text
```

**Requirements:** [ffmpeg](https://ffmpeg.org/) must be installed for audio conversion.

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Quick Start

### Command Line

```bash
# Transcribe audio file (default: Czech)
gstt recording.wav

# Specify language
gstt recording.wav --language en-US

# Output as JSON
gstt recording.wav --json

# Show confidence score
gstt recording.wav --confidence
```

### Python API

```python
from google_speech_to_text import transcribe, GoogleSpeechToText

# Simple usage
result = transcribe("recording.wav", language="cs-CZ")
print(result.transcript)  # "Ahoj, toto je test"
print(result.confidence)  # 0.95

# Using client class
client = GoogleSpeechToText(language="en-US")
result = client.transcribe_file("speech.mp3")
print(result)
```

## Supported Languages

Common language codes:

| Language | Code |
|----------|------|
| Czech | `cs-CZ` |
| English (US) | `en-US` |
| English (UK) | `en-GB` |
| German | `de-DE` |
| Slovak | `sk-SK` |
| Polish | `pl-PL` |
| French | `fr-FR` |
| Spanish | `es-ES` |

See [full list of supported languages](https://cloud.google.com/speech-to-text/docs/languages).

## API Reference

### `transcribe(file_path, language="cs-CZ")`

Convenience function to transcribe an audio file.

**Parameters:**
- `file_path`: Path to audio file (wav, mp3, ogg, flac, etc.)
- `language`: Language code (default: "cs-CZ")

**Returns:** `TranscriptionResult` with `transcript`, `confidence`, and `raw_response`

### `GoogleSpeechToText(language="cs-CZ", api_key=None)`

Client class for more control.

**Methods:**
- `transcribe_file(file_path)` - Transcribe audio file
- `transcribe_raw(audio_data, sample_rate=16000)` - Transcribe raw PCM audio

### `TranscriptionResult`

Dataclass with transcription results:
- `transcript: str` - Transcribed text
- `confidence: float` - Confidence score (0.0 - 1.0)
- `raw_response: dict` - Raw API response

## How It Works

This library uses Google's unofficial Speech API endpoint that powers Chrome's Web Speech API:

```
https://www.google.com/speech-api/v2/recognize
```

### About the API Key

The library uses a Chromium API key (`AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw`) that has been extracted from the Chromium project and is widely used in open-source projects.

**Important facts:**

| | |
|---|---|
| **Origin** | Internal Chromium project key |
| **Intended use** | Chromium development only, NOT for public use |
| **Documentation** | None - Google doesn't officially support this |
| **Quota** | Limited, cannot be increased |

**What Google/Chromium says:**

> *"The 'Google Speech API' is intended for use by Chromium only; it's not for general public use. That is why there is no documentation and no way to get additional quota."*
> — [Chromium Dev Group](https://groups.google.com/a/chromium.org/g/chromium-dev/c/5PrGai_wOZU)

> *"The API key allows you to use them within your own build of Chromium, not for some other application. If you choose to try to use them anyway, you do so at your own risk."*
> — [Chromium API Keys Documentation](https://www.chromium.org/developers/how-tos/api-keys/)

**Summary:** This is a **gray area**. The key works, but using it outside of Chromium technically violates Google's Terms of Service. It may stop working at any time. For production/commercial use, please use [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text).

## Limitations

- Audio files should be under 1 minute for best results
- Rate limiting may apply for high-volume usage
- API key may stop working at any time (unofficial)
- Not recommended for production/commercial use
- Technically violates Google's ToS

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/Olbrasoft/google-speech-to-text).
