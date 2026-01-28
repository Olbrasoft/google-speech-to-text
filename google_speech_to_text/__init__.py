"""Google Speech-to-Text - Python library for speech recognition using free Chromium API."""

from .client import GoogleSpeechToText, TranscriptionResult, transcribe

__version__ = "0.1.0"
__all__ = ["GoogleSpeechToText", "TranscriptionResult", "transcribe"]
