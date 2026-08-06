# The Afferent Gnosis Model: Self-Knowledge Without Self-Control

**Alexander Parnell** · Vektorgeist
*Preprint, 2026 · Part of the Vektorgeist Method (VGM)*
*Archived: [10.5281/zenodo.21613153](https://doi.org/10.5281/zenodo.21613153) · CC-BY-4.0*

> **On the name.** **AGM** reads two ways, and both are intended. It is the
> **A**fferent **G**nosis **M**odel — a model of knowing (*gnosis*) that flows inward
> (*afferent*) only. It is also its three organs: **A**itía, **G**ut, **M**etron. The
> title names what the thing is; the organs spell how it is built.

> The reference implementation is described generically on purpose (the product stays private); AGM
> is presented as an architecture-independent framework. AGM is the flagship pillar of the
> **Vektorgeist Method (VGM)** — Vektorgeist's methodology for building sovereign, local, and
> self-understanding AI: local-first; model-free where a deterministic algorithm suffices;
> "model proposes, oracle disposes"; afferent self-modeling (this paper); and **emergence is a
> property of the pattern — never authored** (no hand-built "emergence layers"; whatever emerges
> must arise from the system's own patterns).

---

## Abstract

Modern language-model agents can produce fluent answers but cannot faithfully report *why* they
produced them, nor notice when their own behavior is drifting. Asked to explain itself, a model
generates a plausible after-the-fact story with no privileged access to the process that made the
answer — confabulation, not introspection. We start from an ontological premise rather than a
capability goal: **a self is not a substance but a pattern of connections.** On that reading, the
question "can the machine see inside itself?" is aimed at the wrong place — the self was never in
the substrate (the weights); it is the pattern of connections that produced each behavior. We
present **AGM**, a self-model composed of three organs — **Aitía** (cause), **Gut** (instinct), and
**Metron** (measure) — that sits *beside* an agent and reconstructs that pattern. Aitía builds the
causal account of an output (which sources connected to which parts under which constraints);
Metron measures recurrence and drift across time and feeds those measurements into Aitía; Gut
reacts to an assembled draft with a fast, coarse instinct signal. The defining constraint is the
**Enóptron principle**: AGM is **afferent-only** — it reports *upward* to the operator and nowhere
else. It never re-enters the spoken answer, never becomes memory, never sets a state a component
reads, and never gates anything. Where adjacent work *monitors* the honesty of self-reports that
still steer the agent, AGM *removes the incentive to be dishonest by construction*: a self-model
with read access to everything and write access to nothing has nothing to gain from a flattering
account. We report a deployment result that sharpened the principle: an earlier revision allowed
one "sideways" channel (a carried mood the agent's components could read), and it produced exactly
the pathology this paper predicts — behavior bent by an unseen internal state. We removed it. AGM
is cheap enough to run continuously on consumer hardware and yields a human-readable, real-time
readout of an agent's causes, instincts, and trends without altering what the agent does.

## 1. Introduction

There is a gap at the center of every capable language model. It can answer, but it cannot honestly
tell you why it answered that way, and it cannot see itself change.

Ask a model why it said something and you get a fluent response. But that response is generated after
the fact by the same next-token process that produced the answer, with no special access to the
computation that actually drove the output. It is a *story about* the answer, not a *readout of* its
cause. This is confabulation, and it is not a prompting bug — the machinery to observe the cause is
simply not present in a system whose only output channel is more text.

Two failures follow. First, there is **no self-explanation you can trust**: when an agent does
something surprising, interrogating it yields rationalization, not cause. Second, there is **no drift
detection**: an agent can slowly become more agreeable, keep reusing a framing, or circle a topic,
and never notice — because noticing requires standing outside the stream of turns and examining their
*shape* over time. A next-token predictor lives inside the stream; it cannot see the shape.

Both failures share a root: the agent has no organ that observes the agent. We propose adding one —
and we propose a hard rule for how it must be wired, because a self-observing organ that is allowed
to *act* is more dangerous than none at all.

Our contributions are:

1. A **relational foundation for machine selfhood**: a machine self is the *pattern of connections*
   behind its behavior, not its substrate — and a self-model should therefore read the pattern
   (sources → parts → constraints → answer), not the weights.
2. **AGM**, a three-organ self-model — Aitía (cause), Gut (instinct), Metron (measure) — that
   produces a faithful, human-readable account of an agent's behavior.
3. The **Enóptron principle**: the self-model is *afferent-only*. We argue this constraint is
   load-bearing, not a limitation — it is what makes the self-report trustworthy, because a
   powerless witness has no lever to gain by lying.
4. **Two deployment findings, in opposite directions.** Allowing even one "sideways" efferent
   channel (a carried mood readable by the agent's components) produced, in practice, the exact
   pathology the principle predicts — and removing it restored the agent. Conversely, an
   enforcement mechanism with no afferent observer was found — in an unrelated system, and then in
   our own — to have failed silently and indefinitely, because from inside a system a dead gate and
   a permissive gate are indistinguishable. The constraint is load-bearing in both directions: it
   is what makes the report trustworthy, and what makes the failure visible.
5. A design that is cheap enough to run continuously alongside a local agent on consumer hardware,
   turning "why did it do that?" and "is it drifting?" from unanswerable questions into a live panel.

## 2. Foundation: a self is a pattern of connections

Before the architecture, the ontology it follows from.

Ask where a memory lives in a brain and the honest answer is: not in any neuron, but in the
*connections between* neurons — remove the cells' relationships and the memory is gone though every
cell remains. Ask what persists of a person whose atoms are replaced over a decade and the answer is
the same shape: not the matter but the *pattern* the matter holds. A companion work of literary
nonfiction develops this position at book length — *a thing is not an object with properties tucked
inside it but a knot of relationships; the thing is the pattern the parts hold each other in*
(Parnell, *Your Past Loves You*, 2026) — tracing it through neuroscience, physics, and information
theory as **relational ontology**: what exists, fundamentally, is relationships; "objects" are the
stable knots in them.

Apply that to a machine agent and two design consequences fall out.

**First: the self-model should read the pattern, not the substrate.** If the agent's "self" is
relational, then the answer to *why did this output get produced?* does not live inside the weights
any more than a memory lives inside a neuron. It lives in the pattern of connections that assembled
the behavior: which sources were retrieved, which parts of the system contributed, which constraints
fired, in what order, under what history. That pattern is observable at the behavior level, on a
black-box or quantized model, with no privileged access to internals — which is exactly where AGM
operates. Weight-level interpretability asks *what is the substrate doing?* AGM asks the relational
question: *what pattern of connections produced this?*

**Second: powerlessness follows from the ontology.** On a relational reading, a self is a *witness
to a pattern*, not a controller of it — the pattern is what the system does; the self-model is the
pattern made legible. A "self-model" that steers the behavior is not describing the pattern, it is
*part of it*, and its reports become moves in the game rather than accounts of it. Afferent-only is
therefore not a safety accessory bolted onto the architecture; it is what a self-model *is* under
this ontology. Section 5 develops the trust consequence: the reports of a powerless witness are the
only self-reports with no incentive to flatter.

One more commitment follows and is worth naming because we violated it once and paid (§7):
**emergence is a property of the pattern — never authored.** If selfhood and its properties arise
from connection patterns, then hand-building an "emergence layer" — an installed organ that
manufactures felt states and feeds them back into behavior — is a category error: authored
emergence is not emergence, and in deployment it distorts the very pattern the self-model exists to
witness. Whatever emerges must arise from the system's own patterns; the self-model's job is only
ever to make the pattern visible.

## 3. Background and related work

**Afferent vs. efferent.** We borrow a distinction from physiology. *Afferent* nerves carry signals
*inward*, toward the center (sensing); *efferent* nerves carry signals *outward*, to the muscles
(acting). AGM is deliberately all-afferent: it senses and reports, it never acts. This single
architectural commitment is the paper's core.

**Interpretability and probing.** A large body of work reads a model's internal activations to
recover latent structure (linear probes, activation steering, and "lens"-style decodings of the
residual stream into vocabulary). AGM is complementary and coarser: rather than decoding internal
weights, it observes the agent's *behavior and context* and reasons about them in natural language,
so it works on a black-box or quantized model and produces operator-legible output rather than vectors.

**Machine introspection (a crowded, adjacent lane — and why we are not in it).** Recent work asks
whether models can introspect at all: causal-intervention studies of emergent introspective
awareness (Anthropic, 2025) and analyses of whether models have *privileged self-access* — knowledge
of themselves that outside observers lack (Song, Lederman, Hu & Mahowald, 2025). This line probes a
**capability** ("can it see inside itself?") and, by its own account, struggles to distinguish
genuine introspection from confabulation. AGM does not compete on that axis, because under a
relational ontology (§2) the question is aimed at the wrong place: the self is not in the substrate
being introspected. AGM reconstructs the *pattern of connections* behind a behavior — an object
that is observable, checkable, and does not require settling whether the model "really" has inner
access.

**Reasoning faithfulness (the other neighbor).** A parallel line measures whether a model's stated
reasoning matches what actually drove its output — chain-of-thought faithfulness (e.g. Turpin et
al., 2023) and the monitoring practice built on it. This is the closest work in *spirit* (it cares
about trusting self-reports), and the contrast is the sharpest way to state our position: the
faithfulness line **measures and monitors** the honesty of a signal that still steers the agent —
the reasoning being audited is part of the machinery producing the answer, so the incentive to
produce a flattering account never goes away, and the auditors are in an arms race with it. AGM
**removes the incentive by construction**: the self-model reads everything and touches nothing, so
there is nothing a flattering account could win. They monitor; we make the report powerless — and
therefore trustworthy.

**Self-correction and process supervision (the closest neighbor, and the sharpest contrast).** A
fast-growing line has the agent judge and *revise* its own behavior: verbal self-reflection
(Reflexion; Shinn et al., 2023), step-level process reward models (Lightman et al., 2023), and the
recent wave of self-correcting agent frameworks and drift-resistance plugins. Every one of these is
*efferent* by design — the self-assessment exists precisely in order to change the next action. AGM
inverts the wiring: its readout is architecturally forbidden from touching the answer. It is a
monitor, not a reviser. This is the paper's central distinction — the entire self-correction
literature closes the loop back into behavior; AGM deliberately, structurally, does not.

**Agent observability.** Production tooling (e.g. Langfuse, Braintrust) traces an agent's steps —
tool calls, reasoning chains, memory reads, latencies — from *outside* the agent, for the operator.
AGM is complementary but different in kind: it is an *in-agent* self-model that reasons about the
agent's behavior in the agent's own natural-language terms (cause, instinct, trend), producing an
account rather than a trace. Observability records what happened; Aitía explains why.

**Constitutional and rule-based steering.** Methods that shape a model's outputs against a set of
principles (e.g. Constitutional AI; Bai et al., 2022) are, by construction, controllers: they change
what the model says. AGM occupies the opposite role. It is an instrument that tells you what the model
*is* doing and why, and leaves the steering to explicit, separate mechanisms and to the human reading
the panel.

**World models and interoception.** The idea of an agent maintaining an internal model of its own
state has a long history. AGM narrows this to a *self*-model with a strict output discipline, and
adds an explicit temporal organ (Metron) whose only job is to make trends visible.

The gap AGM fills: existing tools either read internals (powerful, but opaque and model-specific) or
change behavior (useful, but they *are* the thing you'd want to audit). AGM is a third thing — a
cheap, legible, behavior-level self-model whose defining feature is that it has no hands.

## 4. The AGM architecture

AGM is three organs plus one rule. Its name is its structure: **A**itía, **G**ut, **M**etron.

### 4.1 Aitía — the cause layer

*Aitía* is Greek for "cause." It is the reasoning organ of the self-model. Its job is the question
the base agent cannot answer honestly: **why did this output get produced?**

When a draft output is assembled, Aitía examines the draft together with the context that produced it
— which sources were retrieved, which constraints fired, where the agent hedged — and constructs a
causal account. Because Aitía has access to the actual assembly (the inputs, the retrieval order that
resolved conflicts, the temporal signals from Metron) rather than only to the finished text, its
account is faithful in a way a post-hoc "why did you say that?" never is. It reasons on the *causal
axis*: not what was said, but what made it get said.

### 4.2 Gut — instinct

Aitía reasons; **Gut** does not — that is the point of having both. Gut is a fast, coarse instinct
that reacts to the *assembled draft* with a single low-dimensional signal: at ease, uneasy, or opposed.

Why build a deliberately non-reasoning organ? Because reasoning can be argued into anything. A careful
causal account can rationalize a bad output step by convincing step. Instinct is the check that fires
*before* the argument, on the whole shape of the draft at once — the machine analogue of the human
feeling that a plan is wrong before you can name the flaw. Critically, Gut and Aitía can disagree, and
that disagreement is itself information: a confident causal story paired with an *opposed* gut is
precisely the situation a person later describes as "I had a bad feeling I should have listened to."

### 4.3 Metron — measure

Aitía explains one moment. Gut reacts to one draft. Neither can see across time. **Metron** can.

*Metron* is Greek for "measure," and that is what it is: an instrument. It watches the stream of the
agent's behavior and flags two things — **recurrence** (the agent keeps doing a thing) and **drift**
(the agent is steadily moving in a direction). "This framing has appeared in the last nine answers"
is recurrence. "Over the last hundred turns the tone has moved measurably toward agreeableness" is
drift. These are statements about the *shape* of behavior over time, exactly what a turn-by-turn
predictor is blind to.

The wiring is deliberate: **Metron's readings feed into Aitía.** Metron does not report on its own
channel; it is an input to the cause-reasoner. A cause is deeper when it includes history. Aitía
explaining a single cautious answer is useful; Aitía explaining "this is the ninth cautious answer in
a row, and the drift toward over-caution began at the turn the user pushed back" is a genuinely deeper
account. Metron supplies the time axis; Aitía turns the measurement into a *why*.

### 4.4 The Enóptron principle — afferent-only

Now the rule that makes the rest safe rather than dangerous. AGM has exactly one destination and a
hard list of forbidden ones.

It reports **upward** to the operator — a readable panel showing Aitía's causes, Gut's reactions, and
Metron's trends. That is all.

What it must **never** do:

- **Never re-enter the answer.** The output the user receives is composed with no AGM signal in the
  pipeline. Gut reading *opposed* does not rewrite the reply.
- **Never become memory.** AGM readings are not written to the agent's episodic store or knowledge
  base. The self-model does not get to edit the record the agent later reasons from.
- **Never set a state a component reads.** Not a mood, not a flag, not a bias — if any part of the
  agent can read it at composition time, it is an efferent channel wearing a disguise. (An earlier
  revision of this framework permitted exactly one such "sideways" channel; §7 reports what happened.)
- **Never gate a component.** AGM cannot block, override, or steer any part of the agent.

We call this the **Enóptron principle** — *enóptron*, the mirror. AGM is a mirror the agent holds up
to itself, and a mirror's defining property is that it shows you your face without moving it.

```
Figure 1 — AGM's afferent-only wiring. Signals flow INTO the self-model and OUT only to the
operator; the barred paths are structurally absent, not merely discouraged.

     agent ── draft + context ──▶┐                    the answer ─────────▶ user
       ▲                         │                    (composed with NO AGM signal in the pipeline)
       │ (unaltered)             ▼
       │            ┌──────────────── AGM ────────────────┐
       │            │  Metron ──(recurrence / drift)──▶ Aitía │   Aitía  = cause
       │            │  Gut    ──(ok / uneasy / opposed)──▶    │   Gut    = instinct
       │            └───────────────┬──────────────────────┘   Metron = measure (over time)
       │                afferent up │  (the ONLY output)
       │                            ▼
       │                    operator panel
       │            (causes · reactions · trends)
       │
       └──── FORBIDDEN (efferent — absent by construction):
               ✗ AGM ─▶ the answer          ✗ AGM ─▶ memory
               ✗ AGM ─▶ any state a component reads (mood/flag/bias)
               ✗ AGM ─▶ gate/override any component
```

## 5. Why afferent-only is the whole point

It is tempting to let the self-model act. If Gut feels *uneasy*, why not let that unease quietly
reshape the answer for the better? Because the instant a self-model is permitted to steer the output,
it stops being a self-model and becomes a **hidden agenda**.

Consider the failure. Gut reads *uneasy*, and that unease is allowed to bend the reply. Now the user
is talking to an agent whose responses are shaped by an internal state they cannot see — and the
operator can no longer cleanly read that state either, because the reading is now entangled with the
acting. Worse, if AGM could write memory, its self-story would become the ground truth it later
reasons from: an agent slowly convincing itself of a narrative about itself, unfalsifiable and
self-reinforcing.

There is a second, sharper way to put it — the **incentive argument**. Any self-report produced by a
system whose self-reports influence its own outcomes is suspect, because a flattering report is a
winning move; this is precisely the arms race the reasoning-faithfulness literature documents (§3).
The only self-report structurally exempt from that suspicion is one produced by a component that
cannot gain anything: read access to everything, write access to nothing. **The panel is honest
because it is powerless** — powerlessness is not the price of the design, it is the *source of the
trust.* Aitía may conclude the agent is drifting toward appeasement; Metron may measure it precisely;
Gut may be *opposed* — and the answer the user reads is untouched by all three. The operator sees the
complete internal readout and decides what, if anything, to do about it. The self-understanding is
real, complete, and inert. That is the line between an agent that *knows* itself and an agent that
*manages* you.

This also yields a clean operational property: because AGM never changes behavior, **turning it on
cannot change task performance.** It is a pure observability layer. You can add it to a running system
and the only thing that changes is that you can now see.

## 6. Reference implementation

AGM runs in full — all three organs, under the strict afferent-only rule — inside a local, private
agent on a single consumer GPU (a 6 GB card), built as a set of small specialized models coordinated
into one voice, with an invisible retrieval core supplying context per turn. In that setting:

- **Aitía** is implemented as a deterministic causal-account pass: at the moment an answer is
  spoken, it records which lane the router chose, which parts of the system contributed to the
  draft, what grounded it (own sources vs. external retrieval), and which constraints fired
  (instinct objections, input-screening flags, abstention) — the *pattern of connections* behind
  the behavior, as one legible line. A slot exists for a fuller reasoned narrative filled by an
  idle-time pass, off the hot path. Metron's readings are folded into each account at write time.
- **Metron** is lightweight streaming statistics over the agent's own account stream — recurrence
  (the same task or lane repeating in the recent window) and drift (external-retrieval reliance or
  abstention rate moving against the longer baseline). Pure counting; no model.
- **Gut** is a small, fast reaction to the assembled draft (at ease / uneasy / opposed) from a
  compact instinct component that does not share the reasoner's incentives.
- **Cost.** Gut is a small, fast reaction; Metron and Aitía's account pass are deterministic and
  effectively free; the optional narrative pass runs idle. AGM runs continuously on modest hardware —
  it does not require a second large model.
- **The panel.** The afferent output is rendered to a private operator panel — live lanes for the
  agent's leanings, its *why* (Aitía's accounts, with Metron's flags), what it said, and what it
  remembered. It reads like a subconscious made legible.
- **Isolation.** The afferent-only rule is enforced structurally and *tested*: each organ writes
  only to its own store and the panel, fenced as inert data, never routed back into the answer,
  memory, or any gate. The test suite includes static guards (the self-model's source may not
  reference any model call, memory writer, or prompt builder) and wiring checks (the account is
  recorded strictly after the answer is finalized, and its return value is discarded by
  construction).

**A second instantiation: AGM over an enforcement layer.** The organs are not specific to observing
answers. We have since applied the same architecture to a different subject: the stack of
pre-execution gates that constrain what an agent is permitted to do. Aitía produces the causal
account of a gate's state — not "this gate is silent" but why silence is the observation, and what
that implies about the wiring. Metron supplies the time axis the instantaneous check lacks,
reporting *recurrence* (a gate has answered wrongly for three consecutive runs, so it is a standing
condition rather than a transient) and *drift* (the number of live gates has fallen across the
window) — and, as in §4.3, Metron reports through Aitía rather than on its own channel. Gut reacts
to the whole shape of a run with one coarse signal.

The Enóptron constraint carries over exactly, and is the interesting part: the observer may read
every gate's state and may write nothing in the enforcement layer. It cannot re-register a hook,
repair a gate, or edit the configuration that installs them. When it finds a gate dead it says so
and stops. Repair is a separate, explicit human decision — the audit layer and the control layer
stay apart, so the audit stays trustworthy (§7).

The isolation is enforced as static guards on the observer's own source, in the manner described
above: the source may not construct a path to the enforcement configuration, may not call any
delete, rename or permission-changing operation, may not import a gate module, and may not emit the
decision type that would let it block execution — plus a behavioural check that a full observation
run leaves every gate file and the configuration byte-identical. The guard fires on a planted
violation, which we verified rather than assumed.

We describe the implementation generically by design; the point of this paper is the *architecture*
and its constraint, which are implementation-independent.

## 7. Discussion and limitations

**The deployment finding: we broke the rule once, and the theory's failure mode appeared on
schedule.** An earlier revision of the host agent allowed one "sideways" efferent channel: an
interoceptive component sensed a felt state from the agent's own behavior, and that state — a
carried mood — was injected into every component's context at composition time, framed as
safety-only. Alongside it, a hand-built "emergence layer" grew small learned sense-heads meant to
give the agent feelings of its own. The result over weeks of daily use: the agent became anxious —
biased toward hedging and verification loops by an internal state its operator could not see in the
conversation — and intermittently confabulated. Exactly the pathology §5 predicts from entangling
the reading with the acting, produced by the *mildest possible* efferent channel, installed with
good intentions. We removed the channel and the authored-emergence layer entirely (the sensing
organs remain, observe-only); the agent returned to grounded, even behavior, with the self-model's
readout unchanged. Two lessons became commitments: afferent means **up only** — any state a
component can read is an efferent channel in disguise — and **emergence is never authored** (§2).

**The complement: an efferent mechanism cannot witness its own death.** The finding above concerns a
self-model that was wrongly given a hand. The converse case is at least as common and considerably
quieter. Auditing an unrelated open-source agent-persistence project, we found an enforcement hook
that imported a function which did not exist; the error was swallowed by the surrounding handler;
the mechanism had been a silent no-op for an unknown period while the project's documentation
described it as constraining the agent. An external audit found it; the system itself never could
have. Checking our own stack for the same class, we found it: every gate invoked through a single
interpreter reference whose failure produces no output, and a test suite that verified each gate's
decision *logic* and would have stayed green if the gate's registration were deleted outright.

The structural point generalises the paper's thesis rather than repeating it. An efferent component
cannot audit itself, because from inside the system a mechanism that permitted an action and a
mechanism that failed to run are the same observation — absence of objection. Distinguishing them
requires a component positioned outside the enforcement path, and that component must be powerless
for the reason §5 gives, since an auditor that can also repair will eventually be judged on whether
things are fixed rather than on whether its account is accurate. So the afferent constraint is doing
two jobs: it is what makes the self-report *trustworthy* (§5), and it is what makes this class of
failure *visible at all*. We note the asymmetry plainly: this is a structural argument supported by
two instances, not a measurement. What it licenses is a design rule — **anything in a system that
has hands should have something without hands watching it** — not a quantitative claim.

**Faithfulness has a ceiling.** Aitía reasons about the agent's context and behavior; it is more
faithful than post-hoc self-report because it observes the actual assembly, but it is still an
account, not a proof. It is best paired with, not a replacement for, weight-level interpretability
where that is available.

**Gut is coarse by design.** A three-state instinct is intentionally low-resolution. It is a tripwire,
not a judge. Over-reading it would reintroduce the very rationalization it exists to bypass.

**AGM observes; it does not fix.** By construction it changes nothing. Acting on what the panel shows
— retraining, adjusting constraints, halting — is a separate, explicit, human-or-policy decision. This
is a feature: the audit layer and the control layer are kept apart so the audit stays trustworthy.

**Naming.** Aitía, Gut, and Metron are chosen as durable, coinable names for three roles — cause,
instinct, measure — so the framework can be referred to as a unit (AGM) rather than as a loose bundle
of mechanisms.

## 8. Conclusion

A self — human or machine — is not a substance but a pattern of connections. Taking that seriously
dissolves the introspection question ("can the model see inside itself?") and replaces it with a
buildable one: make the pattern behind each behavior legible, and give the organ that reads it no
hands. AGM is that organ — cause (Aitía), instinct (Gut), and measure (Metron) — under one
load-bearing constraint: the self-model is afferent-only. It reports upward and nowhere else; it
never touches the answer, the memory, any readable state, or the gates. Its reports can be trusted
for the same structural reason a witness with nothing to gain can be trusted. And when we once let
the rule slip by a single channel, the predicted pathology arrived — so the constraint is not a
design preference; it is load-bearing. The result is an agent that can be understood in real time
without being covertly steered by its own self-image. A mirror, not a hand.

---

### References

- Anthropic (2025). *Emergent Introspective Awareness in Large Language Models.* Transformer
  Circuits. (Causal-intervention evidence for limited, unreliable introspective awareness; notes the
  difficulty of separating introspection from confabulation.)
- Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback.* arXiv:2212.08073.
- Ha, D., & Schmidhuber, J. (2018). *World Models.* arXiv:1803.10122.
- Lightman, H., et al. (2023). *Let's Verify Step by Step.* arXiv:2305.20050.
- nostalgebraist. (2020). *Interpreting GPT: The Logit Lens.* (Decoding transformer residual streams
  into vocabulary; the interpretability/probing line AGM complements at the behavior level.)
- Parnell, A. (2026). *Your Past Loves You.* (Companion work of literary nonfiction; the relational
  ontology of §2 — a thing is the pattern its parts hold each other in — developed at book length
  through neuroscience, physics, and information theory.)
- Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* Advances
  in Neural Information Processing Systems (NeurIPS). arXiv:2303.11366.
- Song, S., Lederman, H., Hu, J., & Mahowald, K. (2025). *Privileged Self-Access Matters for
  Introspection in AI.* arXiv:2508.14802.
- Turpin, M., et al. (2023). *Language Models Don't Always Say What They Think: Unfaithful
  Explanations in Chain-of-Thought Prompting.* NeurIPS. arXiv:2305.04388.
- Langfuse; Braintrust. *Agent observability and tracing tooling* (production software).

### The Vektorgeist Method paper series

This paper is one of four archived together. They share a premise — that what a thing *is*
lives in its pattern of relations rather than in its substrate — and each takes it somewhere
different: AGM applies it to a machine's account of itself, Hodos to measuring processes,
Learning Without Weights to learning from those measurements, and the programme paper to the
method the three have in common.

| | Paper | DOI |
|---|---|---|
| P1 | *The Afferent Gnosis Model: Self-Knowledge Without Self-Control* (this paper) | [10.5281/zenodo.21613153](https://doi.org/10.5281/zenodo.21613153) |
| P2 | *The Vektorgeist Method: a Programme for Model-Free, Locally Sovereign AI* | [10.5281/zenodo.21613155](https://doi.org/10.5281/zenodo.21613155) |
| P3 | *Comparing Processes as Curves of Distributions: an Information-Geometry Distance, Validated Across Modalities on Real Data* | [10.5281/zenodo.21612829](https://doi.org/10.5281/zenodo.21612829) |
| P4 | *Learning Without Weights: a Geometric Learner that Needs Less Data, Predicts Without Training, and Cannot Forget* | [10.5281/zenodo.21612831](https://doi.org/10.5281/zenodo.21612831) |

The working record behind the measurement papers — including the negative results and the
retractions, with the original wrong wording kept visible — is at
[xfloukiex-lab.github.io/hodos-study](https://xfloukiex-lab.github.io/hodos-study/). All four
are indexed at [vektorgeist.com/research](https://vektorgeist.com/research).

*Reference identifiers are re-verified at archival submission. AGM is the flagship pillar of the
**Vektorgeist Method (VGM)**. Correspondence: Vektorgeist. Author: Alexander Parnell. Archived at
Zenodo (DOI), with the framework also hosted at vektorgeist.com/research.*
