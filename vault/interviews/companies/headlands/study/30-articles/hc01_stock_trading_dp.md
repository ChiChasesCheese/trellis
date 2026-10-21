# hc01 · 买卖股票家族（动态规划）—— 讲义

> 读者：会写基本 Java，不需要见过「DP 表」「状态转移方程」。检验标准：合上讲义，自己推出「最多 k 次交易」。

---

## 1. 问题是什么

给一张**价格表**：一只股票连续 n 天的收盘价。规则：

* 任何时候手里**最多一股**；再买必须先卖；
* 一天只能做**一个**动作：买、卖、休息；
* 问**最多能赚多少钱**。

题目一层层加规则（面试官的追问方式）：

| 层 | 规则 | LeetCode |
|---|---|---|
| Part 1 | 只能买一次、卖一次 | 121 |
| Part 2 | 次数不限 | 122 |
| Part 3 | 最多 k 次 | 188（k=2 即 123） |
| Part 4 | 卖出后冷静一天才能再买；或每次卖出扣手续费；再进一步：报出**具体哪天买哪天卖** | 309 · 714 |

### 手算一遍

价格 `[7, 1, 5, 3, 6, 4]`：

* **一次**：第 1 天买（1），第 4 天卖（6），赚 5。
* **不限次数**：第 1 天买 → 第 2 天卖赚 4；第 3 天买 → 第 4 天卖赚 3；合计 7。不「1 买 4 卖」赚 5，因为躲过中间第 2→3 天的下跌能多赚 2。
* 最多 1 次 = 5；最多 2 次 = 7；最多 100 次也是 7（没有更多好机会）。

答案随「允许的次数」变化，这就是第 3 层要处理的。

---

## 2. 前置知识

### 2.1 复杂度

n 是天数。`O(n)` 步数与 n 成正比，`O(n²)` 是每天都和每天比一次。n = 10 万时前者约 10 万步，后者约 100 亿步（几十秒以上）。面试官说「数据很大」，就是 `O(n²)` 过不了。

### 2.2 动态规划（dynamic programming, DP）—— 从与股票无关的例子讲起

**是什么**：**把大问题拆成一串小问题，小问题的答案存起来反复用，不重复算。**

#### 例子：斐波那契

`fib(0) = 0`，`fib(1) = 1`，`fib(n) = fib(n-1) + fib(n-2)`。数列 0, 1, 1, 2, 3, 5, 8, 13, ……

直接抄定义：

```java
static long fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
```

对，但看 `fib(5)` 的调用树：

```
                      fib(5)
                 /              \
            fib(4)              fib(3)
           /      \            /      \
       fib(3)    fib(2)     fib(2)    fib(1)
       /   \     /   \      /   \
   fib(2) fib(1) ...  ...  ...
```

`fib(3)` 算了 2 次，`fib(2)` 算了 3 次……`fib(40)` 约 3.3 亿次调用，`fib(50)` 约 400 亿次。问题在**同一个小问题被反复重算**。

**改进 1（记忆化，memoization）**：算过的存进数组，下次直接用。

```java
static long fib(int n, long[] memo) {
    if (n < 2) return n;
    if (memo[n] != 0) return memo[n];            // 算过了，直接拿
    return memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
}
```

每个 `fib(i)` 只算一次 → `O(n)`。

**改进 2（自底向上的表，tabulation）**：从小到大填表，不用递归：

```java
long[] f = new long[n + 1];
f[1] = 1;
for (int i = 2; i <= n; i++) f[i] = f[i - 1] + f[i - 2];
```

**改进 3（滚动数组，rolling array）**：算 `f[i]` 只需前两个，只留两个变量：

```java
long a = 0, b = 1;                 // a = f[i-2], b = f[i-1]
for (int i = 2; i <= n; i++) { long c = a + b; a = b; b = c; }
```

空间从 `O(n)` 降到 `O(1)`。

DP 的全部「形状」：找出**小问题**（「第 i 项」）→ 写出小问题间的关系 `f[i] = f[i-1] + f[i-2]`，叫**转移**（transition）→ 确定**起点** → 按依赖顺序**从小到大填**并存下 → 答案是某一格 → 新一格只依赖最近几格时旧的可丢（滚动数组）。

斐波那契的关系是白送的；**别的题里「小问题」和「关系」要自己发明。**

#### 术语

* **状态**（state）：描述「现在处于什么局面」的一小撮信息。判断标准：**知道状态就足以决定「接下来能做什么、能得到什么」，不必回头看怎么走到这一步。**
* **转移**：从旧状态到新状态的规则及值的更新。
* **最优子结构**（optimal substructure）：大问题的最优解由小问题的最优解拼成。
* **重叠子问题**（overlapping subproblems）：同一小问题被很多大问题用到，存起来才划算。

#### DP 为什么对：股票的「优势论证」

这是整篇最重要的想法。今天结束时，**为决定明天能做什么，我需要知道什么？**

* 手里有没有股票（有 → 只能卖或休息；没有 → 只能买或休息）；
* （Part 3）已用几次交易额度；
* （Part 4）今天是不是刚卖出（冷却期不能买）。

