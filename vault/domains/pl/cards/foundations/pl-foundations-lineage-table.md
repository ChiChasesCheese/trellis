---
id: pl-foundations-lineage-table
node: foundations.lineage
type: qa
step: 5
---
## Q
Go、Java、Rust、Python 各自从哪些祖先那里借来了核心思想？这些继承让它们获得什么、又带来什么包袱？

## A
| 语言 | 主要祖先 | 借来的核心思想 | 换来 | 包袱 |
|---|---|---|---|---|
| Go | C；Pascal、Oberon；CSP、Newsqueak | C 的骨架，Pascal 系的声明和包，CSP 的通信模型 | 并发写起来像顺序代码，语法对 C 程序员亲切 | 带着 C 的指针和 `nil`，没有 ML 家族的类型表达力 |
| Java | C、C++；Smalltalk、Lisp | C 系语法，Smalltalk 的对象与虚拟机，Lisp 的垃圾回收 | 把 C++ 程序员平滑带进安全的托管环境 | 继承了 C 的隐式数值转换，原始类型与对象的二分 |
| Rust | C++；ML、Haskell；Cyclone | C++ 的 RAII（离开作用域自动释放资源）和零成本抽象，ML 的代数数据类型，Haskell 的类型类，Cyclone（C 的一个安全方言）的区域内存管理 | 系统级性能加函数式语言级的类型表达力 | 两个家族的复杂度叠加，学习曲线陡 |
| Python | ABC；C；Modula-3；Lisp、Haskell | ABC 的缩进与高层数据类型，C 的实现，Lisp 的函数式工具 | 极高的可读性和开发效率 | 动态语义难以优化，解释器绑定 C 实现 |

背后的逻辑：血统决定了「天然擅长什么」。Rust 一半来自 C++、一半来自 ML，所以它的特点是性能与类型表达力同时有；Go 来自 C 加 CSP，所以特长是工程规模下的并发服务；Java 来自 C++ 加 Smalltalk，所以特长是托管环境下的大型对象系统；Python 与 C 系语法无关，来自「教学语言」的可读性传统。理解谱系的价值在于预测：遇到新语言，先看它的祖先，就能猜到它在哪些地方强、哪些地方有包袱。
