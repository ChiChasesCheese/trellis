---
id: pl-functional-generators-table
node: functional.generators
type: qa
step: 7
---
## Q
Go、Java、Rust、Python 在生成器 / 协程上的选择有什么不同？

## A
| 语言 | 惰性序列的写法 | 协程类型 | 代价 |
|---|---|---|---|
| Python | `yield` 生成器，`send`，`yield from` | 无栈 | 递归要层层 `yield from`，只能在生成器函数内暂停 |
| Go | `iter.Seq` + `range`，`iter.Pull` 转拉取 | 有栈（Pull 用协程） | 要显式 `stop`，切换有成本 |
| Rust | 手写 `Iterator`，`gen` 未稳定；`async` 状态机 | 无栈，编译期状态机 | 生成器语法缺位，`async` 的函数着色 |
| Java | 手写 `Iterator` / `Stream.iterate` / 虚拟线程 | 无语言级生成器；虚拟线程是有栈 | 样板多，或线程交接开销 |

规律：**无栈协程换取小体积与确定的内存布局，有栈协程换取暂停点任意深度的灵活性**。

Python 在 2001 年用生成器让惰性序列几乎零样板，后来又基于它长出了 `async`；Go 把协程放在运行时里，由调度器统一管理，程序员不需要区分「会暂停的函数」；Rust 因为没有运行时，必须在编译期把暂停点变成状态机，所以 `async` 先落地，生成器语法等待稳定；Java 在语言保守的传统下，先用类库（Stream）解决大部分需求，最终用虚拟线程从运行时层面提供有栈协程。