**不需要**知道哪天买的、买入价是多少——已体现在「手里现金」里。

于是状态是「（有没有股票，已用次数，是否冷却）」这几个**有限**情形，每个状态记一个数：**「到今天结束、处于该状态时手里最多有多少现金」**。

为什么只记「最多」就够？**优势论证**：两种历史今天结束时处于同一状态，现金 100 和 80。未来任何操作序列对两者同样可行（可行性只取决于状态），现金变化量也相同，所以 100 的历史永远多 20，**80 的历史永远不会成为最优，可直接丢掉**。历史数是指数级，状态数是小常数——这就是从指数降到多项式的原因。

> 一句话：**状态 = 能决定未来的最小信息；值 = 到达该状态的最优结果；转移 = 一天天更新。**

### 2.3 状态机（finite state machine）：把「每天做什么」画成图

**是什么**：圈是状态，箭头是「一天里做了某动作后状态怎么变」。

**为什么需要**：DP 难在「状态定义」和「转移写全」。先画图，转移就是**把每条箭头翻译成一行代码**，漏箭头、多箭头一眼可见；面试先在白板上画它，思路显得清楚。

**一次交易（Part 1/2）**——两个状态：

```
              休息                      休息
            ┌──────┐                  ┌──────┐
            ▼      │                  ▼      │
          [ FREE ] ───── 买入 ─────▶ [ HOLD ] 
            ▲                          │
            └─────────── 卖出 ─────────┘
```

* `FREE`：手里**没有**股票（可买）。
* `HOLD`：手里**有**一股（可卖）。
* 每天三种选择：休息（留在原状态）、买（FREE → HOLD，现金减价格）、卖（HOLD → FREE，现金加价格）。

**加冷却（Part 4）**——多一个状态 `COOL`（今天刚卖出，明天只能休息）：

```
            休息                    休息
          ┌──────┐               ┌──────┐
          ▼      │               ▼      │
        [ FREE ] ──── 买入 ───▶ [ HOLD ]
          ▲                        │
          │                       卖出
          │                        ▼
          └──── 休息（被迫）──── [ COOL ]
```

**加「最多 k 次」（Part 3）**：每个状态加下标 j = 「已用几次买入」。图复制成 k+1 层，买入箭头从第 j−1 层指向第 j 层。

**Java**：用 `enum` 表示状态，每个箭头一个方法（第 5 节读它）：

```java
public enum State {
    FREE, HOLD, COOL;
    public State afterRest() { return this == COOL ? FREE : this; }
    public State afterBuy()  { if (this != FREE) throw new IllegalStateException(...); return HOLD; }
    public State afterSell(Rules r) { if (this != HOLD) throw ...; return r.cooldown() ? COOL : FREE; }
}
```

### 2.4 滚动数组与「更新顺序」

DP 表本是「天数 × 状态」的大表；明天只依赖今天，所以只留「今天」一行，每天原地更新。n = 400 万天、k = 100 时完整表 4 亿格装不下，滚动后只有 k+1 格。

**最易出错——更新顺序。**原地更新时，新值可能覆盖后面还需要的旧值：

```java
// 想要：b' = a（用旧的 a），a' = a + 1
a = a + 1;
b = a;      // ❌ 这里的 a 已经是新的了，b 得到的是 a'，不是 a
```

正确做法：**先算依赖旧值的，再算会覆盖旧值的**，或用临时变量暂存旧值。Part 3 里 `hold[j]` 依赖旧的 `free[j-1]`，所以 `j` **从大到小**更新（第 4 节详述）。

### 2.5 回溯（backtracking）：从最优值还原最优方案

DP 只告诉你「最多赚多少」，不告诉「怎么赚的」。还原：正向填表时**每格记「最优值从哪个旧状态来」**（决策记录）；填完从终点**倒着走**，沿决策记录跳回起点，沿途的「买」「卖」箭头就是方案。代价：不能再滚动（要保留每天的决策），空间 O(n · 状态数)；这里每格 2 个比特，不贵。

### 2.6 哨兵值（sentinel）、溢出与「从源头消灭」

* **哨兵值**：有些状态一开始**不可达**（没买过，不可能 HOLD），给它「极小的数」，`max` 自动忽略。代码里 `NEG = Long.MIN_VALUE / 4`：直接用 `Long.MIN_VALUE` 再 `- price` 会**下溢**绕回成巨大正数，反成「最优」；除以 4 留足余量。
* **溢出**：`long` 最大约 9.2 × 10¹⁸。这里入口规定 `0 ≤ price ≤ 2⁴⁰`、`n ≤ 2²²`，则利润 ≤ 2²¹ × 2⁴⁰ = 2⁶¹ < 2⁶³，DP 里**任何中间值都不溢出**，内循环不用写 `Math.addExact`。这叫「从源头消灭」：入口检查一次，比热路径检查百万次便宜，「拒绝」也比「静默回绕」安全。

### 2.7 `enum`、`record`、`sealed` 最小介绍

