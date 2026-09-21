---
id: gc-generations-thresholds
node: memory.cyclic-gc
type: cloze
source: cpython-internals
---
默认构建下，新对象先进入 {{c1::第 0 代（generation 0）}}，若在一次该代回收中存活则晋升到 {{c2::第 1 代}}，再存活一次则晋升到 {{c3::第 2 代（最老一代）}}；`gc.get_threshold()` 的默认返回值 `(2000, 10, 10)` 中，第一个数是「自上次回收以来分配数减去释放数」超过它就触发第 0 代回收的阈值（`threshold0`），后两个数分别控制第 0 代回收多少次后连带扫一次第 1 代、第 1 代回收多少次后连带扫一次第 2 代。
