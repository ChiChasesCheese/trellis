# oa01 · Job Chain 报表 —— 讲义

> 读者：会写基本 Java（类、方法、循环、集合），其余从零讲。

---

## 1. 问题是什么

许多「任务」（job）会**接力**：任务 1 跑完触发 23，23 触发 3，3 后面没有了。首尾相接的一串叫**链**（chain）。

日志是 CSV，每行三个数：

```
任务编号, 这个任务跑了多少秒, 下一个任务的编号（0 表示没有下一个）
```

找出所有链，每条报告起始任务、结束任务、任务数、总时长、平均时长。日志有任何不对劲（格式错、数据矛盾），**什么都不报告**，只输出一行 `Malformed Input`。

### 手算一遍

输入：

```
#job_id,runtime_in_seconds,next_job_id
1,60,23
23,30,3
3,15,0
5,200,0
```

* 任务 1 → 23 → 3 → 结束：三个任务，60 + 30 + 15 = 105 秒，平均 35 秒。
* 任务 5 → 结束：一个任务，200 秒。

105 秒写成 `00:01:45`，200 秒写成 `00:03:20`。按总时长从长到短排：先任务 5 那条，再任务 1 那条。

---

## 2. 前置知识

### 2.1 链表（linked list）与「链」

每个元素记着「下一个是谁」。这里每行是一个元素，`next_job_id` 是「指针」。

**为什么需要**：看出「这是若干条链表」，题目就从「处理 CSV」变成「在链表上走路」：判断输入是不是**若干条单链表拼在一起**。

```
  [1| 60s|→23] ──▶ [23| 30s|→3] ──▶ [3| 15s|→0]      链 A：头 1，尾 3
  [5|200s|→0]                                        链 B：头 5，尾 5
```

* **头**（head）：没有任何人指向它的元素。
* **尾**（tail）：`next = 0` 的元素。
* 从头顺着 `next` 走到尾，就走完一条链。

**Java**：不用自写链表类，用「编号 → 这一行」的 `HashMap`，顺着 `next` 查表就是在走链表。

### 2.2 哈希表（`HashMap`）为什么查得快

**是什么**：「键 → 值」存储，给键几乎立刻拿到值。

**为什么需要**：走链每步都要问「编号 23 在哪一行？」。`List` 每次从头扫，总共约 n² 次（n = 100 万时 1 万亿）；`HashMap` 平均查找与表大小**无关**，总共约 n 次。

**怎么工作**（简化）：

1. 准备一个数组，比如 16 个格子（bucket，桶）。
2. 存 `23 → 那一行`：算哈希值（`Integer.hashCode(23)` 就是 23），取余 23 % 16 = 7，放进第 7 格。
3. 查 `23`：同样算出 7，直接取第 7 格。
4. 两个键落到同一格叫**冲突**（collision）：格子里挂小链表（Java 8 起冲突太多变红黑树），逐个比较。
5. 装到 75% 数组翻倍，保证每格元素很少。

```java
var byId = new HashMap<Integer, Job>();
byId.put(23, job);          // 存
Job j = byId.get(23);       // 取；没有就返回 null
byId.containsKey(7);        // 有没有
byId.putIfAbsent(1, job);   // 只有不存在时才存；返回旧值（存在时）或 null
```

这里用 `LinkedHashMap`（遍历顺序等于插入顺序），输出**确定**，便于调试。

### 2.3 时间复杂度（Big-O）

**是什么**：描述「输入变大 n 倍时程序慢多少倍」的记号。

| 写法 | 意思 | 100 万行大概多少步 |
|---|---|---|
| O(n) | 与行数成正比 | 100 万 |
| O(n log n) | 排序的典型代价 | 2000 万 |
| O(n²) | 每行和每行比一次 | 1 万亿（跑不完） |

被问「百万行多快？」要能答「O(n)，每行只进哈希表一次、只被走一次」。

### 2.4 入度（in-degree）：把「环」和「分叉」一网打尽

