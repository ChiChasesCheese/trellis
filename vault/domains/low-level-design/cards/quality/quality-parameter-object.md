---
id: quality-parameter-object
node: quality.refactoring
type: qa
---
## Q
Introduce parameter object: beyond shortening signatures, what two design payoffs justify it — and what's the anti-pattern version?

## A
```java
book(String from, String to, LocalDate out, LocalDate in, int guests)
→ book(Route route, StayPeriod period, int guests)
```

Payoffs beyond brevity:

- **A home for validation and behavior**: `StayPeriod` enforces `out < in` once in its constructor and grows methods like `nights()` — logic that was duplicated at every call site.
- **A stable seam**: adding a field changes the object, not every signature in the chain (kills a shotgun-surgery vector).

Anti-pattern: the grab-bag `RequestContext`/`Options` object that bundles *unrelated* params just to shorten a signature — that's a data clump faked, coupling every caller to every field. Group only what forms a real concept.

## Q zh
引入参数对象：除了缩短签名，还有哪两个设计收益能证明它值得——以及它的反模式版本长什么样？

## A zh
```java
book(String from, String to, LocalDate out, LocalDate in, int guests)
→ book(Route route, StayPeriod period, int guests)
```

除简洁之外的收益：

- **给校验和行为一个家**：`StayPeriod` 在自己的构造函数里一次性强制 `out < in`，并且能长出 `nights()` 这样的方法 —— 这些逻辑原本在每个调用点重复。
- **一个稳定的接缝**：加字段改的是这个对象，而不是整条调用链上的每个签名（消灭了一条散弹式修改的路径）。

反模式：那种大杂烩式的 `RequestContext`/`Options` 对象 —— 仅仅为了缩短签名就把*互不相关*的参数捆在一起，等于伪造了一个 data clump，让每个调用方都耦合到每个字段。只把真正构成一个概念的东西聚在一起。
