---
id: pl-trends-others-intro-csharp
node: trends.other-languages
type: qa
step: 3
---
## Q
C# 为什么被称为“语言特性的试验场”？async/await、LINQ 和可空引用类型分别是什么，影响了谁？

## A
**背景**：C# 由微软的 Anders Hejlsberg 团队于 2000 年推出，最初与 Java 相似，之后在**语言演进的速度**上走到前面。它背后是一个有强中心设计团队的大厂，能在版本里持续引入新特性，并有 IDE 紧密配合。

**三个有代表性的创新**：
1. **LINQ**（2007）：语言集成查询。把“对集合过滤、映射、分组”写成统一的查询表达式，对内存集合、数据库、XML 都适用。背后是 lambda、扩展方法、泛型和类型推断的组合。影响了 Java 的 Stream、Python 的推导式的使用习惯。
2. **async/await**（C# 5，2012）：把异步代码写成顺序样式，编译器转换成状态机。随后被 Python（3.5）、JavaScript、Rust、Kotlin 和 C++20 采纳，是最成功的“语言特性外溢”案例之一。
3. **可空引用类型**（C# 8，2019）：在类型里区分“可能为 null”和“一定非 null”，编译器检查。目的是减少空引用异常，这是 Kotlin 与 Swift 的核心特性之一的后补。

**还有**：属性（property，`obj.Name` 背后是 getter/setter）、事件、模式匹配、记录（record）、结构体的值语义（所以 C# 在值类型与布局上比 Java 更灵活）。

**对各门语言的意义**：
- **Java**：很多特性（var、record、模式匹配、`switch` 表达式）可以在 C# 或 Kotlin 里看到先行版本。
- **Python/Rust/C++**：async/await 的语法和状态机思想来自 C#（C++20 以 `co_await` 协程的形式引入，只给机制，不带调度器）。
- **差异**：C# 对兼容性更愿意付出代价（引入新语法、偶尔破坏），Java 则非常保守，所以特性落地更慢。

**要记住的一点**：C# 的价值在于展示了“一个有权威设计团队的语言，可以以一年的节奏演进，而不丢掉用户”。
