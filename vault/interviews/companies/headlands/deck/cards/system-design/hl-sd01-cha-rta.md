---
id: hl-sd01-cha-rta
node: system-design.sd01-unused-code
type: qa
step: 16
---
## Q
调用接口方法 `Shape.area()` 时，CHA、RTA 和指向分析（points-to）各怎么决定可能执行的实现？为什么选 RTA？

## A
- **CHA**（Class Hierarchy Analysis，类层次分析）：假设 `Shape` 的**所有**实现类的 `area()` 都可能被调用。保守简单，但会把从未被实例化的实现类保活（降低召回）；
- **RTA**（Rapid Type Analysis，快速类型分析）：只考虑**已被标记为可达的 `new X()`** 的那些类，迭代到不动点（新标到一个 `new Foo()` 就可能让 `Foo.area()` 可达）。精度明显好于 CHA，成本仍近线性；
- **指向分析**：精度更高，但成本高、规模受限，对找死代码性价比不高。

**RTA 是工程上的甜点**；精度不够的符号落在「可达但无人调用」的灰区，由 L3 / 人审处理。保守性原则：宁可多保活（偏向漏报），因为误判活方法为死比漏掉死方法的代价大得多。
