---
id: hi-pt-image-transform-pipeline-3-protocol-step
node: qb.lld.image-transform-pipeline.points
type: qa
step: 3
---
## Q
**图像变换流水线 · Protocol 步骤接口**｜必会 · 出自：图像变换流水线 › 深入 1

流水线里放各种变换，它们之间的共同接口怎么定义？为什么不做一个 `Step` 基类加 `if kind ==` 分发？

## A
**写法。** `typing.Protocol`：只要求有 `apply(image) -> Image`，步骤不必继承任何基类，类型检查器也能检查 `Pipeline` 里放的东西（鸭子类型加静态检查）。

**为什么。** 基类加分发把所有步骤绑在一个层级上；用 Protocol，新增一种步骤只需新增一个类（加注册表一行），流水线、缓存、校验都不用改。
