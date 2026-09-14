---
nodes:
- principles.coupling
title: Forbidding the edge to the dangerous layer
codebase: quant-stroller
ref: 4dae805d2955
artefact: contracts:.importlinter#forbid-alpha-to-execution
---

# Forbidding the edge to the dangerous layer

When research code can reach the execution layer directly, a stray experiment can place a live order — and worse, the live path silently diverges from the measured one, because the bypass is invisible: nothing about it looks different from ordinary code. The remedy has two halves. Name one sanctioned route (every order is expressed as a registered declarative spec that the execution layer consumes), then forbid the edge itself so the shortcut cannot even be written.

A forbidden-import contract is the cheapest form of this. It converts a review convention — "please don't call the broker from a signal module" — into a build failure, and it holds against contributors and code generators who never read the convention. What you buy is one audit point and one place to enforce risk limits: every order that exists passed through the same door.

What you pay is a serialization boundary in the hot path and a permanent tax on convenience. The signal side can no longer ask the venue a question directly, so anything it genuinely needs — fees, lot sizes, current positions — must be passed into it or lifted into a lower shared module. That tax is the point: it forces coupling to be declared rather than improvised.
