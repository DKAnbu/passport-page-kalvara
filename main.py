#!/usr/bin/env python3
"""Entry point for the Kalvara passport spread.

Copies the pre-drawn entry.png (drawn offline with PIL by
draw_image.py) into $MAKEFUN_OUTPUT_DIR/entry.png.
Standard library only, no network.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    print(f"wrote {dst} ({size} bytes)")
    if size > 1_048_576:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
