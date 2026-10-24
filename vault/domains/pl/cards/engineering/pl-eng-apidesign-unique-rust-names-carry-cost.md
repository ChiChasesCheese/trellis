---
id: pl-eng-apidesign-unique-rust-names-carry-cost
node: engineering.api-design
type: qa
step: 8
---
## Q
Rust 标准库的 `as_`、`to_`、`into_` 命名前缀表达了什么？为什么说 Rust 的 API 把“成本”写进了名字和签名？

## A
Rust 的 API 设计指南规定了一套命名约定，调用者看名字就能判断成本，而不必读实现：

| 前缀 | 含义 | 成本 | 所有权 |
|---|---|---|---|
| `as_` | 把数据换一种视图 | 免费（不分配，不复制） | 借用 → 借用 |
| `to_` | 产生一个新值 | 可能昂贵（分配、复制、计算） | 借用 → 拥有 |
| `into_` | 消耗自己，转换成另一个值 | 通常便宜，复用原来的缓冲区 | 拥有 → 拥有 |

实际例子：
```rust
let s = String::from("héllo");
let view: &str = s.as_str();        // free view
let up: String = s.to_uppercase();  // allocates a new String
let bytes: Vec<u8> = s.into_bytes();// consumes s, reuses its buffer
```
输出：`héllo HÉLLO 6` 与 `6`（`é` 占两个字节，所以长度是 6）。`into_bytes` 之后 `s` 就不能再用了。

这是 Rust 价值观的缩影：**成本不应该是隐藏的**。对比：
- **Java**：`list.toString()`、`list.stream()`、`new ArrayList<>(list)` 都是方法调用，一眼看不出哪个复制了几百万个元素；
- **Python**：`list(x)`、`sorted(x)`、`x.copy()` 靠记忆；
- **Go**：`append` 可能共享也可能不共享底层数组，要读文档。

Rust 做不到“没有隐藏成本”，但它把大多数隐藏成本变成签名里能看到的东西：是否拥有（`self`）、是否借用（`&`）、是否可变（`mut`）、是否复制（`Clone` 要显式调用 `.clone()`）。

**对自己写库的启示**：即使在没有所有权的语言里，也可以借鉴这个约定：`toX()` 表示新对象、`asX()` 表示视图、`withX()` 表示返回修改后的副本（不可变对象），让调用者从名字判断开销和副作用。
