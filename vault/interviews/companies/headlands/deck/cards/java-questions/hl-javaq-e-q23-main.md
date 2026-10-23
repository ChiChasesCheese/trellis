---
id: hl-javaq-e-q23-main
node: java-questions.e-jit-gc
type: qa
step: 19
---
## Q
你的 Java 交易组件有延迟尖刺。怎么选择和调优 GC？什么时候用 ZGC，什么时候用 G1？
Your Java trading component has latency spikes. How do you choose and tune the GC? When ZGC, when G1?

## A
一句话：**先量化，再选，再治本**。
1. 量化：谁在暂停？`-Xlog:gc*,safepoint`。
2. 选择：延迟敏感且堆大 → **分代 ZGC**（21 用 `-XX:+UseZGC -XX:+ZGenerational`）；通用 / 吞吐 → **G1**。
3. 治本：降低分配率（热路径零分配）、堆留余量（`-Xms=-Xmx`）、`-XX:+AlwaysPreTouch`，最后才是微调。
- 数据：同一负载最大间隔 Parallel 22.4 ms / G1 8.2 ms / ZGC 0.14 ms。
- 最强的杠杆是**降分配率**，不是换 GC：没垃圾就没 GC。
