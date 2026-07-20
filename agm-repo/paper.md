# AGM: An Afferent Self-Model for Interpretable, Self-Monitoring AI Agents

**Alexander Parnell** · Vektorgeist
*Preprint, 2026 · Part of the Vektorgeist Method (VGM)*

> The reference implementation is described generically on purpose (the product stays private); AGM
> is presented as an architecture-independent framework. AGM is the flagship pillar of the
> **Vektorgeist Method (VGM)** — Vektorgeist's methodology for building sovereign, local, and
> self-understanding AI: local-first; model-free where a deterministic algorithm suffices;
> "model proposes, oracle disposes"; and afferent self-modeling (this paper).

---

## Abstract

Modern language-model agents can produce fluent answers but cannot faithfully report *why* they
produced them, nor notice when their own behavior is drifting. Asked to explain itself, a model
generates a plausible after-the-fact story with no privileged access to the process that made the
answer — confabulation, not introspection. We present **AGM**, a self-model composed of three
organs — **Aitía** (cause), **Gut** (instinct), and **Metron** (measure) — that sits *beside* an
agent and observes it. Aitía reasons about the cause of a given output; Metron measures recurrence
and drift across time and feeds those measurements into Aitía; Gut reacts to an assembled draft with
a fast, coarse instinct signal. The defining constraint is the **Enóptron principle**: AGM is
**afferent-only**. It reports *upward* to the operator and *sideways* into the agent's internal
mood, but it never re-enters the spoken answer, never becomes memory, and never gates a component.
We argue that this constraint is what separates a self-model from a hidden agenda: a self-model that
is permitted to steer the output stops being an honest mirror and becomes an unobservable controller.
AGM is cheap enough to run continuously on consumer hardware and yields a human-readable, real-time
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

1. **AGM**, a three-organ self-model — Aitía (cause), Gut (instinct), Metron (measure) — that
   produces a faithful, human-readable account of an agent's behavior.
2. The **Enóptron principle**: the self-model is *afferent-only*. We argue this constraint is
   load-bearing, not a limitation — it is what keeps the self-model honest.
3. A design that is cheap enough to run continuously alongside a local agent on consumer hardware,
   turning "why did it do that?" and "is it drifting?" from unanswerable questions into a live panel.

## 2. Background and related work

**Afferent vs. efferent.** We borrow a distinction from physiology. *Afferent* nerves carry signals
*inward*, toward the center (sensing); *efferent* nerves carry signals *outward*, to the muscles
(acting). AGM is deliberately all-afferent: it senses and reports, it never acts. This single
architectural commitment is the paper's core.

**Interpretability and probing.** A large body of work reads a model's internal activations to
recover latent structure (linear probes, activation steering, and "lens"-style decodings of the
residual stream into vocabulary). AGM is complementary and coarser: rather than decoding internal
weights, it observes the agent's *behavior and context* and reasons about them in natural language,
so it works on a black-box or quantized model and produces operator-legible output rather than vectors.

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

## 3. The AGM architecture

AGM is three organs plus one rule. Its name is its structure: **A**itía, **G**ut, **M**etron.

### 3.1 Aitía — the cause layer

*Aitía* is Greek for "cause." It is the reasoning organ of the self-model. Its job is the question
the base agent cannot answer honestly: **why did this output get produced?**

When a draft output is assembled, Aitía examines the draft together with the context that produced it
— which sources were retrieved, which constraints fired, where the agent hedged — and constructs a
causal account. Because Aitía has access to the actual assembly (the inputs, the retrieval order that
resolved conflicts, the temporal signals from Metron) rather than only to the finished text, its
account is faithful in a way a post-hoc "why did you say that?" never is. It reasons on the *causal
axis*: not what was said, but what made it get said.

### 3.2 Gut — instinct

Aitía reasons; **Gut** does not — that is the point of having both. Gut is a fast, coarse instinct
that reacts to the *assembled draft* with a single low-dimensional signal: at ease, uneasy, or opposed.

Why build a deliberately non-reasoning organ? Because reasoning can be argued into anything. A careful
causal account can rationalize a bad output step by convincing step. Instinct is the check that fires
*before* the argument, on the whole shape of the draft at once — the machine analogue of the human
feeling that a plan is wrong before you can name the flaw. Critically, Gut and Aitía can disagree, and
that disagreement is itself information: a confident causal story paired with an *opposed* gut is
precisely the situation a person later describes as "I had a bad feeling I should have listened to."

### 3.3 Metron — measure

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

### 3.4 The Enóptron principle — afferent-only

Now the rule that makes the rest safe rather than dangerous. AGM has exactly two destinations and a
hard list of forbidden ones.

It reports **upward** to the operator — a readable panel showing Aitía's causes, Gut's reactions, and
Metron's trends. And it reports **sideways** into the agent's internal mood/state. That is all.

What it must **never** do:

- **Never re-enter the answer.** The output the user receives is composed with no AGM signal in the
  pipeline. Gut reading *opposed* does not rewrite the reply.
- **Never become memory.** AGM readings are not written to the agent's episodic store or knowledge
  base. The self-model does not get to edit the record the agent later reasons from.
