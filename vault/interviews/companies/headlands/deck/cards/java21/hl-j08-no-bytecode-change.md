---
id: hl-j08-no-bytecode-change
node: java21.j08-var
type: qa
step: 9
---
## Q
`var` 在 JVM 层做了什么？它影响运行时性能吗？怎么验证？

## A
**什么都没做**：`var` 纯编译期特性，JVM 看不到。

验证：同一逻辑写两个方法，一个用 `var m = new HashMap<String, List<Integer>>()`，一个显式写类型。用 `javac -g` 编译后 `javap -c -l` 对比：14 条字节码指令**逐条相同**，`LocalVariableTable` 也相同（`m  Ljava/util/HashMap;`）。

`var` 在 class 文件里不留痕迹，性能和调试器所见与手写类型一样；它不会让代码变快变慢，纯粹是**可读性**问题。
