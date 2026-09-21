---
id: dict-iter-keys-vs-values-items
node: iteration.iterator-protocol
type: qa
source: python-docs
---
## Q
对字典 `d` 直接写 `for k in d` 遍历到的是键（key）、值（value）还是键值对？要遍历另外两种该怎么写？

## A
`iter(d)`（以及 `for k in d`）默认遍历的是 key，等价于 `d.keys()`。要遍历值需要显式调用 `d.values()` 取得对应迭代器；要遍历 `(key, value)` 对则调用 `d.items()`。三者各自返回独立的视图迭代器，语义不会混用，选错只会拿到 key 而不是想要的值。
