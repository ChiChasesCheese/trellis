---
id: pl-foundations-tradeoff-axes-principle
node: foundations.tradeoff-axes
type: qa
step: 1
---
## Q
语言设计里有哪几条根本的权衡轴（trade-off axis）？为什么不可能有「什么都好」的语言？

## A
每条轴的两端都是好东西，但拉向一端就必然离开另一端。五条最重要的轴：

1. 安全与控制（safety vs control）：编译器和运行时替你检查越多，你对内存和硬件能做的事就越受限。
2. 表达力与简单（expressiveness vs simplicity）：特性越多，一件事能写得越短越准，但读代码的人要学的东西也越多。
3. 编译期检查与运行期灵活（static vs dynamic）：越早发现错误越安全，但越难写出「运行时才决定行为」的程序。
4. 性能与开发速度（performance vs productivity）：贴近机器的写法快，但要多写、多想；高层写法省事，但隐藏了成本。
5. 向后兼容与演进（compatibility vs evolution）：保证旧代码永远能跑，就不能修正设计错误；允许断裂，就会有迁移成本，甚至像 Python 2 到 3 那样分裂社区。

为什么不可能全都好：这些轴背后是同一个资源约束，即检查要花成本，抽象要花成本，兼容要花成本。一门语言把某一端推到极致，就要由另一端来付账。理解一门语言，等于知道它在这五条轴上各站在哪里，以及站在那里是想解决谁的问题。
