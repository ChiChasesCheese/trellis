---
id: pl-trends-others-intro-kotlin-swift
node: trends.other-languages
type: qa
step: 4
---
## Q
Kotlin 和 Swift 分别是为谁“修好”了什么？空安全、数据类、值语义和协程在这两门语言里是什么样子？

## A
两者都是**在既有大生态上的现代化语言**，目标是让前辈生态的开发者更安全、更高效，而不抛弃生态。

**Kotlin（JetBrains，2011 发布，1.0 在 2016）**：运行在 JVM 上，与 Java 100% 互操作。核心改进：
- **空安全**：类型分成 `String`（非空）与 `String?`（可空），编译器强制处理，大大减少 `NullPointerException`。
- **数据类**：`data class User(val name: String, val age: Int)` 一行得到 `equals`、`hashCode`、`copy`；后来 Java 的 `record` 解决同一问题。
- **扩展函数、默认参数、`val`/`var`**、密封类和 `when` 表达式。
- **协程**（coroutines）：轻量的挂起函数，加上结构化并发。
- 2019 年起成为 Android 官方首选语言。

**Swift（Apple，2014）**：取代 Objective-C，面向 iOS/macOS。核心特性：
- **值语义**：`struct` 是值类型，赋值即复制，类（`class`）才是引用类型。

```swift
struct Point { var x: Int }
var a = Point(x: 1); var b = a; b.x = 2     // a.x = 1, b.x = 2
class Box { var v = 1 }
let c = Box(); let d = c; d.v = 2           // c.v = 2 (shared reference)
```

真实输出：`1 2`、`2`。
- **Optional**：`String?`，用 `?.` 和 `??` 处理，如 `name?.count ?? -1` 在 `nil` 时得到 `-1`。
- **带关联值的枚举**加 `switch`，等于代数数据类型。
- **ARC**（自动引用计数）：编译器插入引用计数操作，不是垃圾回收；需要用 `weak` 打破循环引用。

**流向**：空安全的潮流（Kotlin、Swift、C#、TypeScript）推动了 Java 的 `Optional`、注解式空检查（JSpecify）与 Valhalla 对空值的讨论；`data class`/Swift 的值类型推动了 `record` 与关于值类型的讨论；Swift 的值语义和 ARC 与 Rust 的所有权形成对照。

**要记住的一点**：这两门语言展示了一个路径：不颠覆生态，用可互操作的新语言逐步修复前辈的缺陷。
