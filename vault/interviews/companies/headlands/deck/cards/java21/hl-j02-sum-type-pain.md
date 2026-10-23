---
id: hl-j02-sum-type-pain
node: java21.j02-sealed
type: qa
step: 1
---
## Q
什么是和类型（sum type，也叫代数数据类型 ADT）？为什么 Java 8 用开放的 `interface` 加几个实现类表达它有两个根本问题？

## A
和类型：数据天然是"**要么 A、要么 B、要么 C，没有别的**"，每种带不同数据（计算结果成功带值 / 失败带错误、引擎事件成交 / 挂单 / 撤单）。

Java 8 的两个问题：
1. **接口是开放的**：任何人在任何文件、包、别的团队的代码里都能再写 `class Rejected implements Event`，运行时才会走到兜底的 `IllegalStateException`。
2. **编译器不知道一共几种**，没法检查"处理全了没有"。`else throw` 是人肉兜底：一年后有人加了第四种事件却忘改 `describe`，编译照样过，直到线上炸。

`sealed`（Java 17 正式，15、16 为预览）就是为解决这两点。
