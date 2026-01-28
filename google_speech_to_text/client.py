"""Google Speech-to-Text client using free Chromium API."""

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests

# Chromium API key (public, used by Chrome browser)
API_KEY = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
API_URL = "https://www.google.com/speech-api/v2/recognize"


@dataclass
class TranscriptionResult:
    """Result of speech-to-text transcription."""

    transcript: str
    confidence: float
    raw_response: dict

    def __str__(self) -> str:
        return self.transcript


class GoogleSpeechToText:
    """Client for Google Speech-to-Text API."""

    def __init__(self, language: str = "cs-CZ", api_key: Optional[str] = None):
        """
        Initialize the client.

        Args:
            language: Language code (e.g., 'cs-CZ', 'en-US', 'de-DE')
            api_key: Optional custom API key. Uses Chromium key by default.
        """
        self.language = language
        self.api_key = api_key or API_KEY

    def transcribe_raw(self, audio_data: bytes, sample_rate: int = 16000) -> TranscriptionResult:
        """
        Transcribe raw PCM audio data (Linear16 format).

        Args:
            audio_data: Raw PCM audio bytes (16-bit signed, mono)
            sample_rate: Sample rate in Hz (default: 16000)

        Returns:
            TranscriptionResult with transcript and confidence
        """
        url = f"{API_URL}?output=json&lang={self.language}&key={self.api_key}"
        headers = {"Content-Type": f"audio/l16; rate={sample_rate}"}

        response = requests.post(url, headers=headers, data=audio_data)
        response.raise_for_status()

        return self._parse_response(response.text)

    def transcribe_file(self, file_path: str | Path) -> TranscriptionResult:
        """
        Transcribe audio file (any format supported by ffmpeg).

        Args:
            file_path: Path to audio file (wav, mp3, ogg, flac, etc.)

        Returns:
            TranscriptionResult with transcript and confidence
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # Convert to raw PCM using ffmpeg
        raw_audio = self._convert_to_raw(file_path)
        return self.transcribe_raw(raw_audio)

    def _convert_to_raw(self, file_path: Path, sample_rate: int = 16000) -> bytes:
        """Convert audio file to raw PCM format using ffmpeg."""
        with tempfile.NamedTemporaryFile(suffix=".raw", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            cmd = [
                "ffmpeg",
                "-i", str(file_path),
                "-ar", str(sample_rate),
                "-ac", "1",
                "-f", "s16le",
                "-y",
                tmp_path,
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                check=True,
            )
            with open(tmp_path, "rb") as f:
                return f.read()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ffmpeg conversion failed: {e.stderr.decode()}") from e
        except FileNotFoundError:
            raise RuntimeError(
                "ffmpeg not found. Please install ffmpeg: "
                "sudo apt install ffmpeg (Linux) or brew install ffmpeg (macOS)"
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def _parse_response(self, response_text: str) -> TranscriptionResult:
        """Parse Google Speech API response."""
        # Response contains multiple JSON objects, one per line
        lines = response_text.strip().split("\n")

        for line in reversed(lines):
            if not line:
                continue
            try:
                data = json.loads(line)
                if "result" in data and data["result"]:
                    result = data["result"][0]
                    if "alternative" in result and result["alternative"]:
                        alt = result["alternative"][0]
                        return TranscriptionResult(
                            transcript=alt.get("transcript", ""),
                            confidence=alt.get("confidence", 0.0),
                            raw_response=data,
                        )
            except json.JSONDecodeError:
                continue

        return TranscriptionResult(
            transcript="",
            confidence=0.0,
            raw_response={"error": "No transcription result"},
        )


def transcribe(
    file_path: str | Path,
    language: str = "cs-CZ",
) -> TranscriptionResult:
    """
    Convenience function to transcribe an audio file.

    Args:
        file_path: Path to audio file
        language: Language code (default: 'cs-CZ')

    Returns:
        TranscriptionResult with transcript and confidence

    Example:
        >>> result = transcribe("recording.wav", language="en-US")
        >>> print(result.transcript)
        "Hello world"
        >>> print(result.confidence)
        0.95
    """
    client = GoogleSpeechToText(language=language)
    return client.transcribe_file(file_path)
