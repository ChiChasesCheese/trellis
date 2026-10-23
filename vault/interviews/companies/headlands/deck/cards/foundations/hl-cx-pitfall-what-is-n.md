---
id: hl-cx-pitfall-what-is-n
node: foundations.complexity
type: qa
step: 41
---
## Q
报复杂度时为什么要先说清 n 是什么？两个独立规模的双重循环怎么写？

## A
n 可能是行数、字符数、价位数，含义不同结果不同。例：`BigInteger` 加法若数有 d 位，每次是 O(d) 而不是 O(1)。

两个独立规模 n 和 m 的双重循环是 **O(n × m)**，不能简化成 O(n²)。订单簿题尤其常见：价位数 L、订单数 n、事件数 k 各是各的。

模板答法：「设订单数为 n。建表 O(n)，每次查询 `HashMap.get` 平均 O(1)，总共 O(n + q)，空间 O(n)。」
