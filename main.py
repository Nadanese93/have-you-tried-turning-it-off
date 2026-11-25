#!/usr/bin/env python3
"""Have You Tried Turning It Off? — one funny tech-support line.

Writes the entry to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic: no network, no randomness, no clock.
"""

import os
import sys

ENTRY = (
    "Your files are safe in the cloud \u2014 which is great, "
    "because I have absolutely no idea where the cloud is either."
)


class LengthError(ValueError):
    """Entry is not 1-199 characters."""


class BlankError(ValueError):
    """Entry is empty or only whitespace."""


class MultiLineError(ValueError):
    """Entry contains more than one line."""


def validate(text: str) -> bytes:
    """Validate one entry line; return its UTF-8 bytes.

    Each gate failure raises a distinct exception type so a bad
    entry can never be mistaken for a different kind of bad entry.
    """
    if not 1 <= len(text) <= 199:
        raise LengthError(f"entry must be 1-199 characters, got {len(text)}")
    if not text.strip():
        raise BlankError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")
    return text.encode("utf-8")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise RuntimeError("MAKEFUN_OUTPUT_DIR is not set")
    encoded = validate(ENTRY)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(encoded)
    # Read-back verification: the bytes on disk must match exactly.
    with open(path, "rb") as f:
        written = f.read()
    if written != encoded:
        raise RuntimeError("read-back mismatch: entry.txt does not match entry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
