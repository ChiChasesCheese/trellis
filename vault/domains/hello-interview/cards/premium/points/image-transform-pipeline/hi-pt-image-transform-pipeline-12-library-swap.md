---
id: hi-pt-image-transform-pipeline-12-library-swap
node: qb.lld.image-transform-pipeline.points
type: qa
step: 12
---
## Q
**图像变换流水线 · 换成图像库**｜加分 · 出自：图像变换流水线 › 深入 7

面试官说可以用任何图像库，你没用过。代码结构该怎么安排，才能既快又不乱？换成彩色图、numpy 时哪些接口不变？

## A
**做法。** 把库调用包进同一个 `Step` 的 `apply` 里（例如 Pillow 的镜像、旋转），`Image` 换成库的图像类型或数组。

**不变的。** 流水线、注册表、`StepError`、缓存、进程池、队列都不变，这正是统一接口的好处。

**变的。** `Image` 的校验、`Brighten`、`Invert` 这类逐像素函数；彩色图的像素从整数变成元组。
