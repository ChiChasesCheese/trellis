---
id: gc-trial-subtraction
node: memory.cyclic-gc
type: qa
source: cpython-internals
---
## Q
循环 GC 用「试减引用」（trial subtraction）算法找不可达环时，第一步具体做什么？

## A
GC 给每个被扫描的容器对象一个 `gc_ref` 副本（初值等于该对象当前的真实引用计数），然后遍历这批对象，对每个容器通过其 `tp_traverse` 找到它引用的其他对象，把这些对象的 `gc_ref` 减一。扫描结束后，`gc_ref` 仍大于 0 的对象说明它还有来自「待扫描集合之外」的引用，一定是可达的；`gc_ref == 0` 只是「暂时可疑」，还需要从可达对象出发做一轮广度优先遍历才能确认哪些真正不可达。
