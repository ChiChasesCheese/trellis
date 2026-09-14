---
nodes:
- quality.smells
title: Dead code needs positive evidence, not silence
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0013-deletion-requires-retired-outdated-duplicate
---

# Dead code needs positive evidence, not silence

Static reachability is only as trustworthy as your model of who the callers are. A dead-code sweep that counts importers across a repository will confidently delete anything reached by reflection, plugin registries, notebooks, operators at a REPL — or, increasingly, agents that import a helper, take a result, and leave no committed caller behind. Absence of evidence of life is not evidence of death: here the naive criterion nominated tens of thousands of lines and roughly half had to be restored.

The durable fix is to require positive evidence in named categories. RETIRED: a decision record says so, or the engine it depends on is gone, or another implementation supersedes it wholesale. OUTDATED: it points at infrastructure that is dead, or was a one-shot migration that has already run. DUPLICATE: a second implementation exists and is demonstrably equivalent, with the comparison published.

"Nobody imports it" is explicitly not a fourth category. A zero-importer module that people call on demand is a capability; the answer is to register its role in a generated module map so the next reader does not have to guess from the import graph. Moving it out of the importable namespace counts as deleting it for those callers.

The cost is honest: a permanent population of zero-importer modules, and line count retired as a progress metric.
