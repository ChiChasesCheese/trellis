---
id: pl-functional-closures-best-practice
node: functional.closures
type: qa
step: 9
---
## Q
资深工程师在各语言里使用闭包时遵循哪些规则？

## A
通用原则：**闭包应当小、短命，并且尽量不依赖会变化的外部状态**。闭包捕获得越多，越难推理（谁改了它？什么时候？）。

- **Java**：把 lambda 当纯函数写，不依赖外部可变状态；需要累计结果用 `reduce`/`collect`，不用外部变量累加。要在 lambda 里共享可变状态时，用 `AtomicInteger` 或并发集合，而不是数组小技巧。
- **Go**：启动 goroutine 时，把要用的值作为**参数**传入，而不是依赖捕获：`go func(id int) { ... }(i)`；这样不依赖循环变量语义，也不依赖变量被谁修改。需要共享状态就加锁或用通道。热点路径上避免让闭包逃逸（测 `-gcflags=-m`）。
- **Rust**：让编译器推导捕获方式；跨线程、跨 `'static` 边界用 `move`；传回调时选最宽松的 trait 约束（`FnOnce` > `FnMut` > `Fn`），以便调用方传入更多种闭包。
- **Python**：在循环里创建闭包时，用默认参数固定当时的值（`lambda i=i: i`）或用 `functools.partial`；需要有状态的回调，优先用小类（带 `__call__`）而不是 `nonlocal` 的层层嵌套。

何时打破：事件处理、中间件、装饰器这类闭包天然需要持有配置状态的场合，闭包是最简洁的表示，只需确保被持有的状态在闭包创建后不再被外界修改。
