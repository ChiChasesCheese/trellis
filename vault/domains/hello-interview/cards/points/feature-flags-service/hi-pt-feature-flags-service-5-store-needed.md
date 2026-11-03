---
id: hi-pt-feature-flags-service-5-store-needed
node: qb.sd.feature-flags-service.points
type: qa
step: 8
---
## Q
**功能开关服务 · 何时才需要存储分配**｜追问 · 出自：功能开关服务 › 深入 4

哈希分桶是默认路径，哪些场景仍然要把分配结果存下来？

## A
**场景。** 多变体权重改变会让部分用户变体变化；若要求「一旦分配永不改变」（正式实验、付费功能权限），首次分配时写入分配表并优先读它。
**要点。** 这是少数场景的补充，不是默认路径。