* `enum`：固定几个取值的类型（`FREE`/`HOLD`/`COOL`），不会被传进「3」，还能带方法。
* `record`：不可变数据类（`Trade(buyDay, sellDay)`），自动生成构造器、访问器、`equals`、`hashCode`、`toString`。
* `sealed` 接口：规定「只有这几种实现」，配合 `switch` 让编译器检查处理全（第 6 节）。

---

## 3. 从最笨的解法开始

### 3.1 Part 1 暴力：试遍所有（买入日，卖出日）

```java
long best = 0;                                  // 0 = 一笔也不做
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)             // 卖出日必须在买入日之后
        best = Math.max(best, prices[j] - prices[i]);
```

对，每一对都试了；约 n²/2 对，`O(n²)`。**慢在哪**：n = 10 万约 50 亿次比较，要几十秒。3 万天暴力 **186 ms**，O(n) 的 `maxProfitOnce` 仅 **0.018 ms**；按 n² 外推，100 万天暴力要 3 分钟以上。

### 3.2 「最多 k 次」暴力更惨

要枚举所有互不重叠的 (买, 卖) 区间集合：n 天选 2k 个分割点，C(n, 2k)，n=1000、k=10 就是天文数字。Part 3 **必须**用 DP；暴力只剩 n ≤ 10，当「标准答案」对拍 DP。

---

## 4. 一步一步改进

### Part 1：从 O(n²) 到 O(n)

**问题**：内层循环为每个卖出日 j 重复回头找最好的买入日 i。**想法**：固定 j，最好的买入日是 j 之前**价格最低**的那天（`prices[j] - prices[i]` 在 `prices[i]` 最小时最大），而「j 之前的最低价」随 j 后移边走边更新。

```java
long minSoFar = Long.MAX_VALUE, best = 0;
for (long p : prices) {
    if (p < minSoFar) minSoFar = p;         // 今天比以前所有天都便宜：更新最低价
    else best = Math.max(best, p - minSoFar); // 否则假设今天卖
}
```

用 `[7, 1, 5, 3, 6, 4]` 手算：

| 天 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 价格 | 7 | 1 | 5 | 3 | 6 | 4 |
| minSoFar | 7 | 1 | 1 | 1 | 1 | 1 |
| best | 0 | 0 | 4 | 4 | 5 | 5 |

复杂度：`O(n)` 时间，`O(1)` 空间。

**换个角度——这是两个状态的 DP**。`hold` = 持股时的最大现金（为负），`free` = 已卖出后的最大现金。每天：`hold = max(hold, 0 - p)`；`free = max(free, hold + p)`。因 `hold = -minSoFar`，所以 `free = max(free, p - minSoFar)`，与上面一致。Part 2、3、4 就是把它逐步扩展。

> 误区：不能写成「全局最大 − 全局最小」。`[10, 9, 8, 1]` 最小值在最大值**后面**，答案是 0 不是 9。

### Part 2：次数不限

**问题**：Part 1 买入现金是 0（只能买一次）。次数不限时，买之前的现金可能是前几笔赚的。**想法**：把「0」换成「现在的 `free`」：

```
hold' = max(hold,  free - p)      // 休息 或 今天买（用 free 里的全部现金）
free' = max(free,  hold + p)      // 休息 或 今天卖
```

（`'` 表示今天结束时的值，右边是昨天结束时的值。）

这是 2.3 节第一张图的逐箭头翻译：休息 → 两个 `max` 的第一项；买入 → `free - p` 进 `hold`；卖出 → `hold + p` 进 `free`。

手算 `[7, 1, 5, 3, 6, 4]`（初始 `free = 0`，`hold = −∞`），每天结束时：

| 天 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| free | 0 | 0 | 4 | 4 | 7 | 7 |
| hold | −7 | −1 | −1 | 1 | 1 | 3 |

第 2 天卖：−1 + 5 = 4；第 3 天用赚到的 4 买入：4 − 3 = 1；第 4 天卖：1 + 6 = 7。答案 `free = 7` ✓。

**更简单的写法**：化简后答案等于「所有『今天比昨天贵』的差之和」：

```java
for (int i = 1; i < n; i++) if (prices[i] > prices[i-1]) sum += prices[i] - prices[i-1];
```

**为什么**：方案 = 每个相邻日对 (i−1, i) 持有或不持有，持有的赚 `prices[i] − prices[i−1]`（可能为负）。**上界**：所赚不超过「所有正差之和」；**可达**：只持有正差日对即可（连续正差合并成一笔，买最低点卖最高点）。

这个贪心（greedy）只在「次数不限、无冷却、无手续费」时成立，有任何限制必须回到状态机。**面试两种都讲**：先状态机（通用），再说可化简（要能证明）。

复杂度：`O(n)`，`O(1)` 空间。

### Part 3：最多 k 次

**问题**：买入次数受限，状态必须记「已用几次」。**想法**：给 `free`、`hold` 各加下标 j（0..k）：

