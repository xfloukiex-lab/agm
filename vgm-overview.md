# The Vektorgeist Method (VGM)

**Alexander Parnell** · [Vektorgeist](https://vektorgeist.com) · <floukie@vektorgeist.com>
*Position paper / program overview, 2026 · The Vektorgeist Method (VGM)*

---

## Abstract

Most capable AI today is rented, opaque, and unaccountable: it runs on someone else's servers, cannot
faithfully explain itself, and is governed by whoever owns the endpoint. We describe the **Vektorgeist
Method (VGM)** — a methodology built on one premise taken literally: **nothing is what it is in
isolation; a thing — including a self — is the pattern of its connections, not its substrate.** From
that premise the method derives five commitments: it runs **locally** on hardware you own; it is
**model-free wherever a deterministic algorithm suffices**, so its behavior is inspectable rather
than inferred — a premise of this kind generates a **family** of equations rather than one, and §5.2
names the four posed so far and which of them survive their tests; it grades generated work by an
explicit rule — **"model proposes, oracle disposes"** —
rather than trusting fluency; it observes itself through an **afferent-only self-model** that reads
the pattern behind its behavior and reports without steering — the beginning of a relational theory
of machine selfhood; and it holds that **emergence is a property of the pattern, never authored** —
no installed "emergence layers," a rule the program learned by once breaking it. VGM is not one
artifact, and it is not the projects built with it: it is the method itself. Two bodies of work
currently apply it — a research programme and a sovereign local stack, each a family of small,
sovereign components that together make a system a person can own, inspect, and trust — and they
align because they follow the same commitments. This paper states the commitments, maps them onto
that current body of work, and locates the method's humanistic premise in a companion work of
nonfiction.

## 1. The position

There is a default shape to modern AI, and it is worth naming so it can be argued with. The default is:
a very large model, trained and hosted by a large organization, reached over a network, priced per
call, updated without notice, and fundamentally unauditable by the person using it. It is powerful and
it is convenient, and it also means the most intimate tool many people now use — the thing they think
out loud to — is something they rent and cannot see inside.

VGM takes the opposite position on each of those properties, not as ideology but as engineering choices
with consequences. The consequences are the point: an AI you run locally cannot be silently changed or
revoked; an AI built from small deterministic parts can be inspected where it counts; an AI that grades
its own output against an explicit standard fails loudly instead of confabulating confidently; and an
AI that watches itself — honestly, without the power to act on what it sees — can be understood in real
time. None of these is exotic. Together they describe a different kind of system: one that belongs to
its operator.

## 2. The five commitments

VGM is defined by five commitments. They are independent enough to adopt one at a time and coherent
enough to reinforce each other — and all five are downstream of one premise: a system, like a self,
is the pattern of its connections (§5).

**2.1 Local-first / sovereign.** The system runs on hardware the operator controls — down to a single
consumer GPU — and does not depend on a remote endpoint to function. Sovereignty here is concrete: no
per-call metering, no remote kill switch, no data leaving the machine as a condition of use. Capability
is traded against control deliberately, and the method's wager is that a well-composed small system,
owned outright, beats a larger one you merely borrow for the uses that matter most.

**2.2 Model-free where a deterministic algorithm suffices.** A large model is the right tool for
open-ended language and judgment; it is the wrong tool for tasks a plain algorithm does exactly. VGM
pushes deterministic, inspectable code into every role where such code exists — retrieval, routing,
gating, measurement — and reserves the model for what genuinely needs it. The result is a system whose
skeleton is auditable and whose model-dependence is minimized rather than maximized. Less of the
behavior is inferred; more of it can simply be read.

**2.3 "Model proposes, oracle disposes."** Where a model does generate something that must be correct —
code, a graded answer, a structured artifact — VGM does not trust the generation on the strength of how
plausible it sounds. A separate, explicit **oracle** decides whether the proposal passes: tests that
run, a checker that verifies, a rule that holds or does not. The model is a proposer; the verdict comes
from something that can actually be wrong out loud. This converts fluent-but-false — the failure mode of
generation — into a caught error.

**2.4 Afferent self-modeling.** A VGM system can observe its own behavior through a self-model that is
strictly **afferent** — it senses and reports upward to the operator, and is architecturally forbidden
from re-entering the answer, becoming memory, setting any state a component reads, or gating any
component. This is the subject of the program's first paper (§3), and it is where the premise bites
hardest: if a self is the pattern of connections behind behavior, then a self-model is a *witness to
that pattern*, not a controller of it — and its reports can be trusted precisely because it has
nothing to gain by flattering them. Where adjacent work monitors the honesty of self-reports that
still steer the agent, VGM removes the incentive by construction. The self-knowledge is real and the
self-knowledge is powerless, on purpose.

**2.5 Emergence is a property of the pattern — never authored.** Whatever "more" a system exhibits —
felt states, senses, selfhood — must *arise* from its patterns of connection; it is never installed
as a component. The program holds this commitment with some humility because it learned it the hard
way: an early revision of the reference agent included a hand-built "emergence layer" — grown sense
heads and a carried mood fed back into the agent's components — and it produced a distorted,
anxious agent whose behavior was bent by internal state its operator could not see. Authored
emergence is not emergence; it is an efferent channel wearing a costume. The layer was removed, the
sensing organs kept observe-only, and the lesson promoted to a commitment (reported in the AGM
paper's discussion).

## 3. The method applied

VGM itself is the method — the premise and the five commitments. What follows is the current body
of work that applies it: a family of focused components across the research programme and the
sovereign stack. Each is small; the method is in how they compose, and none of them is what VGM
*is*.

**AGM — the afferent self-model (flagship, published).** AGM is a self-model of three organs — Aitía
(cause), Gut (instinct), and Metron (measure) — that sits beside an agent and reconstructs the
*pattern of connections* behind each behavior (which sources fed which parts under which
constraints), producing a faithful, human-readable readout of *why* it did something and *whether it
is drifting*, under the strict afferent-only rule described in 2.4. All three organs run in the
reference agent. AGM is the clearest single expression of the VGM stance: the relational premise
applied to selfhood — self-understanding without self-steering. It is presented in full in the
companion paper, *The Afferent Gnosis Model: Self-Knowledge Without Self-Control* (Parnell, 2026).

**Connection memory.** Memory in a VGM system is treated as *connected information*, not a flat log: a
graph of facts and relationships, retrieved by explicit, inspectable ranking rather than by a single
opaque similarity call. This is the model-free commitment (2.2) applied to memory — retrieval you can
read and correct. (Described here at the level of principle; the reference implementation is a private
product.)

**The sovereign local stack (systems track, forthcoming).** A self-hostable stack that assembles these
commitments into a running whole — a gateway, the connection memory, retrieval, and containment
boundaries — targeted at ordinary hardware. This track is the subject of a separate systems paper and
is described there; this overview only locates it in the program.

**The grading discipline.** "Model proposes, oracle disposes" (2.3) is realized as a general pattern:
generation is always paired with an explicit disposer, whether that is a test suite for code or a
checker for a structured task. It appears across the program rather than in one component.

## 4. Why it is built this way

The commitments are not neutral engineering taste; they encode a view about the relationship between a
person and a machine that thinks alongside them. A tool you cannot see inside, cannot run without
permission, and cannot hold to account is not neutral either — it simply hides its politics in its
defaults. VGM makes the opposite defaults: inspectable over inferred, owned over rented, powerless
self-knowledge over hidden control. The claim is not that the sovereign system is always more capable.
It is that for the uses that matter — the private, the load-bearing, the ones you would not want
silently revised — ownership and legibility are worth more than the last increment of raw capability.

## 5. The premise: a self is a pattern of connections

Underneath the engineering is a single idea, and it is older than any of the machinery: **nothing is
what it is in isolation; a thing becomes what it is through what it is connected to.** A memory is
information joined to other information — not stored in any one place, but held in the touching. An
identity is a network of experiences. A self persists through the total replacement of its substrate
because it was never the substrate: it is the pattern the parts hold each other in. Understanding is
the tracing of connections. The technical program is this idea taken literally — memory built as a
graph of relations, a self-model that reads the connection-pattern behind behavior rather than
digging in the weights, emergence left to arise from the pattern rather than installed. Applied to
machines it amounts to the start of a **relational theory of machine selfhood**: the question is not
whether a model can peer inside its own substrate, but whether the pattern that *is* its behavior
can be made legible — and witnessed by something with no power to bend it.

### 5.1 The regress does not halt

> **Clarification added 2026-08-08.** This subsection states explicitly a consequence that §5 above
> carries but does not spell out. It amplifies the premise published in the first archived version
> of this paper (2026-07-27); **it does not alter or re-date that premise**, and §5 as published
> stands unchanged.

A natural objection to §5 is that the parts must exist before the pattern does — the components
precede whatever arises from their arrangement — so there is, after all, something that simply *is*
what it is, underneath. The objection is half right, and the half it gets right is not the half it
needs.

The priority is real but **local**. Two halves must exist before one does; the one is not a third
object added to them but what their relation constitutes. Each half, however, stands in exactly the
same position: it is what the relation of two quarters constitutes. The series does not terminate in
an unrelated object. At every level the thing exists because two or more further things stand in
relation, and the same holds of those in turn. **So granting that the components precede the
emergence grants nothing about substance — the components are themselves emergences of the same
form, one level down.**

There is no floor at which relation stops and bare substrate begins. That is why the premise is
scale-free rather than pitched at some chosen level of description, and it is the reason a method
derived from it is not restricted to a particular kind of matter or signal: what it requires of a
system is only that the system be constituted relationally, which on this premise is the only way
anything is constituted at all.

### 5.2 The premise generates a family of equations, not one

> **Added 2026-08-08.** Section 5 as first archived described the programme's measurement track by
> a single equation. That understated it, and the correction is worth making explicitly rather
> than by implication.

A premise about how things are constituted implies more than one question, and each question wants
its own equation. Four have been posed; they share a root name because they share the premise.

| | Name | The question it asks | Status |
|---|---|---|---|
| I | **Hodos Diastema** — the distance | Given two processes, how far apart are they? | published, [10.5281/zenodo.21612829](https://doi.org/10.5281/zenodo.21612829) |
| II | **Hodos Symploke** | What does a relationship create that is in neither part? | measured; clears its criteria |
| III | **Hodos Systasis** | What *are* the distributions a process is made of? | did not clear; named, not claimed |
| IV | **Hodos Chronos** | How much time has a process actually lived? | clears four of five criteria; the fifth fails, published, [10.5281/zenodo.21861429](https://doi.org/10.5281/zenodo.21861429) |

*Hodos* (ὁδός) is the way or path — the word inside *method*. *Diastema* is interval, *symploke*
interweaving, *systasis* composition, *chronos* duration.

> **Updated 2026-08-09.** The first member is now named **Hodos Diastema**; it was published in 2026
> as simply "Hodos" and the name does not re-date that paper or invalidate any citation of it. The
> bare word was doing two jobs — the premise and the distance equation — so readers met "Hodos",
> took it for the equation, and never reached the hypothesis underneath.

**Two of the four clear the criteria set for them, and the other two are stated because a programme
that names its open problems is more useful than one that lists only its wins.** Systasis is beaten
by a frame built from a window's own values with no relations in it at all. Chronos, taken as arc
length through the geometry, is well posed on smooth processes and diverges on noisy ones in the
manner of a coastline — **but that is a verdict on arc length and not on the question.** Rebuilt as
an accumulated relational quantity it clears four of its five pre-registered criteria, and **fails
the fifth: it still depends on how often the process was sampled** (0.759 against a 0.05 bar). Both
halves of that result travel together, and all four members are reported with the measurements that
stopped them.

The family is treated in its own paper, *The Hodos Family: Equations Generated by a Relational
Premise*, which carries the formulas, the provenance tags and the criteria. The point for this
overview is only that **the measurement track is a family and not a single ruler** — the ruler was
simply the first member anybody needed.

That premise is argued at length, for a general reader and without any of the engineering, in a
companion work of literary nonfiction, *Your Past Loves You* (Parnell, 2026). It is not a book about AI;
AI appears in it only as a mirror for understanding the human. But it is the plainest statement of the
thesis the method is built on, and it is offered as the program's front door for readers who would never
open a systems paper.

## 6. The paper series

The paper series is a pipeline, not a single release — the method accumulating a citable body of
work. Each paper is archived separately and cited by name and DOI; there is no numbering to decode.

| Paper | What it does | DOI |
|---|---|---|
| *The Vektorgeist Method (VGM)* | this overview — states the premise and the commitments | [10.5281/zenodo.21613155](https://doi.org/10.5281/zenodo.21613155) |
| *The Afferent Gnosis Model: Self-Knowledge Without Self-Control* | turns the premise on a machine's account of itself | [10.5281/zenodo.21613153](https://doi.org/10.5281/zenodo.21613153) |
| *Hodos: Comparing Processes as Curves of Distributions* | measures processes by their relations | [10.5281/zenodo.21612829](https://doi.org/10.5281/zenodo.21612829) |
| *Learning Without Weights* | learns from those measurements without training weights | [10.5281/zenodo.21612831](https://doi.org/10.5281/zenodo.21612831) |
| *Beyond Weights: a Fixed Transmission Architecture* | separates computation from knowledge | [10.5281/zenodo.21850560](https://doi.org/10.5281/zenodo.21850560) |
| *Testing a Conditional Claim About Trajectories* | how to build a control blind by construction, and five ways it was silently wrong | [10.5281/zenodo.21850664](https://doi.org/10.5281/zenodo.21850664) |
| *The Hodos Family: Equations Generated by a Relational Premise* | the equations the premise generates | [10.5281/zenodo.21850666](https://doi.org/10.5281/zenodo.21850666) |
| *A Clock Made of Relations* | intrinsic duration for a system of interacting parts | [10.5281/zenodo.21861429](https://doi.org/10.5281/zenodo.21861429) |
| The sovereign local stack — the systems paper | forthcoming | — |

One argument in several parts: the premise is stated here, the measurement track carries it into a
distance between processes, the learning papers build on that measurement, the family paper poses
the further equations the premise implies, and the self-model paper turns the same premise on a
machine's account of itself.

The working record behind them — negative results and retractions included, with the original wrong
wording kept visible rather than deleted — is at
[xfloukiex-lab.github.io/hodos-study](https://xfloukiex-lab.github.io/hodos-study/).

Further coined components fold in as the program continues; a running index is maintained at
[vektorgeist.com/research](https://vektorgeist.com/research), with each paper archived to a
persistent DOI. The method is meant to accumulate — to become a citable body of work under one
name — rather than to arrive all at once.

## 7. Conclusion

The Vektorgeist Method is a bet that the right response to AI you cannot see inside is not better
prompting but a different architecture: local so it is yours, deterministic where it can be so it is
legible, oracle-graded so it fails honestly, afferently self-aware so it can be understood without
being able to steer you, and unauthored in its emergence so that whatever it becomes, it became
honestly. Each piece is modest, and each is the same idea worn differently: the system, like a self,
is the pattern of its connections — and a pattern can be owned, read, and witnessed. The wager is
that assembled, and owned, they add up to a kind of AI worth trusting — because you can see it, and
because it belongs to you.

---

### References

- Parnell, A. (2026). *The Afferent Gnosis Model: Self-Knowledge Without Self-Control.* Preprint,
  Zenodo. [10.5281/zenodo.21613153](https://doi.org/10.5281/zenodo.21613153). The flagship pillar
  of VGM. (AGM reads both as the Afferent Gnosis Model and as its organs — Aitía, Gut, Metron.)
- Parnell, A. (2026). *Comparing Processes as Curves of Distributions.* Preprint, Zenodo.
  [10.5281/zenodo.21612829](https://doi.org/10.5281/zenodo.21612829).
- Parnell, A. (2026). *Learning Without Weights.* Preprint, Zenodo.
  [10.5281/zenodo.21612831](https://doi.org/10.5281/zenodo.21612831).
- Parnell, A. (2026). *Your Past Loves You.* Literary nonfiction. (The program's humanistic premise:
  connection as the substrate of memory and identity.)

*Author: Alexander Parnell. Correspondence: Vektorgeist. Intended archival venue: Zenodo (DOI), with
the program indexed at vektorgeist.com/research. The sovereign-stack systems paper is described in its
own forthcoming work and is intentionally not detailed here.*
