---
id: pl-functional-first-class-functions-best-practice
node: functional.first-class-functions
type: qa
step: 9
---
## Q
资深工程师在各语言里怎样使用函数值？什么时候该用，什么时候该换成别的结构？

## A
通用判断：**函数值适合「一小段由调用者决定的行为」**；行为复杂、有状态、需要多个相关方法时，用具名的接口 / trait / 类更清晰。

- **Java**：优先使用标准函数式接口（`Function`、`Predicate`、`Supplier`），不要为每个场景发明新接口；lambda 简短，复杂就提成具名方法再用方法引用（`this::validate`）。lambda 里不要修改外部状态。涉及受检异常的 API，要么在边界处统一包装成非受检异常，要么自定义带 `throws` 的函数式接口。
- **Go**：函数选项模式用于有很多可选配置的构造函数；回调参数用最小的函数类型；超过两三个相关的函数就换成接口。注意闭包捕获的变量逃逸到堆上的开销（热路径上测一下）。
- **Rust**：函数参数默认用泛型 `F: Fn(...)`（零成本）；需要存放不同闭包（回调表、事件处理器）才用 `Box<dyn Fn>`；`impl Fn` 作返回类型要求所有分支是同一个闭包。选择最宽松的 trait：只调用一次用 `FnOnce`，要修改状态用 `FnMut`，只读用 `Fn`。
- **Python**：短小的键函数用 `lambda`，其他用 `def`（有名字，回溯可读）；能用推导式就不要 `map`/`filter` + `lambda`；`functools.partial` 可以代替只为固定参数写的 lambda。

何时打破：性能关键路径上，函数值的间接调用会阻碍内联，此时把「行为」改成泛型参数（Rust、有限地在 Java 里）或枚举分支。
