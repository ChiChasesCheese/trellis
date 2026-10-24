---
id: pl-types-algebraic-data-types-pitfall-wildcard
node: types.algebraic-data-types
type: qa
step: 10
---
## Q
在 Rust 的 `match` 里写了 `_ =>` 通配分支，后来给 `enum` 新增变体时会发生什么？

## A
穷尽检查只在没有通配分支时才起作用。`_ =>` 告诉编译器「其余情况我都处理了」，于是新增的变体被它悄悄吞掉，编译器不再报错：

```rust
enum Shape { Circle(f64), Rect(f64, f64), Tri(f64, f64, f64) }
fn area(s: &Shape) -> f64 {
    match s {
        Shape::Circle(r) => 3.14 * r * r,
        Shape::Rect(w, h) => w * h,
        _ => 0.0,
    }
}
// area(&Shape::Tri(3.0, 4.0, 5.0))
```

这段代码编译通过，实际输出 `0`。三角形的面积被当成 0，没有任何错误。

反过来，去掉 `_ =>` 之后，编译器给出精确的提示：

```console
error[E0004]: non-exhaustive patterns: `&Shape::Tri(_, _, _)` not covered
```

这是线上事故的常见成因：同一个 `enum` 在二十个地方被 `match`，新增变体时，没有通配分支的地方都会编译失败，逼你逐个考虑；有通配分支的地方则悄悄用了默认行为，错误可能几个月后才暴露。

对策：

- 自己拥有的 `enum` 避免通配，必要时逐个列出变体，哪怕分支体相同（用 `A | B => ...`）。
- 对外部库的 `#[non_exhaustive]` 枚举，通配分支是必须的，此时在通配分支里写日志或返回错误，而不是静默返回默认值。
- Java 的 `default` 分支同理：对 `sealed` 类型写了 `default`，等于关掉了穷尽检查。
