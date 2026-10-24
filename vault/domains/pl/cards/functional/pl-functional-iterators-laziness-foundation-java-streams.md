---
id: pl-functional-iterators-laziness-foundation-java-streams
node: functional.iterators-laziness
type: qa
step: 3
---
## Q
Java 的 Stream 是什么？中间操作、终端操作是什么意思，为什么 Stream 只能用一次？

## A
`Stream<T>` 是对一个数据源的**声明式流水线**。三部分：

- **源**：集合、数组、`Stream.of`、文件行等；
- **中间操作**（intermediate）：`filter`、`map`、`sorted`……**只登记步骤，不执行**，返回新的 Stream；
- **终端操作**（terminal）：`collect`、`findFirst`、`count`、`forEach`……触发整条流水线真正执行并产生结果。

执行时是**逐个元素穿过整条流水线**，不是一步处理完所有元素再下一步：

```java
var s = Stream.of(1, 2, 3, 4, 5)
    .filter(x -> { System.out.println("filter " + x); return x % 2 == 1; })
    .map(x -> { System.out.println("map " + x); return x * 10; });
System.out.println("built");     // 此时什么都没执行
System.out.println(s.findFirst().get());
// 输出：built / filter 1 / map 1 / 10
```

`findFirst` 是短路操作，拿到第一个结果后就停止，元素 2 到 5 根本没被检查。

Stream **只能消费一次**：终端操作之后流就关闭，再用抛 `IllegalStateException: stream has already been operated upon or closed`。这是因为 Stream 对象代表的是「一次正在进行的遍历」，不是「可重复遍历的集合」。要重复用，每次从源重新创建一个 Stream，或把结果收集成集合。

注意区分：`Stream<Integer>` 会装箱，数值场景有 `IntStream`、`LongStream`，避免装箱开销。
