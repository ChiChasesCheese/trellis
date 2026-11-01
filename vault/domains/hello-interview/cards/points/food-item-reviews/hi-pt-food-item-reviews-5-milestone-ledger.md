---
id: hi-pt-food-item-reviews-5-milestone-ledger
node: qb.sd.food-item-reviews.points
type: qa
step: 5
---
## Q
**带打赏的菜品评价系统 · 里程碑账本保证只付一次**｜出自：带打赏的菜品评价系统 › 深入 2

菜品评价每 100 个赞付 1 美元，并发或重复处理下怎样保证每个里程碑只付一次？

## A
**要点。** 里程碑编号 k = floor(upCount / 100)，只在 k 增长时触发；对每个新里程碑 m 执行 INSERT INTO payout(reviewId, m) ... ON CONFLICT DO NOTHING，插入成功的进程才有权付款。
**支付幂等。** 支付调用用 payout:{reviewId}:{m} 作幂等键。
**状态机。** PENDING → PAID | FAILED，失败重试，卡住的由扫描任务补做。
