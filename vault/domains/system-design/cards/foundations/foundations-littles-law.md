---
id: foundations-littles-law
node: foundations.estimation
type: cloze
---
Little's Law: average requests in flight = {{c1::arrival rate × average time in system (L = λ·W)}}. So 2,000 QPS at 50 ms mean response time means {{c2::100}} concurrent requests — the number that sizes worker pools, DB connection pools, and per-server concurrency limits. Corollary: when latency doubles under load, required concurrency {{c3::doubles too}}, which is how slowdowns exhaust pools and cascade.


## zh
Little's Law：平均在途请求数 = {{c1::到达率 × 平均在系统中停留的时间（L = λ·W）}}。所以 2,000 QPS、平均响应时间 50 ms，意味着{{c2::100}} 个并发请求——这个数用来定 worker 池、数据库连接池和单机并发上限。推论：当负载升高使延迟翻倍时，需要的并发数{{c3::也翻倍}}，慢下来的服务就是这样耗尽连接池并级联扩散的。
