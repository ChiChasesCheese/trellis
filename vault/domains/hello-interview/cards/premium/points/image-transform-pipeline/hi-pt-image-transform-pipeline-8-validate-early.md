---
id: hi-pt-image-transform-pipeline-8-validate-early
node: qb.lld.image-transform-pipeline.points
type: qa
step: 8
---
## Q
**图像变换流水线 · 提前校验形状**｜追问 · 出自：图像变换流水线 › 深入 4

200 个变换文件里个别裁剪会越界。怎么在碰第一张图之前就发现，而不是处理到一半才失败？

## A
**做法。** 每个步骤多一个 `output_size(h, w)`，只算形状不碰像素；`Pipeline.output_size` 逐步推演，非法的步骤以 `StepError` 报出，和 `apply` 报同一个 `index`。

**数字。** 大图、小图两种形状，200 个文件 x 2 种形状 = 400 次推演，几乎免费。

**对比。** "先跑一遍看会不会出错"在大图上很贵，还会让缓存里留下半截结果。
