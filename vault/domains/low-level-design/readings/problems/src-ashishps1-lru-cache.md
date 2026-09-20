---
nodes: [problems.components.lru-cache]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/lru-cache.md
---
# awesome-low-level-design — lru-cache

值得读：五种语言的实现索引之一，Java 版本用 `synchronized` 关键字直接加在 `get`/`put`
方法上做线程安全，是本文"扩展与追问·并发与线程安全"一节要对照、也要拒绝的 Java 式答案——
Python 没有语言内置的 `synchronized`，`threading.Lock` 加 `with` 语句是对应写法，但更值得
说清楚的是"为什么这里没有只加锁在 get 或只加锁在 put 就够"，这份索引本身没有展开这一点。
`get` 未命中返回 `null`/`-1` 而不是抛异常，也是本文选择 `KeyError` 时要论证的对比对象。
