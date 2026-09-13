---
id: runtime-openresty-request-phase
node: runtimes.lua-openresty
type: qa
---
## Q
Where should OpenResty authenticate, choose an upstream, and mutate response headers, and why does request-phase placement matter?

## A
Authenticate and reject early in access phase, choose or rewrite the upstream before proxying, and adjust response headers in header-filter phase. Body transformation belongs in body-filter only when unavoidable. Phase placement defines what data exists and whether upstream work has already happened; doing authorization late wastes origin capacity, while performing blocking or yielding work in a non-yieldable filter phase can break the request.

## Q zh
OpenResty 应分别在哪个 phase 做 authentication、upstream selection 和 response-header mutation？为什么 request-phase placement 很重要？

## A zh
在 access phase 尽早 authentication 并 reject；在 proxy 前选择或 rewrite upstream；在 header-filter phase 调整 response headers。只有无法避免时才在 body-filter 做 body transformation。phase placement 决定当时有哪些数据，以及 upstream work 是否已经发生；太晚 authorization 会浪费 origin 容量，而在不可 yield 的 filter phase 执行 blocking/yielding work 会破坏请求。
