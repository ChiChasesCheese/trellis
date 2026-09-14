---
nodes:
- structure.state-machines
title: A durable phase machine that decides nothing
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0007-research-loop-checkpoint-hitl-wrap-cli
---

# A durable phase machine that decides nothing

A long-lived process with human checkpoints is far easier to reason about as an explicit state machine than as a script with flags.

Three parts do the work. A fixed tuple of phases is the single source of order, so "what comes next" is data rather than control flow scattered across functions. A durable checkpoint holds current phase, status, and an append-only history, giving crash resumption and replay — and it is the history, not the current value, that makes an incident reviewable afterwards. Human approval is modelled as a state, not a boolean: after certain phases the machine parks in an `awaiting-approval` state and the tick function refuses to advance until an explicit approval with a note is recorded.

The important constraint is what the orchestrator is allowed to know. It wraps existing entry points and reads only their exit codes; it never re-implements a decision it sequences. The moment sequencing code also computes a verdict, that verdict has two implementations, they will diverge, and the one users see will be the wrong one.

Phases with no automation yet are wired as empty steps that stop for a human. The funnel's shape is therefore complete before its automation is, and a later change can fill in a step without renegotiating the order.
