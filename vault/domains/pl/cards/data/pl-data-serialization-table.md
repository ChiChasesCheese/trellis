---
id: pl-data-serialization-table
node: data.serialization
type: qa
step: 8
---
## Q
比较 Go、Java、Rust、Python 的序列化路线：各选了什么机制，买到什么，付出什么？

## A
| 语言 | 主要机制 | 买到 | 付出 |
|---|---|---|---|
| Go | 反射加 struct tag 的 `encoding/json` | 标准库自带，零依赖，够用 | 默认宽松（忽略未知字段、数字变 `float64`），较慢 |
| Java | Jackson（反射加注解）；内建 `Serializable` | 功能最丰富，多态、流式、注解定制 | 内建序列化是安全隐患；Jackson 的多态类型同样要小心 |
| Rust | serde（编译期 `derive`，数据模型与格式分离） | 快、严格、一份类型多种格式 | 要加依赖和编译时间；格式需要引入对应 crate |
| Python | `json`（窄而安全）；`pickle`（宽而危险） | 开箱即用，`pickle` 能保存几乎一切 | `pickle` 是代码执行；自定义类要自己转换 |

**逻辑**：这张表其实是第一张反射对比表的续篇。序列化是反射最重要的客户：Go 用运行时反射，因为语言只给了这条路，换来简单；Java 在反射之上叠了注解，换来丰富；Rust 因为没有反射，用宏在编译期生成，换来性能和严格；Python 的动态性让 `pickle` 可以把任意对象当程序来存，换来便利，也换来风险。

**一个有意义的对照**：Rust 的 serde 是唯一把「数据模型」抽成独立层的方案，所以它新增一种格式的成本是写一个 crate，不影响任何用户类型。Go 和 Java 的 JSON 库则是各自语言里把 JSON 与反射耦合在一起，换格式要换整套库。
