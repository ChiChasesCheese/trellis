---
id: reliability-load-cache-scenarios
node: reliability.load-testing
type: qa
---
## Q
A CDN passes a steady-state test with a 99% warm-cache hit ratio. Which additional scenarios are required before claiming origin protection?

## A
Test cold fleet start, regional cache loss, synchronized TTL expiry, one hot key, a long-tail object distribution, purge waves, and slow or failing origin. Measure goodput, queue depth, collapse ratio, origin concurrency, stale serving, and recovery time. Warm steady state proves the cheap path; reliability depends on transitions and miss amplification.

## Q zh
CDN 在 99% warm-cache hit ratio 的 steady-state test 中通过。还需要哪些 scenario，才能声称 origin protection 有效？

## A zh
测试 cold fleet start、regional cache loss、synchronized TTL expiry、single hot key、long-tail object distribution、purge wave，以及 slow 或 failing origin。测量 goodput、queue depth、collapse ratio、origin concurrency、stale serving 和 recovery time。warm steady state 只证明 cheap path；reliability 取决于 transition 和 miss amplification。
