"""Print what the P3 record actually SERVES — title, version, and the description a reader meets
first. The description is the first thing anyone sees on the record page, before the PDF.

A deliberate script rather than an inline one-liner (banked: inline `python -c` is not a grep
bypass, and shell mangles quoted payloads).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                             # noqa: BLE001
        pass

CONCEPT = "10.5281/zenodo.21613155"

r = subprocess.run(["curl", "-sS", "-m", "60", "-o", "/dev/null", "-w", "%{url_effective}",
                    "-L", f"https://doi.org/{CONCEPT}"], capture_output=True, text=True)
rec = r.stdout.strip().rstrip("/").split("/")[-1]
raw = subprocess.run(["curl", "-sS", "-m", "60", f"https://zenodo.org/api/records/{rec}"],
                     capture_output=True, text=True, encoding="utf-8",
                     errors="replace").stdout
m = json.loads(raw)["metadata"]

print(f"record {rec}   version {m.get('version')}")
print(f"TITLE: {m['title']}")
print("--- DESCRIPTION AS SERVED ---")
print(re.sub(r"<[^>]+>", "", m.get("description", "")))
