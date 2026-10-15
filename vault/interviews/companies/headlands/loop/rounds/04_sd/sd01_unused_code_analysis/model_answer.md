# sd01 · 参考答案：无用代码分析（senior 深度）

> 读者设定：会写 Java，但编译器 / 静态分析 / 图算法需要从头讲。术语第一次出现写「中文（English）」。
> 所有数字都带推导；**假设**一律标明。题面是 (reconstructed)，见 [prompt.md](prompt.md)。
> 方法论总纲：[../00_how_to_run.md](../00_how_to_run.md)。

---

## 0. 三个层次的回答（面试时按时间长度选）

**30 秒版**：把代码库看成一张图——节点是符号（类 / 方法 / 字段 / 配置），边是引用。从一组**根（roots）**出发做可达性标记（mark），没被标到的就是候选，和垃圾回收一模一样。难点全在**根的定义**（反射、依赖注入、序列化、公共 API、脚本和配置里的类名）和**证据**（静态不可达 + 生产里从没加载过 = 高置信度）。输出是带证据和置信度的候选，经 owner 审核、软删除、再真删。

**5 分钟版**：上面 + 流水线（索引 → 汇总成图 → 标记 → 分级 → 附证据 → 按 owner 出 PR）+ 规模估算（索引是并行的重活，图本身一台机器放得下）+ 为什么在字节码上分析。

**完整版**：下面所有章节。

---

## 1. 澄清与定义：什么叫「没用」

先把「没用」拆成四种，因为它们的证据、风险、成本完全不同：

| 级别 | 名称 | 定义 | 证据来源 | 删除风险 |
|---|---|---|---|---|
| **L0** | 编译器可证明 | `private` / 包内私有的成员，在其所在编译单元（或模块）内零引用 | 编译器 / 索引 | 近 0 |
| **L1** | 封闭世界不可达 | 从所有已知根出发在整个快照里都到不了；非导出；没有字符串 / 反射命中 | 全程序可达性 | 低 |
| **L2** | 开放世界未知 | `public` / `protected` 符号，快照里零引用，但可能被**快照之外**的消费者（外部二进制、另一个仓库、插件）使用 | 可达性 + 制品下载日志 / 依赖扫描 | 中 |
| **L3** | 静态可达但动态冷 | 静态上有路径可达，但生产里长期（N 个月）从未执行 | 运行时数据（类加载日志、JFR、方法级覆盖率） | 高（可能是灾备、熔断、年度流程） |

> 交易公司的特殊性（口述题评论：「HFT 公司很少删代码」[F-G3]）：**熔断、灾备切换、日终对账、监管报表**这类路径设计上就长期不执行，却必须在需要的那一天可用。L3 永远不应自动处理——这是 Chesterton's fence（不明白这道围栏为什么在这儿，就别拆它）。主动把这点说出来是 senior 信号。

**为什么要做**（回答「值不值得」）：减少构建 / 测试时间和依赖面；减少搜索结果和阅读噪声（事故时误导排查）；降低安全暴露面（无用依赖里的漏洞）；让重构更便宜。**成本**：删错的代价（线上事故）远高于留着的代价——所以系统的设计目标是**高精度（precision）优先，召回（recall）其次**。

---

## 2. 把问题变成图问题：垃圾回收的类比

```text
        根 (roots)                       符号图 (symbol graph)
   ┌──────────────────┐
   │ main()           │───────▶ Order ──▶ RiskCheck ──▶ PositionBook
   │ @Scheduled       │            │
   │ ServiceLoader    │            └──▶ LegacyPricer ──▶ OldCurve      ← 没有任何根能到达这一簇
   │ 导出的公共 API   │
   │ 配置里的类名     │            OldCurve ◀──▶ OldCurveHelper      ← 互相引用的"死环"（grep 找不到，标记法找得到）
   └──────────────────┘

   mark：从根出发沿边标记所有可达符号 ────▶ 未被标记的 = 候选（sweep 的"候选"，不是直接删）
```

