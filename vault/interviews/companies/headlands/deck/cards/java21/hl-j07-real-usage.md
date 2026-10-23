---
id: hl-j07-real-usage
node: java21.j07-text-blocks
type: qa
step: 21
---
## Q
真实项目里文本块主要用在生产代码还是测试？一般怎么用？

## A
参考实现是纯逻辑，没有文本块；**文本块全在测试里**，题面每个样例逐字进测试。

例：订单簿测试把命令序列用文本块写成输入，期望输出也用文本块，辅助方法 `lines(String block)` 返回 `block.lines().toList()`。同样用法出现在 job chain 测试（CSV 日志）、寄存器程序测试、队列均值和订单序列测试。
