---
id: pl-abstraction-interfaces-traits-best-practice
node: abstraction.interfaces-traits
type: qa
step: 8
---
## Q
资深工程师在 Go、Java、Rust、Python 里怎样设计和使用接口？背后的原则是什么？

## A
通用原则：**接口应窄、应由使用方的需求塑造、不要为了「以后可能替换」预先抽象**。接口每多一个方法，实现者的负担和以后的破坏面就大一分。

- **Go**：「接受接口，返回具体类型」（accept interfaces, return structs）。参数写成最小的接口（常常一个方法），返回值给出具体类型，让调用方保留所有能力。接口放在使用它的包里，而不是实现它的包。只有存在第二个实现或需要测试替身时才引入接口。
- **Java**：接口作为模块之间的稳定边界；给公共接口新增方法时用 `default`，避免破坏已有实现。不要为每个类机械地配一个 `FooService` / `FooServiceImpl`，只有一个实现且没有替换需求时它是纯噪音。
- **Rust**：函数参数默认用泛型约束 `T: Trait`（静态分派），需要异构集合时才用 `dyn Trait`；trait 保持小而聚焦，复杂能力用多个 trait 组合（`T: A + B`）。
- **Python**：参数只依赖需要的方法，用 `Protocol` 注解表达；只有需要强制子类实现、并想在实例化时报错时才用 ABC。

何时打破：对外发布的库、要长期稳定的 API，值得提前设计接口并写文档，因为后期加方法会破坏所有实现者。