**是什么**：一个元素被多少个其他元素指着。

**为什么需要**：这里「数据矛盾」几乎都能用入度描述：

| 情况 | 图 | 入度的表现 |
|---|---|---|
| 正常链 | 1→23→3 | 头入度 0，其余都是 1 |
| 多 parent | 1→3，2→3 | 任务 3 入度 2 ❌ |
| 环 | 2→3→2 | 环上每点入度 1，**没有入度 0 的头** |

规则一：**任何元素入度不能超过 1**。之后只剩两种形状：从某个头出发的链，或封闭的环。
「多 children」不会出现（每行只有一个 `next`），但同一 `job_id` 出现两行就等于有两个 next，所以要查**重复编号**。

### 2.5 为什么「从所有头走一遍，没走到的就在环上」

前提：每个元素入度 ≤ 1，且每个 `next` 都指向真实存在的元素。

1. 从每个入度为 0 的元素（头）出发往下走。
2. 入度 ≤ 1，两条不同的链不可能中途汇合（汇合点入度会是 2），所以每个元素**最多被走到一次**。
3. 假设 X 没被走到，顺着「谁指向 X」往回找：X = P0 ← P1 ← P2 ← …（入度 ≤ 1，前驱唯一）。
   * 若找到入度 0 的元素，它是头，会走到 X——矛盾。所以永远找不到头。
   * 元素有限，必然重复。设第一次重复是 Pk = Pj（j < k）。若 j > 0，同一元素只有一个 `next`，故 P(j−1) = P(k−1)，是更早的重复，矛盾。
     所以 j = 0，绕回 X 自己：**X 在环上**。

结论：**走完所有头后，只要「走到的元素个数」不等于「元素总数」，就一定有环**。一次比较即可，不需要 DFS 染色。

### 2.6 秒 → `hh:mm:ss`：整除与取余

`/` 在整数间是**整除**（扔掉小数），`%` 是**取余**。

```
7265 秒
小时 = 7265 / 3600          = 2      （7265 里有 2 个完整的 3600）
分钟 = 7265 / 60 % 60       = 121 % 60 = 1
秒   = 7265 % 60            = 5
→ 02:01:05
```

**分钟为什么要 `% 60`**：`7265 / 60 = 121` 是总分钟数，其中 120 分钟已算进 2 小时。漏掉它，7200 秒会输出 `02:120:00`，最易被边界用例抓到。

Java：`"%02d:%02d:%02d".formatted(h, m, s)`，`%02d` 表示「整数，至少两位，不够补 0」。

### 2.7 整数溢出（overflow）

`int` 最大 2,147,483,647（约 21 亿），超过会**悄悄绕回负数**，不报错。

```java
int a = 2_000_000_000;
int b = a + a;            // -294967296 ！
long c = (long) a + a;    // 4000000000 ✓
Math.addExact(a, a);      // 抛 ArithmeticException：明确告诉你溢出了
```

**这里**：两个各 20 亿秒的任务用 `int` 累加会变负数。所以时长用 `long`（最大约 9.2 × 10^18）并用 `Math.addExact` 累加：万一 `long` 也溢出，至少报错而不是给错答案。

---

## 3. 从最笨的解法开始

```
对每个 next = 0 的任务（尾）:
    从尾往回找：在全部行里找「谁的 next 是我」，找到就继续往回找
```

问题：

1. **慢**：每往回一步扫全部行，O(n²)。
2. **漏查环**：环上没有 `next = 0`，从尾出发碰不到。`1,10,0 / 2,10,3 / 3,10,2` 会被当成合法（只报链 1），应为 `Malformed Input`。
3. **漏查分叉**：两个任务都指向我时通常只取第一个，分叉被静默忽略。

---

## 4. 一步一步改进

**第 1 步：解决「慢」**
* 慢在「找编号在哪一行」。先把所有行放进 `HashMap<编号, 行>`，之后查找 O(1)；`putIfAbsent` 返回非 null 说明编号重复 → 报错。建表 O(n)。

