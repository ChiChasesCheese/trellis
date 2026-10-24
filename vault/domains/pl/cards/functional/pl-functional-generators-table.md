---
id: pl-functional-generators-table
node: functional.generators
type: qa
step: 7
---
## Q
Go、Java、Rust、Python、C++ 在生成器 / 协程上的选择有什么不同？

## A
| 语言 | 惰性序列的写法 | 协程类型 | 代价 |
|---|---|---|---|
| Python | `yield` 生成器，`send`，`yield from` | 无栈 | 递归要层层 `yield from`，只能在生成器函数内暂停 |
| Go | `iter.Seq` + `range`，`iter.Pull` 转拉取 | 有栈（Pull 用协程） | 要显式 `stop`，切换有成本 |
| Rust | 手写 `Iterator`，`gen` 未稳定；`async` 状态机 | 无栈，编译期状态机 | 生成器语法缺位，`async` 的函数着色 |
| Java | 手写 `Iterator` / `Stream.iterate` / 虚拟线程 | 无语言级生成器；虚拟线程是有栈 | 样板多，或线程交接开销 |
| C++ | C++20 协程：函数里写 `co_yield` 产出值；C++23 的 `std::generator` 是现成的封装 | 无栈，编译器改写成状态机；帧默认在堆上，可被优化到栈上 | 直接写要手写 `promise_type` 样板；`std::generator` 的库支持滞后（本机的 libc++ 还没有 `<generator>`） |

规律：**无栈协程换取小体积与确定的内存布局，有栈协程换取暂停点任意深度的灵活性**。

Python 在 2001 年用生成器让惰性序列几乎零样板，后来又基于它长出了 `async`；Go 把协程放在运行时里，由调度器统一管理，程序员不需要区分「会暂停的函数」；Rust 因为没有运行时，必须在编译期把暂停点变成状态机，所以 `async` 先落地，生成器语法等待稳定；Java 在语言保守的传统下，先用类库（Stream）解决大部分需求，最终用虚拟线程从运行时层面提供有栈协程。

C++ 在这条线上和 Rust 同类：没有运行时，所以只能是编译期状态机。区别在于它先给了通用的机制（C++20），再用后续标准逐步补库封装（C++23 才有 `std::generator`）。这是 C++ 的惯常节奏：零开销原则要求语言只给不带成本的积木，高层便利由库和后续标准补，用户要么等，要么自己写 `promise_type`（规定协程如何开始、暂停、产出值的类型）。
