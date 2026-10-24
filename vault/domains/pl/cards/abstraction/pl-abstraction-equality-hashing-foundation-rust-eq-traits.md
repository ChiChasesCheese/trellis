---
id: pl-abstraction-equality-hashing-foundation-rust-eq-traits
node: abstraction.equality-hashing
type: qa
step: 4
---
## Q
Rust 为什么把相等拆成 `PartialEq` 和 `Eq`？`f64` 为什么不能做 `HashMap` 的键？

## A
Rust 里相等、哈希、顺序都是 trait，通常用 `#[derive(...)]` 自动生成（按字段逐个比较）：

- `PartialEq`：提供 `==`。**部分**等价关系：允许有些值不等于自己。
- `Eq`：一个没有方法的标记 trait，承诺相等关系是**完全**的等价关系（自反、对称、传递）。
- `Hash`：提供哈希，契约是 `a == b` ⇒ 哈希相同。
- `PartialOrd` / `Ord`：部分排序 / 全序，分别对应 `<` 和 `sort()`、`BTreeMap` 的要求。

`f64` 实现 `PartialEq` 但**不实现 `Eq`**，因为 `NaN != NaN` 违反自反性。`HashMap` 的键要求 `Eq + Hash`，于是：

```rust
let mut m = HashMap::new();
m.insert(1.5f64, "x");
// error[E0277]: the trait bound `f64: Eq` is not satisfied
```

编译器在类型层面阻止了「用浮点数当键，NaN 永远查不到」这个运行期陷阱。同样，`Vec<f64>` 不能直接 `sort()`（需要 `Ord`），要显式写 `sort_by(|a, b| a.partial_cmp(b).unwrap())`，或用 `f64::total_cmp`。

派生也带来责任：`#[derive(PartialEq, Eq, Hash)]` 为所有字段递归生成，只要有一个字段没实现就编译失败；自己手写 `Hash` 时，要保证与 `PartialEq` 一致（比较什么字段，就哈希什么字段）。
