---
id: dist-retries-idempotency-key
node: distributed.retries
type: qa
---
## Q
A publish request times out after the server may have committed. How should an idempotency key make retry safe?

## A
The client generates one stable key for the logical operation and reuses it on every attempt. The server atomically records key, request fingerprint, status, and result with the commit; duplicates with the same fingerprint return the stored result, while mismatched payloads are rejected. Retention must cover the retry window. A key stored after the side effect leaves a crash gap and is not true idempotency.

## Q zh
publish request timeout 时，server 可能已经 commit。idempotency key 应如何让 retry 安全？

## A zh
client 为一次 logical operation 生成稳定 key，并在所有 attempt 中复用。server 必须把 key、request fingerprint、status、result 与业务 commit 原子记录；相同 fingerprint 的 duplicate 返回已存结果，不同 payload 则 reject。retention 必须覆盖 retry window。若 side effect 之后才记录 key，就存在 crash gap，不是真正 idempotency。
