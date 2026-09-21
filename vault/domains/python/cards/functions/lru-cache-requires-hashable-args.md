---
id: lru-cache-requires-hashable-args
node: functions.functools
type: qa
source: python-docs
---
## Q
用 `@functools.lru_cache` 缓存一个函数时，为什么要求所有参数都必须是可哈希的（hashable）？`f(a=1, b=2)` 和 `f(b=2, a=1)` 会被当成同一次调用命中缓存吗？

## A
`lru_cache` 内部用一个字典把「调用时的参数」映射到「返回值」，字典的 key 必须可哈希，所以传进去的位置参数和关键字参数都必须是可哈希对象（比如列表、字典这类不可哈希的参数会直接报错）。缓存 key 按参数的具体值和传参顺序构造，`f(a=1, b=2)` 和 `f(b=2, a=1)` 关键字顺序不同，会被当成两次不同的调用，各占一条缓存记录，不会互相命中。
