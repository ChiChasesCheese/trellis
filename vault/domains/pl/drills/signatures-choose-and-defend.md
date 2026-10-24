---
nodes: [signatures.choosing, signatures.gotchas, signatures.go, signatures.java, signatures.rust, signatures.python]
tags: [drill]
---
# 练习：为行情平台选语言，并向质疑你的同事辩护

五人团队、六个月，要做一个行情与研究平台，包含三个组件。A：行情网关，接入 40 个交易所的 WebSocket，峰值 20 万条消息每秒，单条处理 p99 低于 2 ms，7×24 运行，部署到 3 台机器，希望单个二进制交付。B：策略研究与回测，研究员迭代很快，大量表格和数值计算，代码会被反复改写。C：内部管理 API 与定时任务，业务逻辑多、变化多、要对接公司现有的 Java 基础设施。一位资深同事说：「别搞多语言，全用 Java，团队都会。」另一位说：「全用 Rust，一次写对。」你要为每个组件选择语言（可以相同也可以不同），并当面说服这两位同事。

同一台机器上的 hello world 数据（只衡量启动与占用，不代表吞吐）：

| 语言 | 冷启动 | 常驻内存 | 交付物 |
|---|---|---|---|
| Go | 约 2 ms | 约 4 MB | 单个 2.4 MB 的二进制 |
| Rust（`-O`） | 约 1.5 ms | 约 2 MB | 单个 0.47 MB 的二进制 |
| Java 25 | 约 14 ms | 约 40 MB | 需要 JDK 或 JRE（本机安装约 294 MB） |
| Python 3.14 | 约 7.5 ms | 约 16 MB | 需要解释器与依赖环境 |

另一组数据：一亿次 `s += i*i % 7` 的循环，Java 约 28 ms，Go 约 37 ms，Rust `-O` 约 32 ms，CPython 约 2246 ms。

**要你给出的**
- 每个组件的语言选择，以及一句话决定性理由；如果选了多语言，说明它们之间的边界与交接方式。
- 对「全用 Java」和「全用 Rust」两位同事的回应，各 3 句话，必须承认他们的合理之处。
- 每个选择最可能让团队踩到的 3 个陷阱，以及上线前怎样提前发现。
- 哪些数据不能直接拿来做决策，并说明还需要什么测量。

**评分要点**
- 先写约束，再选语言：延迟尾部、部署形态、团队技能、迭代速度、生态各占多少权重。选型的输出应当是「在这些约束下哪个最合适」，而不是「哪个最好」 ([[pl-sig-choosing-best-practice]], [[pl-foundations-tradeoff-axes-best-practice]])。
- 组件 A（延迟敏感、长期运行、单二进制）：候选是 Go 和 Rust。Go 的 goroutine 与 channel 适合大量并发连接，部署为单个静态二进制，GC 停顿通常很短；Rust 没有 GC，尾部延迟最可控，代价是开发速度与学习曲线。选 Go 要说明可以接受的 GC 停顿并用基准验证；选 Rust 要说明团队有人能带 ([[pl-sig-go-principle]], [[pl-sig-rust-principle]], [[pl-sig-choosing-intro-deploy-footprint]])。
- 组件 B（迭代快、数值计算）：Python，因为生态（数组、表格、绘图）和迭代速度压倒一切；热点循环要放进已经编译好的库，自己写的纯 Python 循环比编译语言慢约 70 倍，这类代码要么向量化，要么下沉到 Rust 或 C 扩展 ([[pl-sig-python-principle]], [[pl-sig-choosing-intro-speed-bands]])。
- 组件 C（业务逻辑多、对接 Java 基础设施）：Java 是合理的默认选项，生态、人才和现有基础设施都在，虚拟线程让阻塞式代码也能扛并发；代价是 JVM 启动与预热、内存占用 ([[pl-sig-java-principle]], [[pl-sig-java-intro-virtual-threads]])。
- 回应「全用 Java」：承认团队熟悉度和基础设施的价值；指出 Java 要为 2 ms 的 p99 付出预热和 GC 调优成本，且 hello world 就要 40 MB 常驻内存与运行时依赖，交付形态和单二进制要求不匹配。回应「全用 Rust」：承认尾部延迟和安全性；指出研究和管理 API 的瓶颈是迭代速度，用 Rust 重写这些部分会拖慢六个月的交付 ([[pl-sig-choosing-evolution-hybrid]], [[pl-sig-choosing-philosophy-boring-polyglot]])。
- 多语言的代价要说出来：边界处的序列化与类型对齐、两套构建与部署流程、团队要维护两种技能。好的边界是进程间的明确接口（消息队列、gRPC 或文件），而不是同一进程里的外部函数调用 ([[pl-sig-choosing-table]], [[pl-sig-choosing-principle]])。
- 每种语言的典型陷阱：Go 的 nil 接口与 goroutine 泄漏，Java 的预热与装箱，Rust 与借用检查器的对抗，Python 的 GIL 与默认可变参数；上线前用 `-race`、负载测试、`cargo clippy`、`mypy` 与往返测试提前发现 ([[pl-sig-gotchas-table]], [[pl-sig-go-pitfall-nil-interface]], [[pl-sig-rust-pitfall-fighting-borrowck]], [[pl-sig-python-pitfall-gil-threads]])。
- hello world 的启动和占用不能决定吞吐与尾部延迟：要用真实消息回放测 p99 和 p99.9，测稳态而不是启动，测峰值内存，而且不要因为一次基准就重写整个系统 ([[pl-sig-choosing-pitfall-benchmark-rewrite]], [[pl-sig-java-pitfall-warmup-boxing]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