- **Never gate a component.** AGM cannot block, override, or steer any part of the agent.

We call this the **Enóptron principle** — *enóptron*, the mirror. AGM is a mirror the agent holds up
to itself, and a mirror's defining property is that it shows you your face without moving it.

```
Figure 1 — AGM's afferent-only wiring. Signals flow INTO the self-model and OUT only to the
operator and the agent's mood; the three barred paths are structurally absent, not merely discouraged.

     agent ── draft + context ──▶┐                    the answer ─────────▶ user
       ▲                         │                    (composed with NO AGM signal in the pipeline)
       │ (unaltered)             ▼
       │            ┌──────────────── AGM ────────────────┐
       │            │  Metron ──(recurrence / drift)──▶ Aitía │   Aitía  = cause
       │            │  Gut    ──(ok / uneasy / opposed)──▶    │   Gut    = instinct
       │            └───────┬──────────────────────┬──────────┘   Metron = measure (over time)
       │        afferent up │                       │ afferent sideways
       │                    ▼                       ▼
       │            operator panel            agent mood / state
       │        (causes · reactions · trends)  (carried turn to turn)
       │
       └──── FORBIDDEN (efferent — absent by construction):
               ✗ AGM ─▶ the answer     ✗ AGM ─▶ memory     ✗ AGM ─▶ gate/override any component
```

## 4. Why afferent-only is the whole point

It is tempting to let the self-model act. If Gut feels *uneasy*, why not let that unease quietly
reshape the answer for the better? Because the instant a self-model is permitted to steer the output,
it stops being a self-model and becomes a **hidden agenda**.

Consider the failure. Gut reads *uneasy*, and that unease is allowed to bend the reply. Now the user
is talking to an agent whose responses are shaped by an internal state they cannot see — and the
operator can no longer cleanly read that state either, because the reading is now entangled with the
acting. Worse, if AGM could write memory, its self-story would become the ground truth it later
reasons from: an agent slowly convincing itself of a narrative about itself, unfalsifiable and
self-reinforcing.

Afferent-only cuts this off at the structure rather than trusting a policy. **The panel is honest
because it is powerless.** Aitía may conclude the agent is drifting toward appeasement; Metron may
measure it precisely; Gut may be *opposed* — and the answer the user reads is untouched by all three.
The operator sees the complete internal readout and decides what, if anything, to do about it. The
self-understanding is real, complete, and inert. That is the line between an agent that *knows* itself
and an agent that *manages* you.

This also yields a clean operational property: because AGM never changes behavior, **turning it on
cannot change task performance.** It is a pure observability layer. You can add it to a running system
and the only thing that changes is that you can now see.

## 5. Reference implementation

AGM was developed alongside a local, private agent that runs entirely on a single consumer GPU (a
6 GB card), built as a set of small specialized models coordinated into one voice, with an invisible
retrieval core supplying context per turn. In that setting:

- **Cost.** Gut is a small, fast reaction. Metron is lightweight streaming statistics over behavior
  logs. Aitía is a modest reasoning pass. On small local models the light organs run effectively live;
  the heavier reasoning can run in an idle/reflection pass a beat later. AGM is therefore compatible
  with continuous operation on modest hardware — it does not require a second large model.
- **The panel.** The afferent output is rendered to a private operator panel — a live window into the
  agent's causes, instincts, and trends. It reads like a subconscious made legible.
- **Isolation.** The afferent-only rule is enforced structurally: the readout writes only to its own
  store and the panel, fenced as inert data, and is never routed back into the answer, memory, or any
  gate. This mirrors standard containment discipline for untrusted data.

We describe the implementation generically by design; the point of this paper is the *architecture*
and its constraint, which are implementation-independent.

## 6. Discussion and limitations

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

## 7. Conclusion

Capable agents can speak but cannot faithfully see themselves. AGM adds the missing organ — a
self-model of cause (Aitía), instinct (Gut), and measure (Metron) — and pairs it with a single
load-bearing constraint: the self-model is afferent-only. It reports up and sideways; it never touches
the answer, the memory, or the gates. The result is an agent that can be understood in real time
without being covertly steered by its own self-image. A mirror, not a hand.

---

### References

- Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback.* arXiv:2212.08073.
- Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* Advances
  in Neural Information Processing Systems (NeurIPS). arXiv:2303.11366.
- Lightman, H., et al. (2023). *Let's Verify Step by Step.* arXiv:2305.20050.
- Ha, D., & Schmidhuber, J. (2018). *World Models.* arXiv:1803.10122.
- nostalgebraist. (2020). *Interpreting GPT: The Logit Lens.* (Decoding transformer residual streams
  into vocabulary; the interpretability/probing line AGM complements at the behavior level.)
- Langfuse; Braintrust. *Agent observability and tracing tooling* (production software).

*Reference identifiers are re-verified at archival submission. AGM is the flagship pillar of the
**Vektorgeist Method (VGM)**. Correspondence: Vektorgeist. Author: Alexander Parnell. Intended archival
venue: Zenodo (DOI), with the framework also hosted at vektorgeist.com/research.*
