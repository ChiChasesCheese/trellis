---
id: pl-types-gradual-typing-history-evolution
node: types.gradual-typing
type: qa
step: 7
---
## Q
Python 的类型提示是怎样一步步形成的？这条路线说明动态语言的类型化趋势是什么？

## A
Python 的类型系统是社区在语言之外长出来、再被语言吸收的，时间线：

- 2008 年（Python 3.0，PEP 3107）：函数参数和返回值可以写注解，但语言没有规定含义，只是留了位置。
- 2012 年前后：`mypy` 项目开始，证明在 Python 里做静态检查可行。
- 2015 年（Python 3.5，PEP 484）：规定了类型提示的含义，引入 `typing` 模块，包括 `Any`、`Union`、`TypeVar`。
- 3.6：变量注解（PEP 526）。3.8：`Protocol` 结构化类型。3.10：`X | Y` 联合写法，`match` 语句。3.12：泛型的新语法 `class Box[T]`。3.14：注解延迟求值（PEP 649）。
- 工具也在演进：`pyright` 的速度和严格度，新一代用 Rust 写的检查器（如 Astral 的 `ty`、Meta 的 `pyrefly`）追求更快。

趋势背后是同一个规律：动态语言的代码库到了足够规模后，团队几乎都会补上类型。JavaScript 有 TypeScript（2012），Ruby 有 Sorbet 和 RBS，PHP 有逐步加强的类型声明，Python 有类型提示。共同点是路线选的是「可选、可擦除、逐步采用」，因为改变语言运行时语义的代价太高、存量代码太多。

未来的争论点是：类型提示是否应该承担更多运行时职责（校验、优化）。CPython 的 JIT 和特化解释器目前主要靠运行时观察到的类型，而不是提示，但这个边界可能会随着提示越来越完整而移动。