**第 2 步：从头往下走，不从尾往回找**
* 往回找需要额外建「谁指向我」的反向表；往下走只需现成的 `next`。
* 先找**头**：把每个非 0 的 `next` 记进集合 `hasPredecessor`，不在集合里的就是头。
* 顺便查两个错误：
  * `next` 指向的编号不在表里 → **悬空引用** → 报错。
  * 加入集合时发现已存在（`Set.add` 返回 false）→ 两个任务指向它，**入度 2** → 报错。
* O(n)。

**第 3 步：走链并统计**
* 对每个头：计数、累加时长、记下尾，走过的编号放进 `visited`。每个元素只走一次（2.5 节第 2 点），总共 O(n)。

**第 4 步：查环**
* 用 2.5 节结论：`visited.size() != byId.size()` → 有环 → 报错。O(1)。

**第 5 步：排序和输出**
* 链数 k ≤ n，排序 O(k log k)。规则：总时长降序，相同时头编号升序（题面没规定时自己选一个 tie-break 并写清楚是好习惯）。

总复杂度 O(n + k log k)，内存 O(n)。

---

## 5. 逐段讲解法

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

* `record` 一行声明三个 `private final` 字段、构造器、读取方法 `id()` 等，以及按字段比较的 `equals`、`hashCode`、`toString`（老写法 40 行）。
* `public Job { ... }` 是**紧凑构造器**（compact constructor）：无参数列表，在字段赋值**之前**运行。校验放这里，非法的 Job 就不可能被创建——**让非法状态无法表示**。
* 单行规则放这里（编号为正、时长非负、不指向自己）；跨行规则（重复、悬空、分叉、环）放 `chains()`。

### 5.2 解析一行

```java
private static final Pattern LINE = Pattern.compile("\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*");
...
var m = LINE.matcher(raw);
if (!m.matches()) throw new MalformedInputException("bad line: " + raw);
```

* 正则：`\s*` 任意空白，`(-?\d+)` 可选负号加数字（括号是捕获，`m.group(1)` 取）。
* `matches()` 要求**整行**匹配；`find()` 只要某段匹配，会把 `1,2,3,4` 误判合法。
* 允许负号：让 `3,-5,0` 由 `Job` 构造器报「时长为负」，比正则报「格式错」信息更准（输出都是 `Malformed Input`）。
* `Integer.parseInt("99999999999")` 超出 int 会抛 `NumberFormatException`，转成同一种 `MalformedInputException`，调用方只处理一种异常。

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

* `var`：按右边的表达式确定类型，只在右边类型一眼可见时用。
* `Set.add` 返回 `boolean`（这次是否真的加进去）：一个调用同时完成「记录」和「查重」。

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

* `while (true)` 不会死循环：只从头出发，2.5 节证明从头出发不会进环（进环意味着某点入度为 2，已在上一段被拒绝）。

### 5.4 排序

```java
out.sort(Comparator.comparingLong(Chain::totalSeconds).reversed().thenComparingInt(Chain::startJob));
```

从左往右读：按 `totalSeconds` 比较 → 反过来（降序）→ 相等时按 `startJob` 升序。`Chain::totalSeconds` 是**方法引用**，等价于 `c -> c.totalSeconds()`。

⚠️ 经典坑：`comparingLong(A).thenComparingInt(B).reversed()` 把**两个**条件都反过来，`reversed()` 的位置很重要。

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

* 内部各层**抛异常**；在 `analyze` 这**一个**边界把异常变成值，之后只处理值。
* `sealed ... permits Ok, Malformed`：只有这两种实现，两个 `case` 就「穷尽」，不需要 `default`。加第三种结果（如 `Partial`）时，所有没处理它的 `switch` 都**编译失败**，编译器帮你找全要改的地方。
* `case Ok(var chains)`：**record 模式**，一步完成「判断类型 + 取字段」。
* `case Malformed _`：`_` 表示不需要里面的字段（Java 21 预览特性）。
* `yield`：在 `switch` 表达式的代码块里返回该分支的值。

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

