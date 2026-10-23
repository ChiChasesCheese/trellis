---
id: hl-javaq-a-q04-main
node: java-questions.a-speed
type: qa
step: 14
---
## Q
你的 Java 服务启动后头几秒很慢，之后就正常了。为什么？你会怎么处理？
Your Java service is slow for the first few seconds after start-up, then fine. Why, and what would you do about it?

## A
一句话：代码一开始在**解释器**里跑，热点要累计到阈值才被编译；JIT 编译线程、类加载、CDS 都要时间。

要说的点：
- 原因链：解释执行 → 计数器过阈值 → 后台线程编译 → 切换到 C1 → 更热再 C2。
- 处理：**预热**（回放真实流量）、减少启动期类加载（CDS）、必要时提前编译（AOT / native image）。
- 预热完成前**不加入负载均衡**，也不把预热前的数据计入延迟 SLO。
- 口径数字：解释器约 24 ns/次调用，编译后约 2 ns，约 10 倍。
