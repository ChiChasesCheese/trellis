# hc08 · REPORT

## 概要

「前缀 count / quantity + 亚线性」是在考：看到「前缀和 + 在线修改」能不能想到树状数组（Fenwick）；再往下是删除留洞、下标写满怎么办（内存管理）。
Headlands 的电面是一小时一位工程师，题目会一路加要求，所以先写对朴素版、再优化、再谈内存，比一上来背 Fenwick 更稳。
讲义（含 lowbit 的逐步图解）：`study/30-articles/hc08_order_sequence_api.md`。

## 来源与置信度

置信度 **高**（2 个独立来源：FastPrep lastSeen 2024-05-10 + 1p3a 帖 1066045 同日；QuantVault 的标题不计）。
有证据的只有：Put / Delete(unique_id, quantity) 的名字、「4 个 API」、「前缀 count / quantity」、「sublinear」、「API design and memory management」。
**(reconstructed)**：Delete 的 quantity 含义（我们定为「减去这么多单位」）；第 4 个 API（我们补 `idAt(k)`）；错误类型与字符串；文本命令；Part 3 的 `capacity()` / `compactions()` 与容量公式 `max(初始, 1.5m+1)`；"memory management" 解读为「下标空间压缩」。

## 逐 Part 思路

1. **语义**：先用 `ArrayList` + 线性扫描写出来（测试里的 `Model` 就是这个）。同时定下全部边界：重复 id、`qty ≤ 0`、删除超量、未知 id、总量溢出，以及「失败时状态不变」。
2. **Fenwick**：每张订单 put 时领一个递增的「插入下标」，删除只留洞（不挪）。两棵树 `cnt`（活跃数）、`sum`（数量）按下标累加；`countUpTo` / `qtyUpTo` = 前缀和，`idAt(k)` = `cnt` 树上的二分下降。`HashMap<id, 下标>` 做换算。全部 O(log n)。
3. **部分删除 + 压缩**：部分删除只动 `sum`（订单还活着，`cnt` 不动）；剩余为 0 才 `cnt −1`。下标写满时压缩：按原顺序给活跃订单重编号，线性建树，容量 = 2 的幂 ≥ `max(初始, 1.5m+1)`，摊还 O(1)，活跃订单少时容量缩回去。

## 隐藏测试会打的坑

* Fenwick 下标从 0 开始（`i & -i` 在 0 上死循环）。
* 删除后把后面的订单往前挪，下标全乱。
* 部分删除时也把 `cnt` 减 1；或者 `cnt` / `sum` 共用一棵树。
* 压缩后忘了更新 `indexOf`；压缩容量取 `m+1`，导致每次 put 都压缩。
* 总量溢出：先改树后检查，抛异常时状态已被改。
* 查询已删除的 id 返回 0 而不是抛 `NoSuchElementException`。
* 容量不是 2 的幂时直接套二分下降。
* id 取 0 / 负数 / `Long.MIN_VALUE`（不能用 0 当「空」标记）。

## 复杂度 + 实测时间

n = 活跃订单数，C = 容量。本机（M 系列 Mac，JDK 21.0.12）：

| 操作 | 复杂度 | 实测 |
|---|---|---|
| `put` | O(log C)，压缩摊还 O(1) | 50 万 put + 约 50 万次查询 / 删除：约 130 ms（Fenwick）；朴素扫描 5 万 / 5 万就要约 1.9 s，外推 50 万 / 50 万约 190 s |
| `delete` · `countUpTo` · `qtyUpTo` · `idAt` | O(log C) | 同上 |
| 压缩 | O(C)，摊还每次 put O(1) | 活跃 ≤ 1000、200 万次 put + 删最老：约 115 ms，容量稳定 **2048**，压缩 **1914** 次 |
| `entries()` | O(C) | 仅测试 / 调试用 |

内存：O(C)，C 跟活跃量走（不压缩则要 200 万以上）。

## 测试清单

`python3 tools/jtest.py run loop/rounds/01_video/hc08_order_sequence_api --impl reference`：**36 个测试**（含参数化展开），全绿。按 tag（可重叠）：

| tag | 个数 | tag | 个数 |
|---|---|---|---|
| part1 | 24 | edge | 9 |
| part2 | 4 | fmt | 18 |
| part3 | 8 | perf | 2 |

对拍：`differentialAgainstNaiveModel`（Part 2，4 万步）、`differentialWithTinyCapacityAndPartialDeletes`（Part 3，容量 4 起步、6 万步、含部分删除）；`everySmallSizeEveryPrefix` 对 1..70 张订单逐个全查。

## Java 21 特性

| id | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| J01 record | `Entry`、全部 `Op` 与 `Result` | 值对象一行定义，`equals` 按字段，测试直接比较 `entries()` |
| J02 sealed | `Op permits Put, Delete, CountUpTo, QtyUpTo, IdAt`；`Result permits Ok, Num, Err` | 新增命令时所有 switch 编译报错 |
| J03 + J04 模式匹配 switch + record 解构 | `apply`：`case Put(var id, var q) -> …`；`render`：`case Num(var v) -> …` | 判型 + 拆字段一步完成，穷尽无 `default` |
| J05 switch 表达式 + `yield` | `parse` 每个 case 先校验参数个数再 `yield` | 无 fallthrough，不需要临时变量 |
| J09 Sequenced Collections | 测试里 `entries().getFirst()` / `getLast()` / `reversed()` | 代替 `get(size() - 1)` 与手写倒序 |
| J13 未命名模式 `_`（预览） | `render`：`case Ok _ -> "OK"` | `Ok` 没有字段，明说不绑定 |
| J14 `IntStream` + `toList()` | `entries()` | 一条管道，返回不可变快照 |
| J15 `Math.addExact` | `put` 里守住 `totalQty` 不溢出 | 溢出抛异常而不是回绕；只检查全局总量即可保证所有前缀和不溢出 |
| J07 文本块 | 测试里的脚本样例与期望输出 | 多行原样可读 |

## 面试官可能的追问

1. **为什么选 Fenwick 不选线段树？** 只有单点修改 + 前缀求和（可逆运算）；Fenwick 一个数组、常数小、十几行。需要区间最值 / 区间修改才用线段树。Fenwick 的限制：运算要有逆元。
2. **删除后内存怎么办？/ 下标写满了？** 压缩：按原顺序重编号，线性建树；新容量 ≥ 1.5m+1 的 2 的幂，压缩后至少腾出约 1/3 的空位 → 摊还 O(1)；容量跟活跃量走。偶发的 O(C) 停顿要避免可以做增量压缩或双缓冲。
3. **多线程？** 读写锁（读多写少）或单线程所有者 + 命令队列；不能只靠 `ConcurrentHashMap`（两棵树 + 一张表的更新不是一个原子操作，查询会读到改了一半的状态）。前缀查询跨分片，按 id 简单分片行不通。
4. **`idAt(k)` 是怎么 O(log n) 的？** `cnt` 树上二分下降：从大步长到小步长，若整块的活跃数 < k 就整块跳过。要求容量是 2 的幂。
5. **id 很大很稀疏？/ 在中间插入？** `HashMap` 不依赖 id 范围，Fenwick 按插入下标而非 id 建，不需要离散化。中间插入做不到——要平衡树（order-statistic tree）或离线预分配下标。
6. **如果要的是「后缀」或「某价格区间」的数量？** 后缀 = 总量 − 前缀；区间 = 两个前缀相减；价格区间要按价格建树（离散化价格）。
