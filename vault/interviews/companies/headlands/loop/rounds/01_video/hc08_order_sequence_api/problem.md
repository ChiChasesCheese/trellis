# hc08 · Order Sequence API（订单序列的前缀 count / quantity 查询）

## 读题前你需要知道

* **前缀和（prefix sum）**是什么，为什么「每次查询都从头加一遍」在数据量大时不行；
* **树状数组（Fenwick tree / BIT）**——一个用 `i & -i` 就能在 O(log n) 里做「改一个数、求前缀和」的数组；
* 为什么「删除只留洞、下标只增不减」会让内存无限涨，以及怎么**压缩（compaction）**。


## 背景

交易系统里有一串**活跃订单**，按**到达（插入）顺序**排好。你要实现几个 API：往末尾放订单、删订单，
以及问「从序列头数到订单 X，一共有几张订单 / 总共多少数量」。订单数很大、查询很多，所以查询不能是 O(n)。

## 语义

* 订单由 `unique_id`（任意 `long`，同时只能有一张同 id 的活跃订单）和 `quantity`（正整数）组成。
* `put(id, qty)`：放到序列**末尾**。`qty ≤ 0` → `IllegalArgumentException("invalid quantity")`；id 已活跃 → `IAE("duplicate id")`；
  全体活跃订单数量之和会超过 `Long.MAX_VALUE` → `ArithmeticException("overflow")`，**状态不变**。
* `delete(id, qty)`：从订单里删掉 `qty` 个单位，返回**剩余数量**；剩余为 0 时订单从序列里移除。订单**位置不变**。
  `qty ≤ 0` → `IAE("invalid quantity")`；未知 id → `NoSuchElementException("unknown id")`；`qty >` 剩余 → `IAE("quantity exceeds remaining")`，状态不变。
  **Part 1–2 只考整单删除（`qty` = 剩余量）；`qty` < 剩余量的部分删除在 Part 3 才被测试。**
* `countUpTo(id)`：从序列头到该订单（含）的活跃订单数。`qtyUpTo(id)`：同范围内剩余数量之和。未知 id → `NoSuchElementException`。
* `idAt(k)`：第 `k` 张（1 起）活跃订单的 id（我们补的第 4 个 API，对应「亚线性」的另一半）。越界 → `IndexOutOfBoundsException("index out of range")`。
* `size()` · `totalQty()` · `entries()`（全部活跃订单 `List<Entry(id, qty)>`，插入顺序）。
* 同一个 id 删光后可以再 `put`，它排到**最后**。

## Part 一览

| Part | 内容 |
|---|---|
| 1 | 语义做对。允许朴素实现（`ArrayList` 线性扫描）。另有文本接口 `parse / apply / render / replay`（sealed `Op` / `Result`） |
| 2 | **亚线性查询**：`countUpTo` / `qtyUpTo` / `idAt` 都是 O(log n)；50 万张订单 + 50 万次操作 < 2 s |
| 3 | **部分删除** + **压缩**：`OrderSequence(initialCapacity)`，下标空间写满时把活跃订单重新编号；`capacity()` / `compactions()` 可观察；200 万次 put/delete 循环，活跃订单 ≤ 1000，容量必须 ≤ 4096 |

### 文本接口

```
PUT id qty     DELETE id qty     COUNT id     QTY id     AT k
```

大小写不敏感、空白任意；`replay` 跳过空行和 `#` 行；格式错抛 `IAE`，信息以 `line N` 开头。输出：`PUT` → `OK`；`DELETE` → 剩余数量；`COUNT` / `QTY` / `AT` → 数字；
业务错误 → `ERR <message>`（message 就是上面的字符串）。

### 样例 1（Part 1–2）

```
# 样例
PUT 10 5
PUT 20 3
PUT 30 7
COUNT 30
QTY 20
DELETE 20 3
QTY 30
AT 2

DELETE 10 5
put 20 4
QTY 20
DELETE 99 1
DELETE 30 9
PUT 30 1
AT 3
AT 2
```

输出：

```
OK
OK
OK
3
8
0
12
30
0
OK
11
ERR unknown id
ERR quantity exceeds remaining
ERR duplicate id
ERR index out of range
20
```

手算：序列 `[10:5, 20:3, 30:7]`。`COUNT 30` = 3；`QTY 20` = 5+3 = 8；删掉 20 之后 `QTY 30` = 5+7 = 12，`AT 2` = 30；
再删光 10 → 序列 `[30:7]`，`put 20 4` 排到最后 → `[30:7, 20:4]`，`QTY 20` = 11；最后 `AT 2` = 20。

### 样例 2（Part 3，部分删除）

```
PUT 1 10
PUT 2 10
PUT 3 10
DELETE 2 4
QTY 3
COUNT 3
DELETE 2 6
COUNT 3
AT 2
```

输出：`OK OK OK 6 26 3 0 2 3`（每个一行）。`DELETE 2 4` 只是减量（10 → 6），订单还在序列里，所以 `COUNT 3` 还是 3；
再删 6 才真正移除，`COUNT 3` 变 2，第 2 张变成 3 号。

## Part 3 的接口

* `new OrderSequence()` = 初始容量 16；`new OrderSequence(n)`：下标空间向上取整到 2 的幂（`n ≤ 0` → `IAE`）。`capacity()` 返回当前大小。
* 下标写满（再 `put` 就没位置）时必须压缩：按原顺序给活跃订单重新编号。压缩后的新容量 = 2 的幂 ≥ `max(初始容量, 1.5m + 1)`（m 是活跃订单数）——
  这个公式是我们的约定，目的是「压缩后至少腾出约 m/2 个空位」，保证摊还 O(1)。`compactions()` 返回压缩次数。
* 压缩不能改变任何可观察的行为：顺序、`countUpTo`、`qtyUpTo`、`idAt`、`entries` 都和压缩前一致。

## 边界清单

空序列上的所有查询；重复 id；`qty ≤ 0`；删除超过剩余；已删除的 id 再查询；id 为 0 / 负数 / `Long.MIN_VALUE`；总量到 `Long.MAX_VALUE` 的边界；
Fenwick 的边界（大小不是 2 的幂、只剩头 / 只剩尾）；洞全堆在序列前面（永远删最老的）；容量 1 / 4 这种极小空间下的压缩。

## 相关变体

* 真题可能要求 4 个 API 是 `put / delete / count(id) / quantity(id)`，没有 `idAt`；或把前缀改成「后缀」/「某个价格区间」。
* "memory management" 可能指：删除后内存要能回收（本题 Part 3），也可能指订单对象池（见 hc05 Part 4 的思路）。
* 并发追问：多个线程同时 put / query 怎么办？（读写锁、分片、或单线程 + 队列。）

## 考什么

「看到前缀和 + 在线修改，想到树状数组」；再往下问：删除怎么办（留洞）、下标写满怎么办（压缩 + 摊还分析）、边界和溢出怎么守。
前面的数据结构选对了，Part 3 的问题其实是工程问题：**内存应该跟活跃量走，而不是跟历史总量走**。
