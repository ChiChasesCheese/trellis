---
id: hl-j02-three-modifiers-quiz
node: java21.j02-sealed
type: qa
step: 24
---
## Q
面试追问：Java 的 `sealed` 要解决什么问题，给出一句话定义，再说它解锁了 `switch` 的哪项能力？

## A
`sealed` 把"这个类型**恰好有哪几种**"写进类型系统：`permits` 列出许可的直接子类，每个子类必须是 `final` / `sealed` / `non-sealed`，名单由 `javac` 和 JVM 共同强制。

解锁的能力：**穷尽性检查**。`switch` 覆盖了所有许可子类就不需要 `default`；以后新增变体，所有漏处理的 `switch` 在编译期报错。

与 `record` 搭配，就得到 Java 版的代数数据类型。
