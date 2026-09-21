---
id: map-filter-vs-comprehension-when-to-prefer
node: iteration.comprehensions
type: qa
source: python-docs
---
## Q
`map(f, iterable)`/`filter(predicate, iterable)` 和功能等价的列表推导式相比，什么时候更值得选前者？

## A
两者功能重复：`map(f, it)` 等价于 `(f(x) for x in it)`，`filter(pred, it)` 等价于 `(x for x in it if pred(x))`。当变换或判断逻辑已经是一个现成的命名函数（标准库函数或已定义好的函数）时，直接把它传给 `map`/`filter` 比在推导式里再包一层调用更简洁；但如果逻辑需要临时的 lambda 或要嵌入判断表达式，推导式通常更直接、可读性更好。
