---
id: problems-ticket-booking-payment-hold-extension-saga
node: problems.commerce.ticket-booking
type: qa
step: 7
tags: [grown]
---
## Q
In a ticket booking system, why does entering the payment page extend a seat hold's TTL, and how does the reserve-charge-confirm saga combined with idempotency on the hold id prevent both double-selling and double-charging?

## A
The base hold TTL (e.g. 10 minutes) is sized for browsing and form-filling, but the payment gateway itself adds latency, retries, and asynchronous webhook delivery; without extension, a hold could expire mid-payment, letting the seat resell out from under a buyer who is about to pay. Structuring the flow as a saga — reserve (done) → charging (call the PSP) → confirmed (one transaction flips the seat to sold and the order to confirmed, keyed by the hold id) — means a failed charge or an expired hold triggers automatic compensation (refund/release), and a duplicate payment webhook for the same hold id just hits the already-confirmed branch and returns idempotently instead of re-running the state transition.

## Q zh
在票务系统中，为什么进入支付页面会把座位占座（hold）的有效期续长，reserve-charge-confirm 这个 saga 配合以 hold id 为幂等键的确认逻辑，是如何同时防止重复售出和重复扣款的？

## A zh
基础占座有效期（如 10 分钟）是按浏览和填表所需时间定的，但支付网关本身会带来延迟、重试和异步 webhook，如果不续期，占座可能在支付过程中过期，导致座位在买家即将付款时被转卖给别人。把流程做成一个 saga——reserve（已完成）→ charging（调用 PSP）→ confirmed（一个事务里同时把座位改为 sold、订单改为 confirmed，以 hold id 为键）——意味着扣款失败或 hold 已过期都会触发自动补偿（退款/释放），而同一个 hold id 的重复支付 webhook 只会命中已确认分支并幂等返回，不会重新执行状态转移。
