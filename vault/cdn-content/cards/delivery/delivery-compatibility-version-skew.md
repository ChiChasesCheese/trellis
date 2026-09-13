---
id: delivery-compatibility-version-skew
node: delivery.compatibility
type: qa
---
## Q
A rolling update changes both cache-key construction and response metadata. Which version-skew test is essential?

## A
Exercise every supported old/new interaction: old writer with new reader, new writer with old reader, and requests crossing old and new nodes through shared cache. Assert representation safety and rollback, not merely parse success. If mixed versions cannot safely share entries, namespace the cache by policy/deployment version until the fleet converges.

## Q zh
rolling update 同时改变 cache-key construction 和 response metadata。哪个 version-skew test 必不可少？

## A zh
覆盖所有支持的 old/new interaction：old writer + new reader、new writer + old reader，以及 request 通过 shared cache 跨越 old/new node。断言 representation safety 和 rollback，而不只是 parse success。如果 mixed version 无法安全共享 entry，就按 policy/deployment version namespace cache，直到 fleet 收敛。