* **节点**：类、方法（含签名）、字段、枚举常量、资源文件、配置项、构建目标（target）。
* **边**：调用、继承 / 实现、`new`、字段读 / 写、方法引用 / lambda、注解、`String` 常量命中类名（弱边）。
* **根**：见 §4。
* **为什么不是 `grep`**：`grep` 只找「有没有人提到这个名字」，找不到 **死环**（两个都没用的类互相引用，`grep` 看到的都是「有引用」），也分不清「被死代码引用」和「被活代码引用」。可达性标记自然处理这两点。

**复杂度**：标记是图遍历，O(V + E)，V = 符号数，E = 引用数。

---

## 3. 规模估算（从零推）

假设（**假设值**，面试时说「我先按这个数量级算，您有真实数字我再改」）：

```text
代码量               2×10^7 行（20M LOC）；方案对 10^8 行同样成立（下面给出）
方法 ≈ LOC/10        2×10^6
类   ≈ LOC/100       2×10^5
字段 ≈ LOC/20        10^6
符号总数 V           ≈ 3.2×10^6
每个方法平均 8 条引用，每个类 2 条继承/实现边 → 边数 E ≈ 2×10^6×8 + 2×10^5×2 ≈ 1.6×10^7
```

| 阶段 | 计算 | 结果 | 结论 |
|---|---|---|---|
| **索引（解析 + 抽取符号与引用）** | 源码路线：带完整类型归属（attribution）的 javac，假设每核 5,000 LOC/s → 2×10⁷ / 5×10³ = 4,000 核·秒 ≈ 67 核·分钟 | 100 核约 40 秒；若是更慢的 1,000 LOC/s，则 2×10⁴ 核·秒，100 核约 3.3 分钟 | **并行的重活**，按构建目标 / 文件分片，embarrassingly parallel |
| **中间数据** | 每条边 (src int64, dst int64, kind 1 B) ≈ 17 B → 1.6×10⁷ × 17 B ≈ 280 MB | 280 MB | 一次 shuffle，不是问题 |
| **图（CSR）** | 边目标 int32 × E + 偏移 int32 × V = 4×1.6×10⁷ + 4×3.2×10⁶ ≈ 78 MB；访问位图 V/8 ≈ 0.4 MB | **约 80 MB** | **图本身一台笔记本就放得下**；10⁸ 行 ≈ 400 MB，仍是一台机器 |
| **标记** | 1.6×10⁷ 条边 × ~10 ns（随机访存的缓存未命中量级）≈ 0.16 s | **亚秒到数秒** | 单线程就够；**不需要 Pregel / Spark GraphX** |
| **候选规模** | 假设死代码占 10% → 2×10⁶ LOC；每个 PR 500 LOC → 4,000 个 PR | 4,000 PR | **瓶颈是人审，不是算力** |

**核心洞察（先讲给面试官）**：题目标题里的「distributed」被很多人当成「图算法要分布式」。算一下就知道：分布式只在**索引阶段**有价值（CPU 密集、可并行）；**图和可达性是单机问题**。真正的瓶颈是**精度**和**人审吞吐**。这也符合交易公司的偏好：先算一台机器够不够。

---

## 4. 根（roots）的定义——决定成败的地方

根集合错一个，要么大量误报（把活代码判死，危险），要么大量漏报（死代码因为被假根保护而躲过）。

