#!/usr/bin/env python3
"""同步规范副本；--check 只报告漂移，不改写文件。"""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    sources = sorted((root / "using-redberry" / "references").glob("*.md"))
    if not sources:
        parser.error("using-redberry/references/ 中没有规范源文件")
    changed = []
    for skill in sorted(root.glob("*/SKILL.md")):
        destination = skill.parent / "references"
        if not destination.is_dir():
            continue
        for source in sources:
            target = destination / source.name
            data = source.read_bytes()
            if not target.exists() or target.read_bytes() != data:
                changed.append(str(target.relative_to(root)))
                if not args.check:
                    target.write_bytes(data)
    for name in changed:
        print(name)
    print(f"{'发现漂移' if args.check else '已同步'}：{len(changed)} 个文件")
    return int(args.check and bool(changed))


if __name__ == "__main__":
    raise SystemExit(main())
