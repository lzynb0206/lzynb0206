#!/usr/bin/env python3
"""Scale every millisecond animation duration in generated snake SVG files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DURATION = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)ms\b")


def scale_durations(svg: str, factor: float) -> tuple[str, int]:
    def replace(match: re.Match[str]) -> str:
        value = float(match.group(1)) * factor
        rendered = str(int(value)) if value.is_integer() else f"{value:g}"
        return f"{rendered}ms"

    return DURATION.subn(replace, svg)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--factor", type=float, default=2.0)
    args = parser.parse_args()

    if args.factor <= 0:
        parser.error("--factor must be greater than zero")

    for path in args.files:
        original = path.read_text(encoding="utf-8")
        slowed, replacements = scale_durations(original, args.factor)
        if replacements == 0:
            raise SystemExit(f"{path}: no millisecond animation durations found")
        path.write_text(slowed, encoding="utf-8")
        print(f"{path}: scaled {replacements} durations by {args.factor:g}x")


if __name__ == "__main__":
    main()
