---
id: hl-javaq-e-q20-failures
node: java-questions.e-jit-gc
type: qa
step: 11
---
## Q
逃逸分析在哪些场景会失败？怎么验证对象真的没被分配？怎么写代码帮助它？
Does that mean allocation is free in Java? How would you write code to help escape analysis?

## A
- **依赖内联**：被调方法没内联，`new Point` 就"逃逸给了被调用者"（参数逃逸），所以方法大小限制直接影响 EA。
- **失败场景**：对象放进 `ArrayList` / `Map`、赋给字段、经 `Object` 参数传进不能内联的方法、数组太大（`EliminateAllocationArraySizeLimit` 默认 64 个元素）、控制流汇合处对象逃逸（C2 不做部分逃逸分析，Graal 做）。
- **验证**：`getThreadAllocatedBytes` 差值、JFR 分配事件，或调试选项 `-XX:+PrintEliminateAllocations`。
- **分配是不是免费**：只在被消除时；否则仍是 TLAB 分配加之后的 GC 压力。
- **帮助 EA 的写法**：小方法、短生命周期的不可变值对象、不存进容器或字段；热点处别用捕获大量变量的 lambda。
