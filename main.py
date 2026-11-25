import os

ENTRY = "My smart fridge judges my midnight snacks, so I eat in the dark like it's a heist."


def check(text):
    """Gate check: 1-140 characters, valid UTF-8, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= 140):
        raise ValueError("entry must be 1 to 140 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")
    return True


def verify_written(path, expected):
    """Re-read the written file and confirm it matches the entry exactly:
    same bytes, no trailing newline, still within the gate."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw.endswith(b"\n"):
        raise ValueError("written file ends with a newline")
    actual = raw.decode("utf-8")
    if actual != expected:
        raise ValueError("written file does not match the entry")
    check(actual)
    return True


def main():
    check(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    verify_written(path, ENTRY)


if __name__ == "__main__":
    main()
