---
id: pl-data-strings-intro-rust
node: data.strings-text
type: qa
step: 5
---
## Q
Rust 的 `String` 与 `&str` 是什么？为什么编译器拒绝 `s[0]`，却允许 `&s[0..1]`，它们的行为有何不同？

## A
**两个类型**：
- `String`：拥有所有权的、可增长的字符串，内部是一个 `Vec<u8>`（堆上的字节数组）。
- `&str`：对一段 UTF-8 字节的借用视图（指针加长度），可指向 `String` 的一部分，也可指向程序里的字面量。

**核心不变量**：两者的内容**保证**是合法的 UTF-8。不合法的字节序列根本构造不出来：`String::from_utf8(vec![0xff, 0xfe])` 返回错误。

**为什么禁止 `s[0]`**：「第 0 个」是第 0 个字节、码点还是字形簇？按字节没有意义，按码点不是 O(1)。Rust 不替你选，直接报编译错误：

```rust
let s = String::from("hello");
let c = s[0];
// error[E0277]: the type `str` cannot be indexed by `{integer}`
```

你必须明说：`s.chars()` 迭代码点，`s.bytes()` 迭代字节，`s.char_indices()` 同时给偏移。对 `"a😀é"`，`s.len()` 是 7，`chars().count()` 是 3，偏移是 0、1、5。

**切片按字节，但要求落在字符边界**：`&s[0..1]` 对 `"a😀é"` 取到 `a`；对 `"é"` 做同样的切片会在运行时 panic：`end byte index 1 is not a char boundary; it is inside 'é'`。

**要记住的一点**：Rust 用类型保证编码正确，换来的是拿到 `&str` 的代码永远不用再验证；代价是需要多一步转换，并且错误的切片位置会 panic，而不是静默产生乱码。
