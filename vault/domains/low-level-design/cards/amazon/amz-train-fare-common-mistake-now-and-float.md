---
id: amz-train-fare-common-mistake-now-and-float
node: amazon.amz-train-fare
type: qa
step: 9
tags: [grown]
---
## Q
在 Amazon 火车票价设计里，候选人最常见的错误是什么？给出一个会暴露它的输入。

## A
在计费方法里直接调 `datetime.now()` 判断周末，同时用 float 存价格。前者使测试无法固定「今天是周六」，也让第 4 关加规则时必须改核心方法；后者：`0.1 * 3` 得 `0.30000000000000004`，三个 0.10 的区间累计不等于 0.30。修法：注入时钟，金额用整数分的值对象。另一个同类错误：只处理 start 在 stop 之前，I 到 G 得到负数。
