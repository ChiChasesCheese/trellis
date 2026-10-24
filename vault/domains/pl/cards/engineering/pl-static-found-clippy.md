---
id: pl-static-found-clippy
node: engineering.static-analysis
type: qa
step: 3
---
## Q
Rust 的 clippy 是什么？它的 lint 分组有什么意义，编译器本身又承担了哪些检查？

## A
**clippy** 是 Rust 官方的 linter，随工具链分发，用 `cargo clippy` 运行。它在编译器之上再查「能通过编译，但写得不地道或有隐患」的代码。

**例**：

```rust
pub fn total(v: &Vec<i32>) -> i32 {
    let mut s = 0;
    for i in 0..v.len() { s += v[i]; }
    if v.len() == 0 { return 0; }
    s
}
```

`cargo build` 无任何提示。`cargo clippy` 给出三条警告：

```text
warning: writing `&Vec` instead of `&[_]` involves a new object where a slice will do   (ptr_arg)
warning: the loop variable `i` is only used to index `v`                              (needless_range_loop)
warning: length comparison to zero  -> using `is_empty` is clearer                      (len_zero)
```

三条分别指出：参数应该是切片 `&[i32]`，这样更通用；用索引循环不如迭代器，迭代器还省去了越界检查；与 0 比较长度不如 `is_empty()`。

**lint 分组**是 clippy 的设计重点：按「多大把握是问题」分层，不同组有不同默认级别。
- `correctness`：几乎一定是 bug，默认就是**错误**；
- `suspicious`、`style`、`complexity`、`perf`：默认警告；
- `pedantic`、`nursery`、`restriction`：默认关闭，需要时手动打开，规则更挑剔或更有争议。

**编译器承担的检查**：别的语言靠 linter 或测试抓的很多问题，在 Rust 里是编译错误或编译器自带的 lint：借用冲突、使用已移动的值、未处理的 `Result`（`#[must_use]`）、`match` 不穷尽、未使用的变量与导入（默认警告）。CI 的常规做法是 `cargo clippy -- -D warnings`，把警告当作错误。
