#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261117 bounty.

The picture itself is painted ahead of time by generate_entry.py and kept
in this repository as entry.png; all this program does is place a copy of
it where the grader looks for the output image.

It uses only the Python standard library, reads the output folder from
MAKEFUN_OUTPUT_DIR (falling back to /output, the grader's folder), and
writes exactly the same bytes on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
