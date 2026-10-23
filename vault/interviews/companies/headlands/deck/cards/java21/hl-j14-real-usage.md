---
id: hl-j14-real-usage
node: java21.j14-stream-api
type: qa
step: 21
---
## Q
订单簿、撮合、寄存器模拟这类代码里，Stream 的常见用法有哪些？被问「一次遍历怎么同时算 VWAP 分子分母」怎么答？

## A
- `events.stream().<Trade>mapMulti((e, sink) -> { if (e instanceof Trade t) sink.accept(t); }).toList()`：从混合事件里挑 `Trade`。
- `book(side).entrySet().stream().limit(n).map(...).toList()`：取最优 n 档，靠短路 `limit(n)` 只遍历前 n 个。
- `lines.stream().filter(l -> !l.isBlank() && !l.strip().startsWith("#")).toList()`；`Arrays.stream(out).boxed().toList()`。
- `IntStream.range(1, n).filter(...).mapToObj(...).toList()`：基本类型流 + `toList()`。
- `IntStream.range(0, chunks).parallel().mapToObj(...).reduce(...)`：对 CPU 密集求和合理。
- `in.lines().toList()`：`BufferedReader.lines()` 返回 `Stream<String>`。

问 VWAP：答 `teeing`，并说明增量/流式场景用累加器字段更合适。
