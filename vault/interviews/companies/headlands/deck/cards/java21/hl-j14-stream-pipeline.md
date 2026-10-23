---
id: hl-j14-stream-pipeline
node: java21.j14-stream-api
type: qa
step: 1
---
## Q
Java 的流（Stream）和集合有什么区别？一条流水线由哪三个阶段组成？

## A
集合（`List`、`Map`）**存**数据；流是**对数据做的一条流水线**。

| 阶段 | 做什么 | 例子 |
|---|---|---|
| 来源（source） | 产生流 | `list.stream()` |
| 中间操作（intermediate） | 一步步加工，可接很多个 | `filter` → `map` → `sorted` |
| 终止操作（terminal） | 拉动整条流水线，产出结果 | `collect` / `count` / `findFirst` / `toList` |

相关新方法（全部是正式特性，不是预览）：`Collectors.teeing` 12；`takeWhile/dropWhile`、三参数 `iterate`、`Stream.ofNullable`、`Collectors.filtering/flatMapping` 9；`Stream.toList()`、`Stream.mapMulti` 16。
