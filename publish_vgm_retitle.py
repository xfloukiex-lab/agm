"""Publish the RETITLED P3 as a new Zenodo version: "The Vektorgeist Method (VGM)".

Same deposit flow the other papers used (deposit API, NOT the records API — the two schemas differ
and feeding one to the other 400s):

    POST /deposit/depositions/{id}/actions/newversion  -> draft (inherits the OLD file)
    delete the inherited file, upload the new one
    PUT  /deposit/depositions/{draft}                  -> metadata (title, version)
    POST /deposit/depositions/{draft}/actions/publish

⚠ RECORD 21861828 IS THE LIVE TIP, resolved from the concept DOI. A newversion must branch from the
newest version; branching from the original record forks the lineage.

The concept DOI 10.5281/zenodo.21613155 is unchanged, so every existing link and citation follows
to this version automatically. A retitle does not re-date the work.

    python publish_vgm_retitle.py            # dry run
    python publish_vgm_retitle.py --apply
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                             # noqa: BLE001
        pass

HERE = Path(__file__).resolve().parent
API = "https://zenodo.org/api"
RECORD = "21861828"          # live tip of concept 10.5281/zenodo.21613155
PDF = HERE / "VGM-Overview.pdf"
SRC = HERE / "vgm-overview.md"
VERSION = "v7"


def token() -> str:
    for line in (Path.home() / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("ZENODO_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ZENODO_TOKEN not in ~/.env")


def h1_of(src: Path) -> str:
    """Title is DERIVED from the document's own H1 — never hardcoded.

    Hardcoding is what once shipped a record whose title disagreed with its own first line.
    """
    return next(l[2:].strip() for l in src.read_text(encoding="utf-8").splitlines()
                if l.startswith("# "))


def curl(method: str, url: str, tok: str, *, data=None, upload: Path | None = None):
    cmd = ["curl", "-s", "--max-time", "180", "-X", method,
           "-H", f"Authorization: Bearer {tok}"]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(data)]
    if upload is not None:
        cmd += ["-H", "Content-Type: application/octet-stream", "--data-binary", f"@{upload}"]
    cmd.append(url)
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
    if not out.strip():
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"_raw": out[:400]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    tok = token()
    title = h1_of(SRC)

    cur = curl("GET", f"{API}/deposit/depositions/{RECORD}", tok)
    if "title" not in cur:
        raise SystemExit(f"cannot read deposit {RECORD}: {str(cur)[:250]}")
    print(f"record {RECORD}")
    print(f"  published title: {cur['title']}")
    print(f"  new title      : {title}")
    print(f"  version        : {cur.get('metadata', {}).get('version')} -> {VERSION}")
    print(f"  file           : {PDF.name} ({PDF.stat().st_size:,} B)")

    if "Model-Free" in title:
        raise SystemExit("refusing: the new title still carries the subtitle this change removes")

    if not args.apply:
        print("\nDRY RUN — nothing changed")
        return

    nv = curl("POST", f"{API}/deposit/depositions/{RECORD}/actions/newversion", tok)
    draft_url = (nv.get("links") or {}).get("latest_draft")
    if not draft_url:
        raise SystemExit(f"newversion FAILED: {str(nv)[:300]}")
    draft_id = draft_url.rstrip("/").split("/")[-1]
    print(f"\n  draft {draft_id}")

    draft = curl("GET", f"{API}/deposit/depositions/{draft_id}", tok)
    for f in draft.get("files", []):
        curl("DELETE", f"{API}/deposit/depositions/{draft_id}/files/{f['id']}", tok)
        print(f"  removed inherited file {f['filename']}")

    bucket = (draft.get("links") or {}).get("bucket")
    up = curl("PUT", f"{bucket}/{PDF.name}", tok, upload=PDF)
    print(f"  uploaded {PDF.name}: {up.get('size')} B")

    md = dict(draft.get("metadata", {}))
    md.pop("prereserve_doi", None)          # server-managed; echoing it back is rejected
    md["title"] = title
    md["version"] = VERSION
    put = curl("PUT", f"{API}/deposit/depositions/{draft_id}", tok, data={"metadata": md})
    if "title" not in put:
        raise SystemExit(f"metadata PUT FAILED: {str(put)[:300]}\n"
                         "leaving the draft UNPUBLISHED — resolve it, do not leave it hanging")
    print(f"  metadata set: {put['title']}")

    pub = curl("POST", f"{API}/deposit/depositions/{draft_id}/actions/publish", tok)
    print(f"  state={pub.get('state')}  doi={pub.get('doi')}  conceptdoi={pub.get('conceptdoi')}")


if __name__ == "__main__":
    main()
