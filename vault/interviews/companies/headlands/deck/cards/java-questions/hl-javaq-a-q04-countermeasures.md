---
id: hl-javaq-a-q04-countermeasures
node: java-questions.a-speed
type: qa
step: 17
---
## Q
Java 服务启动预热慢，有哪几种对策？为什么预热不能只用单一类型的请求？native image（AOT）的取舍是什么？

## A
- **预热**：上线前用与生产**同分布**的流量回放。只用单一类型预热，C2 会做过于乐观的推测，真实流量一来触发去优化（deoptimization）。
- **减少类加载 / 初始化**：CDS（类数据共享，class data sharing；JDK 类默认有归档，应用类用 AppCDS）。
- **预热完成才注册**：负载均衡只加入已预热的实例。
- **AOT / native image（GraalVM）**：启动快，但峰值通常低于 C2，且反射 / 动态特性受限。
- **Leyden 项目**在推进 AOT 缓存，但 Java 21 里**没有**，不要说已有。
