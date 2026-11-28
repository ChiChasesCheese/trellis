---
id: hi-pt-image-transform-pipeline-1-value-objects
node: qb.lld.image-transform-pipeline.points
type: qa
step: 1
---
## Q
**图像变换流水线 · 不可变值对象**｜必会 · 出自：图像变换流水线 › 深入 1

`Image` 和每个变换（`Flip`、`Rotate`、`Crop`……）为什么都做成 `@dataclass(frozen=True, slots=True)`？对缓存和并发有什么用？

## A
**得到什么。** 自动的按值比较、哈希、不可变；`slots` 去掉每个实例的字典。

**用处。** 能做缓存的键，能直接 pickle 跨进程传递，调用方改自己的数据也伤不到它。

**对比。** 普通类要手写 `__eq__` 和 `__hash__`，漏了哈希就不能做字典的键（不可变值对象）。
