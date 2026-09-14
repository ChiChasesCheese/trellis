---
nodes:
- patterns.creational
title: 'Sealed constructors: when holding the object is the proof'
codebase: quant-stroller
ref: 4dae805d2955
artefact: contracts:.importlinter#protect-tradable-seal
---

# Sealed constructors: when holding the object is the proof

Some objects are permissions: holding one means a check was passed — this strategy is cleared to trade, this boot sequence reconciled, this batch was charged. The value only means something if it cannot be forged, so restrict construction to exactly one module. The constructor demands a sentinel that lives in a private module; everyone else must call that module's function and be refused when the check fails. Possession then *is* the proof, and downstream code can stop re-validating.

That rule needs enforcement, because any caller can import the sentinel and mint its own. A module-level import contract does it: the sentinel may be imported only by its minting module, and the layers most tempted to self-certify are named explicitly.

Two details decide whether the guard actually holds. Import-graph tools see modules, not symbols, so `from x import _SEAL` needs an extra syntactic check alongside. And the sanctioned door must stay open: forbidding the module that legitimately *calls* the minting function would forbid using the feature at all — the rule is "nobody mints their own permission", not "nobody may ask".

The cost is an awkward private module plus two checkers. The gain is that the bypass becomes structurally impossible rather than review-dependent.
