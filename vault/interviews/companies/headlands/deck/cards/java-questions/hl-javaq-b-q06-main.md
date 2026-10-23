---
id: hl-javaq-b-q06-main
node: java-questions.b-versions
type: qa
step: 5
---
## Q
除了语言特性，Java 8 到 21 之间 JVM 和运行时有哪些对性能重要的变化？
Beyond language features: what changed in the JVM and runtime between Java 8 and 21 that matters for performance?

## A
按"你会遇到的现象"组织，不要背清单：
- **默认 GC**：Parallel（8）→ **G1**（9 起默认）；ZGC 15 起正式，21 起可 `-XX:+ZGenerational` 开分代。
- **字符串**：紧凑字符串（9）、`invokedynamic` 拼接（9）。
- **锁**：偏向锁移除。
- **容器感知**（10）、统一日志与免费 JFR（9 / 11）。
- **虚拟线程**（21）。
- 重点：知道升级 8 → 21 **白捡的**（G1 改进、字符串、锁、JIT 优化）和**需要动手的**（强封装导致的 `--add-opens`、被移除的 API）。
