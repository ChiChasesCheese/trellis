---
id: pl-foundations-tradeoff-axes-found-bounds-unsafe
node: foundations.tradeoff-axes
type: qa
step: 2
---
## Q
什么是边界检查（bounds checking）？Rust 的 `unsafe` 块又是什么，它放弃了什么？

## A
边界检查：访问数组或切片的第 `i` 个元素时，运行时先核对 `i` 是否小于长度；越界就报错，而不是去读相邻的内存。Go、Java、Rust、Python 默认都做，C 默认不做，缓冲区溢出漏洞就由此而来。

Rust 默认就做边界检查。取元素有两种风格：下标 `v[i]` 越界会 panic（终止当前线程）；`v.get(i)` 返回 `Option`，越界得到 `None`。

`unsafe` 是 Rust 里标出的一小块代码，在里面编译器放松一部分检查，允许做几类原本禁止的事：解引用裸指针、调用不做检查的函数。责任转给程序员：你向编译器保证这里不会出事。

```rust
let v = vec![1, 2, 3];
let i = v.len() + 7;
println!("{:?}", v.get(i));                      // None
println!("{}", unsafe { *v.get_unchecked(1) });   // 2：你保证 1 在范围内
```

实际输出 `None` 和 `2`。`get_unchecked` 省掉了比较，但如果下标越界就是未定义行为。

要点：`unsafe` 不是「关闭所有检查」，借用规则等照常有效，它只是解锁几个需要人来担保的操作；它的价值在于把危险限制在可搜索、可评审的小范围内，其余代码仍然由编译器保证安全。