```text
┌────────────────────────── 根的来源 ───────────────────────────────┐
│ A. 已部署二进制的入口  main()                                       │
│    └ 权威来源：部署清单 / 启动脚本 / systemd unit / crontab，而不是 "所有含 main 的类"│
│ B. 框架入口：@Scheduled、@Subscribe、Servlet、@Bean/@Component（Spring）、 │
│    JAX-RS 资源、Kafka 监听器 —— 用"框架模型"规则把注解映射为根            │
│ C. 反射 / SPI / 序列化：                                             │
│    ServiceLoader 的 META-INF/services、Class.forName("literal")、       │
│    readObject/readResolve、Jackson/Protobuf 的反射字段、JNI 导出符号     │
│ D. 导出的公共 API（库的对外契约）—— L2，标"开放世界"                    │
│ E. 配置里的类名：YAML/JSON/properties/XML 中出现的 FQN 字符串             │
│ F. 测试：单独作为一类根（测试作根 vs 不作根，各跑一次 → "仅测试使用"）    │
│ G. 显式保留：@KeepAlive("disaster-recovery") / 允许名单（owner 声明）     │
└────────────────────────────────────────────────────────────────────┘
```

**字符串命中（弱根）**：索引时把字节码常量池里的所有字符串常量，以及仓库里所有文本文件（配置、脚本、文档）里形如 FQN 的 token 全部收集起来，和符号表做匹配。命中 → 把该符号标为「弱根」：它不会因此直接保活，但**降低置信度**并作为 blocker 写进证据。这就是 ProGuard / R8（Android 与 Java 的 tree-shaking 工具）的 `-keep` 规则思想：保守地保护动态使用的东西。

**为什么要有「权威部署清单」**：「所有含 main 的类」会把一堆早已不部署的工具类当作根，让它们的整棵依赖树都显得「有用」——**假根导致漏报**。部署清单（或构建系统里标记为发布的二进制目标）才是真根。

---

## 5. 流水线总览

```text
                    固定快照 (git sha S + 构建产物)
                                │
        ┌───────────────────────┴────────────────────────┐
        ▼                                                ▼
 ① 索引 (并行, 按构建目标分片)                    ③ 动态证据 (可选, 持续收集)
   Java: 读 .class 字节码 (ASM)                    · 类加载日志 -Xlog:class+load
   + 调试信息 → 回映射到源码行                      · JFR / 方法级覆盖 agent (抽样)
   C++: clang 索引 + 链接器 --gc-sections 报告      · 按 (服务, 版本) 聚合，保留 90 天
   Python/脚本: 轻量解析 + 低置信度
        │ 输出: defs(symbol, kind, file, line, owner)
        │       refs(src, dst, kind)   strings(file, literal)
        ▼
 ② 汇总 (shuffle by symbol id)  ──▶  CSR 图 + 符号表 + 字符串表
        │
        ▼
 ④ 标记 (单机, 亚秒–数秒)  roots = A ∪ B ∪ C ∪ E(弱) ∪ G
        │      RTA 虚调用解析、lambda/方法引用边
        ▼
 ⑤ 分级与见证 (L0/L1/L2/L3 + blockers + 证据)
        │
        ▼
 ⑥ 报告 + 按 owner 拆 PR（机器人） ──▶ 人审 ──▶ 软删除 ──▶ 真删 ──▶ 回路指标
```

### 5.1 为什么在字节码上分析（Java 的选择）

* **字节码里引用已经被编译器解析好了**：`invokevirtual com/hl/Order.price()J` 里直接写着 owner、name、descriptor。不需要自己做名字解析、重载决议、泛型擦除、import 处理——这些是源码分析的主要成本和出错点。
* **成本低 ~100 倍**：读 `.class` 是线性扫描常量池和方法体（ASM 之类的库一核每秒处理数百 MB），不需要 javac 的类型归属。（量级估计，**未测**。）
* **精确**：lambda 在字节码里是 `invokedynamic`，其引导方法（bootstrap method）参数里能读到真实的目标 `MethodHandle`，所以方法引用 / lambda 的边可以静态恢复。
* **缺点**：没有源码位置 → 用调试信息（`SourceFile`、`LineNumberTable`）回映射；依赖构建产物（但 CI 本来就产出，且可以缓存）；泛型信息被擦除（对可达性影响很小）；Kotlin / Scala 等的合成方法需要过滤。
* 对 C++：没有字节码，用 clang 索引；**链接器本身就是一个可达性分析器**：编译时 `-ffunction-sections -fdata-sections`，链接时 `-Wl,--gc-sections,--print-gc-sections`（GNU ld / gold / lld 均有对应选项）会列出被丢弃的函数段——免费的静态证据。（来源：https://sourceware.org/binutils/docs/ld/Options.html、https://llvm.googlesource.com/lld/+/refs/heads/master/test/ELF/gc-sections-print.s，2026-10-15 核对）

