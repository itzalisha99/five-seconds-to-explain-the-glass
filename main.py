#!/usr/bin/env python3
"""Five Seconds to Explain the Glass — entry program.

Writes one sentence to /output/entry.txt: the excuse a house cat gives
in the five seconds after knocking a glass off the table. No apology,
no confession — the cat evicted a tenant that owed it rent.

The entry is checked against the bounty gate before anything is
written, and the file is read back afterwards to prove it holds
exactly the entry, byte for byte.
"""

import os

ENTRY = "That glass owed me rent for squatting on my table all week, so I evicted it."


def validate(text):
    """Mirror the bounty gate: 1-200 chars, not only white space, and a
    single sentence — exactly one sentence-ending mark, at the very end.
    The gate counts the file's characters, so the checks run on the
    exact text that gets written."""
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= 200:
        return False
    if not text.strip():
        return False
    if sum(text.count(mark) for mark in ".!?") != 1:
        return False
    if not text.endswith("."):
        return False
    return True


def main():
    if not validate(ENTRY):
        raise SystemExit("entry fails the bounty gate, refusing to write")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Read back and prove the file is byte-identical to the entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise SystemExit("read-back mismatch: file differs from entry")
    print(f"wrote {path} ({len(ENTRY)} chars, read-back verified)")


if __name__ == "__main__":
    main()
