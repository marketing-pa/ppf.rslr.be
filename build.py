#!/usr/bin/env python3
"""
RSLR PPF landingpage — build.

  python3 build.py

Leest copy.md, vult template.html, schrijft index.html.
Meldt lege sleutels en ongebruikte sleutels zodat je niets stil verliest.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
COPY = HERE / "copy.md"
TPL = HERE / "template.html"
OUT = HERE / "index.html"


def read_copy(path: Path) -> dict:
    data, seen = {}, set()
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            print(f"  ! copy.md regel {n}: geen ':' gevonden — overgeslagen")
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        if key in seen:
            print(f"  ! copy.md regel {n}: sleutel '{key}' staat er dubbel in")
        seen.add(key)
        data[key] = val.strip()
    return data


def main() -> int:
    for f in (COPY, TPL):
        if not f.exists():
            print(f"FOUT: {f.name} niet gevonden.")
            return 1

    copy = read_copy(COPY)
    tpl = TPL.read_text(encoding="utf-8")

    used = set()

    def sub(match):
        key = match.group(1).strip()
        used.add(key)
        if key not in copy:
            print(f"  ! template gebruikt '{key}' maar copy.md heeft die sleutel niet")
            return ""
        return copy[key]

    out = re.sub(r"\{\{([^}]+)\}\}", sub, tpl)

    leftover = re.findall(r"\{\{([^}]+)\}\}", out)
    if leftover:
        print(f"  ! nog {len(leftover)} onvervangde placeholders")

    unused = sorted(set(copy) - used)
    if unused:
        print("  ! ongebruikt in template: " + ", ".join(unused))

    empty = sorted(k for k in used if k in copy and not copy[k])
    if empty:
        print("  · leeg gelaten (bewust?): " + ", ".join(empty))

    OUT.write_text(out, encoding="utf-8")
    print(f"OK — index.html geschreven ({len(out):,} tekens, {len(used)} sleutels gebruikt)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