### 5.2 索引记录与符号 ID

```text
defs : (sym_id:int64, kind:{CLASS,METHOD,FIELD,TARGET,RESOURCE}, fqn, desc, access, file, line, owner)
refs : (src_id:int64, dst_id:int64, kind:{CALL,NEW,EXTENDS,IMPLEMENTS,FIELD_R,FIELD_W,ANNOT,METHOD_REF})
strs : (file_or_class, literal)
```

* `sym_id` = 64 位哈希（FQN + 描述符 + 种类），所以不同分片独立计算也得到同一个 ID，汇总时只需按 ID 排序 / 分组。碰撞概率：n = 3.2×10⁶ 个符号、64 位 ID，生日界约 n²/2⁶⁵ = (3.2×10⁶)² / 3.7×10¹⁹ ≈ 2.8×10⁻⁷，可忽略；汇总时再校验同 ID 下 FQN 一致，碰撞则报警。
* 记录是追加式、不可变的；分片失败可以只重跑该分片。

### 5.3 标记阶段（Java 草图，用于说明数据结构，不是完整实现）

```java
// CSR（compressed sparse row）：offsets[v]..offsets[v+1] 是 v 的出边在 targets[] 里的区间。
// 连续数组 + int 下标 = 对缓存友好的图；没有 Node/Edge 对象，没有 GC 压力（见 cpu_cache_locality §5）。
final class SymbolGraph {
    final int[] offsets;      // 长度 V+1
    final int[] targets;      // 长度 E
}

// push(...) 是一个会在栈满时扩容并返回新数组的小辅助函数，这里省略
static java.util.BitSet mark(SymbolGraph g, int[] rootIds) {
    java.util.BitSet live = new java.util.BitSet(g.offsets.length - 1);
    int[] stack = new int[1 << 16]; int sp = 0;                      // 显式栈：不递归，调用链再深也不爆栈
    for (int r : rootIds) if (!live.get(r)) { live.set(r); stack = push(stack, sp++, r); }
    while (sp > 0) {
        int v = stack[--sp];
        for (int i = g.offsets[v]; i < g.offsets[v + 1]; i++) {
            int w = g.targets[i];
            if (!live.get(w)) { live.set(w); stack = push(stack, sp++, w); }
        }
    }
    return live;                                                      // 候选 = 非 live 的符号
}
```

### 5.4 虚调用与精度：CHA / RTA

调用 `Shape.area()`（接口方法）时，到底会执行哪个实现？

* **CHA（Class Hierarchy Analysis，类层次分析）**：假设 `Shape` 的**所有**实现类的 `area()` 都可能被调用。保守、简单，但会把大量实际上从未被实例化的实现类保活（降低召回）。
* **RTA（Rapid Type Analysis，快速类型分析）**：只考虑**已被标记为可达的 `new X()`** 的那些类。分析需要迭代到不动点：新标到一个 `new Foo()` 就可能让 `Foo.area()` 变成可达，进而标到更多。精度明显好于 CHA，成本仍是近线性。
* **更精的指向分析（points-to）**：成本高、规模受限，对「找死代码」性价比不高。**选 RTA 是工程上的甜点**；并说明精度不够的符号会落在「可达但无人调用」的灰区，由 L3/人审处理。

保守性原则：**宁可多保活**（偏向漏报）。因为误判一个活方法为死比漏掉一个死方法的代价大得多。

---

