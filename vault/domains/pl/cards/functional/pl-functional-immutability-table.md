---
id: pl-functional-immutability-table
node: functional.immutability
type: qa
step: 7
---
## Q
Go、Java、Rust、Python 对不可变性的支持有什么区别？

## A
| 语言 | 默认 | 语言提供的手段 | 不可变的深度 |
|---|---|---|---|
| Go | 可变，按值复制 | `const`（仅编译期标量），其余靠约定 | 无类型层保证 |
| Java | 可变 | `final`、`record`、`List.of` | 浅（`final` 只管绑定，`record` 管字段） |
| Rust | 不可变，`mut` 才可改 | `let`/`mut`，`&`/`&mut` | 深（对拥有的数据），且排他 |
| Python | 可变 | `tuple`、`frozenset`、`frozen` dataclass | 浅 |

规律：默认值决定了行为。默认可变的语言里，不可变是需要主动选择的优良实践，忘了写就是可变；Rust 把默认翻转，可变需要显式标记。

Rust 的哲学是「状态变化是需要被看见的事」，所以 `mut` 要写出来，`&mut` 要写出来，读代码时一眼就看到哪里会变。Java 作为企业语言，倾向于通过规范和类库（`record`、不可变集合）提供不可变，而不改变默认。Go 的设计者认为共享内存加锁与通道已足以管理状态，没有必要增加类型层的复杂性。Python 作为动态语言，信任程序员，提供几个不可变类型作为工具。

一个共同事实：没有一门主流语言默认深不可变（只有 Haskell 等纯函数式语言如此），因为性能与表达上的代价通常被认为不值得。
