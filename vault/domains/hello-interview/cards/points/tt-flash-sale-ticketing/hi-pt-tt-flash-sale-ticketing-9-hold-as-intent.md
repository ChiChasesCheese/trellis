---
id: hi-pt-tt-flash-sale-ticketing-9-hold-as-intent
node: tt.sd.tt-flash-sale-ticketing.points
type: qa
step: 9
---
## Q
**秒杀抢票 · 占位即意图记录**｜追问 · 出自：秒杀抢票 › 深入 4

秒杀抢票预占成功后要往队列发建单消息，Redis 成功而队列失败怎么办？

## A
**要点。** 占位本身就是意图记录。
**修复。** 清扫任务发现创建超过 60 秒而数据库无对应订单的占位，补发消息或直接释放；消费者按 hold_id 幂等。
**最坏结果。** 票被占用最多 10 分钟，之后回补，不会永久丢失。
**积压。** 队列积压只延迟建单，占位 10 分钟内有效。
