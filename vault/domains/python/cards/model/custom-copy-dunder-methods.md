---
id: custom-copy-dunder-methods
node: model.copy
type: qa
source: python-docs
---
## Q
自定义类如果想接管自己被 `copy.copy()` / `copy.deepcopy()` 复制时的行为，应该实现哪两个特殊方法？在 `__deepcopy__` 里递归复制某个成员时要注意什么？

## A
实现 `__copy__(self)` 接管浅拷贝逻辑（不接收额外参数）；实现 `__deepcopy__(self, memo)` 接管深拷贝逻辑。在 `__deepcopy__` 内部如果还要递归复制某个成员对象，必须显式调用 `copy.deepcopy(component, memo)` 并把同一个 `memo` 字典继续传下去，否则会破坏防止重复复制和循环引用的机制。
