"""Command-line interface for Google Speech-to-Text."""

import argparse
import json
import sys
from pathlib import Path

from .client import GoogleSpeechToText


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        prog="gstt",
        description="Google Speech-to-Text - Transcribe audio files to text",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Audio file to transcribe (wav, mp3, ogg, flac, etc.)",
    )
    parser.add_argument(
        "-l", "--language",
        default="cs-CZ",
        help="Language code (default: cs-CZ). Examples: en-US, de-DE, sk-SK",
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "-c", "--confidence",
        action="store_true",
        help="Show confidence score",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    try:
        if args.verbose:
            print(f"Transcribing: {args.file}", file=sys.stderr)
            print(f"Language: {args.language}", file=sys.stderr)

        client = GoogleSpeechToText(language=args.language)
        result = client.transcribe_file(args.file)

        if args.json:
            output = {
                "transcript": result.transcript,
                "confidence": result.confidence,
                "language": args.language,
                "file": str(args.file),
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        elif args.confidence:
            print(f"{result.transcript} [{result.confidence:.2%}]")
        else:
            print(result.transcript)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