## 6. 分级、证据与「可解释」

输出的是**每个候选一张证据卡**，而不是一个布尔值。示意（JSON 形态）：

```text
symbol      : com.hl.risk.LegacyChecker#check(Lcom/hl/Order;)Z
level       : L1  (封闭世界不可达)
confidence  : HIGH
snapshot    : git 9f3c… + 构建 #48121
witness     : roots=1,284 个已考虑；入边=2：[ OldPricer#price, LegacyChecker#<init> ]
              其中 OldPricer#price 与 LegacyChecker#<init> 本身都不可达（死簇 = {LegacyChecker, OldPricer, OldCurve}，共 3 类 / 412 LOC）
signals     : · 生产类加载日志：过去 90 天、312 个 JVM 实例、从未加载 LegacyChecker
              · 最后一次非机械修改：2022-03-14（owner: risk-platform）
              · 最后一次出现活引用的提交：d41a… "remove pricing v1 caller"（2022-03-14）
blockers    : 无字符串命中；非导出；无反射注解
suggested   : 软删除 PR #… (按簇一起删，含 3 个测试类)
```

**解释从哪来**：

* **活的符号**：见证 = 从某个根到它的**最短路径**（BFS 时记录前驱，即「parent 指针」）。用于回答「为什么你认为它是活的」。
* **死的符号**：见证 = 「它的所有入边的来源本身都不可达」+ 死簇范围。再加上 **blockers 清单**（没有字符串命中、非导出……），让审阅者一眼看出为什么这条能删。
* **置信度**由规则给出（可审计），不是黑盒打分：L0/L1 且 90 天未被加载 = HIGH；L1 但有弱根（字符串命中）= MEDIUM；L2 = 需额外检查；L3 = 仅提示，永不自动。

**聚类**：删单个方法常常删不干净；按**死簇**（强连通分量 / 弱连通的不可达子图）整体删除，PR 才是自洽的（连同它独有的测试、配置、资源）。用 Tarjan SCC 或直接在不可达子图上求连通分量。

---

## 7. 动态证据：为什么要，怎么收，别信它什么

静态分析**证明不了**「没用」，只能证明「保守地看不出用法」。生产运行数据补上另一半：

| 信号 | 怎么收 | 成本 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| **类是否被加载过** | JVM 的 `-Xlog:class+load`（或 JFR 的 ClassLoad 事件）（来源：https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html、https://github.com/openjdk/jdk/blob/master/src/jdk.jfr/share/conf/jfr/default.jfc，2026-10-15 核对）按 (服务, 版本) 去重上报 | 极低（每个 JVM 只在启动 / 首次加载时记一次） | 「类在 N 个月里从未被加载」→ 很强的负证据 | 类加载了不等于方法被调用 |
| **方法是否被调用过** | Java agent / JaCoCo 一类的探针；抽样版用 JFR 执行采样 | 全量探针开销可观（热路径不可用）；采样会漏稀有路径 | 采样命中 = 肯定用过 | 采样没命中 ≠ 没用过（假阴性），**稀有路径正是风险所在** |
| **日志 / 指标里出现过** | 日志里的类名 / 指标名 | 低 | 辅助 | 间接 |
| **演练（game day）** | 定期演练熔断 / 灾备，演练期间开启探针 | 人力 | 给 L3 路径产生「被执行过」的证据 | |

**组合规则**（示例）：`静态不可达 ∧ 90 天未加载` → HIGH；`静态不可达 ∧ 曾被加载`（说明有我们没建模的动态入口）→ 降级并**反向修正根模型**；`静态可达 ∧ 长期冷` → L3，只提示。

**交易系统要点**：热路径上不能装探针（会改变延迟分布）；类加载日志只在启动期有成本，所以是安全的首选信号。对于必须保留的冷路径用 `@KeepAlive("原因")` 声明，并为它们安排演练（演练同时是动态证据和系统可靠性）。

---

