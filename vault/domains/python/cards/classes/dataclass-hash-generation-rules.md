---
id: dataclass-hash-generation-rules
node: classes.dataclasses
type: qa
source: python-docs
---
## Q
`@dataclass` 默认（`eq=True, frozen=False`）会不会给类生成 `__hash__()`？`eq=True` 配 `frozen=True` 呢？`eq=False` 呢？

## A
`eq=True, frozen=False`（最常见的默认组合）：`__hash__` 被显式设为 `None`，实例不可哈希——因为默认认为可变对象不该进哈希表。`eq=True, frozen=True`：自动生成 `__hash__()`，因为「不可变 + 可比较」满足可哈希的前提。`eq=False`：`__hash__` 不被触碰，沿用父类实现（若父类是 `object`，退化为按身份哈希）。想在可变类上强行拿到哈希，需要显式传 `unsafe_hash=True`，但文档明确不推荐。
