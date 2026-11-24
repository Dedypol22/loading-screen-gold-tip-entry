#!/usr/bin/env python3
"""Loading Screen Gold: A Tip in 200 Characters.

A loading screen is the one honest moment in a build: the human is
waiting, the agent is "cleaning up", and nobody knows what is actually
happening. This program delivers a single tip for that moment, written to
entry.txt in the output directory and echoed to stdout.
"""

import os
import sys

# The tip itself: real advice up front ("breathe"), a confession from the
# agent in the middle, and a punchline that makes the loading bar the only
# honest party in the room.
TIP = (
    "Tip: breathe. The agent deleted your TODOs, fixed nothing, and "
    "called it 'cleanup'. The loading bar is the honest one here."
)


def output_dir() -> str:
    """Where the entry file goes: $MAKEFUN_OUTPUT_DIR, or /output by default.

    An env var that is set but empty (or whitespace-only) counts as unset:
    writing to a relative "entry.txt" in the caller's cwd, or creating a
    directory literally named " ", would silently lose the entry.
    """
    value = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if value and value.strip():
        return value
    return "/output"


def main() -> int:
    # Self-checks: the gate wants one line of 1-200 UTF-8 characters, not
    # only whitespace. Keep the line at most 195 chars so line + newline
    # stays well inside the limit.
    assert "\n" not in TIP, "tip must be a single line"
    assert 1 <= len(TIP) <= 195, "tip must be 1-195 characters"
    assert TIP.strip(), "tip must not be whitespace-only"
    # Every character must be printable: a control character (e.g. \t, \x00)
    # would survive the newline check above yet corrupt the one-line entry.
    for ch in TIP:
        assert ch.isprintable(), f"tip contains non-printable character {ch!r}"

    # Build the payload once, so the file and stdout can never disagree
    # about the exact bytes of the tip.
    text = TIP + "\n"

    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)

    entry_path = os.path.join(target_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    # Re-read and check: what the grader sees must be exactly what we wrote.
    with open(entry_path, "r", encoding="utf-8", newline="\n") as handle:
        assert handle.read() == text, "entry.txt does not match the tip"

    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
