---
id: hi-pt-video-moderation-system-10-precision-model-update
node: qb.sd.video-moderation-system.points
type: qa
step: 10
---
## Q
**视频内容审核系统 · 精度召回与模型更新**｜追问 · 出自：视频内容审核系统 › 取舍与追问

视频审核阈值怎么权衡误伤与漏判？新模型怎么上线？

## A
**阈值。** 越低误伤越多，越高漏判越多；灰区交人工是常见折中，不同违规类型阈值不同。
**新模型。** 先影子运行比对再切流；分数库按模型版本存储，规则可指定使用哪个版本。
**全球化。** 规则带地区维度，就近区域处理，审计记录按地区合规存放。
