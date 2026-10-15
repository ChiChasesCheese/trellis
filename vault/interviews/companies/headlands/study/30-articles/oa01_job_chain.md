# oa01 · Job Chain 报表 —— 讲义

> 题面：`loop/rounds/00_oa/oa01_job_chain/problem.md` · 速查：同目录 `REPORT.md` · 代码：同目录 `reference/JobChains.java`
> 写法说明见 `study/TEXTBOOK.md`。这一篇是全 kit 讲义的样板，所以每一步都写得特别细。

---

## 1. 这道题在问什么

一台机器上跑着很多「任务」（job）。有些任务是**接力**的：任务 1 跑完，自动触发任务 23；任务 23 跑完，触发任务 3；
任务 3 后面没有了。这样首尾相接的一串就叫一条**链**（chain）。

日志是一份 CSV 文件，每行三个数：

```
任务编号, 这个任务跑了多少秒, 下一个任务的编号（0 表示没有下一个）
```

题目要你把所有链找出来，每条链报告：从哪个任务开始、到哪个任务结束、一共几个任务、总共跑了多久、平均每个任务多久。
如果日志有任何不对劲（格式错、数据矛盾），**什么都不报告**，只输出一行 `Malformed Input`。

### 手算一遍

输入：

```
#job_id,runtime_in_seconds,next_job_id
1,60,23
23,30,3
3,15,0
5,200,0
```

* 任务 1 → 任务 23 → 任务 3 → 结束。三个任务，60 + 30 + 15 = 105 秒，平均 105 ÷ 3 = 35 秒。
* 任务 5 → 结束。一个任务，200 秒。

105 秒 = 1 分 45 秒，写成 `00:01:45`；200 秒 = 3 分 20 秒，写成 `00:03:20`。
按总时长从长到短排：先报任务 5 那条，再报任务 1 那条。这就是 `problem.md` 里的样例输出。

---

## 2. 前置知识

### 2.1 链表（linked list）与「链」

**是什么**：一串元素，每个元素记着「下一个是谁」。本题里每一行就是一个元素，`next_job_id` 就是那根「指针」。

**为什么需要这个概念**：一旦看出「这是若干条链表」，题目就从「处理一堆 CSV」变成「在链表上走路」，思路清楚得多。
WSO 上 2020 年的考生原话就是：「detect if the input data is an union of single linked list」——判断输入是不是**若干条单链表拼在一起**。

**它怎么工作**：

```
  [1| 60s|→23] ──▶ [23| 30s|→3] ──▶ [3| 15s|→0]      链 A：头 1，尾 3
  [5|200s|→0]                                        链 B：头 5，尾 5
```

* **头**（head）：没有任何人指向它的元素。
* **尾**（tail）：`next = 0` 的元素。
* 从头出发，顺着 `next` 一直走，走到尾，就把一条链走完了。

**Java 里怎么写**：我们不需要自己写链表类——用一张「编号 → 这一行」的表，顺着 `next` 去查表就是在走链表。这张表就是下一节的 `HashMap`。

### 2.2 哈希表（`HashMap`）为什么查得快

**是什么**：一种「键 → 值」的存储，给它键，几乎立刻拿到值。

**为什么需要它**：走链时每一步都要问「编号为 23 的任务在哪一行？」。

* 如果用一个 `List` 存所有行，每次都要从头到尾找一遍：n 行就要找 n 次，走完所有链一共要找 n 次，总共大约 n × n 次。
  n = 100 万时就是 1 万亿次，几个小时也跑不完。
* `HashMap` 的平均查找时间和表有多大**无关**，所以总共只要大约 n 次。

**它怎么工作**（简化版）：

1. 准备一个数组，比如 16 个格子（bucket，桶）。
2. 存 `23 → 那一行` 时，先算 `23` 的哈希值（`Integer.hashCode(23)` 就是 23），再取余：23 % 16 = 7，放进第 7 格。
3. 查 `23` 时同样算出 7，直接去第 7 格拿，不用看别的格子。
4. 两个键算出同一个格子叫**冲突**（collision）：格子里挂一个小链表（Java 8 起冲突太多会变成红黑树），逐个比较。
5. 元素太多时数组扩容（默认装到 75% 就翻倍），保证每个格子里平均只有很少几个元素。

