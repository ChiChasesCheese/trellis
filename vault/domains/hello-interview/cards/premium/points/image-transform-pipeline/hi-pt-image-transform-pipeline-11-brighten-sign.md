---
id: hi-pt-image-transform-pipeline-11-brighten-sign
node: qb.lld.image-transform-pipeline.points
type: qa
step: 11
---
## Q
**图像变换流水线 · 亮度合并的符号条件**｜加分 · 出自：图像变换流水线 › 逐步扩展 4

两个相邻的亮度调整 `Brighten(200)` 和 `Brighten(-100)` 能合并成 `Brighten(100)` 吗？同号时为什么可以？

## A
**不能。** 亮度加完要截断到 0..255。像素 100 先加 200 得 300，截断成 255，再减 100 得 155；合并成加 100 得 200。

**同号可以。** `min(255, min(255, x+a)+b)` 等于 `min(255, x+a+b)`，所以守卫是 `d1 * d2 >= 0`。

**原则。** 化简只做保证等价的改写。
