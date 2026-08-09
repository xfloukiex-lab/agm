"""Rewrite the P3 record DESCRIPTION so it leads with the premise, not with AI commitments.

⚠ THE DEFECT. The 2026-08-09 retitle fixed the record TITLE and left its DESCRIPTION alone, so the
first thing a reader met on the record page was still the old framing: an opening list of
AI-engineering commitments (local-first, model-free, 'model proposes, oracle disposes',
afferent-only self-modelling), with the premise arriving third as an aside. The paper's own front
matter had already been rewritten to lead with the premise — the record disagreed with the document
it holds. Fixing a title without fixing the abstract beside it leaves the misreading fully intact,
because the description is what search results and the record page show first.

⚠ METADATA-ONLY. No new version, no new DOI, no file change — the same edit class used on
2026-07-26 for the Aitía entity and the sibling cross-references. The published PDF is untouched.

    python fix_p3_description.py            # dry run, prints old vs new
    python fix_p3_description.py --apply

⚠ Deposit API, NOT the records API — the two schemas differ and feeding one to the other 400s.
⚠ urllib gets 403 from Zenodo (bot protection) — curl, per the routed reference.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                             # noqa: BLE001
        pass

API = "https://zenodo.org/api"
CONCEPT = "10.5281/zenodo.21613155"

# Order is the whole point: the premise first, the explicit not-an-AI-method line second, the
# commitments demoted to what they are — consequences — and the book as the ontology's long form.
NEW = (
    "<p>The Vektorgeist Method is a research programme built on one premise: nothing is what it is "
    "in isolation &mdash; a thing, including a self, is the pattern of its connections, not its "
    "substrate. That premise is the Hodos Hypothesis, and everything in the programme derives from "
    "it.</p>"
    "<p>VGM is not a method for artificial intelligence. The equations the premise generates have "
    "been measured on speech, handwriting, cardiac rhythm, human body motion, turbulence, "
    "jet-engine degradation, spacecraft telemetry, emission spectra, sonar returns and the Riemann "
    "zeta zeros. Most of that is not AI. Building AI that runs on your own machine was the first "
    "thing the method was pointed at &mdash; one application, never the subject.</p>"
    "<p>From the premise follow the commitments the programme is run under, and what they rule "
    "out: local-first; model-free wherever a problem is deterministic; 'model proposes, oracle "
    "disposes'; afferent-only self-modelling; and emergence as a property of the pattern, never "
    "authored. The last was learned the hard way and is documented as such.</p>"
    "<p>The ontology is stated at length in the companion work of literary nonfiction, "
    "<em>Your Past Loves You</em> (Parnell, 2026): nothing exists in isolation, and a thing is the "
    "pattern its parts hold each other in.</p>"
    "<p>Retitled 2026-08-09. This was published as <em>The Vektorgeist Method: a Programme for "
    "Model-Free, Locally Sovereign AI</em>, and that subtitle is why the programme kept being read "
    "as an AI method. The concept DOI, the 2026-07-27 publication date and every existing citation "
    "are unchanged &mdash; a retitle does not re-date the work.</p>"
    "<p>Research programme: <a href=\"https://vektorgeist.com/research\">"
    "https://vektorgeist.com/research</a></p>"
)


def token() -> str:
    for line in (Path.home() / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("ZENODO_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ZENODO_TOKEN not in ~/.env")


def curl(method: str, url: str, tok: str, data=None):
    cmd = ["curl", "-s", "--max-time", "180", "-X", method,
           "-H", f"Authorization: Bearer {tok}"]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(data)]
    cmd.append(url)
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=300,
                         encoding="utf-8", errors="replace").stdout
    if not out.strip():
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"_raw": out[:400]}


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).replace("&mdash;", "—")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    tok = token()

    r = subprocess.run(["curl", "-sS", "-m", "60", "-o", "/dev/null", "-w", "%{url_effective}",
                        "-L", f"https://doi.org/{CONCEPT}"], capture_output=True, text=True)
    rec = r.stdout.strip().rstrip("/").split("/")[-1]

    dep = curl("GET", f"{API}/deposit/depositions/{rec}", tok)
    if "title" not in dep:
        raise SystemExit(f"cannot read deposit {rec}: {str(dep)[:250]}")
    md = dict(dep.get("metadata", {}))

    print(f"record {rec}   title: {dep['title']}")
    print(f"\n--- CURRENT (first thing a reader meets) ---\n{plain(md.get('description',''))[:600]}")
    print(f"\n--- NEW ---\n{plain(NEW)}")

    if "Programme for Model-Free" in NEW.split("Retitled")[0]:
        raise SystemExit("refusing: the new lead still carries the framing this change removes")

    if not args.apply:
        print("\nDRY RUN — nothing changed")
        return

    # edit -> PUT -> publish. A published deposit must be reopened before metadata will take.
    curl("POST", f"{API}/deposit/depositions/{rec}/actions/edit", tok)
    md.pop("prereserve_doi", None)                 # server-managed; echoing it back is rejected
    md["description"] = NEW
    put = curl("PUT", f"{API}/deposit/depositions/{rec}", tok, data={"metadata": md})
    if "title" not in put:
        raise SystemExit(f"metadata PUT FAILED: {str(put)[:300]}\n"
                         "the deposit is left OPEN — resolve it, do not leave it hanging")
    pub = curl("POST", f"{API}/deposit/depositions/{rec}/actions/publish", tok)
    print(f"\n  state={pub.get('state')}  doi={pub.get('doi')}  (unchanged: metadata-only edit)")

    # verify from what is SERVED, never from the publish response
    served = json.loads(subprocess.run(
        ["curl", "-sS", "-m", "60", f"https://zenodo.org/api/records/{rec}"],
        capture_output=True, text=True, encoding="utf-8",
        errors="replace").stdout)["metadata"]
    live = plain(served.get("description", ""))
    ok = live.startswith("The Vektorgeist Method is a research programme built on one premise")
    print(f"  served description leads with the premise: {ok}")
    print(f"  first 120: {live[:120]}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
