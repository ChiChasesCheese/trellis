---
nodes: [ecosystem.modules, ecosystem.compatibility]
tags: [drill]
---
# 练习：模块互相依赖，以及升级后「编译通过、行为不同」

平台组要把一个 Python 单体拆成四个服务，各自用 Go、Java、Rust 和 Python 重写。拆分计划里有两个风险：模块 `a` 和模块 `b` 互相引用；以及统一升级语言版本。你要预测互相引用在四门语言里的后果，预测「只改一行版本配置」会让哪些语言的行为改变，并写出依赖图与升级的团队规则。

```python
# a.py: from b import B_VALUE     # b.py: from a import A_VALUE
# 在另一对文件里改成 import a2 / import b2，在函数体内才用 a2.X
```

```go
// 包 cyc/a 导入 cyc/b，包 cyc/b 又导入 cyc/a
```

```rust
// 同一个 crate 里的 mod a 与 mod b 互相调用；另一组：crate a 与 crate b 在 Cargo.toml 里互相依赖
```

```go
for i := 0; i < 3; i++ { fs = append(fs, func() int { return i }) }   // go.mod: go 1.21 对 go 1.22
```

```rust
let a = [10, 20, 30];
for x in a.into_iter() { /* x 的类型是什么 */ }                      // edition 2018 对 edition 2021
```

**要你给出的**
- 四门语言各自遇到「甲依赖乙、乙依赖甲」时在哪个阶段、以什么形式出现；Python 里哪种写法不会出问题。
- Go 闭包的三个输出（两个版本），Rust `x` 的类型（两个 edition）；它们为什么被称作「静默的语义变化」。
- 一条防循环依赖的规则，一条升级流程规则。

**评分要点**
- Python：`from b import B_VALUE` 与 `from a import A_VALUE` 互相引用时，导入阶段抛 `ImportError: cannot import name ...`，因为被引用的模块还执行到一半；只导入模块、在函数里再取属性的写法（`import a2`，用时才 `a2.X`）可以正常运行并输出 `x` ([[pl-eco-modules-pitfall-python-imports]], [[pl-eco-modules-mechanism]])。
- Go：包之间的循环导入是编译错误（`import cycle not allowed`）；Rust 的 crate 之间循环依赖，`cargo build` 报 `cyclic package dependency`，但同一个 crate 里的 `mod` 之间可以互相调用，示例中 `a(3)` 与 `b(2)` 交替调用得到 `abab`；Java 的类与包之间允许循环引用，两个类互相调用能编译运行（示例输出 `aba`），只有 JPMS 的模块之间禁止。四种选择反映出：依赖图是否必须无环，是语言强加的还是团队纪律 ([[pl-eco-modules-philosophy-acyclic]], [[pl-eco-modules-table]])。
- 为什么 Go 和 Rust 的包级别要求无环：编译单元按依赖顺序构建，无环才能并行编译、增量构建，也迫使设计者把共同依赖抽出来；代价是需要引入接口或新包来打破环 ([[pl-eco-modules-philosophy-acyclic]], [[pl-eco-modules-best-practice]])。
- Go 闭包在 `go 1.21` 下输出 `3 3 3`，在 `go 1.22` 下输出 `0 1 2`；Rust 的 `[10, 20, 30].into_iter()` 在 2018 edition 里 `x` 是 `&i32`（调用的是数组引用的 `into_iter`），在 2021 edition 里是 `i32`（按值）。源码一字未改，类型或结果变了，编译器多数情况下不报错，只给迁移警告 ([[pl-eco-compat-pitfall-silent-semantics]], [[pl-eco-compat-intro-go]], [[pl-eco-compat-intro-rust]])。
- 为什么这是最危险的升级：报错的变化会被编译器和 CI 挡住，静默的变化只能靠测试发现；Go 的做法是把新语义绑定到 `go.mod` 的 `go` 行，让每个模块自己选择何时采用；Rust 的 edition 同理，两者的目标都是让「破坏」变成局部的、可选择的 ([[pl-eco-compat-mechanism]], [[pl-eco-compat-philosophy-promise]])。
- Java 和 Python 的升级风险在另一侧：Java 倾向于保留旧 API，只在运行时抛 `UnsupportedOperationException`；Python 在次版本里移除标准库模块，表现为批量 `ModuleNotFoundError` ([[pl-eco-compat-intro-java]], [[pl-eco-compat-intro-python]])。
- 规则：依赖图用工具检查并在 CI 里禁止新增环，打破环的办法是抽出共同依赖或反转为接口；升级拆成「工具链升级」和「语言版本升级」两个独立发布，每次先在旧版本上让测试全绿，再只改版本号对比结果，并打开所有迁移与弃用检查 ([[pl-eco-compat-best-practice]], [[pl-eco-compat-evolution-opt-in]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
