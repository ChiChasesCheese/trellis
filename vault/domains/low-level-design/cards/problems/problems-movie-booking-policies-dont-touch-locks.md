---
id: problems-movie-booking-policies-dont-touch-locks
node: problems.booking.movie-booking
type: qa
step: 8
tags: [grown]
---
## Q
电影订票的第 4 关追加"按座位档次和排次定价、周末加价、分档退票"。怎么把它们加进来才能一行都不碰已经写好的锁座与并发代码？在 Python 里这些策略该写成类还是函数？

## A
把定价和退票做成**注入到服务构造函数里的普通函数**：定价是 `(Seat, Show) -> int`（金额用整数的分，不用浮点），退票是 `(Booking, Show, now) -> int` 返回退款额。它们只读对象、跨调用不记任何状态，所以不需要抽象基类，更不需要每条规则配一个实现类——函数签名本身就是接口。"叠一层规则"就是包一个函数：`row_surcharge(by_seat_type(...), {"A": 500})` 先按档次定价再给 A 排加价。下单流程只调 `self._pricing(seat, show)`，完全不知道规则是哪一种，所以加价格档、加优惠券、加退票档位都碰不到锁座机器。只有当一条策略真的需要记状态（比如优惠券要记"这张用过了"）或要多暴露一个查询方法时，才升级成类。
