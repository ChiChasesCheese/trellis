---
id: hl-javaq-a-q04-say60
node: java-questions.a-speed
type: qa
step: 22
---
## Q
用英文 60 秒回答：Your Java service is slow for the first few seconds after start-up, then fine. Why, and what would you do about it?

## A
结构：解释器起步（约 10 倍慢）→ 计数器触发 C1/C2 后台编译 → 对策：真实流量预热、预热完再接流量、CDS，必要时 native image 并说明取舍。

> "A JVM starts every method in the interpreter, which is about ten times slower than compiled code in my test - 24 ns per call versus 2 ns. Counters trigger C1 compilation, then C2 for the really hot code, in background compiler threads, so there is a window where you're slow. In production I handle it by warming up before taking traffic - replaying realistic requests, not a single synthetic one, so the profile isn't skewed - keeping the instance out of the load balancer until it's warm, and using class-data sharing to cut start-up work. If start-up matters more than peak throughput, native image is an option, with trade-offs."
