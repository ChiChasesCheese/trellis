---
id: hi-pt-crowdfunding-share-purchase-4-idempotency
node: qb.sd.crowdfunding-share-purchase.points
type: qa
step: 4
---
## Q
**限时众筹购股系统 · 购买幂等**｜出自：限时众筹购股系统 › 整体设计

众筹购股里用户重复点击或客户端重试，同一次购买意图会被提交多次。系统怎么保证只生效一次？

## A
**要点。** purchaseId 由客户端按"用户 + 活动 + 随机数"生成，作为幂等键；以它为主键 INSERT ... ON CONFLICT DO NOTHING，已存在就返回已有状态，不再执行后续步骤。
**扣款侧。** 调用 withdraw(userId, 金额, purchaseId) 时也用 purchaseId 当幂等键，要求余额服务只扣一次。
**配合。** 同一用户同一时刻只允许一笔未完成的购买。