**Java 里怎么写**：

```java
var byId = new HashMap<Integer, Job>();
byId.put(23, job);          // 存
Job j = byId.get(23);       // 取；没有就返回 null
byId.containsKey(7);        // 有没有
byId.putIfAbsent(1, job);   // 只有不存在时才存；返回旧值（存在时）或 null
```

我们的参考解用的是 `LinkedHashMap`：它是 `HashMap` 再加一条「按插入顺序」串起来的链，遍历时顺序和插入顺序一致。
用它是为了输出**确定**（同一份输入每次跑结果顺序都一样），方便调试。

### 2.3 时间复杂度（Big-O）——只需要知道这么多

**是什么**：描述「输入变大 n 倍时，程序变慢多少倍」的记号。

| 写法 | 意思 | 100 万行大概要做多少步 |
|---|---|---|
| O(n) | 和行数成正比 | 100 万 |
| O(n log n) | 排序的典型代价 | 2000 万 |
| O(n²) | 每行都和每行比一次 | 1 万亿（跑不完） |

**为什么需要它**：面试官问「百万行多快？」时，要能说出「O(n)，因为每行只进哈希表一次、只被走过一次」。
（更完整的讲解会放在 `study/00-foundations/complexity.md`。）

### 2.4 入度（in-degree）：一个能把「环」和「分叉」一网打尽的概念

**是什么**：一个元素被多少个其他元素指着。

**为什么需要它**：这道题的「数据矛盾」几乎都能用入度描述：

| 情况 | 图 | 入度的表现 |
|---|---|---|
| 正常链 | 1→23→3 | 头的入度 0，其余都是 1 |
| 两个任务指向同一个（多 parent） | 1→3，2→3 | 任务 3 的入度是 2 ❌ |
| 环 | 2→3→2 | 环上每个点入度都是 1，**没有入度 0 的头** |

所以第一条规则是：**任何元素入度都不能超过 1**。入度 ≤ 1 之后，图里只剩两种形状：从某个头出发的链，或者一个封闭的环。
（「多 children」——一个任务指向两个——在本题输入里不可能出现，因为每行只有一个 `next`；但如果同一个 `job_id` 出现两行，就等于有两个 next，所以要查**重复编号**。）

### 2.5 为什么「从所有头走一遍，没走到的就在环上」

这是本题最巧的一步，单独证明一下。

前提：每个元素入度 ≤ 1，且每个 `next` 都指向真实存在的元素。

1. 从每个入度为 0 的元素（头）出发往下走。
2. 因为入度 ≤ 1，两条不同的链不可能在中途汇合（汇合点的入度就会是 2）。所以每个元素**最多被走到一次**。
3. 假设某个元素 X 没被走到。顺着「谁指向 X」往回找：X 的前驱、前驱的前驱……
   * 如果往回找能找到一个入度 0 的元素，那它是头，第 1 步就会从它出发走到 X——矛盾。
   * 所以往回找永远找不到头。元素只有有限个，往回走一定会遇到重复的元素。
   * 重复的那个元素就是 X 自己。把往回走的序列记作 X = P0 ← P1 ← P2 ← …（入度 ≤ 1，所以每个元素至多一个前驱，这个序列是唯一的）。
     设第一次重复是 Pk = Pj（j < k）。如果 j > 0：Pj 的 `next` 是 P(j−1)，Pk 的 `next` 是 P(k−1)；Pj 和 Pk 是同一个元素，
     而一个元素只有一个 `next`，所以 P(j−1) = P(k−1)——这是一个**更早**的重复，和「第一次重复」矛盾。
     所以 j = 0，即往回走绕回了 X 自己：**X 在一个环上**。

结论：**走完所有头之后，只要「走到的元素个数」不等于「元素总数」，就一定有环**。一次比较就够了，不需要写专门的找环算法（DFS 染色）。

