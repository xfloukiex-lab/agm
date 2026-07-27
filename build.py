"""Build the AGM-programme papers: markdown -> self-contained HTML -> PDF.

Why this exists (2026-07-26): there was NO build script here. `AGM-Paper.pdf` and
`VGM-Overview.pdf` were both built 2026-07-20, while `agm.md` and `vgm-overview.md` were
re-spined on 2026-07-23 (+197/-64 lines on P1 alone, 272 -> 405 lines). Publishing those
artifacts would have shipped the PRE-re-spine voice under the post-re-spine title. Rebuilding
by hand each time is how that drift happened, so it gets a script.

Reuses the converter from the Hodos paper build, which is the same minimal markdown subset and
as of 2026-07-26 renders real <a> links -- these papers cite vektorgeist.com and the book, and
inert link text in a preprint helps nobody.

    python build.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HODOS_PAPER = Path("C:/Users/Alexa/Projects/hodos/paper")
sys.path.insert(0, str(HODOS_PAPER))

import build as hodos_build  # noqa: E402  (the Hodos paper builder)

# No hand-passed titles. Each document's H1 IS its title (hodos_build.build_one
# derives it), so the source and the built artifact cannot disagree.
#
# 2026-07-26: they did disagree. This list used to pass "The Afferent Gnosis Model"
# as a literal while agm.md's H1 still read "AGM: An Afferent Self-Model for
# Interpretable, Self-Monitoring AI Agents". The literal reached Zenodo; the H1 was
# never consulted; nothing could flag it. agm.md's H1 now carries the published
# title, and the title lives in exactly one place.
PAPERS = [
    ("agm.md", "AGM-Paper.html", "AGM-Paper.pdf"),
    ("vgm-overview.md", "VGM-Overview.html", "VGM-Overview.pdf"),
]


def main():
    # point the borrowed builder at THIS directory
    hodos_build.HERE = HERE
    for src, html_name, pdf_name in PAPERS:
        hodos_build.build_one(src, html_name, pdf_name)


if __name__ == "__main__":
    main()
