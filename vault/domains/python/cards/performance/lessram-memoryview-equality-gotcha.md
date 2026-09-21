---
id: lessram-memoryview-equality-gotcha
node: performance.less-ram
type: qa
source: python-docs
---
## Q
两个 `memoryview` 满足 `v is w` 为 `False`，是否就意味着 `v == w` 一定也是 `False`？

## A
不一定。`memoryview` 的相等比较不看内存地址，而是看两者的 shape 以及按 `struct` 语法解释后的元素值是否一致，等价于 `v.tolist() == w.tolist()`；即便一个底层是 `array('I', ...)`、一个是 `array('d', ...)`，只要格式能被 `struct` 模块识别且元素值相同，也会判定相等。