* `free[j]`：手里没股票、**最多**做过 j 笔交易时的最大现金；
* `hold[j]`：手里有一股、这一股的买入算在第 j 笔内（买它前至多做过 j−1 笔）时的最大现金。

转移（每个 j ≥ 1，每天价格 p）：

```
hold'[j] = max(hold[j],  free[j-1] - p)    // 休息；或今天买（买之前只能做过 j-1 笔）
free'[j] = max(free[j],  hold[j]   + p)    // 休息；或今天卖
```

初始：`free[j] = 0`（「最多」j 笔，0 笔也算）；`hold[j] = −∞`。答案 `free[k]`。用「最多」而非「恰好」：`free[k]` 直接是答案，不必对 j 取最大，初值全 0。

手算 `k = 2`，`prices = [3, 3, 5, 0, 0, 3, 1, 4]`（LC 123，答案 6）。`hold[0]` 永远是 −∞，省略：

| 天 | 价格 | free[1], free[2] | hold[1], hold[2] |
|---|---|---|---|
| 0 | 3 | 0, 0 | −3, −3 |
| 2 | 5 | 2, 2 | −3, −3 |
| 3 | 0 | 2, 2 | 0, 2 |
| 5 | 3 | 3, 5 | 0, 2 |
| 7 | 4 | 4, 6 | 0, 2 |

（第 1、4、6 天与前一行相同。）验证：第 2 天 `free[1] = max(0, −3 + 5) = 2`（第 0 天买、第 2 天卖）；第 3 天 `hold[2] = max(−3, free[1] − 0) = 2`（已赚 2，再以 0 价买第二笔）；第 7 天 `free[2] = max(5, 2 + 4) = 6` ✓。

**更新顺序（接 2.4 节）**：第 d 天新 `hold[j]` 需要「昨天的 `free[j-1]`」，所以：

```java
for (int j = k; j >= 1; j--) {                              // j 从大到小
    free[j] = Math.max(free[j], hold[j] + p);               // 先用「昨天的 hold[j]」
    hold[j] = Math.max(hold[j], free[j - 1] - p);           // free[j-1] 还没被今天覆盖：仍是昨天的
}
```

若 j 从小到大，处理 j 时 `free[j-1]` 已被今天更新，等于「同一天先卖再用卖出的钱买入」，违反「一天一个动作」。
**纯 Part 3 里两种顺序答案碰巧一样**（对 n ≤ 5、价格 0..3 的全部输入验证过）：同天同价「卖了又买」现金不变。但这依赖「同价、无手续费、无冷却」；加冷却后读「今天已更新的 free」去买就错（见 Part 4）。**习惯：每个转移只用昨天的值——j 倒序，或先存旧值。**

**k 很大**：`new long[k + 1]` 在 `k = Integer.MAX_VALUE` 时 `OutOfMemoryError`。每笔交易至少占两天，**最多 n/2 笔**；`k ≥ n/2` 时限制等于没有 → 用 Part 2。

```java
if (k >= n / 2) return maxProfitUnlimited(prices);
```

复杂度：时间 `O(n · min(k, n/2))`，空间 `O(min(k, n/2))`。n = 20 万、k = 50 约 3.6 ms（预热后）。

### Part 4：冷却、手续费、还原交易

#### 手续费（LC 714）：只改一处

卖出箭头 `hold + p` 变成 `hold + p − fee`，状态机不变；「买了又立刻卖」亏钱，DP 自动不做。

#### 冷却（LC 309）：多一个状态

卖出后下一天不能买。「今天是不是刚卖出」影响明天能否买，按 2.2 的标准它必须是状态。新增 `COOL`（2.3 节第二张图）：

```
hold'[j] = max(hold[j],  free[j-1] - p)    // 买入只能从 FREE 来（不能从 COOL 买！）
cool'[j] = hold[j] + p - fee                // 今天卖出 → 进入 COOL
free'[j] = max(free[j], cool[j])            // 休息；或冷却结束（昨天卖的，今天自动变回 FREE）
```

无冷却时卖出直接回 FREE：`free'[j] = max(free[j], hold[j] + p - fee)`。

手算 LC 309：`prices = [1, 2, 3, 0, 2]`，不限次数（j 压成 1 格）。答案 `max(free, cool)`：

| 天 | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 价格 | 1 | 2 | 3 | 0 | 2 |
| free | 0 | 0 | 1 | 2 | 2 |
| hold | −1 | −1 | −1 | 1 | 1 |
| cool | −∞ | 1 | 2 | −1 | 3 |

第 1 天 cool = 昨天 hold(−1) + 2 = 1（卖出进入冷却）；第 2 天 free = max(0, 昨天 cool=1) = 1（冷却结束），买入只看**昨天**的 free = 0；第 3 天 hold = max(−1, 昨天 free(1) − 0) = 1；第 4 天 cool = 昨天 hold(1) + 2 = 3。最终 `max(2, 3) = 3` ✓。

