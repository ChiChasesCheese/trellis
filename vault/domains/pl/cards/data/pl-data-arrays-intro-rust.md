---
id: pl-data-arrays-intro-rust
node: data.arrays-slices
type: qa
step: 5
---
## Q
Rust 的 `[T; N]`、`&[T]` 和 `Vec<T>` 各是什么？借用检查器怎样挡住「扩容后悬空引用」这类错误？

## A
**三个类型**：
- `[T; N]`：长度编译期已知的数组，值类型，通常放在栈上。`[i32; 3]` 占 12 字节。
- `Vec<T>`：堆上的动态数组，持有数据，自己是三个字：（指针，长度，容量）。满了自动扩容，类似 Go 但拥有数据。
- `&[T]`：切片引用，是一个「胖指针」（指针加长度，共两个字，本机 16 字节），借用某段连续元素。数组、`Vec` 的一部分都可以取得它，函数参数通常写成 `&[T]`，同时接受数组和 `Vec`。

```rust
let a = [1, 2, 3];
let s: &[i32] = &a[1..];       // [2, 3], no copy
size_of_val(&a) == 12; size_of::<&[i32]>() == 16
```

**借用规则让别名安全**：切片是借用，所以编译器追踪它的生命周期。`Vec` 扩容会换地址，如果允许你同时持有指向旧元素的引用，那就是悬空指针（C++ 里的迭代器失效）。Rust 在编译期拒绝：

```rust
let mut v = vec![1, 2, 3];
let first = &v[0];
v.push(4);
println!("{}", first);
// error[E0502]: cannot borrow `v` as mutable because it is also
// borrowed as immutable
```

**要记住的一点**：Go 里这类问题是运行时的静默别名，Rust 里是编译期错误。三个类型把「拥有」「定长」「借用」分开，代价是需要学会选对类型，收益是别名问题在编译期消失。
