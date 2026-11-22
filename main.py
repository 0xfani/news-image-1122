# Sunday 22 November 2026 in one picture: the entry for make.fun's news-image-20261122 bounty.
# The page is already drawn (entry.png in this folder); the sandbox has no network, so the program
# only has to put those exact bytes where the grader looks. Stdlib only; two runs give the same file.
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


MAX_BYTES = 1048576          # the rules' 1 MiB cap
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_dir() -> Path:
    """The grader names the output folder in MAKEFUN_OUTPUT_DIR; /output is the documented default."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def looks_valid(data: bytes) -> bool:
    """A PNG under the size cap whose IHDR says at most 1024 x 1024 pixels."""
    if len(data) > MAX_BYTES or not data.startswith(PNG_MAGIC) or data[12:16] != b"IHDR":
        return False
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return 0 < width <= 1024 and 0 < height <= 1024


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing {SOURCE}", file=sys.stderr)
        return 1
    if not looks_valid(SOURCE.read_bytes()):
        print(f"{SOURCE} is not a PNG within 1 MiB and 1024 x 1024", file=sys.stderr)
        return 1
    target = output_dir()
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target / "entry.png")
    print(f"wrote {target / 'entry.png'} ({SOURCE.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