错把买入写成 `hold' = max(hold, free' - p)`（用今天**已更新**的 free'，含「昨天卖出、今天冷却结束」的钱），同一份数据得到 **4**：第 2 天卖出、第 3 天立刻以 0 买入，跳过了冷却。这是冷却题最常见的错，样例 `[1,2,3,0,2]` 就能抓到。

#### 还原交易：回溯（接 2.5 节）

现在只有一个数字，要报买卖日必须记下每格怎么来的。每个 (天, j) 格记 2 个比特：
* bit0：`hold` 这格是不是「今天买入」得来（`free[j-1] − p > hold[j]` 严格成立）；
* bit1：`free` 这格是不是不是「休息」得来（来自卖出，或来自冷却结束）。

**平局选「休息」**（严格 `>`）：不产生净利润为 0 的废交易。从终点状态（`FREE` 或 `COOL`，取现金多的）倒着走，每天看当前状态对应的比特：

* `COOL`：这天卖出 → 记卖出日，状态变 `HOLD`；
* `HOLD`：bit0 = 1 → 这天买入 → 配对记 `(买入日, 刚记的卖出日)`，状态变 `FREE`（j 减 1）；bit0 = 0 → 昨天也持有，原地不动；
* `FREE`：bit1 = 1 → 有冷却时是「昨天卖，今天冷却结束」→ 状态变 `COOL`；无冷却时是「今天卖出」→ 记卖出日，状态变 `HOLD`；bit1 = 0 → 休息，原地不动。

`[1, 2, 3, 0, 2]`（冷却，不限次数）正向每天的 bits（bit1 在左）依次：`01`、`00`、`10`、`11`、`00`。倒着走：

```
终点：cool=3 > free=2  →  状态 COOL
第 4 天，COOL        →  这天卖出            记 sell=4，状态 → HOLD
第 3 天，HOLD, bit0=1 →  这天买入            记 Trade(3,4)，状态 → FREE
第 2 天，FREE, bit1=1 →  冷却在这天结束      状态 → COOL
第 1 天，COOL        →  这天卖出            记 sell=1，状态 → HOLD
第 0 天，HOLD, bit0=1 →  这天买入            记 Trade(0,1)，状态 → FREE   ← 回到起点 FREE，一致
```

倒着得到 `[Trade(3,4), Trade(0,1)]`，反转为 `[Trade(0,1), Trade(3,4)]` ✓。

**回溯自检**：走到起点状态必须是 `FREE`，否则决策记录写错了（代码用 `AssertionError`）。

**更强的自检——`replay`**：再写一个**独立检查器**把方案逐天回放（有动作按动作，没动作休息，非法就报错），最后算利润；`plan(...).profit()` 必须等于 `replay(...)`。「验证」与「计算」分开，两者的错误很难恰好抵消。

**复杂度**：`maxProfit` 时间 `O(n·min(k, n/2))`，空间 `O(min(k, n/2))`；`plan` 多 `O(n·min(k, n/2))` 字节决策记录，超过 2²⁸ 字节就拒绝。

---

## 5. 逐段讲解法

### 5.1 数据类型

```java
public record Trade(int buyDay, int sellDay) {
    public Trade {
        if (buyDay < 0 || sellDay <= buyDay)
            throw new IllegalArgumentException("need 0 <= buyDay < sellDay: " + buyDay + "," + sellDay);
    }
}
public record Plan(long profit, List<Trade> trades) {
    public Plan { trades = List.copyOf(trades); }
}
public record Rules(int maxTransactions, long fee, boolean cooldown) { ... }
```

* `Trade` 紧凑构造器保证「买入日 < 卖出日」：非法 `Trade` 构造不出来。
* `Plan` 紧凑构造器把 `trades` 赋成 `List.copyOf(...)`（**不可变拷贝**），外部改不了，`Plan` 才真不可变。
* `Rules` 把 k / fee / cooldown 打包成一个值。121 = `atMost(1)`，122 = `unlimited()`，188 = `atMost(k)`，309 = `unlimited().withCooldown(true)`，714 = `unlimited().withFee(f)`——**六道题是同一函数的六组参数**。

### 5.2 状态机 `State`

```java
public enum State {
    FREE, HOLD, COOL;
    public State afterRest() { return this == COOL ? FREE : this; }
    public State afterBuy() {
        if (this != FREE) throw new IllegalStateException("cannot buy while " + this);
        return HOLD;
    }
    public State afterSell(Rules rules) {
        if (this != HOLD) throw new IllegalStateException("cannot sell while " + this);
        return rules.cooldown() ? COOL : FREE;
    }
}
```

三个方法 = 三类箭头；非法箭头（如在 `COOL` 买入）抛 `IllegalStateException`。它**不参与** DP 计算（转移手写在数组更新里），只用于 `replay`：用同一规则的另一种表达独立检查方案。

### 5.3 输入校验与 Part 1/2

```java
private static void check(long[] prices) {
    Objects.requireNonNull(prices, "prices");
    if (prices.length > MAX_DAYS) throw new IllegalArgumentException("too many days: " + prices.length);
    for (int i = 0; i < prices.length; i++)
        if (prices[i] < 0 || prices[i] > MAX_PRICE) throw new IllegalArgumentException(...);
}
```