### 2.6 秒 → `hh:mm:ss`：整除与取余

**是什么**：`/` 在两个整数之间是**整除**（扔掉小数），`%` 是**取余数**。

```
7265 秒
小时 = 7265 / 3600          = 2      （7265 里有 2 个完整的 3600）
分钟 = 7265 / 60 % 60       = 121 % 60 = 1
秒   = 7265 % 60            = 5
→ 02:01:05
```

**为什么分钟要 `% 60`**：`7265 / 60 = 121` 是「总共多少分钟」，其中 120 分钟已经算进了 2 小时，只剩 1 分钟要显示。
网上公开的那份 C++ 题解就**漏了这个 `% 60`**，7200 秒会输出 `02:120:00`。隐藏测试很可能专门测这个。

**Java 里怎么写**：`"%02d:%02d:%02d".formatted(h, m, s)` —— `%02d` 的意思是「整数，至少两位，不够前面补 0」。

### 2.7 整数溢出（overflow）

**是什么**：`int` 只有 32 位，最大是 2,147,483,647（约 21 亿）。超过它会**悄悄绕回负数**，不报错。

```java
int a = 2_000_000_000;
int b = a + a;            // -294967296 ！
long c = (long) a + a;    // 4000000000 ✓
Math.addExact(a, a);      // 抛 ArithmeticException：明确告诉你溢出了
```

**为什么本题要管**：两个各跑 20 亿秒的任务（题目没说不行），总时长用 `int` 累加就变成负数，格式化出来是乱码。
所以时长一律用 `long`（最大约 9.2 × 10^18），并且用 `Math.addExact` 累加：万一连 `long` 都溢出，至少会报错而不是给错答案。

---

## 3. 从最笨的解法开始

最直接的想法：

```
对每个 next = 0 的任务（尾）:
    从尾往回找：在全部行里找「谁的 next 是我」，找到就继续往回找
```

问题：

1. **慢**：每往回一步都要扫一遍所有行，O(n²)。100 万行时跑不完。
2. **漏查环**：环上没有 `next = 0` 的元素，从尾出发永远碰不到它。输入 `1,10,0 / 2,10,3 / 3,10,2` 会被当成合法（只报告链 1），实际应该是 `Malformed Input`。
3. **漏查分叉**：往回找时如果两个任务都指向我，选哪个？笨办法通常只取第一个，于是分叉被静默忽略。

---

## 4. 一步一步改进

**第 1 步：解决「慢」**
* 发现：慢在「找某个编号在哪一行」。
* 想法：先用一遍循环把所有行放进 `HashMap<编号, 行>`，之后每次查找都是 O(1)。
* 顺便：放进去时如果 `putIfAbsent` 返回了非 null，说明编号重复 → 报错。
* 新复杂度：建表 O(n)。

**第 2 步：从头往下走，而不是从尾往回找**
* 发现：往回找需要「谁指向我」，这是反方向的信息，要额外建一张表；而往下走只需要 `next`，现成的。
* 想法：先找出所有**头**。头 = 没人指向的元素。所以再扫一遍，把每个 `next`（非 0）记进一个集合 `hasPredecessor`；不在集合里的就是头。
* 顺便查两个错误：
  * `next` 指向的编号不在表里 → **悬空引用** → 报错。
  * 把 `next` 加进集合时发现它已经在里面（`Set.add` 返回 false）→ 有两个任务指向它，**入度 2** → 报错。
* 新复杂度：O(n)。

**第 3 步：走链并统计**
* 对每个头：计数、累加时长（`Math.addExact`）、记下尾，顺手把走过的编号放进 `visited`。
* 每个元素只会被走一次（2.5 节第 2 点），所以总共 O(n)。

**第 4 步：查环**
* 用 2.5 节的结论：`visited.size() != byId.size()` → 有环 → 报错。O(1)。

