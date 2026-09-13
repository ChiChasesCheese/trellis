---
id: reliability-testing-real-protocol
node: reliability.testing
type: qa
---
## Q
Unit tests mock the object store and all pass, but production mishandles conditional and range requests. What test boundary was missing?

## A
Add an integration test against a real protocol-compatible service or the actual dependency for `ETag`, conditional headers, `Range`, metadata, and error semantics. Keep fakes for fast local logic, but contract behavior owned by another system must be verified at the wire boundary. Record production-shaped fixtures so the exact failing header combinations become regression cases.

## Q zh
unit test mock 了 object store 且全部通过，但 production 错误处理 conditional 和 range request。缺少什么 test boundary？

## A zh
应针对真实 protocol-compatible service 或 actual dependency 增加 integration test，覆盖 `ETag`、conditional header、`Range`、metadata 和 error semantics。fake 继续用于快速验证 local logic，但由其他 system 拥有的 contract behavior 必须在 wire boundary 上验证。保存 production-shaped fixture，让实际失败的 header combination 成为 regression case。