每个公共入口第一行调用 `check`（`Objects.requireNonNull` 抛带信息的 NPE，好定位）。`maxProfitBrute`、`maxProfitOnce`、`maxProfitUnlimited` 就是第 3、4 节的代码。

### 5.4 Part 3：`maxProfitAtMost`

```java
if (k == 0 || n < 2) return 0;
if (k >= n / 2) return maxProfitUnlimited(prices);
long[] free = new long[k + 1];
long[] hold = new long[k + 1];
Arrays.fill(hold, NEG);
for (long p : prices) {
    for (int j = k; j >= 1; j--) {
        free[j] = Math.max(free[j], hold[j] + p);
        hold[j] = Math.max(hold[j], free[j - 1] - p);
    }
}
return free[k];
```

* `new long[k + 1]` 默认全 0 = `free` 初值。
* `hold[j]` 可能是 `NEG`，加不超过 2⁴⁰ 的 p 仍极负，`max` 忽略且不溢出。
* 内层循环无分配，20 万天 × 50 只要几毫秒。

### 5.5 Part 4 的引擎 `run`

```java
private static Solved run(Rules rules, long[] prices, byte[] how) {
    int n = prices.length;
    boolean unbounded = rules.maxTransactions() >= n / 2;
    int bound = unbounded ? 0 : rules.maxTransactions(); // 无限次时不需要「交易次数」这一维，压成 1 格
    int w = bound + 1;
    long[] free = new long[w], hold = new long[w], cool = new long[w];
    Arrays.fill(hold, NEG);
    Arrays.fill(cool, NEG);
```

* `unbounded`：次数不限（或大到等于不限）时 j 这一维无意义，压成 1 格。此时买入的钱从 `free[j-1]` 变成同格 `free[j]`，故 `src = unbounded ? j : j - 1`。
* 三个数组 `free` / `hold` / `cool` 对应三个状态。

```java
    for (int i = 1; i <= n; i++) {
        long p = prices[i - 1];
        for (int j = bound; j >= 0; j--) {
            int src = unbounded ? j : j - 1;
            long oldHold = hold[j], oldFree = free[j], oldCool = cool[j];
            long buy = src >= 0 ? free[src] - p : NEG;
            long sell = oldHold + p - fee;
```

* 开头把「旧值」存进局部变量（`oldHold` 等），后面无论先写谁，别的转移用的都是昨天的值；`src = j-1` 时 j 递减循环里 `free[src]` 仍是昨天的（2.4 节）。
* `buy`：昨天 FREE 的现金 − 今天价格。`src < 0` 表示「第 0 笔不能买」，给 `NEG`。
* `sell`：昨天 HOLD 的现金 + 价格 − 手续费。

```java
            int bits = 0;
            if (buy > oldHold) { hold[j] = buy; bits |= 1; } else hold[j] = oldHold;
            if (rules.cooldown()) {
                cool[j] = sell;
                if (oldCool > oldFree) { free[j] = oldCool; bits |= 2; } else free[j] = oldFree;
            } else {
                if (sell > oldFree) { free[j] = sell; bits |= 2; } else free[j] = oldFree;
            }
            if (how != null) how[i * w + j] = (byte) bits;
```

* 四个 `if` 是状态机四类带值的箭头：「买」「休息(HOLD)」「卖」「冷却结束 / 休息(FREE)」。严格 `>` = 平局选休息。
* `how` 为 `null`（只要利润）时完全不记录，所以 `maxProfit` 和 `plan` 共用同一引擎，答案必然一致。
* `cool[j] = sell` 而非 `max(cool[j], sell)`：`COOL` 意为「**今天刚**卖出」，昨天的 COOL 今天已变 FREE。

```java
    if (rules.cooldown() && cool[bound] > free[bound]) return new Solved(cool[bound], State.COOL);
    return new Solved(free[bound], State.FREE);
}
```

终点：最后一天结束时，没股票的两种情形取现金多的（不会停在 `HOLD`：没卖出的股票不算利润）。

### 5.6 `plan`：回溯

```java
var reversed = new ArrayList<Trade>();
State state = solved.end();
int j = bound;
int pendingSell = -1;
for (int i = n; i >= 1; i--) {
    int bits = how[i * w + j];
    int day = i - 1;
    switch (state) {
        case HOLD -> { if ((bits & 1) != 0) { reversed.add(new Trade(day, pendingSell)); pendingSell = -1; state = State.FREE; if (!unbounded) j--; } }
        case COOL -> { pendingSell = day; state = State.HOLD; }
        case FREE -> { if ((bits & 2) != 0) { if (rules.cooldown()) state = State.COOL; else { pendingSell = day; state = State.HOLD; } } }
    }
}
```

与第 4 节倒走一一对应。读 `bits` 用的是**当前的 j**，j 在买入分支里才减 1。最后：

```java
for (Trade t : reversed.reversed()) { ... if (net > 0) trades.add(t) ... }
if (sum != solved.profit()) throw new AssertionError(...);
```

