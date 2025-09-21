from pathlib import Path

def load_sentences(path: Path) -> list[str]:
    DEFAULT_SENTENCES = ["The quick brown fox jumps over the lazy dog"]

    lines: list[str] = []
    try:
        with path.open(encoding="utf-8") as handle:
            for raw_line in handle:
                stripped = raw_line.strip()
                if stripped:
                    lines.append(stripped)
    except FileNotFoundError:
        return DEFAULT_SENTENCES.copy()

    return lines or DEFAULT_SENTENCES.copy()