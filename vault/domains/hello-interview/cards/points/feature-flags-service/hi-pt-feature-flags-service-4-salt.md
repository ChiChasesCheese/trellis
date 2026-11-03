---
id: hi-pt-feature-flags-service-4-salt
node: qb.sd.feature-flags-service.points
type: qa
step: 7
---
## Q
**功能开关服务 · 盐与跨语言一致**｜追问 · 出自：功能开关服务 › 深入 4

为什么哈希输入要带上开关键和 `salt`？多语言 SDK 怎么保证结果一致？

## A
**盐。** 否则每个开关都是「用户 ID 排名前 X%」开启，同一批人永远是所有实验的小白鼠；想整体重新洗牌某个开关就换 `salt`。
**一致。** 哈希函数明确定义（如 MurmurHash3 的 32 位输出，或 SHA-1 取前 4 字节）并给出标准测试向量，保证 Java、Go、JavaScript 的 SDK 结果完全相同。