新写法一行，且表达**意图**：纯数据、不可变、字段相同就相等（`List.of(new Chain(5, 5, 1, 200))` 可直接比较）。

**不该用**：需要可变字段、需要继承别的类（record 隐式继承 `java.lang.Record`，不能再 `extends`）、字段很多且大部分可选。

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

新写法由编译器保证类型判断、取字段和穷尽检查。「封闭类型族 + 按类型分派」叫**代数数据类型**（algebraic data type），是 Java 21 最重要的建模工具，订单簿题用它表示「下单 / 撤单 / 成交」事件。

---

## 7. 追问预演

**问：百万行要多久？瓶颈在哪？**
* 思考：O(n)；常数瓶颈是正则解析和 `Integer` 装箱。
* 答：O(n)，100 万行不到 1 秒。再快：手写逐字符解析代替正则；已知编号范围时用 int 数组代替 `HashMap<Integer, …>`。
* 说出口：「线性的。压常数第一刀是解析，第二刀是去掉装箱。」

**问：文件 10 GB 放不进内存？**
* 思考：时长可流式累加，难的是链结构需要全局信息。
* 答：先只存 `(id, next)`，每行 8 字节，10 亿行仍 8 GB → 按 id 范围分片写磁盘或外部排序。
* 说出口：「先只留结构不留时长；再不行按 id 分片外部处理，最后合并。」

**问：允许一个任务有两个前驱（汇合）怎么办？**
* 答：那不是链而是**有向无环图**（DAG），变成拓扑排序 + 最长路径（关键路径）。用 Kahn 算法：反复取入度为 0 的点。带时间戳的拓扑排序是常见变体。

**问：为什么用异常而不是 `Optional` 或错误码？**
* 答：校验分散在多层，异常让中间层不转发错误，只在 `analyze` 一个边界转成值。异常较贵（要抓栈），但只在出错时抛一次，不在热路径。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 分钟 = `seconds / 60` | 含已算进小时的分钟，7200 秒输出 `02:120:00` | `seconds / 60 % 60` |
| 时长用 `int` 累加 | 两个 20 亿秒任务溢出成负数 | `long` + `Math.addExact` |
| 只从 `next = 0` 的尾往回找 | 独立的环没有尾，查不出来 | 从头往下走 + 比较个数 |
| `comparing(A).thenComparing(B).reversed()` | B 也被反过来 | `comparing(A).reversed().thenComparing(B)` |
| 用 `matcher.find()` 校验整行 | `1,2,3,4` 能 find 到 `1,2,3` | `matcher.matches()` |
| 假设第一行一定是表头直接跳过 | 没有表头时丢第一条数据 | 按 `#` 开头判断 |

---

## 9. 自测题

1. 入度 ≤ 1 的有向图里，可能出现哪两种连通形状？
2. 为什么 `visited.size() != byId.size()` 就能断定有环？
3. 3599 秒、3600 秒、360000 秒分别格式化成什么？
4. 写一个 `Comparator<Chain>`：按 job 数升序，相同按总时长降序。
5. 把 `Outcome` 改成 `sealed interface Outcome permits Ok, Malformed, Empty`，`render` 会怎样？

<details><summary>答案</summary>

1. 从一个头出发的链；一个封闭的环。
2. 从所有头出发每个点最多走一次；没走到的点往回追溯找不到头，只能绕回自己，所以在环上。
3. `00:59:59`、`01:00:00`、`100:00:00`。
4. `Comparator.comparingInt(Chain::count).thenComparing(Comparator.comparingLong(Chain::totalSeconds).reversed())`
5. 编译失败：`switch` 不再穷尽，必须加 `case Empty ...`。这正是 sealed 的价值。

</details>

---

## 延伸阅读

* Sedgewick《算法》第 3.4 节「散列表」。
