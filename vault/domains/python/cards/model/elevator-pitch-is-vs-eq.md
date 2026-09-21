---
id: elevator-pitch-is-vs-eq
node: model.names-objects
type: qa
source: cpython-internals
---
## Q
用 60 秒讲清楚：为什么判断两个值是否相等要用 `==` 而不是 `is`？

## A
`is` 比较对象身份（内存地址），`==` 比较值。CPython 出于性能会驻留短字符串、缓存小整数，让内容相同的对象恰好共享同一份内存，但这只是实现细节、不是语言承诺，也只覆盖部分场景。所以除了和 `None` 或哨兵对象比较外，判断「内容是否相同」用 `==`，把 `is` 留给「是不是同一个对象」这个问题。
