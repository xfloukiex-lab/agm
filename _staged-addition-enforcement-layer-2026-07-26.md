# STAGED ADDITION — AGM applied to the enforcement layer

**Staged 2026-07-26 17:5x CDT. NOT merged into `agm.md`.**

`agm.md` is being released right now (Flouk, 2026-07-26). Editing the source mid-release
would put the file on disk out of step with the artifact going out, which is the exact
drift the P1/P3 stale-PDF note in the VGM router already warns about. So this is written
as ready-to-merge blocks, to be folded into the **next** revision on Flouk's word.

Voice matched to the Flouk-approved P1 (2026-07-20). Nothing here contradicts the current
text; it extends §6 and §7 and adds one reference.

---

## Why this is worth adding

The paper's deployment finding (§7) is about **an observer that was given hands**: we
allowed one sideways efferent channel, and the predicted pathology arrived.

This is the **complement**, and it arrived from outside our own system:

> A mechanism that HAS hands cannot audit itself, because from the inside a dead
> enforcement mechanism and a permissive one are the same observation. Only a witness
> with no hands can tell "allowed" from "did not run".

That is not a restatement of §5's incentive argument. §5 says a powerless observer is the
only *trustworthy* one. This says a powerless observer is, for a class of failure, the only
*possible* one — the signal does not exist anywhere else in the system. It strengthens the
paper from "afferent-only is what makes the report honest" to "afferent-only is also what
makes certain failures observable at all."

It also gives the framework a **second instantiation in a different domain**, which the
current paper lacks: P1 describes AGM over an agent's answers, implemented once, in our own
memory system. This applies the same three organs to an agent's *enforcement layer*, and the
motivating evidence comes from a system we did not build.

---

## BLOCK A — for §6 (Reference implementation), appended after "Isolation"

> **A second instantiation: AGM over an enforcement layer.** The organs are not specific to
> observing answers. We have since applied the same architecture to a different subject: the
> stack of pre-execution gates that constrain what an agent is permitted to do. Aitía
> produces the causal account of a gate's state — not "this gate is silent" but why silence
> is the observation, and what that implies about the wiring. Metron supplies the time axis
> the instantaneous check lacks, reporting *recurrence* (a gate has answered wrongly for
> three consecutive runs, so it is a standing condition rather than a transient) and *drift*
> (the number of live gates has fallen across the window) — and, as in §4.3, Metron reports
> through Aitía rather than on its own channel. Gut reacts to the whole shape of a run with
> one coarse signal.
>
> The Enóptron constraint carries over exactly, and is the interesting part: the observer may
> read every gate's state and may write nothing in the enforcement layer. It cannot
> re-register a hook, repair a gate, or edit the configuration that installs them. When it
> finds a gate dead it says so and stops. Repair is a separate, explicit human decision — the
> audit layer and the control layer stay apart, so the audit stays trustworthy (§7).
>
> The isolation is enforced as static guards on the observer's own source, in the manner
> described above: the source may not construct a path to the enforcement configuration, may
> not call any delete/rename/permission-changing operation, may not import a gate module, and
> may not emit the decision type that would let it block execution — plus a behavioural check
> that a full observation run leaves every gate file and the configuration byte-identical. The
> guard fires on a planted violation, which we verified rather than assumed.

## BLOCK B — for §7 (Discussion and limitations), as a new paragraph after the deployment finding

