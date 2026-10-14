# oa01 · REPORT

## 概要

Headlands 的 HackerRank 六年没换题。Chi 已经用 Java 过了这一关，这里重做一遍是为了：(1) 把 Java 21 的数据建模特性练熟；
(2) 电面可能从 OA 延伸追问（「你的解法怎么处理环？百万行多快？」）。

## 来源与置信度

见 `problem.md` §来源。题面主体高；排序与取整 (reconstructed)。

## 逐 Part 思路

1. **parse**：正则 `\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*` 整行匹配，故意接受负号，交给 `Job` 的紧凑构造器报「负数」而不是「格式错」——错误信息更准。`Integer.parseInt` 溢出的 `NumberFormatException` 转成 `MalformedInputException`。
2. **chains**：`LinkedHashMap<id, Job>` 查重；第二遍建「谁有前驱」集合，同时查悬空与多前驱（入度 ≤ 1）。从所有无前驱节点往下走就是全部链；走完后**没被访问到的节点只可能在环上**（入度 ≤ 1 的图里，不在任何头的路径上 ⇒ 在环上），一次 `size` 比较即可查环，不用 DFS 染色。
3. **analyze / render**：异常在边界处转成 `Malformed`，内部一律抛异常，外部一律返回值。

## 隐藏测试会打的坑

* 分钟忘记 `% 60`（公开 C++ 题解就有这个 bug）。
* `int` 累加时长溢出：两个 2e9 秒的 job。
* 「好链 + 独立环」：只从链尾往回走的解法查不出这个环。
* 输入乱序：链头可能在最后一行。
* 表头缺失或多余空行。

## 复杂度 + 实测

O(n) 时间、O(n) 空间。100 万行（平均链长 100、行序打乱）在 M 系列 Mac 上整题 < 1 s（`perf` 测试，预算 2 s）。

## 测试清单

运行 `python3 tools/jtest.py run loop/rounds/00_oa/oa01_job_chain --impl reference`：25 个测试（含参数化展开）。

## Java 21 特性

| id | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| J01 record + 紧凑构造器 | `Job`、`Chain` | 不变量写在类型里，非法对象构造不出来；`equals/hashCode` 白送，测试直接比 `List<Chain>` |
| J02 sealed | `Outcome permits Ok, Malformed` | 结果类型封闭，新增一种结果时所有 switch 编译报错 |
| J03 + J04 模式匹配 switch + record 解构 | `render`：`case Ok(var chains) -> …` | 代替 `instanceof` + 强转；穷尽性由编译器检查，不需要 `default` |
| J13 未命名模式 `_`（预览） | `case Malformed _ ->` | 明说「不需要这个绑定」 |
| J05 switch 表达式 + `yield` | `render` 的块分支 | 表达式化，没有 fallthrough |
| J07 文本块 | 测试的输入与期望输出 | 多行字符串原样可读 |
| J09 Sequenced Collections | 测试里 `getFirst()` | 代替 `get(0)`，`List`/`Deque`/`LinkedHashSet` 统一 |
| J15 `Math.addExact` · `String.formatted` | 累加时长、`hhmmss` | 溢出直接抛而不是静默变负 |
| J18 `Comparator` 组合子 | `comparingLong(...).reversed().thenComparingInt(...)` | tie-break 一眼可读 |

## 面试官可能的追问

1. **输入是 10 GB 的流，内存放不下？** 外部排序按 `job_id` 分片；或者两遍扫描：第一遍只存 `(id, next)` 的 int 数组（每条 8 字节），第二遍再累加时长。
2. **改成允许多前驱（DAG）怎么办？** 链就变成路径，问题变成「每个源点到汇点」或拓扑序上的最长路径（关键路径），Kahn + DP。
3. **为什么用异常而不是返回 `Optional`？** 校验分布在多层，异常让中间层不必层层透传；在 `analyze` 这一个边界上统一转成值（`Outcome`）。热路径上异常很贵——这里只在出错时抛一次。
4. **为什么 record 的 id 用 `int`、时长用 `long`？** id 题面是正整数且要做 map key（装箱成本另说）；时长要累加，必须 `long` + `addExact`。
