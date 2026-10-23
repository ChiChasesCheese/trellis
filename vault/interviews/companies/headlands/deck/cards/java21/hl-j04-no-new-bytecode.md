---
id: hl-j04-no-new-bytecode
node: java21.j04-record-patterns
type: qa
step: 13
---
## Q
record 模式编译后用了新的 JVM 指令或 `invokedynamic` 吗？`case Add(var l, var r)` 展开成什么？

## A
**没有**新 JVM 指令，也没有 `invokedynamic`。编译器把它展开成**普通类型检查 + 访问器调用**：

1. 外层类型判断由 `typeSwitch` 完成，之后只是 `checkcast` 转型；
2. `invokevirtual Add.left()` 取第一个组件，存临时变量，再赋给绑定变量 `l`；
3. `invokevirtual Add.right()` 取第二个；
4. 然后执行分支体。

嵌套模式展开成多层"取组件 → 查类型 → 再取"，没有额外对象分配。编译出的字节码**基本等价于手写的 `instanceof` + 强转 + getter**，没有额外开销。
