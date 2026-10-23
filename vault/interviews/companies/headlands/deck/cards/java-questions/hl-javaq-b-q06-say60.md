---
id: hl-javaq-b-q06-say60
node: java-questions.b-versions
type: qa
step: 10
---
## Q
用英文 60 秒回答：Beyond language features: what changed in the JVM and runtime between Java 8 and 21 that matters for performance?

## A
结构：GC 变化 → 字符串紧凑与 indy 拼接 → 偏向锁移除 → 容器、日志、JFR、虚拟线程 → 升级 8 到 21 的主要摩擦是强封装。

> "Several things changed under the hood. G1 became the default collector, and ZGC went production, with a generational mode in 21 that gets pauses well under a millisecond in my test. Strings got compact - one byte per Latin-1 character - and concatenation goes through invokedynamic so the runtime can pick a strategy. Biased locking was removed - on 21 the flag isn't even recognised. The JVM understands container limits, there's unified logging and JFR is free, and in 21 we have virtual threads. When upgrading from 8, the main friction is strong encapsulation of JDK internals, which needs `--add-opens` for reflective code."
