---
id: oop-program-to-interface-scope
node: oop.interfaces
type: qa
---
## Q
"Program to an interface" — where does it pay off in a machine coding round, and where does it become interface bloat?

## A
- **Pays** at variation points and boundaries: pricing/allocation strategies, notification channels, storage — so extension probes are additive and tests can inject fakes.
- **Bloat**: an interface per class with one implementation and no seam need — pure ceremony (speculative generality).

Extract the interface when the second implementation or the test seam actually arrives; requirements hinting at variants ("support multiple pricing schemes") count as arrival.

## Q zh
"面向接口编程" —— 在机考里它在哪些地方真的划算，又在哪里会变成 interface 膨胀？

## A zh
- **划算**的地方是变化点和边界：定价/分配策略、通知渠道、存储 —— 这样扩展性追问可以靠新增来回答，测试也能注入 fake。
- **膨胀**：每个类都配一个接口，却只有一个实现、也不需要任何接缝 —— 纯粹的仪式感（speculative generality）。

等第二个实现或者测试接缝**真的出现**时再抽接口；需求里透出的变体暗示（"要支持多种定价方案"）也算出现。
