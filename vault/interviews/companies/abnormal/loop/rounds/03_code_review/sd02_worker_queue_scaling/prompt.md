# sd02 · Extend the reviewed system and reason about it at scale (worker / queue scaling)

> 原话（#8496901 Round 4 part 2）："The second part involved extending the system and discussing how it would behave at larger scale … Concurrency · Parallelism · Worker scaling · Message queue scaling · Throughput · Bottlenecks · Failure scenarios … be prepared to go beyond 'add more workers' or 'use a queue.' You should be able to reason about the limits of those approaches and explain what happens when individual components become bottlenecks." 系统 **(reconstructed)** = `../cr01_alert_fanout/`（code review 刚评过的通知 fan-out worker），这样两段在同一个心智模型上。
> 20–25 min，接在 cr01 的 code review 之后。

## The prompt

"Now that we've fixed the P0s: this worker sends alert notifications to customer webhooks, email and Slack. Today it handles a few messages a second. A new product line will push **5,000 notifications/s at peak**; webhook endpoints answer in ~200 ms median, some customers rate-limit us at **50 requests/s**, and one tenant is ~40% of traffic. How does the system behave, and what do you change?"

## Interviewer answers if asked

- Ordering? → "Per alert, updates should not arrive out of order at a customer. Across alerts we don't care."
- Delivery guarantee? → "At least once is fine if customers can dedupe; say how they would."
- Latency SLO? → "P99 under a minute for high severity; low severity can wait."
- Can a customer's endpoint be down for hours? → "Yes, it happens weekly."

## 中文题意

P0 修完之后：这个 worker 把告警通知发给客户的 webhook、邮件和 Slack。现在每秒几条。新产品线峰值会到 **每秒 5,000 条通知**；webhook 中位响应 ~200 ms；有些客户对我们限流 **每秒 50 次**；一个租户占 ~40% 流量。**系统会怎样表现？你会改什么？**
可问到的答案：同一告警的更新到客户那里不能乱序，不同告警之间无所谓；至少一次投递可以，但要说明客户怎么去重；高严重度 p99 < 1 分钟，低严重度可以等；客户端点每周都会挂几个小时。
