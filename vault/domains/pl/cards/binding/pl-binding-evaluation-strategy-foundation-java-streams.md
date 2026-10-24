---
id: pl-binding-evaluation-strategy-foundation-java-streams
node: binding.evaluation-strategy
type: qa
step: 4
---
## Q
Java 的 `Stream` 和 `Supplier` 怎样在严格求值的语言里表达惰性？流水线里每个元素按什么顺序经过各个阶段？

## A
**`Supplier<T>`**（供应者）是只有一个方法 `get()` 的函数接口。传 `Supplier` 而不是传值，就是把「现在算」换成「需要时再算」：调用方写 `() -> expensive()`，被调用方决定调不调用 `get()`。

**`Stream`** 把一串操作描述成流水线：`filter`、`map` 这类**中间操作**只是登记，什么都不执行；`findFirst`、`toList`、`forEach` 这类**终结操作**才驱动整条流水线。而且元素是**一个一个**穿过所有阶段，不是先把全部元素过滤完再映射：

```java
Stream.of(1, 2, 3, 4)
  .filter(x -> { System.out.println("filter " + x); return x % 2 == 0; })
  .map(x -> { System.out.println("map " + x); return x * 10; })
  .findFirst();
// filter 1
// filter 2
// map 2
```

实际输出只有这三行：元素 `1` 没通过过滤；元素 `2` 通过并被映射；`findFirst` 拿到结果后立刻停止，元素 `3`、`4` 从未被看到（这叫**短路终结操作**）。

没有终结操作的流水线什么也不做：

```java
Stream<Integer> s = Stream.of(1, 2).peek(x -> System.out.println("never"));
System.out.println("built");   // prints only "built"
```

这种「逐元素穿过」的执行方式有两个好处：不需要为中间结果分配整个集合；`limit`、`findFirst` 可以让无限流（`Stream.iterate`、`Stream.generate`）变得可用。

约束：`Stream` 只能消费一次，再用会抛 `IllegalStateException`；lambda 里应该没有副作用，否则执行次数与顺序取决于流水线的优化，行为难以预料。
