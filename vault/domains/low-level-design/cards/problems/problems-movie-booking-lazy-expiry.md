---
id: problems-movie-booking-lazy-expiry
node: problems.booking.movie-booking
type: qa
step: 4
tags: [grown]
---
## Q
电影订票设计里，选座锁定（seat hold）带 10 分钟超时。超时释放应该靠后台清扫线程定期扫，还是靠每次读写时按注入的时钟当场判断？为什么？

## A
以**惰性判断**为准，清扫只是把结论落实。每次读或写座位时拿注入的时钟和 `expires_at` 比一下，过期的 HELD 一律当成 AVAILABLE，正确性就完全不依赖任何后台任务跑没跑、跑得及不及时。只靠清扫线程有两个坏处：两次清扫之间，已经过期的座位仍然显示为"已占"，用户看到一个空着却买不到的座；而且测试要么得 `sleep`，要么得把线程调度也做成可注入的。保留一个 `release_expired()` 仍然有用——它清掉格子里残留的 `hold_id` 和过期时间——但它不是正确性的一部分。验收方法：一次清扫都不调用，把假时钟往前拨过 TTL，可用座位数必须已经变回来了。
