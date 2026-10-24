---
id: pl-memory-lifetimes-foundation-dangling
node: memory.lifetimes
type: qa
step: 2
---
## Q
Rust 里生命周期（lifetime）是什么？“不能比被引用的值活得更久”在一个最小例子里怎么被拒绝？

## A
引用只是一个地址。如果它指向的值已经被销毁，就成了悬空引用，读写它是未定义行为。Rust 要求每个引用都有一个**生命周期**：这个引用在程序中有效的那段区间；并要求被引用的值的存活区间必须**包住**引用的区间。

最小例子：

```rust
let r;
{
    let x = 5;
    r = &x;          // r borrows x
}                    // x is dropped here
println!("{}", r);   // r would point to freed memory
```

```console
error[E0597]: `x` does not live long enough
  `x` dropped here while still borrowed
  borrow later used here
```

`x` 在内层花括号结束时销毁，`r` 却在之后还要使用，它的有效区间超出了 `x`，编译器据此拒绝。注意：整个检查在编译期完成，没有运行时成本。

在 Java、Go、Python 里同样的写法是合法的：对象在堆上，只要还有引用指向它，GC 或引用计数就不会回收它，所以引用永远不会悬空。

要记住的一个事实：生命周期不是运行时的东西，而是编译器用来证明“引用不会悬空”的一个标签，GC 语言把这个证明推迟到运行时靠保活来完成。
