---
id: delivery-cicd-reproducible
node: delivery.cicd
type: qa
---
## Q
Two builds from the same source produce different static asset hashes. Why must the release stop?

## A
Content-addressed names drive long-lived immutable caching, so nondeterministic output creates needless cache misses and makes provenance or rollback ambiguous. Diff the artifacts and remove uncontrolled inputs such as time, file order, locale, network-fetched dependencies, or unpinned tools. If nondeterminism is intentional, isolate and document it rather than pretending the build is reproducible.

## Q zh
同一 source 的两次 build 产生不同 static asset hash。为什么必须停止 release？

## A zh
content-addressed name 会驱动长期 immutable caching，因此 nondeterministic output 会制造不必要的 cache miss，并让 provenance 或 rollback 变得模糊。diff artifact，移除 time、file order、locale、network-fetched dependency 或 unpinned tool 等 uncontrolled input。如果 nondeterminism 是有意的，就应隔离并记录，而不是假装 build 可重复。