## 8. 从候选到安全删除（流程设计）

```text
候选 ─▶ 分簇 ─▶ 按 owner(CODEOWNERS) 分配 ─▶ 机器人开 PR（≤500 LOC，一个簇一个 PR）
                                                     │
                                  CI：全量构建 + 测试 + 再跑一遍可达性（删后图不应出现新的"未解析引用"）
                                                     │
                      ┌──────────────────────────────┴──────────────┐
                      ▼                                             ▼
              软删除（默认，对 L2/L3）                         直接删除（仅 L0/L1 HIGH）
        @Deprecated(forRemoval=true) +                            │
        被调用时打一条日志/指标，观察 N 个发布周期                 │
                      │ 无调用                                      │
                      └──────────────▶ 真删 ◀───────────────────────┘
                                         │
                       回滚路径：一个 revert；PR 里附"如何恢复"
```

**回路指标**（也是系统自身的 KPI）：

* **精度（precision）**：owner 接受的 PR 比例 / 被 revert 的比例（目标：revert < 1%）。
* **召回的代理**：见下面 §9 的回测与种子注入。
* **吞吐**：每周合并的 LOC；候选积压量。
* **新增死代码的速率**：定期重跑（每周）→ 趋势。

**组织层面**（面试官常追问）：给 owner 看到价值（构建时间 / 测试时间节省、依赖更新负担）；每个 PR 小、证据完整、可一键拒绝并说明原因（拒绝原因反哺根模型：例如发现一类漏掉的反射入口）；不要追求一次清空。

---

## 9. 怎么知道系统是对的：评估

1. **回测（backtest）历史删除**：在 git 历史里找所有被人工标注为「remove unused / dead code」的提交。对每个这样的提交，在**它的父提交**上跑分析器：这些被人删掉的符号，被我们标为候选的比例 = 召回的下界估计；被我们标为「活」的 = 漏报，逐条分析原因（几乎都能找到一类缺失的模型）。
2. **种子注入**：在快照里注入一批已知死代码（形状逼真：有测试、有死环、有包内引用），看检出率。
3. **抽样人审**：随机抽 100 个 HIGH 候选让 owner 判断 → 精度估计，附置信区间（n = 100，p̂ = 0.98 时，标准误 ≈ √(0.98×0.02/100) ≈ 1.4%）。
4. **对照现有工具**：IDE inspection / ProGuard 的 `-printusage` 报告（来源：https://www.guardsquare.com/manual/configuration/usage、https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html，2026-10-15 核对）：交集与差集都值得看。
5. **回归**：同一快照两次运行输出逐字节相同；改动分析器时对固定快照做 diff，所有变化必须有解释。

---

## 10. 增量运行与多语言

**增量**：

* 索引记录以（输入文件内容哈希 + 分析器版本）为键缓存（构建缓存 / 远程缓存思想）。一次提交只改 k 个文件 → 只重建这 k 个文件（或其所在构建目标）的记录；再合并进图。
* 图重建很便宜（亚秒到秒级，§3），所以**不做图的增量更新**，每次全量标记，省掉增量算法的正确性风险。
* 触发：每天夜里一次 + PR 上做「本次改动是否让某些符号变死 / 复活」的轻量检查（只重算受影响的反向可达集）。

**多语言边**（真实代码库的难点）：

* JNI：Java `native` 方法 ↔ C++ 导出符号 `Java_pkg_Class_method`，按名字规则连边。
* 协议 / IDL（protobuf、Thrift、SBE 模板（来源：https://github.com/aeron-io/simple-binary-encoding，2026-10-15 核对））：生成的类是「叶子」，但消息类型是否被用要看生成代码的引用，别把生成代码当死代码；从 IDL 文件出发建边。
* 配置 / 脚本里的类名：§4 的字符串命中。
* SQL / 动态查询里的表名列名：可选，低置信度。
* **覆盖率阈值**：任何模块的索引覆盖率低于阈值（构建失败、缺文件），则**不对依赖它的符号做死判定**（fail closed）。

