import os

def load_ignores(ignore_path: str) -> list[str]:
    if not os.path.exists(ignore_path):
        return []

    patterns: list[str] = []
    with open(ignore_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            patterns.append(line)

    return patterns
