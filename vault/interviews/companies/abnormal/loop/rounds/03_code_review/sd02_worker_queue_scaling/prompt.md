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
