# AGM — An Afferent Self-Model for Interpretable, Self-Monitoring AI Agents

**Alexander Parnell · Vektorgeist** — the flagship pillar of the **Vektorgeist Method (VGM)**.

A language-model agent can produce a fluent answer but cannot faithfully report *why* it produced it,
nor notice when its own behavior is drifting. **AGM** adds the missing organ: a self-model of three
parts — **Aitía** (cause), **Gut** (instinct), and **Metron** (measure) — that sits *beside* an agent
and observes it, under one load-bearing constraint.

## The idea in one line

A self-model that is allowed to steer the output stops being an honest mirror and becomes a hidden
controller. So AGM is **afferent-only**: it reports *up* to the operator and *sideways* into the agent's
mood, but it **never** re-enters the answer, becomes memory, or gates a component. The panel is honest
*because it is powerless* — the **Enóptron principle**.

## The three organs

| Organ | Role | What it answers |
|-------|------|-----------------|
| **Aitía** (cause) | reasons about the assembled draft + its context | *Why did this output get produced?* |
| **Gut** (instinct) | one fast, coarse signal on the whole draft | *At ease / uneasy / opposed* |
| **Metron** (measure) | streaming statistics over behavior; feeds Aitía | *Is it recurring? Is it drifting?* |

See [`figure-1-wiring.txt`](figure-1-wiring.txt) for the afferent-only wiring (the three forbidden
efferent paths are absent by construction, not merely discouraged).

## Read the paper

- **[`paper.md`](paper.md)** — full text (Markdown source).
- **[`AGM.pdf`](AGM.pdf)** — formatted PDF.
- **Zenodo DOI:** _pending upload_ → this line is updated with the DOI once archived.

## How to cite

See [`CITATION.cff`](CITATION.cff). BibTeX:

```bibtex
@misc{parnell2026agm,
  author       = {Parnell, Alexander},
  title        = {{AGM: An Afferent Self-Model for Interpretable, Self-Monitoring AI Agents}},
  year         = {2026},
  howpublished = {Preprint, Zenodo},
  note         = {The flagship pillar of the Vektorgeist Method (VGM)},
  doi          = {PENDING}
}
```

## Context — the Vektorgeist Method (VGM)

AGM is one pillar of a larger program for building **sovereign, local, self-understanding AI**:
local-first · model-free where a deterministic algorithm suffices · "model proposes, oracle disposes" ·
afferent self-modeling. The program overview and running index of coined terms + papers live at
[vektorgeist.com/research](https://vektorgeist.com/research).

## License

Text and figures © 2026 Alexander Parnell / Vektorgeist, released under
**[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)** — reuse freely with attribution.
