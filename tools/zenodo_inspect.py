"""Read-only inspection of the four published Zenodo records. Changes nothing.

Answers, before anything is touched:
  - is the DOI on vektorgeist.com/research the CONCEPT doi or a VERSION doi?
    (matters: a new version leaves a version-doi link pointing at the old file)
  - does the P1 description really contain the misspelling "Aitia" with the wrong accent?
  - what related_identifiers exist already?
"""
import json
import urllib.request
from pathlib import Path

TOKEN = Path(__file__).with_name("zenodo_token.txt").read_text(encoding="utf-8").strip()
RECORDS = {"P1 AGM": 21613154, "P2 VGM": 21613156,
           "P3 Hodos": 21612830, "P4 Learning": 21612832}


def api(path):
    req = urllib.request.Request(f"https://zenodo.org/api{path}",
                                 headers={"Authorization": f"Bearer {TOKEN}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


for label, rid in RECORDS.items():
    d = api(f"/records/{rid}")
    md = d.get("metadata", {})
    concept = d.get("conceptdoi") or md.get("conceptdoi")
    print(f"\n=== {label} (record {rid}) ===")
    print(f"  title        : {md.get('title')}")
    print(f"  version doi  : {d.get('doi')}")
    print(f"  concept doi  : {concept}")
    print(f"  this id IS   : {'the CONCEPT record' if str(concept or '').endswith(str(rid)) else 'a VERSION record'}")
    rel = md.get("related_identifiers") or []
    print(f"  related ids  : {len(rel)}")
    for r in rel:
        print(f"      {r.get('relation')} -> {r.get('identifier')}")
    files = d.get("files") or []
    print(f"  files        : {[f.get('key') for f in files]}")
    desc = md.get("description", "")
    if rid == 21613154:
        print(f"  'Aitiá' (wrong accent) present: {'Aitiá' in desc}")
        print(f"  'Aitía' (correct)       present: {'Aitía' in desc}")
    print(f"  description  : {len(desc)} chars")
