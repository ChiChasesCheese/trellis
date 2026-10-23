---
id: hft-java-modern-records-sealed
node: java.modern
type: qa
step: 1
---
## Q
records、sealed 类型和模式匹配（pattern matching）这些现代 Java 特性，对低延迟代码有什么帮助和风险？

## A
帮助主要在可读性和正确性：
- `record` 一行定义不可变的数据载体；
- `sealed interface Msg permits NewOrder, Cancel, Fill` 把消息类型封闭起来；
- `switch` 加模式匹配时，编译器检查是否穷尽，漏处理一种消息会直接报错，以后新增类型时所有 `switch` 都会被点名。

风险在热路径：`record` 仍然是普通堆对象（对象头加字段），每次 `new` 仍是分配；只有逃逸分析能证明它不逃出方法时才会被消除，而这并不保证。所以研究平台、命令解析、风控规则这些中冷路径放心用；每条行情都 `new` 一个 record，就是在制造垃圾。（模式匹配 `switch` 在 JDK 21 正式，`sealed` 在 JDK 17 正式。）
