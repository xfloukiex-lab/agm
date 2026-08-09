"""Verify the retitle from what Zenodo now SERVES, not from the publish log.

A publish response saying state=done is not evidence the public sees the new title. This resolves
the concept DOI, reads the record metadata, downloads the served PDF and checks its first page.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import urllib.request

from pypdf import PdfReader

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                             # noqa: BLE001
        pass

CONCEPT = "10.5281/zenodo.21613155"

r = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{url_effective}",
                    "-L", f"https://doi.org/{CONCEPT}"], capture_output=True, text=True)
rec = r.stdout.strip().rstrip("/").split("/")[-1]
meta = json.loads(subprocess.run(["curl", "-sS", f"https://zenodo.org/api/records/{rec}"],
                                 capture_output=True, text=True,
                                 encoding="utf-8", errors="replace").stdout)

title = meta["metadata"]["title"]
ver = meta["metadata"].get("version")
f0 = meta["files"][0]
print(f"concept {CONCEPT} -> record {rec}  ({ver})")
print(f"served title: {title}")

raw = urllib.request.urlopen(f0["links"]["self"], timeout=180).read()
pages = PdfReader(io.BytesIO(raw)).pages
first = " ".join((pages[0].extract_text() or "").split())
flat = " ".join("\n".join((p.extract_text() or "") for p in pages).split())

fails = []
if title != "The Vektorgeist Method (VGM)":
    fails.append(f"record title is still {title!r}")
if "The Vektorgeist Method (VGM)" not in first:
    fails.append("served PDF page 1 does not open on the new title")
if "floukie@vektorgeist.com" not in flat:
    fails.append("contact address missing from the served PDF")
if "Alexander Parnell" not in flat:
    fails.append("byline missing from the served PDF")

print(f"served PDF   : {f0['size']:,} B, opens {first[:70]!r}")
print(f"\n{'✅ RETITLE LIVE ON THE PUBLIC RECORD' if not fails else '⛔ PROBLEM'}")
for f in fails:
    print(f"  FAIL {f}")
sys.exit(0 if not fails else 1)