**第 5 步：排序和输出**
* 链的条数 k ≤ n，排序 O(k log k)。
* 排序规则：总时长降序，相同时按头编号升序（降序是原题原文；同总时长时按头编号升序是原题没说的 (inferred) 选择——写清楚 tie-break 是好习惯）。

总复杂度 O(n + k log k)，内存 O(n)。

---

## 5. 逐段讲参考解

### 5.1 用 record 表示一行

```java
public record Job(int id, long runtimeSeconds, int nextId) {
    public Job {
        if (id <= 0) throw new MalformedInputException("job_id must be positive: " + id);
        if (runtimeSeconds < 0) throw new MalformedInputException("negative runtime: " + runtimeSeconds);
        if (nextId < 0) throw new MalformedInputException("negative next_job_id: " + nextId);
        if (nextId == id) throw new MalformedInputException("self loop: " + id);
    }
}
```

* `record` 一行声明了：三个 `private final` 字段、构造器、三个读取方法 `id()` / `runtimeSeconds()` / `nextId()`、
  以及按字段比较的 `equals`、`hashCode`、`toString`。老写法要 40 行。
* `public Job { ... }` 是**紧凑构造器**（compact constructor）：没有参数列表，在字段赋值**之前**运行。这里放校验，
  于是「一个非法的 Job 对象」根本不可能被创建出来——这叫**让非法状态无法表示**。
* 只能在单行内判断的规则放这里（编号为正、时长非负、不能指向自己）；需要看多行才能判断的规则（重复、悬空、分叉、环）放在 `chains()` 里。

### 5.2 解析一行

```java
private static final Pattern LINE = Pattern.compile("\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*");
...
var m = LINE.matcher(raw);
if (!m.matches()) throw new MalformedInputException("bad line: " + raw);
```

* 正则逐段读：`\s*` 任意空白，`(-?\d+)` 一个可选负号加若干数字（括号表示「捕获」，之后用 `m.group(1)` 取），`,` 逗号。
* `matches()` 要求**整行**都匹配；`find()` 只要求某一段匹配——用 `find()` 的话 `1,2,3,4` 会被误判为合法。
* 为什么允许负号？如果正则直接拒绝负号，`3,-5,0` 的报错是「格式错」；允许之后交给 `Job` 的构造器，报错是「时长为负」，信息更准确。两种都输出 `Malformed Input`，但调试时差别很大。
* `Integer.parseInt("99999999999")` 超出 int 范围会抛 `NumberFormatException`，我们把它转成同一种 `MalformedInputException`，调用方只需要处理一种异常。

### 5.3 拼链（第 1–4 步的代码）

```java
var byId = new LinkedHashMap<Integer, Job>();
for (var j : jobs) {
    if (byId.putIfAbsent(j.id(), j) != null) throw ...("duplicate job_id " + j.id());
}
var hasPredecessor = new HashSet<Integer>();
for (var j : jobs) {
    if (j.nextId() == 0) continue;
    if (!byId.containsKey(j.nextId())) throw ...("dangling next_job_id " + j.nextId());
    if (!hasPredecessor.add(j.nextId())) throw ...("two jobs point at " + j.nextId());
}
```

* `var`：让编译器根据右边推断类型，`var byId` 就是 `LinkedHashMap<Integer, Job>`。只在右边类型一眼可见时用。
* `Set.add` 返回 `boolean`：「这次是否真的加进去了」。已经在里面就返回 false——一个调用同时完成「记录」和「查重」。

```java
for (var head : byId.values()) {
    if (hasPredecessor.contains(head.id())) continue;   // 不是头，跳过
    int count = 0;
    long total = 0;
    Job cur = head;
    while (true) {
        visited.add(cur.id());
        count++;
        total = Math.addExact(total, cur.runtimeSeconds());
        if (cur.nextId() == 0) break;
        cur = byId.get(cur.nextId());
    }
    out.add(new Chain(head.id(), cur.id(), count, total));
}
if (visited.size() != byId.size()) throw ...("cycle ...");
```

* 为什么 `while (true)` 不会死循环？因为我们只从头出发，而 2.5 节证明了从头出发不会进入环（进入环意味着环上某个点入度为 2，已经在上一段被拒绝了）。

