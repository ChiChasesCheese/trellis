# 题集规范（Java 21 版）

Headlands 是 Java 岗，Chi 要求题集用 **Java 21** 并且「顺便学新特性，越多越好」。所以本 kit 的题集不沿用
Python 版（`stripe/CONVENTIONS.md`）的 pytest 布局，改成下面这套；其余方法论（来源、置信度、(reconstructed) 标注、
REPORT 小节）不变。

## 目录

```
loop/rounds/<轮次>/<id>_<slug>/
  problem.md        题面：背景、输入输出、Part 1..N、样例、边界清单、野外变体、来源与置信度、考什么
  starter/          候选人起点：和 reference 同名同签名，方法体 `throw new UnsupportedOperationException("TODO")`
  reference/        参考实现（同名类，默认包）
  test/             JUnit 5 测试（默认包），只依赖 starter/reference 共有的公共 API
  work/             Chi 的工作副本（`jtest.py start` 从 starter 复制；提交与否随意）
  REPORT.md         见下
```

轮次目录：`00_oa`（HackerRank）· `01_video`（一小时技术视频面，当前重点）· `02_onsite` · `03_lld` · `04_sd`。

## 命令（在 kit 根目录跑）

```bash
python3 tools/jtest.py start  loop/rounds/01_video/hc01_xxx           # starter → work
python3 tools/jtest.py run    loop/rounds/01_video/hc01_xxx --tag part1 # 只跑 Part 1（默认 --impl work）
python3 tools/jtest.py run    loop/rounds/01_video/hc01_xxx --impl reference
python3 tools/jtest.py verify "loop/rounds/*/*"                         # 验收门：reference 绿 + starter 编译且红
python3 tools/jtest.py main   loop/rounds/00_oa/oa01_job_chain --impl reference < input.txt
```

JDK：`brew install openjdk@21`（脚本自动找 `/opt/homebrew/opt/openjdk@21`）。JUnit console jar 首次运行时用 Maven 下载到
`~/.cache/trellis-java/`。编译参数固定 `--release 21 --enable-preview`；运行用 Generational ZGC。

## 公共 API 约定

* 每个 Part 一个公共入口（方法或类），**签名写在 problem.md 里**，starter 与 reference 完全一致。
* 需要 stdin/stdout 的题（OA 类）有 `Main` 类：`public static void main(String[] args)` 读 `System.in` 写 `System.out`，
  另有纯函数 `static List<String> solve(List<String> lines)` 供测试直接调。
* 金额用 `long` 最小单位或 `BigDecimal` + 明确 `RoundingMode`；排序写全 tie-break；输出确定。
* 并发题：测试要能稳定复现（`CountDownLatch` 对齐起跑，重复 N 次），不得依赖 `Thread.sleep` 的时序。

## 测试（`test/<Name>Test.java`）

每个测试方法恰好一个 `@Tag("partN")`，再按需加 `@Tag("edge")` / `@Tag("fmt")` / `@Tag("perf")` / `@Tag("io")` / `@Tag("conc")`。必须覆盖：

1. problem.md 里每个样例（逐字）
2. 每个 Part 的边界：空输入、单条、重复、乱序、0 和负数、阈值 ==/差一、溢出（`Long.MAX_VALUE` 附近）、tie
3. `fmt`：逐字符比较输出
4. `perf`：`new Random(0)` 生成最大合理规模（10^5–10^6），`assertTimeoutPreemptively(Duration.ofSeconds(2), …)`
5. `conc`（并发题）：多线程压测下不变量成立（总数守恒、无丢失、无重复）

starter 必须能编译，并且至少一个测试红：验收门 `jtest.py verify` 检查这两点。

## Java 21 特性矩阵（每题 ≥ 3 个，REPORT 里逐条写「用在哪一行、为什么比旧写法好」）

| id | 特性 | 版本 | 典型用处 |
|---|---|---|---|
| J01 | `record`（含紧凑构造器校验） | 16 | 不可变值对象、map key、解析后的行 |
| J02 | `sealed` 接口 / 类 + `permits` | 17 | 事件/命令/结果的封闭代数类型 |
| J03 | `switch` 模式匹配（JEP 441），`when` 守卫，穷尽性检查 | 21 | 对 sealed 层级分派 |
| J04 | record 模式 / 嵌套解构（JEP 440） | 21 | `case Order(var id, Side.BUY, var px, var q)` |
| J05 | `switch` 表达式 + `yield` | 14 | 无 fallthrough 的映射 |
| J06 | `instanceof` 模式 | 16 | `if (o instanceof Foo f && f.x() > 0)` |
| J07 | 文本块 `"""` | 15 | 测试里的多行输入/期望输出 |
| J08 | `var` | 10 | 局部类型推断（只在类型显然时） |
| J09 | Sequenced Collections（JEP 431）：`getFirst/getLast/reversed`、`SequencedMap.firstEntry/pollFirstEntry` | 21 | 有序集合两端操作、order book 最优价 |
| J10 | 虚拟线程（JEP 444）：`Thread.ofVirtual()`、`Executors.newVirtualThreadPerTaskExecutor()` | 21 | 大量 I/O 型并发任务 |
| J11 | 结构化并发 `StructuredTaskScope`（预览 JEP 453） | 21 预览 | 一组子任务同生共死、失败即取消 |
| J12 | `ScopedValue`（预览 JEP 446） | 21 预览 | 代替 ThreadLocal 传上下文 |
| J13 | 未命名模式和变量 `_`（预览 JEP 443） | 21 预览 | 不用的绑定、`catch (Exception _)` |
| J14 | 新 Stream/Collector API：`Stream.toList()`、`mapMulti`、`Collectors.teeing`、`Stream.iterate(seed, hasNext, next)` | 9–16 | 管道式聚合 |
| J15 | 数学与字符串小工具：`Math.addExact/multiplyExact`、`Math.clamp`（21）、`StringBuilder.repeat`（21）、`String.formatted`、`HexFormat`、`Integer.compress/expand`（19） | 8–21 | 溢出检测、格式化、位操作 |
| J16 | 并发原语：`VarHandle`、`LongAdder`、`ConcurrentSkipListMap`、`ReentrantLock`（虚拟线程下不 pin，`synchronized` 在 21 会 pin） | 9–21 | 无锁/低锁结构 |
| J17 | Foreign Function & Memory API：`Arena`、`MemorySegment`（21 预览，22 正式） | 21 预览 | 堆外内存池、定长记录 |
| J18 | `Comparator` 组合子、接口 `default`/`private` 方法、`Objects.requireNonNull*` | 8–9 | 排序 tie-break、API 卫语句 |
| J19 | 运行时：Generational ZGC（JEP 439）、JFR、`-XX:+PrintCompilation`/JIT 基础 | 21 | 口头题：低延迟 Java 怎么调 |

不要用：String Templates（21 预览，JDK 23 已撤回）。

## REPORT.md

小节：概要（Headlands 为什么问这个）· 来源与置信度 · 逐 Part 思路 · 隐藏测试会打的坑 · 复杂度 + 实测时间 ·
测试清单（按 tag 计数，脚本数） · **Java 21 特性**（id + 用在哪 + 旧写法对比） · 面试官可能的追问（≥ 3 条，含答案要点）。
