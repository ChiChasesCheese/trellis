---
id: problems-ticket-booking-hot-seats-candidate-set
node: problems.commerce.ticket-booking
type: qa
step: 5
tags: [grown]
---
## Q
In a ticket booking system, if the front/VIP section has 200 seats and 500,000 people are trying to book them, giving a per-seat contention ratio of 2,500:1, what mitigation lowers the wasted-work rate without changing the seat-per-row data model?

## A
Instead of the client specifying one exact seat id to hold, the client submits a batch of several acceptable candidate seat ids and the server's conditional update tries them and returns whichever one succeeds first. This spreads contention from 'many buyers racing for the same single row' to 'many buyers racing for any one of a larger candidate set,' cutting the rate of failed 409 attempts, at the cost of the buyer giving up the ability to pick one exact seat.

## Q zh
在票务系统中，如果前排/VIP 区有 200 个座位，同时有 50 万人在抢，单座竞争比高达 2,500:1，在不改变一票一行数据模型的前提下，什么方法能降低无效竞争的比例？

## A zh
让客户端不再指定唯一的一个座位 id 去占座，而是一次提交一批可接受的候选座位 id，服务器的条件更新依次尝试，返回第一个成功的那个。这把竞争从"很多买家抢同一行"打散成"很多买家抢一个更大候选集合中的任意一行"，降低了 409 失败尝试的比例，代价是买家放弃了精确挑选某个座位的能力。
