# AGM — Zenodo submission package (ready to upload)

**Status:** ready. Zenodo needs no endorser (unlike arXiv). This file is the fill-in sheet — copy
each field into the Zenodo "New upload" form. **Flouk does the actual upload** (identity + outbound).

## Files to upload
- `AGM-Paper.pdf` (generate from `Desktop/AGM-Paper.html` — see "Make the PDF" below), OR the `agm.md`
  source. A PDF is the expected archival artifact.

## Form fields

- **Resource type:** Publication → *Preprint*
- **Title:** `AGM: An Afferent Self-Model for Interpretable, Self-Monitoring AI Agents`
- **Authors:** `Parnell, Alexander` — Affiliation: `Vektorgeist`
  - (Pen name. If you want your legal name on the archival record, add it yourself here at submission —
    Vanta never writes it. ORCID optional; you can register one free if you want a persistent author ID.)
- **Description (abstract — paste as-is):**

  > Modern language-model agents can produce fluent answers but cannot faithfully report *why* they
  > produced them, nor notice when their own behavior is drifting. Asked to explain itself, a model
  > generates a plausible after-the-fact story with no privileged access to the process that made the
  > answer — confabulation, not introspection. We present AGM, a self-model composed of three organs —
  > Aitía (cause), Gut (instinct), and Metron (measure) — that sits beside an agent and observes it.
  > Aitía reasons about the cause of a given output; Metron measures recurrence and drift across time
  > and feeds those measurements into Aitía; Gut reacts to an assembled draft with a fast, coarse
  > instinct signal. The defining constraint is the Enóptron principle: AGM is afferent-only. It reports
  > upward to the operator and sideways into the agent's internal mood, but it never re-enters the
  > spoken answer, never becomes memory, and never gates a component. We argue this constraint is what
  > separates a self-model from a hidden agenda: a self-model permitted to steer the output stops being
  > an honest mirror and becomes an unobservable controller. AGM is cheap enough to run continuously on
  > consumer hardware and yields a human-readable, real-time readout of an agent's causes, instincts,
  > and trends without altering what the agent does.

- **License:** `Creative Commons Attribution 4.0 International (CC BY 4.0)` — max reach, keeps
  attribution. (Alternative if you want it locked tighter: CC BY-NC 4.0.)
- **Keywords:** `AI agents`, `interpretability`, `self-model`, `AI safety`, `agent observability`,
  `introspection`, `drift detection`, `afferent`, `local AI`, `Vektorgeist Method`, `AGM`
- **Language:** English
- **Publisher:** Zenodo
- **Notes / Additional:** `Flagship pillar of the Vektorgeist Method (VGM). Also hosted at
  vektorgeist.com/research.`
- **Related identifiers:** (add after publish) link back from `vektorgeist.com/research`; and once P3
  (VGM overview) has a DOI, cross-link them as "isPartOf".

## Make the PDF (one command, when ready)
Headless Chrome print of the readable page (already on the Desktop):

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu \
  --print-to-pdf="C:\Users\Alexa\Projects\agm-paper\AGM-Paper.pdf" \
  --print-to-pdf-no-header "file:///C:/Users/Alexa/Desktop/AGM-Paper.html"
```

## After Zenodo (the ICM playbook, in order)
1. GitHub repo `agm` (or under a Vektorgeist org): the paper + a short guide/README + the Figure-1 wiring.
2. `vektorgeist.com/research` page linking the DOI (deploy via the shared-repo lockstep — reconcile first).
3. Substack / blog writeup — the funnel into VG Lyceum + the products.
4. arXiv on a parallel track once an endorser (cs.AI / cs.SE) is found.

## Discipline (do not violate)
- Byline = **Alexander Parnell** only. Legal name, if ever, is added by Flouk at submission.
- Zenodo upload + any arXiv submission are **Flouk's action** (identity + outbound). Vanta preps only.