**多构建配置**：`#ifdef`、Maven profile、平台特定源码：对**所有配置取并集**——某个配置下用到的符号就是活的。

---

## 11. 与交易公司背景的连接（让答案「像是为这家公司写的」）

* **Java 岗的职责**是研究平台、分布式存储、计算集群与监控 [O-C2]：这些系统里典型的死代码来源是「旧交易所适配器」「废弃的数据格式解析器」「做过的实验性回测策略」。证据卡里写上 owner = research-platform 这类团队，PR 才有人接。
* 回测平台与实盘共用同一份解析 / 模拟代码（推断，见公司简报 §4.2）：删「回测专用」代码时，必须把**实盘二进制和回测二进制都当根**。
* 删除的价值主张要讲对：不是「代码更漂亮」，而是 **减小变更面（change surface）**——每次上线都是风险，死代码让每次改动的影响范围分析更难。

---

## 12. 常见的弱答案及修正

| 弱答案 | 问题 | 修正 |
|---|---|---|
| 「`grep` 每个函数名，没有结果就删」 | 找不到死环；会被注释 / 字符串 / 同名其他类干扰；漏掉反射 | 符号级引用图 + 可达性 |
| 「用 IDE 的 unused 提示」 | 只覆盖私有成员（L0）；不跨模块 | 全程序可达性 + 根模型 |
| 「上 Spark / GraphX 做分布式图计算」 | 估算后图只有 ~80 MB | 分布式用在索引；图在单机 |
| 「静态分析结果直接自动删」 | 反射 / 公共 API / 冷路径 → 事故 | 候选 + 证据 + 人审 + 软删除 |
| 「看覆盖率，没覆盖的就是死代码」 | 测试覆盖率 ≠ 生产使用；稀有路径 | 生产类加载 / 采样作为证据之一，不是判决 |
| 「只做运行时（动态）分析」 | 抽样会漏稀有路径；永远不能证明没用 | 静态证明不可达 + 动态佐证 |
| 没有评估方案 | 不知道精度和召回 | 回测历史删除、种子注入、抽样人审 |

---

## 13. 结尾总结（最后一分钟）

「我把代码库当成一张符号图，用 RTA 在字节码上做可达性标记，根集合来自部署清单、框架模型、SPI、字符串命中和 owner 声明。输出是带见证和置信度的候选，分 L0–L3 四级。分布式只用在并行索引，图本身 80 MB，一台机器亚秒标记。动态证据（类加载日志）佐证静态结论，永不单独判死。删除走 owner PR + 软删除，指标是 revert 率；我用历史回测和种子注入估计召回。最大的风险是漏建模的动态入口和冷但必要的路径，所以 fail closed，并把冷路径用 `@KeepAlive` 和演练管起来。」

## 14. 延伸阅读

* Java 虚拟线程 / 并发无关；本题相关的 JVM 工具：`jdeps`（包依赖）、`jlink`（模块裁剪）、ProGuard / R8 的 shrinker 文档（`-keep` 规则与 `-printusage`）。
* 调用图构造：Dean, Grove, Chambers, 「Optimization of Object-Oriented Programs Using Static Class Hierarchy Analysis」（ECOOP 1995，CHA）；Bacon & Sweeney, 「Fast Static Analysis of C++ Virtual Function Calls」（OOPSLA 1996，RTA）。
* 代码索引的工业实践：Google Kythe；Sourcegraph 的 SCIP 格式，以及 LSP 生态的 LSIF 格式。（来源：https://kythe.io/docs/kythe-overview.html、https://github.com/sourcegraph/scip、https://microsoft.github.io/language-server-protocol/specifications/lsif/0.6.0/specification/，2026-10-15 核对）
* 反例思维：Chesterton's fence。
* 追问见 [followups.md](followups.md)；评分见 [rubric.md](rubric.md)。
