---
id: hl-sd01-bytecode
node: system-design.sd01-unused-code
type: qa
step: 13
---
## Q
为什么在字节码而不是源码上做 Java 的引用分析？有什么缺点？C++ 怎么办？

## A
优点：
- **引用已被编译器解析好**：`invokevirtual com/hl/Order.price()J` 直接写着 owner、name、descriptor，不用自己做名字解析、重载决议、泛型擦除、import 处理；
- **成本低约 100 倍**（量级估计）：读 `.class` 是线性扫描常量池和方法体，ASM 一核每秒处理数百 MB，不需要 javac 的类型归属；
- **精确**：lambda 在字节码里是 `invokedynamic`，其引导方法参数里能读到真实的目标 `MethodHandle`，方法引用 / lambda 的边可静态恢复。

缺点：没有源码位置（用 `SourceFile`、`LineNumberTable` 回映射）；依赖构建产物（CI 本来就产出，可缓存）；泛型被擦除（对可达性影响很小）；Kotlin / Scala 的合成方法要过滤。

C++ 没有字节码，用 clang 索引；**链接器本身就是可达性分析器**：编译 `-ffunction-sections -fdata-sections`，链接 `-Wl,--gc-sections,--print-gc-sections` 会列出被丢弃的函数段，是免费的静态证据。