### 5.4 排序

```java
out.sort(Comparator.comparingLong(Chain::totalSeconds).reversed().thenComparingInt(Chain::startJob));
```

从左往右读：按 `totalSeconds` 比较 → 反过来（降序）→ 相等时再按 `startJob` 比较（升序）。
`Chain::totalSeconds` 是**方法引用**，等价于 `c -> c.totalSeconds()`。

⚠️ 一个经典的坑：`comparingLong(A).thenComparingInt(B).reversed()` 会把**两个**条件都反过来。`reversed()` 的位置很重要。

### 5.5 结果类型与输出

```java
public sealed interface Outcome permits Ok, Malformed {}
public record Ok(List<Chain> chains) implements Outcome {}
public record Malformed(String reason) implements Outcome {}

public static Outcome analyze(List<String> lines) {
    try { return new Ok(chains(parse(lines))); }
    catch (MalformedInputException e) { return new Malformed(e.getMessage()); }
}

public static List<String> render(Outcome outcome) {
    return switch (outcome) {
        case Malformed _ -> List.of("Malformed Input");
        case Ok(var chains) -> { ...; yield lines; }
    };
}
```

* 内部各层**抛异常**（简单，不用层层返回错误码）；在 `analyze` 这**一个**边界上把异常变成一个值。之后的代码只和值打交道。
* `sealed ... permits Ok, Malformed`：只有这两种实现，编译器知道。所以 `switch` 写了这两个 `case` 就算「穷尽」，不需要 `default`。
  以后如果加第三种结果（比如 `Partial`），每个没处理它的 `switch` 都会**编译失败**——编译器帮你找到所有要改的地方。
* `case Ok(var chains)`：**record 模式**，一步完成「判断类型 + 取出字段」。
* `case Malformed _`：`_` 表示「我知道它是 Malformed，但不需要里面的字段」（Java 21 预览特性）。
* `yield`：在 `switch` 表达式的代码块里「返回这个分支的值」。

---

## 6. Java 21 特性小课

### record（Java 16）

旧写法（Java 8）：

```java
public final class Job {
    private final int id; private final long runtimeSeconds; private final int nextId;
    public Job(int id, long runtimeSeconds, int nextId) { /* 校验 + 赋值 */ }
    public int getId() { return id; }  // ... 另外两个 getter
    @Override public boolean equals(Object o) { /* 10 行 */ }
    @Override public int hashCode() { return Objects.hash(id, runtimeSeconds, nextId); }
    @Override public String toString() { /* ... */ }
}
```

新写法一行。更重要的是**意图**：record 告诉读代码的人「这是纯数据，不可变，两个字段相同的对象就是相等的」。
测试里可以直接 `assertEquals(List.of(new Chain(5, 5, 1, 200)), chains)`，因为 `equals` 是按字段比的。

**什么时候不该用**：需要可变字段、需要继承别的类（record 隐式继承 `java.lang.Record`，不能再 `extends`）、或者字段很多且大部分可选时。

### sealed 接口（Java 17）+ 模式匹配 switch（Java 21）

旧写法：

```java
if (outcome instanceof Ok) {
    Ok ok = (Ok) outcome;            // 手动强转
    List<Chain> chains = ok.chains();
    ...
} else if (outcome instanceof Malformed) {
    ...
} else {
    throw new IllegalStateException();  // 「不可能到这里」——但编译器不知道
}
```

新写法让编译器参与：类型判断、取字段、穷尽检查都由它保证。这种「一个封闭的类型族 + 按类型分派」的组合，
在别的语言里叫**代数数据类型**（algebraic data type），是 Java 21 最重要的建模工具。后面订单簿那题会用它表示「下单 / 撤单 / 成交」事件。

详细课本：`study/10-java21/J02_sealed.md`、`J03_pattern_switch.md`、`J04_record_patterns.md`（待写）。

---

## 7. 追问预演

