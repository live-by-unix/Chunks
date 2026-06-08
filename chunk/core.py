import os
import re
import sys
import shutil

_chunk_size_bytes = 1024 * 1024

_UNITS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024**2,
    "GB": 1024**3,
    "TB": 1024**4,
    "KIB": 1024,
    "MIB": 1024**2,
    "GIB": 1024**3,
    "TIB": 1024**4,
}

def _parse_human_size(s: str) -> int:
    s = s.strip().upper().replace(" ", "")
    match = re.fullmatch(r"(\d+)([A-Z]+)", s)
    if not match:
        raise ValueError(f"Invalid chunk size format: {s}")
    number, unit = match.groups()
    if unit not in _UNITS:
        raise ValueError(f"Unknown size unit: {unit}")
    return int(number) * _UNITS[unit]

def set_chunk_size(value: str) -> None:
    global _chunk_size_bytes
    _chunk_size_bytes = _parse_human_size(value)

def _progress_bar(prefix: str, current: int, total: int) -> None:
    width = shutil.get_terminal_size((40, 20)).columns - len(prefix) - 15
    width = max(10, width)
    ratio = current / total if total else 1
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(ratio * 100)
    sys.stdout.write(f"\r\033[96m{prefix} {bar}  <-- {percent}%\033[0m")
    sys.stdout.flush()

def chunk(file_path: str) -> int:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    total_size = os.path.getsize(file_path)
    written = 0
    index = 1
    with open(file_path, "rb") as f:
        while True:
            data = f.read(_chunk_size_bytes)
            if not data:
                break
            out_name = f"chunk{index}of{name}{ext}"
            out_path = os.path.join(directory, out_name)
            with open(out_path, "wb") as out:
                out.write(data)
            written += len(data)
            _progress_bar(f"Chunking {filename}", written, total_size)
            index += 1
    sys.stdout.write("\n")
    return index - 1
