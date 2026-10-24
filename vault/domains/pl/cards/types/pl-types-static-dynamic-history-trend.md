---
id: pl-types-static-dynamic-history-trend
node: types.static-dynamic
type: qa
step: 7
---
## Q
静态类型和动态类型之争是怎样演变的？今天的语言为什么都在往中间靠？

## A
早期两派泾渭分明：1958 年的 Lisp 是动态类型的代表，1960 年代的 Algol 家族和之后的 Pascal、C 是静态类型。动态类型靠「写得快、交互式」在脚本和原型领域占了上风（Python、Ruby、JavaScript）；静态类型靠「大规模代码可维护」在大型系统领域站稳（Java、C++）。

趋势是互相补课：

- 静态类型语言降低标注成本。类型推断（type inference）让你少写类型：C++11 的 `auto`、Go 的 `:=`、Java 10 的 `var`、Rust 的整体类型推断。
- 动态类型语言加上可选类型。TypeScript（2012）给 JavaScript 加类型；Python 3.5（2015）通过 PEP 484 规定类型提示的含义，`mypy`、`pyright` 等外部工具据此检查。
- 编译器和 IDE 的工具化：静态类型让「跳转到定义」「安全重命名」成为可能，动态类型语言的工具靠类型提示获得同样能力。

原因是项目规模：当代码库从几千行长到几十万行、团队从一个人变成几十人，「这个函数接受什么」就成了需要机器检查的契约。许多大型 Python 代码库都在逐步加类型提示，就是这个规律的体现。