**问：百万行要多久？瓶颈在哪？**
* 思考：每行进哈希表一次、被走一次 → O(n)。常数上的瓶颈是什么？是正则解析和 `Integer` 装箱。
* 答：O(n)。实测 100 万行整题不到 1 秒。如果要再快：手写解析代替正则（逐字符读数字）；用原始类型数组代替 `HashMap<Integer, …>`，避免装箱。
* 说出口：「线性的。真要压常数，第一刀是解析，第二刀是去掉 Integer 装箱，比如编号范围已知时用 int 数组当表。」

**问：文件 10 GB 放不进内存？**
* 思考：时长可以流式累加，难的是「链的结构」需要全局信息。
* 答：第一遍只存 `(id, next)` 两个 int，每行 8 字节，10 亿行 8 GB 仍然大 → 按 id 范围分片写到磁盘，或者用外部排序。
* 说出口：「先降内存：只留结构，不留时长；再不行就按 id 分片做外部处理，最后合并。」

**问：如果允许一个任务有两个前驱（汇合）怎么办？**
* 答：那就不是链而是**有向无环图**（DAG），问题变成拓扑排序 + 最长路径（关键路径）。用 Kahn 算法：反复取入度为 0 的点。
  网上 2 年前的变体就是带时间戳的拓扑排序。

**问：为什么用异常而不是返回 `Optional` 或错误码？**
* 答：校验分散在多层，异常让中间层不用层层转发错误；只在 `analyze` 这一个边界上转换成值。异常在 JVM 上比较贵（要抓栈），但这里只在出错时抛一次，不在热路径上。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 分钟 = `seconds / 60` | 包含了已经算进小时的分钟，7200 秒输出 `02:120:00` | `seconds / 60 % 60` |
| 时长用 `int` 累加 | 两个 20 亿秒的任务溢出成负数 | `long` + `Math.addExact` |
| 只从 `next = 0` 的尾往回找 | 独立的环没有尾，查不出来 | 从头往下走 + 走完比较个数 |
| `comparing(A).thenComparing(B).reversed()` | B 也被反过来了 | `comparing(A).reversed().thenComparing(B)` |
| 用 `matcher.find()` 校验整行 | `1,2,3,4` 能 find 到 `1,2,3` | `matcher.matches()` |
| 假设第一行一定是表头直接跳过 | 没有表头时丢了第一条数据 | 按 `#` 开头判断 |

---

## 9. 自测题

1. 入度 ≤ 1 的有向图里，可能出现哪两种连通形状？
2. 为什么 `visited.size() != byId.size()` 就能断定有环？用自己的话说。
3. 3599 秒、3600 秒、360000 秒分别格式化成什么？
4. 写一个 `Comparator<Chain>`：按 job 数升序，相同按总时长降序。
5. 如果把 `Outcome` 改成 `sealed interface Outcome permits Ok, Malformed, Empty`，`render` 会怎样？

<details><summary>答案</summary>

1. 从一个头出发的链；一个封闭的环。
2. 从所有头出发，每个点最多被走一次；没被走到的点往回追溯永远找不到头，只能绕回自己，所以在环上。
3. `00:59:59`、`01:00:00`、`100:00:00`。
4. `Comparator.comparingInt(Chain::count).thenComparing(Comparator.comparingLong(Chain::totalSeconds).reversed())`
5. 编译失败：`switch` 不再穷尽，必须加 `case Empty ...`。这正是 sealed 的价值。

</details>

---

## 10. 延伸阅读

* JEP 395 Records — https://openjdk.org/jeps/395 —— record 的设计动机，读「Goals」和「Non-Goals」两节就够了。
* JEP 409 Sealed Classes — https://openjdk.org/jeps/409 —— 为什么需要「封闭的继承」。
* JEP 441 Pattern Matching for switch — https://openjdk.org/jeps/441 —— 穷尽性检查的规则。
* `java.util.HashMap` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html —— 第二段讲了容量与装载因子（load factor）。
* 《算法》（Sedgewick）第 3.4 节 散列表 —— 哈希表最好的入门教材。