> **The complement: an efferent mechanism cannot witness its own death.** The finding above
> concerns a self-model that was wrongly given a hand. The converse case is at least as
> common and considerably quieter. Auditing an unrelated open-source agent-persistence
> project, we found an enforcement hook that imported a function which did not exist; the
> error was swallowed by the surrounding handler; the mechanism had been a silent no-op for
> an unknown period while the project's documentation described it as constraining the agent.
> An external audit found it; the system itself never could have. Checking our own stack for
> the same class, we found it: every gate invoked through a single interpreter reference whose
> failure produces no output, and a test suite that verified each gate's decision *logic* and
> would have stayed green if the gate's registration were deleted outright.
>
> The structural point generalises the paper's thesis rather than repeating it. An efferent
> component cannot audit itself, because from inside the system a mechanism that permitted an
> action and a mechanism that failed to run are the same observation — absence of objection.
> Distinguishing them requires a component positioned outside the enforcement path, and that
> component must be powerless for the reason §5 gives, since an auditor that can also repair
> will eventually be judged on whether things are fixed rather than on whether its account is
> accurate. So the afferent constraint is doing two jobs: it is what makes the self-report
> *trustworthy* (§5), and it is what makes this class of failure *visible at all*. We note the
> asymmetry plainly: this is a structural argument supported by two instances, not a
> measurement. What it licenses is a design rule — **anything in a system that has hands
> should have something without hands watching it** — not a quantitative claim.

## BLOCK C — for §1 (contributions), amend contribution 4

Current:

> 4. A **deployment finding**: allowing even one "sideways" efferent channel (a carried mood
>    readable by the agent's components) produced, in practice, the exact pathology the
>    principle predicts — and removing it restored the agent. The principle is not hypothetical.

Proposed:

> 4. **Two deployment findings, in opposite directions.** Allowing even one "sideways" efferent
>    channel (a carried mood readable by the agent's components) produced, in practice, the exact
>    pathology the principle predicts — and removing it restored the agent. Conversely, an
>    enforcement mechanism with no afferent observer was found — in an unrelated system and then
>    in our own — to have failed silently and indefinitely, because from inside a system a dead
>    gate and a permissive gate are indistinguishable. The constraint is load-bearing in both
>    directions: it is what makes the report trustworthy, and what makes the failure visible.

## BLOCK D — reference to add

> - Cited as an external case in §7: an open-source agent-persistence project whose published
>   third-party audit (2026) documented a self-monitoring hook that had become a silent no-op
>   through a swallowed import error. Retained here as a case, not an endorsement or a
>   comparison of architectures.

*(Exact citation form pending: whether to name the repository, or cite the published audit
document, or keep it as an unnamed case. Flouk's call — the project is a friend's, the audit
is public, and their operator has been emailed about this connection. Naming is courteous only
if they are comfortable being named; do not name without asking.)*

---

## What was actually built (the referent for Block A)

Not a proposal — running code, at `~/.claude/hooks/`:

| Piece | Role | Status |
|---|---|---|
| `hook_selftest.py` | Sensing. Probes each gate with a payload it must refuse plus a benign control. | 12 hooks, 6 gates confirmed firing |
| `gate_agm.py` | The three organs + the operator panel. | `HOOK_VERSION = v1`, runs at SessionStart, ~3.7s |
| `tests/test_gate_agm_afferent.py` | The Enóptron static guards + behavioural byte-identity check. | 14/14 |
| `tests/test_selftest_detects.py` | Proves the sensing detects real breaks rather than reporting green. | 6/6 |

Honest notes for whoever merges this:

- **Gut is doing less work here than in P1.** Over answers, Gut is a small model reacting to a
  draft. Over gates it is currently a rule over the problem set. It is the same *role* — one
  coarse, non-reasoning signal on the whole shape — but it is not the same *mechanism*, and the
  paper should not imply it is.
- **Metron is the organ that earned its place.** The instantaneous prober cannot tell a
  one-off from a standing condition; recurrence and drift are exactly the readings that
  distinguish them, and they only exist because the observer keeps history.
- **The system found a bug in itself on its first live run.** Registering the observer made it
  visible to the prober, which executed it, which invoked the prober — mutual recursion, both
  sides timing out. The panel reported it as an Aitía account; the fix was to check the
  observation stack for presence and syntax rather than executing it. Worth a sentence
  somewhere: the first thing a working self-model does is find something.
