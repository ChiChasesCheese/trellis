---
id: problems-amazon-locker-every-container-shrinks
node: problems.machines.amazon-locker
type: qa
step: 6
tags: [grown]
---
## Q
快递柜（Amazon Locker）里有三个容器必须会缩，分别是哪三个、被什么事件缩？怎么在不读私有属性的前提下测它们？

## A
1. **码表** `dict[code, AccessGrant]`：取走、过期、改派三条路径都要立刻删键。这是全系统唯一的码索引，它只增不减就等于码永远有效。
2. **可用索引** `dict[Size, set[locker_id]]`：某个尺寸的桶空了就把**键也删掉**，不留计数为 0 的幽灵尺寸——否则「扫一遍装得下的尺寸类」这个循环会越扫越长。
3. **到期堆**：扫描弹出时丢弃已被取走的陈旧条目。

测法是把不变式做成**只读属性**：`code_count`、`pending_expiry_count`、`free_count(size)`。测试断言这些数字，而不是断言 `_grants` 或 `_free`——练习者完全可能选别的内部表示（用排序列表代替堆），断言私有字段的测试会判一份正确答案不及格。一条只在对象内部可见的不变式，就该有一个属性把它露出来。
