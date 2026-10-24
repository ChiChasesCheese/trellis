---
id: pl-errors-models-philosophy
node: errors.models
type: qa
step: 8
---
## Q
Go 的「错误是值」、Python 的 EAFP、Rust 的「让非法状态无法表示」，各自体现了什么样的语言哲学？

## A
**Go：错误是值（errors are values）。** 错误不是语言里的特殊机制，只是实现了 `Error() string` 的普通值，可以存储、比较、包装、在 channel 里传递，用普通的 `if` 和循环处理。设计者认为异常制造了「隐藏的控制流」：读一段代码，你看不出哪一行会让函数提前离开。Go 宁可让每个失败点都写出来，也要让阅读者一眼看清路径。代价是冗长，并且接受它。

**Python：EAFP（Easier to Ask Forgiveness than Permission，请求原谅比请求许可更容易）。** 先做，出错了再处理，而不是先检查再做。文件是否存在，先 `open`，失败再 `except FileNotFoundError`；这样避免了「检查与使用之间的竞态」，也避免了重复检查。哲学是「鸭子类型加信任」：假定调用有效，把失败当作例外。

**Rust：让非法状态无法表示。** 值可能缺失，就用 `Option<T>`，没有「空指针」；操作可能失败，就用 `Result<T, E>`，返回值必须被处理才能拿到 `T`。失败不是运行时的惊喜，而是类型的一部分。它的背后是 Rust 的整体态度：把尽可能多的错误从运行时提前到编译期。

**Java：试图用编译器强制处理。** 受检异常（checked exception）的设想是：函数的签名必须声明会抛什么，调用者必须处理或继续声明。后来的实践表明，这种强制在大型系统里带来了大量空 `catch` 和 `throws Exception`，削弱了初衷。

对比 Go 与 Rust：二者都是「错误是值」，但 Rust 的编译器参与保证值被处理，Go 把责任留给程序员。
