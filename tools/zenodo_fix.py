"""Fix published Zenodo metadata: the Aitía misspelling + paper-to-paper series links.

Metadata only. No new versions, no file changes — every DOI keeps resolving to exactly
the PDF it resolves to now.

  python zenodo_fix.py           # dry run
  python zenodo_fix.py --apply   # edit + republish
  python zenodo_fix.py --discard # abandon any open edit, leaving records as published

v2 (2026-07-26): v1 fed metadata from `GET /records/{id}` into `PUT /deposit/...`. Those
are different schemas — the records API returns `resource_type` as an object, the deposit
API wants `upload_type`/`publication_type` and rejects the former. All four PUTs failed
validation, which is the good failure: nothing was written. Now the metadata is read from
the deposit API, so it round-trips in the shape the deposit API expects, and
related_identifiers carry only relation/identifier/scheme.

Fixes:
1. P1's description renders "Aitiá" (stored as `Aiti&#225;`). The paper spells it
   "Aitía" — accent on the i. It is a coined term on an archival record.
2. The four papers link out to the research page and the study record but not to EACH
   OTHER. They are one argument in four parts. Added as `references` to each sibling's
   CONCEPT doi, so the link follows the sibling's newest version rather than pinning.
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

TOKEN = Path(__file__).with_name("zenodo_token.txt").read_text(encoding="utf-8").strip()
APPLY = "--apply" in sys.argv
DISCARD = "--discard" in sys.argv

PAPERS = {
    21613154: ("P1 AGM",      "10.5281/zenodo.21613153"),
    21613156: ("P2 VGM",      "10.5281/zenodo.21613155"),
    21612830: ("P3 Hodos",    "10.5281/zenodo.21612829"),
    21612832: ("P4 Learning", "10.5281/zenodo.21612831"),
}
BAD, GOOD = "Aiti&#225;", "Ait&#237;a"


def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(f"https://zenodo.org/api{path}", data=data, method=method,
                                 headers={"Authorization": f"Bearer {TOKEN}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode("utf-8")
        return json.loads(body) if body.strip() else {}


def plan(rid, md):
    md = json.loads(json.dumps(md))
    changes = []

    desc = md.get("description", "")
    if BAD in desc:
        md["description"] = desc.replace(BAD, GOOD)
        changes.append(f'description: "Aitiá" -> "Aitía" ({desc.count(BAD)}x)')

    rel = list(md.get("related_identifiers") or [])
    have = {(r.get("relation"), r.get("identifier")) for r in rel}
    for other, (label, concept) in PAPERS.items():
        if other == rid or ("references", concept) in have:
            continue
        rel.append({"relation": "references", "identifier": concept, "scheme": "doi"})
        changes.append(f"+ references {concept}  ({label})")
    md["related_identifiers"] = rel

    md.pop("prereserve_doi", None)      # server-managed; echoing it back is rejected
    return md, changes


for rid, (label, _) in PAPERS.items():
    dep = api("GET", f"/deposit/depositions/{rid}")
    state = dep.get("state")

    if DISCARD:
        if state == "inprogress":
            try:
                api("POST", f"/deposit/depositions/{rid}/actions/discard")
                print(f"{label}: open edit discarded, back to published")
            except urllib.error.HTTPError as e:
                print(f"{label}: discard failed {e.code}")
        else:
            print(f"{label}: state={state}, nothing to discard")
        continue

    new_md, changes = plan(rid, dep["metadata"])
    print(f"\n=== {label} ({rid}) state={state}")
    if not changes:
        print("   nothing to change")
    for c in changes:
        print(f"   {c}")
    if not APPLY or not changes:
        continue

    try:
        if state != "inprogress":
            api("POST", f"/deposit/depositions/{rid}/actions/edit")
        api("PUT", f"/deposit/depositions/{rid}", {"metadata": new_md})
        api("POST", f"/deposit/depositions/{rid}/actions/publish")
        print("   APPLIED + republished")
    except urllib.error.HTTPError as e:
        print(f"   ! FAILED {e.code}: {e.read().decode()[:300]}")

if not (APPLY or DISCARD):
    print("\n(dry run — nothing changed)")
