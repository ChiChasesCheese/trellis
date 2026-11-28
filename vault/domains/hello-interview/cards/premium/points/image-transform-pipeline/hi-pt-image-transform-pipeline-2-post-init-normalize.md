---
id: hi-pt-image-transform-pipeline-2-post-init-normalize
node: qb.lld.image-transform-pipeline.points
type: qa
step: 2
---
## Q
**图像变换流水线 · 冻结对象里规范化**｜必会 · 出自：图像变换流水线 › 深入 1

`Image` 是冻结的，却要在构造时把传入的列表拷成元组并校验。冻结对象里怎么改字段？为什么不把拷贝写在调用方？

## A
**写法。** 在 `__post_init__` 里用 `object.__setattr__` 做一次规范化，普通赋值会被冻结拦下。

```python
rows = tuple(tuple(r) for r in self.pixels)
...
object.__setattr__(self, "pixels", rows)
```
**为什么。** 不规范化，就要把"拷贝并校验"放在每个调用点；传入的列表之后被调用方修改，缓存里的键就失效了。`Pipeline` 的 `steps` 同理，列表也被规范成元组。
