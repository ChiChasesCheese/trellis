---
id: reliability-testing-production-fixture
node: reliability.testing
type: qa
---
## Q
A cache-key bug appears only for real mobile requests with duplicated headers and unusual query ordering. How should the regression test be built without copying user data?

## A
Reduce the request to the smallest synthetic fixture that preserves the decisive structure: duplicate-field behavior, normalization, encoding, and query order. Remove credentials and payloads, document which production property each field represents, and assert both key output and selected representation. A sanitized but structurally faithful fixture is more valuable than a hand-written happy path or a raw production dump.

## Q zh
一个 cache-key bug 只在真实 mobile request 的 duplicated header 和异常 query ordering 下出现。如何在不复制 user data 的情况下构建 regression test？

## A zh
把 request 缩减为最小 synthetic fixture，同时保留决定性结构：duplicate-field behavior、normalization、encoding 和 query order。移除 credential 与 payload，说明每个 field 代表的 production property，并同时断言 key output 和 selected representation。经过 sanitize 但结构真实的 fixture，比手写 happy path 或 raw production dump 更有价值。