`reversed.reversed()`：第一个是变量名（倒着收集的交易），第二个是 Java 21 的 `List.reversed()`。最后一行把各笔净利润之和与 DP 的数字对账，不等就 `AssertionError`。

### 5.7 `replay`

```java
state = switch (moves.get(day)) {
    case null -> state.afterRest();
    case Buy(var d) -> { cash = Math.subtractExact(cash, prices[d]); yield state.afterBuy(); }
    case Sell(var d) -> { cash = Math.addExact(cash, prices[d] - rules.fee()); yield state.afterSell(rules); }
};
```

* `moves` 是 `TreeMap<Integer, Move>`：天 → 动作。`get(day)` 无动作返回 `null`（休息）。
* `case null`：Java 21 的 `switch` 可显式处理 `null`；以前会直接 `NullPointerException`。
* `case Buy(var d)`：record 模式，同时判断类型并取字段。
* 状态机方法抛的 `IllegalStateException` 在外层被包成 `IllegalArgumentException("illegal plan: ...")`——对调用者，非法方案是参数错误。

---

## 6. Java 21 特性小课

### 6.1 `enum` + `switch` 表达式

旧写法（Java 7）：

```java
switch (state) {
    case FREE: ... break;     // 忘了 break 就会「掉」到下一个 case
    case HOLD: ... break;
}
```

新写法：箭头 `->`、无 fallthrough；`switch` 可**直接产生值**；对 enum 的 `switch` 表达式要求覆盖所有取值，漏一个**编译失败**；块分支用 `yield 值` 返回。

### 6.2 `sealed` 接口 + record + 模式匹配 `switch` + record 模式

```java
public sealed interface Move permits Buy, Sell {}
public record Buy(int day) implements Move {}
public record Sell(int day) implements Move {}
```

`sealed` 告诉编译器 `Move` 只有 `Buy` 和 `Sell`，`switch` 不需要 `default`。以后新增 `Rest`，所有没处理它的 `switch` 立刻编译失败。`case null ->` 让 `switch` 不必先 `if (x == null)`。

**不该用**：取值只有几个、不带各自数据时用 `enum` 就够（如 `State`）；`sealed` + `record` 适合「每种情形带不同数据」。

### 6.3 Sequenced Collections

旧写法：倒着遍历 `List` 要么 `Collections.reverse(list)`（改原列表），要么倒序下标循环。

```java
for (Trade t : reversed.reversed()) { ... }
```

Java 21 的 `List.reversed()` 返回**倒序视图**（不拷贝、不改原列表）。同批还有 `getFirst()` / `getLast()` / `addFirst()`……定义在 `SequencedCollection` 接口，`List`、`Deque`、`LinkedHashSet` 都实现。`list.getLast()` 取代 `list.get(list.size() - 1)`，空列表抛 `NoSuchElementException`。

### 6.4 `record` 紧凑构造器与「不可变拷贝」

`Plan` 里：

```java
public Plan { trades = List.copyOf(trades); }
```

紧凑构造器可在字段赋值**之前**重新赋值参数。这里换成不可变拷贝，外部再改原列表也不影响 `Plan`——**防御性拷贝**（defensive copy）。没有它，字段虽 `final`，里面的列表仍可被外部修改，「不可变」是假的。

### 6.5 数学小工具与 `var`

`Math.addExact` / `subtractExact`：溢出抛 `ArithmeticException`，不静默绕回；`replay` 用它们，因其输入（任意 `Trade` 列表）不如 DP 内循环可控。`var` 只在右边一眼看出类型时用。

---

## 7. 追问预演

**问：你的 DP 状态是什么？为什么这样定义就够？**
* 答要点：状态 = 足以决定未来的信息（有没有股票、已用几笔、是否冷却）；每个状态记最大现金；优势论证——同状态下现金多的历史永远不劣。
* 说出口：「我把每天结束时的情形分成持有、空仓、冷却三类，乘上已用笔数。每个状态只记最大现金，因为未来的可行操作只取决于状态，现金多的历史总是更好。」

**问：k 很大怎么办？**
* 答要点：n 天最多完成 n/2 笔，`k ≥ n/2` 退化为不限次数，O(n)。
* 说出口：「交易至少占两天，有效的 k 不超过 n/2；超过就当不限次数。」

**问：能比 O(nk) 更快吗？**
* 答要点：把价格拆成「波谷-波峰」对，用堆或分治做到 O(n log n)（利用边际收益递减，即凹性）。知道方向即可。
* 说出口：「可以利用边际收益递减，用优先队列合并相邻涨跌段，O(n log n)；k 小时 O(nk) 已够。」

**问：怎么还原具体买卖日？**
* 答要点：每格记决策（2 比特），倒着走；空间 O(n·k)；平局选休息；走到起点必须回到初始状态自检。
* 说出口：「记下每格最优值来自休息还是买/卖，从终点倒着走。空间紧可用分治（Hirschberg 思路）降到 O(k)，但代码复杂得多。」

