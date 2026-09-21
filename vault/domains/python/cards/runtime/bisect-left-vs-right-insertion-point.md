---
id: bisect-left-vs-right-insertion-point
node: runtime.stdlib-map
type: qa
source: python-docs
---
## Q
在一个已排序列表里，`x` 已经存在一个或多个时，`bisect_left(a, x)` 和 `bisect_right(a, x)`（即 `bisect()`）返回的插入点有什么区别？

## A
`bisect_left` 返回的插入点在所有等于 `x` 的元素「之前」，插入后 `x` 会排在这些相等元素最前面；`bisect_right`/`bisect` 返回的插入点在所有等于 `x` 的元素「之后」，插入后 `x` 排在最后面。两者都只用 `__lt__` 做比较、从不调用 `__eq__`，严格说它们定位的是「插入点」而不是在「查找某个值」。
