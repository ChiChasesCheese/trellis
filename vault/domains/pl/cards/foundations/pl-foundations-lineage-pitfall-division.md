---
id: pl-foundations-lineage-pitfall-division
node: foundations.lineage
type: qa
step: 6
---
## Q
`-7 / 2` 和 `-7 % 3` 在 Java、Go、Rust、Python 里各得到什么？这和谱系有什么关系？

## A
实际运行结果：

| 语言 | `-7 / 2` | `-7 % 3` |
|---|---|---|
| Java | -3 | -1 |
| Go | -3 | -1 |
| Rust | -3 | -1 |
| Python（用 `//`） | -4 | 2 |

Java、Go、Rust 都继承了 C 的整数除法：向零取整（truncate toward zero），余数的符号跟随被除数。Python 来自另一条线，`//` 是向下取整（floor），余数的符号跟随除数，保证 `a == (a // b) * b + a % b` 同时让余数总落在 `[0, b)` 里，这对取模做数组下标、哈希桶很方便。

陷阱：语法长得一样，语义不同。从 Java 转 Python，会以为 `-7 // 2` 是 -3；从 Python 转 Go，用 `x % n` 当下标，x 为负时会得到负数而越界。

```python
print(-7 // 2, -7 % 3)   # -4 2
```

```rust
println!("{}", (-7i32).rem_euclid(3));   // 2，Rust 需要显式要求「始终非负」的余数
```

规则：不要因为语法像 C 就假设语义像 C，凡是涉及负数的取整和取模都要查证。