**问：怎么保证答案对？**
* 答要点：n ≤ 10 的暴力枚举所有合法交易序列，与 DP 在几千组随机小数据对拍；再用独立 `replay` 验证 `plan`。
* 说出口：「我用完全不依赖状态机的暴力枚举对拍，还原的方案再用另一套检查器回放。」

**问：价格是 `long`，利润会溢出吗？**
* 答要点：先问约束；没约束用 `Math.addExact` 或 `BigInteger`；有约束就由界限（天数/2 × 最大价格）证明不溢出，入口拒绝越界输入。
* 说出口：「入口限制价格和天数，保证最大利润小于 2⁶³，内循环不用检查溢出。」

**问：流式输入、存不下全部价格？**
* 答要点：只要利润——滚动数组本就是一遍扫描，O(k) 内存；要还原则需保存决策，内存增长。
* 说出口：「只要数字的话我的实现本来就是在线的。」

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 全局最大 − 全局最小（Part 1） | 最小值可能在最大值之后，`[10, 9, 8, 1]` 答案是 0 | 维护「到目前为止的最低价」 |
| Part 3 里 `j` 从小到大，以为「反正答案一样」 | 纯 Part 3 碰巧一样，加冷却 / 手续费就错 | 只用昨天的值：`j` 从大到小，或先存旧值 |
| `new long[k + 1]` 不判断 k | `k = Integer.MAX_VALUE` 直接 `OutOfMemoryError` | `k ≥ n/2` 时退化为不限次数 |
| 用 `Long.MIN_VALUE` 当「不可达」再 `- price` | 下溢绕回成巨大正数，被 `max` 当最优 | `NEG = Long.MIN_VALUE / 4` |
| 冷却用「今天已更新的 free」买入 | 等于冷却期买入：`[1,2,3,0,2]` 得 4 而非 3 | 买入只用「昨天结束时」的 FREE |
| 手续费买入、卖出各扣一次 | 题面每笔交易扣一次（LC 714） | 只在卖出（或只在买入）扣 |
| 回溯时先把 j 减了再读 | 读到别的格子的决策 | 先用当前 j 读 `bits`，买入分支再 `j--` |
| DP 数字直接信，不对拍 | bug 往往只在特定输入暴露 | 暴力对拍 + 独立 `replay` |
| 平局也做交易 | 出现净利润为 0 的废交易 | 严格 `>`，平局选休息 |

---

## 9. 自测题

1. DP 的「状态」要满足什么条件？为什么「只记最优值」不会丢掉更好的解？
2. 画出「最多 k 次、有冷却」的状态机（至少 j=0 和 j=1 两层），在每条箭头上标出现金怎么变。
3. `prices = [2, 1, 4, 5, 2, 9, 7]`，`k = 2`，手算 `free[2]` 的最终值，说出是哪两笔交易。
4. 把 `maxProfitAtMost` 内层循环改成 `j` 从小到大，纯 Part 3 的答案会变吗？为什么？同时加「冷却」会怎样？
5. 不改动 `run`，用 `Rules` 解决「每笔交易买入时扣手续费，而非卖出时」。需要改什么？结果有区别吗？
6. （挑战）只要利润数字，不限次数 + 冷却，空间能降到 O(1) 吗？写出三个变量的更新式。

<details><summary>答案</summary>

1. 知道状态就足以决定接下来能做什么、每个动作的现金变化，与「怎么到达」无关。同一状态的两个历史，现金多的永远不差（未来对两者一样，起点差一个常数），少的可丢。
2. 每层有 FREE、HOLD、COOL 三个圈。FREE→HOLD（买入，现金 −p，j 层 +1）；HOLD→COOL（卖出，现金 +p −fee）；COOL→FREE（被迫休息，现金不变）；FREE→FREE、HOLD→HOLD（休息，现金不变）。买入箭头从 j=0 的 FREE 指向 j=1 的 HOLD。
3. 价格 1 买、5 卖（赚 4）；价格 2 买、9 卖（赚 7）；合计 11，`free[2] = 11`。（1→9 一笔赚 8，不如两笔。）
4. 纯 Part 3 不变：`hold[j]` 用到今天已更新的 `free[j-1]`，相当于同天「卖出再买入」，同价无手续费，现金不变。
   加冷却会变：`hold` 读到含「昨天卖出、今天冷却结束」的钱，等于冷却期内买入（`[1,2,3,0,2]` 得 4 而非 3）。结论：每个转移只用昨天的值。
5. `sell = oldHold + p - fee` 改成 `oldHold + p`，`buy = free[src] - p` 改成 `free[src] - p - fee`。结果相同：每笔**完成**的交易恰好扣一次，最终答案只看 `free` / `cool`（仍持有的不计入）；`plan` 的净利润公式也不变。
6. `free' = max(free, cool)`；`hold' = max(hold, free - p)`；`cool' = hold + p`（都用昨天的值，先存旧值再更新）。答案 `max(free, cool)`。这就是 LC 309 的标准 O(1) 空间解。

</details>

---

## 延伸阅读

* CLRS《算法导论》「动态规划」一章（钢条切割）。
