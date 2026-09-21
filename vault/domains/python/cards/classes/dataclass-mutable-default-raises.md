---
id: dataclass-mutable-default-raises
node: classes.dataclasses
type: qa
source: python-docs
---
## Q
在 `@dataclass` 里写 `x: list = []` 会发生什么？应该怎么改？

## A
会直接抛出 `ValueError`。原因是普通类的可变默认值（如 `x = []`）会被所有实例共享同一个列表对象——这通常是 bug；`dataclasses` 检测到默认值是 `list`/`dict`/`set` 这类可变类型时直接拒绝。正确写法是 `x: list = field(default_factory=list)`：`default_factory` 是一个零参可调用对象，在每次需要默认值时被调用一次，给每个实例一个独立的新列表。
