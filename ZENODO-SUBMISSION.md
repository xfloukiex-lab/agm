# AGM — Zenodo submission package

> ## ⚠ ALREADY PUBLISHED — 2026-07-27. DO NOT USE THIS SHEET AS-IS.
>
> **Published record: [10.5281/zenodo.21613154](https://doi.org/10.5281/zenodo.21613154) —
> *The Afferent Gnosis Model: Self-Knowledge Without Self-Control*.**
>
> This sheet was written 2026-07-20 and was **NOT** what got uploaded. Two of its fields are now
> actively wrong, and both were corrected 2026-07-26:
>
> 1. **The title below was superseded.** The record was published as *The Afferent Gnosis Model:
>    Self-Knowledge Without Self-Control*, not the title this sheet carried.
> 2. **The abstract below described a RETRACTED mechanism.** It said AGM "reports upward to the
>    operator **and sideways into the agent's internal mood**" — that sideways channel is the exact
>    thing §7 reports was removed for producing an anxious agent. Pasting the old abstract would
>    have published, as a live feature, the thing the paper says it took out. It was caught before
>    use; the published description is newly written and correct.
>
> Both fields are corrected in place below. Kept, rather than deleted, because a fill-in sheet
> that silently drifts from the paper is the failure worth remembering.

## Files to upload
- `AGM-Paper.pdf` (generate from `Desktop/AGM-Paper.html` — see "Make the PDF" below), OR the `agm.md`
  source. A PDF is the expected archival artifact.

## Form fields

- **Resource type:** Publication → *Preprint*
- **Title:** `The Afferent Gnosis Model: Self-Knowledge Without Self-Control`
  - (Corrected 2026-07-26. Was `AGM: An Afferent Self-Model for Interpretable, Self-Monitoring AI
    Agents`; the published record uses the title above, and `agm.md`'s H1 now matches it.)
- **Authors:** `Parnell, Alexander` — Affiliation: `Vektorgeist`
  - (Pen name. If you want your legal name on the archival record, add it yourself here at submission —
    never written by the assistant. ORCID optional; you can register one free if you want a persistent author ID.)
- **Description (abstract):** ⚠ **DO NOT reuse the 2026-07-20 text that stood here** — it described
  the retracted "sideways into the agent's internal mood" channel as a live feature. The published
  description is the correct one; read it from the record itself
  ([10.5281/zenodo.21613154](https://doi.org/10.5281/zenodo.21613154)) rather than from this sheet.
  For any future version, take the abstract from `agm.md` — the paper is the source, this sheet is
  not.

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
- Byline = **Alexander Parnell** only. Legal name, if ever, is added by the owner at submission.
- Zenodo upload + any arXiv submission are **the owner's action** (identity + outbound). Vanta preps only.
