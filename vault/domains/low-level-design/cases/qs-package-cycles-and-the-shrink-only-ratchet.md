---
nodes:
- principles.coupling
title: Package cycles, and the exception list that may only shrink
codebase: quant-stroller
ref: 4dae805d2955
artefact: contracts:.importlinter#quant-acyclic-siblings
---

# Package cycles, and the exception list that may only shrink

Two packages that import each other are one package wearing two names: you cannot test, release, reason about, or delete either alone, and the cycle only tightens with time. The acyclic-dependency principle says sibling packages should form a DAG, and a checker can prove that on every commit. Breaking a discovered cycle is a choice of which edge to reverse — usually by sinking a shared type into a lower module, or by having the lower module accept a callback instead of importing the higher one.

The interesting part is what to do with the cycles that already exist. Failing the build outright means the check never lands; deleting the check means it never helps. The middle path is a ratchet: enumerate the existing cycle-closing edges as explicit exceptions, forbid any new one, and require each exception to name the ticket that will remove it. The list may only shrink.

That makes debt visible, bounded and attributable instead of ambient, and turns an all-or-nothing cleanup into background work. The cost is that a ratchet with no owner quietly becomes permanent — if nobody ever reviews the list, you have merely written the tangle down in a tidier font.
