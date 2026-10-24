---
id: pl-data-serialization-intro-rust
node: data.serialization
type: qa
step: 5
---
## Q
Rust 的 serde 是什么？「数据模型」与「格式」分离的设计怎样工作，`derive` 在其中做了什么？

## A
**是什么**：serde 是 Rust 事实标准的序列化框架。它定义两个 trait（可理解为接口）：`Serialize`（我能把自己描述成数据）和 `Deserialize`（我能从数据重建自己）。

**两层分离**：
1. **数据模型**（data model）：serde 约定的一套抽象类型：整数、字符串、序列、映射、结构体、枚举等约三十种。
2. **格式**（data format）：`serde_json`、`toml`、`bincode`、`serde_yaml` 等独立的 crate，各自负责把数据模型写成/读成具体格式。

你的类型只和数据模型打交道，格式是可插拔的：同一个结构体加上 `#[derive(Serialize, Deserialize)]`，就能同时用于 JSON、TOML 和二进制。

**`derive` 做了什么**：它是编译期运行的过程宏，读你的结构体定义，**生成**针对这个具体类型的 `Serialize`/`Deserialize` 实现代码，逐字段展开，没有反射。

```rust
#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct U { id: i64, name: String, tags: Vec<String> }
```

**严格性更强**：真实报错：
- 多余字段（有 `deny_unknown_fields` 时）：报错文本（省略引号）：unknown field nmae, expected one of id, name, tags。
- 类型不符：`invalid type: string "7", expected i64 at line 1 column 9`。
- 缺字段：missing field name。
- 枚举默认的编码：`Shape::Circle { r: 1.0 }` 和 `Shape::Square(2.0)` 输出为 `{"Circle":{"r":1.0}}` 和 `{"Square":2.0}`，变体名成为键（外部标签）。

**要记住的一点**：serde 在编译期把「类型怎么变成数据」做完，运行时没有查表，所以很快；一次本机测量，解码同一个小对象约 100 ns，编码约 30 ns。
