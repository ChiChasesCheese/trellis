---
id: hi-pt-image-transform-pipeline-9-prefix-cache-key
node: qb.lld.image-transform-pipeline.points
type: qa
step: 9
---
## Q
**图像变换流水线 · 前缀缓存的键**｜追问 · 出自：图像变换流水线 › 深入 5

对同一张图跑 200 条前几步相同的流水线，缓存什么、键是什么、怎么淘汰？为什么不用 `id(image)` 做键？

## A
**键与值。** 键是 `(输入图像, 步骤前缀)`，每执行一步存一项，运行时从最长的已缓存前缀接着算。

**LRU。** `OrderedDict`：命中用 `move_to_end` 刷新，超限用 `popitem(last=False)` 淘汰。

**为什么不用 `id`。** 内容相同的另一个对象会错过缓存，对象回收后 `id` 还可能被复用造成错误命中。

**代价。** 每项是一张完整中间图，按项数限制容易撑爆内存，要按字节计量。
