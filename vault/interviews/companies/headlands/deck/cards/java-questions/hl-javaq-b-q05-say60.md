---
id: hl-javaq-b-q05-say60
node: java-questions.b-versions
type: qa
step: 9
---
## Q
用英文 60 秒回答：What are the main differences between Java 8, 11, 17 and 21? Which features would you actually use?

## A
结构：先点明 LTS 线 8/11/17/21 → 每个版本一句话 → 17/21 的数据建模主线（编译器检查穷尽）→ 日常最常用的两样。

> "The LTS line is 8, 11, 17, 21. Java 8 brought lambdas, streams and `java.time`. Between 9 and 11 we got `var`, the module system, the HTTP client, and G1 as the default collector. Java 17 is where the data-modelling features land: records, sealed types, text blocks, switch expressions, pattern matching for `instanceof`. Java 21 completes it - pattern matching for `switch` and record patterns, so with a sealed hierarchy the compiler checks exhaustiveness - and adds virtual threads, sequenced collections, and generational ZGC. The ones I'd use daily are records and sealed types with pattern switches for modelling events, and virtual threads for I/O-heavy code."
