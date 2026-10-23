---
id: hl-j14-boxing-parallel
node: java21.j14-stream-api
type: qa
step: 18
---
## Q
基本类型流（`LongStream`/`IntStream`）与 `Stream<Long>` 有什么区别？并行流（parallel stream）什么时候适合、什么时候是错的？

## A
- `Stream<Long>` 每个元素是 `Long` 对象（装箱）；热路径用 `LongStream`/`IntStream`（`mapToLong`、`summaryStatistics`）。`Arrays.stream(out).boxed().toList()` 的 `boxed()` 就是装箱。
- `.parallel()` 用公共 `ForkJoinPool`，适合 **CPU 密集、数据量大、操作无状态、来源易分割**（数组、`ArrayList`）。
- **阻塞 I/O 用它是错的**：占住公共池线程，该用虚拟线程。
- `teeing`、`groupingBy` 并行下需要 `combiner`，自定义收集器要实现正确。
