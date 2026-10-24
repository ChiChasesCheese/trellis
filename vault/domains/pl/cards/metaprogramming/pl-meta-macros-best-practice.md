---
id: pl-meta-macros-best-practice
node: metaprogramming.macros
type: qa
step: 9
---
## Q
资深工程师在 Rust 里什么时候写宏，什么时候不写？在没有宏的 Go、Java、Python 里，同样的需求怎样解决？

## A
**Rust 的规则：宏是最后一个选项**。顺序是：普通函数，然后泛型加 trait，然后 `derive`，最后才是自己写 `macro_rules!`。理由是函数有类型签名、有文档、IDE 能跳转、错误指向你的代码；宏没有这些。

写宏时：
- 把真正的逻辑放进普通函数，宏只负责「改写语法」那一小层，这样逻辑可以单测。
- 每个参数只求值一次：先 `let v = $x;` 再使用，避免副作用重复发生。
- 宏里引用自己 crate 的东西写 `$crate::path`，否则用户那边会找不到。
- 过程宏的错误要报在用户的代码位置，附清晰的信息；排查展开结果用 `cargo expand`。

**没有宏的语言**：
- **Go**：用泛型取代「为每种类型复制一份」的需求；生成型样板用 `go generate` 调 `stringer` 之类的工具，生成的文件提交进仓库。
- **Java**：用注解加注解处理器（Dagger、MapStruct）；用 Lombok 前要知道它依赖编译器内部 API，升级 JDK 时可能出问题，较新的项目更倾向用 `record` 消除样板。
- **Python**：用装饰器、`dataclass`、`__init_subclass__`。

**何时破例**：当你发现同一段结构一模一样地手写了第四五遍，且无法用泛型或函数消除，才值得写宏。
