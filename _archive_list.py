"""Resolve EVERY concept DOI and report what Zenodo actually serves right now.

⚠ WHY. The router's paper table is a written note and notes go stale — on 2026-08-09 it was missing
P6 and P7 entirely and still carried P3's pre-retitle subtitle. Anything published to the community
(a Discord archive, a research page) must be built from what the archive SERVES, never from the
table. A concept DOI always resolves to the newest version, which is exactly why it is the thing to
publish and the thing to check.

    python _archive_list.py            # human table
    python _archive_list.py --json     # machine-readable, for the Discord archive builder
"""
from __future__ import annotations

import json
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                             # noqa: BLE001
        pass

# label -> concept DOI. Concept DOIs only: a version DOI pins a reader to an old PDF forever.
CONCEPTS = [
    ("P1", "10.5281/zenodo.21613153"),
    ("P3", "10.5281/zenodo.21613155"),
    ("P4", "10.5281/zenodo.21612829"),
    ("P5", "10.5281/zenodo.21612831"),
    ("P6", "10.5281/zenodo.21850560"),
    ("P7", "10.5281/zenodo.21850664"),
    ("P8", "10.5281/zenodo.21850666"),
    ("P9", "10.5281/zenodo.21861429"),
]


def resolve(doi: str) -> dict:
    """⚠ urllib gets 403 from Zenodo (bot protection) — curl, per the routed reference."""
    r = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{url_effective}",
                        "-L", f"https://doi.org/{doi}"],
                       capture_output=True, text=True, timeout=120)
    rec = r.stdout.strip().rstrip("/").split("/")[-1]
    if not rec.isdigit():
        return {"error": f"did not resolve to a record: {r.stdout.strip()[:120]}"}
    meta = subprocess.run(["curl", "-sS", f"https://zenodo.org/api/records/{rec}"],
                          capture_output=True, text=True, timeout=120,
                          encoding="utf-8", errors="replace").stdout
    try:
        d = json.loads(meta)
    except json.JSONDecodeError:
        return {"error": f"record {rec}: unparseable metadata"}
    m = d.get("metadata", {})
    return {
        "record": rec,
        "title": m.get("title", ""),
        "version": m.get("version", ""),
        "published": m.get("publication_date", ""),
        "license": (m.get("license") or {}).get("id", ""),
        "url": f"https://doi.org/{doi}",
    }


def main() -> None:
    out = []
    for label, doi in CONCEPTS:
        info = resolve(doi)
        info.update(label=label, concept=doi)
        out.append(info)
        if "--json" not in sys.argv:
            if "error" in info:
                print(f"{label}  ⛔ {info['error']}")
            else:
                print(f"{label}  {info['version']:>4}  {info['published']}  "
                      f"rec {info['record']}  {info['title']}")
    if "--json" in sys.argv:
        print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
