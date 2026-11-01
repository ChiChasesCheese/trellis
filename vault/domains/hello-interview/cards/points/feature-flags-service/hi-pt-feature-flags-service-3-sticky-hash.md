---
id: hi-pt-feature-flags-service-3-sticky-hash
node: qb.sd.feature-flags-service.points
type: qa
step: 3
---
## Q
**功能开关服务 · 确定性哈希实现粘性**｜出自：功能开关服务 › 深入 1

要让同一用户稳定落在「开」或「关」，放量比例从 10% 调到 20% 时原来开着的用户不翻转。用随机数加存储，还是哈希？公式是什么？

## A
**对比。** 随机加存储：每次评估读存储（热路径网络调用），表规模 = 用户数 × 开关数。
**选哈希。** `bucket = hash(flagKey + salt + userId) mod 10000`，`bucket < percent × 100` 则开启；同输入永远同桶，不存任何东西。
**单调性。** 桶号不随 percent 变化，调大只新增用户，调小从最高桶开始关。
