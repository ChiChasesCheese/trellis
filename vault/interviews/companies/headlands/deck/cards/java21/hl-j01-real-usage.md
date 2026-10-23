---
id: hl-j01-real-usage
node: java21.j01-record
type: qa
step: 29
---
## Q
在真实代码里 `record` 常见的五种用法是什么？各举一个例子。

## A
1. **紧凑构造器校验单行输入**：`Job(int id, long runtimeSeconds, int nextId)` 在构造时拒绝非法 id 或负运行时间。
2. **防御性拷贝**：`Correct(List<Long> contents)` 的紧凑构造器里 `contents = List.copyOf(contents)`。
3. **空值检查**：`Limit(long id, Side side, long price, long qty)` 里 `Objects.requireNonNull(side, "side")`。
4. **不可变数值类型**：`Wide(long hi, long lo)` 带静态常量 `ZERO` 和 `plus` / `merge` 方法。
5. **零组件 record 当事件标签**：`Push(long value)`、`Pop()`、`Query()`；以及作为 `sealed interface` 的各个变体、发布给其他线程的不可变快照。
