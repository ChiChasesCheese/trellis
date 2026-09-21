---
id: copy-method-vs-copy-copy-subclass
node: model.copy
type: qa
source: python-docs
---
## Q
对 list 做切片 `l[:]`、调用 `l.copy()`，与调用 `copy.copy(l)` 都能得到浅拷贝，三者在复制一个 list 子类实例时有什么不同？

## A
切片和 `.copy()` 方法是各容器类型自己实现的浅拷贝，如果 `l` 是 `list` 的子类实例，这两种方式可能只返回一个普通 `list` 基类实例；而 `copy.copy()` 走的是通用拷贝协议，通常会返回和原对象相同的类型（即保留子类类型的浅拷贝）。需要保留子类类型时应优先用 `copy.copy()`。
