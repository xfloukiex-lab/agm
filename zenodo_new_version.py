"""Publish a NEW VERSION of an agm-paper Zenodo record. Concept DOI unchanged; links follow.

    python zenodo_new_version.py --paper vgm            # dry run, changes nothing
    python zenodo_new_version.py --paper vgm --apply

Adapted from Projects/hodos/paper/zenodo_new_version.py with one deliberate difference: the
metadata is FETCHED from the latest published deposition and reused, rather than hand-maintained
in this file — a second hand-kept copy of record metadata is the defect the release map's own
version table was deleted for. Server-managed keys (`prereserve_doi`, `doi`) are stripped before
the PUT per knowledge/references/zenodo_publishing.md (echoing them back is rejected).

⛔⛔ ZENODO COPIES THE PRIOR VERSION'S FILES INTO A NEW DRAFT, so a failed upload publishes
silently stale bytes under a fresh version number (Beyond Weights, 2026-08-09). Every copied file
is deleted, the new build uploaded, and the draft must hold EXACTLY ONE file at the local size or
it is DISCARDED — checked before publishing, never after.

⚠ A DOI IS PERMANENT. Dry run is the default; --apply is required, and applying is a gated
outbound action taken only on the owner's explicit go.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
API = "https://zenodo.org/api"

PAPERS = {
    "vgm": {
        "latest_record": "21866960",   # v9; concept 10.5281/zenodo.21613155 (verified live 2026-08-12)
        "concept": "10.5281/zenodo.21613155",
        "pdf": "VGM-Overview.pdf", "src": "vgm-overview.md",
        "version": "v10",
        # the framing fix, applied to the record description too if the old phrasing is in it
        "description_fixes": [
            ("VGM is not one artifact but a program:",
             "VGM is not one artifact, and it is not the projects built with it: it is the "
             "method itself, currently applied by"),
            ("VGM is not one artifact but a program",
             "VGM is not one artifact, and it is not the projects built with it: it is the "
             "method itself"),
        ],
        "why": "The paper framed VGM as the research program; VGM is the METHOD in general - the "
               "research programme and the sovereign stack are aligned applications of it, not "
               "its definition. Abstract, section 3 heading and section 6 corrected at source.",
    },
}


def token() -> str:
    for line in (Path.home() / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("ZENODO_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ZENODO_TOKEN not in ~/.env")


def h1_of(src: Path) -> str:
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise SystemExit(f"{src.name} has no H1 - a document must own its own name")


def curl(method, url, tok, *, data=None, upload=None):
    cmd = ["curl", "-sS", "-X", method, "-H", f"Authorization: Bearer {tok}"]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(data)]
    if upload is not None:
        cmd += ["--upload-file", str(upload)]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600)
    try:
        return json.loads(r.stdout) if r.stdout.strip() else {}
    except json.JSONDecodeError:
        return {"_raw": r.stdout[:400], "_err": r.stderr[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True, choices=sorted(PAPERS))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    tok = token()

    spec = PAPERS[args.paper]
    pdf, src = HERE / spec["pdf"], HERE / spec["src"]
    if not pdf.exists():
        raise SystemExit(f"missing {pdf} - build it first")
    local_size = pdf.stat().st_size
    h1 = h1_of(src)

    # metadata comes from the LATEST PUBLISHED deposition, reused - never hand-maintained here
    cur = curl("GET", f"{API}/deposit/depositions/{spec['latest_record']}", tok)
    meta = dict(cur.get("metadata") or {})
    if "title" not in meta:
        raise SystemExit(f"could not read current metadata: {str(cur)[:300]}")
    if not meta["title"].startswith(h1):
        raise SystemExit(f"title/H1 drift: record says {meta['title'][:60]!r}, PDF opens {h1!r}. "
                         f"Fix one; do not publish the disagreement.")
    desc = meta.get("description", "")
    applied = []
    for old, new in spec.get("description_fixes", []):
        if old in desc:
            desc = desc.replace(old, new)
            applied.append(old)
    meta["description"] = desc
    meta["version"] = spec["version"]
    for server_key in ("prereserve_doi", "doi"):
        meta.pop(server_key, None)

    print(f"  paper    : {args.paper}")
    print(f"  concept  : {spec['concept']}  (unchanged - every existing link follows)")
    print(f"  from rec : {spec['latest_record']}  ({cur.get('metadata', {}).get('version')})")
    print(f"  new ver  : {spec['version']}")
    print(f"  title    : {meta['title'][:96]}")
    print(f"  file     : {pdf.name} ({local_size:,} B)")
    print(f"  desc fix : {len(applied)} phrase(s) corrected in the record description")
    print(f"  why      : {spec['why']}")
    if not args.apply:
        print("  DRY RUN - nothing published. Re-run with --apply.")
        return

    nv = curl("POST", f"{API}/deposit/depositions/{spec['latest_record']}/actions/newversion", tok)
    draft_url = (nv.get("links") or {}).get("latest_draft")
    if not draft_url:
        raise SystemExit(f"newversion failed: {str(nv)[:400]}")
    new_id = draft_url.rstrip("/").split("/")[-1]
    d = curl("GET", f"{API}/deposit/depositions/{new_id}", tok)
    bucket = (d.get("links") or {}).get("bucket")
    print(f"  draft    : {new_id}")

    for f in d.get("files", []) or []:
        curl("DELETE", f"{API}/deposit/depositions/{new_id}/files/{f['id']}", tok)
        print(f"  removed copied file: {f.get('filename')} ({f.get('filesize'):,} B)")

    up = curl("PUT", f"{bucket}/{pdf.name}", tok, upload=pdf)
    print(f"  uploaded : {up.get('key')} {up.get('size'):,} B")

    m = curl("PUT", f"{API}/deposit/depositions/{new_id}", tok, data={"metadata": meta})
    if "title" not in (m.get("metadata") or {}):
        curl("POST", f"{API}/deposit/depositions/{new_id}/actions/discard", tok)
        raise SystemExit(f"metadata failed, DRAFT DISCARDED: {str(m)[:400]}")
    print(f"  metadata : {m['metadata']['title'][:70]}")

    check = curl("GET", f"{API}/deposit/depositions/{new_id}", tok)
    files = check.get("files", []) or []
    if not (len(files) == 1 and files[0].get("filesize") == local_size):
        curl("POST", f"{API}/deposit/depositions/{new_id}/actions/discard", tok)
        raise SystemExit(f"DRAFT DISCARDED - expected exactly one file of {local_size:,} B; draft "
                         f"held {[(f.get('filename'), f.get('filesize')) for f in files]}")
    print(f"  gate     : draft holds exactly 1 file at {local_size:,} B OK")

    pub = curl("POST", f"{API}/deposit/depositions/{new_id}/actions/publish", tok)
    print(f"  state={pub.get('state')}  doi={pub.get('doi')}  conceptdoi={pub.get('conceptdoi')}")


if __name__ == "__main__":
    main()
