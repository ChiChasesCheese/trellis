---
id: reliability-logging-request-event
node: reliability.logging
type: qa
---
## Q
A user reports one wrong CDN response. Which fields make a request log useful for reconstructing the serving decision without dumping the whole request?

## A
Record a stable request ID, timestamp, deployment/config version, client and compute region, normalized route, cache outcome and tier, hashed or bounded cache-key fingerprint, origin target, status, bytes, latency phases, revalidation state, and error class. The event should explain the decision path while excluding secrets and uncontrolled payloads.

## Q zh
用户报告一次错误的 CDN response。哪些字段能让 request log 重建 serving decision，同时避免 dump 整个 request？

## A zh
记录 stable request ID、timestamp、deployment/config version、client 与 compute region、normalized route、cache outcome 与 tier、hashed 或 bounded cache-key fingerprint、origin target、status、bytes、latency phase、revalidation state 和 error class。event 应能解释 decision path，同时排除 secret 和 uncontrolled payload。
