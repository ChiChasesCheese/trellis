# hc01 · 买卖股票家族（动态规划）—— 讲义

> 题面：`loop/rounds/01_video/hc01_stock_trading_dp/problem.md` · 速查：同目录 `REPORT.md` · 代码：同目录 `reference/StockTrading.java`
> 写法说明见 `study/TEXTBOOK.md`；样板见 `oa01_job_chain.md`。
> 这篇讲义有一个特别的任务：**从零讲清楚动态规划**。Chi 说基础弱，所以这里不假设你见过「DP 表」「状态转移方程」这些词。
> 读完的检验标准：合上讲义，自己把 LeetCode 188（最多 k 次交易）重新推出来。

---

## 1. 这道题在问什么

你手里有一张**价格表**：一只股票连续 n 天的收盘价。你想靠「低买高卖」赚钱。规则：

* 任何时候手里**最多一股**；要再买，必须先卖掉手里的那一股；
* 一天只能做**一个**动作：买、卖、什么都不做（休息）；
* 问：**最多能赚多少钱**。

题目会一层一层加规则（这正是面试官「追问」的方式）：

| 层 | 规则 | LeetCode |
|---|---|---|
| Part 1 | 整段时间只能买一次、卖一次 | 121 |
| Part 2 | 买卖次数不限 | 122 |
| Part 3 | 最多买 k 次 | 188（k=2 就是 123） |
| Part 4 | 卖出后要「冷静」一天才能再买；或者每次卖出扣手续费；再进一步：把**具体哪天买哪天卖**报出来 | 309 · 714 |

### 手算一遍

价格表 `[7, 1, 5, 3, 6, 4]`（第 0 天价格 7，第 1 天价格 1，……）。

* **只能一次**（Part 1）：第 1 天买（价格 1），第 4 天卖（价格 6），赚 5。再没有更好的一对了。
* **不限次数**（Part 2）：第 1 天买（1）→ 第 2 天卖（5）赚 4；第 3 天买（3）→ 第 4 天卖（6）赚 3；合计 7。
  为什么不「第 1 天买、第 4 天卖」一次赚 5？因为中间第 2 天涨到 5、第 3 天掉到 3，把「掉下来」的那一段躲过去，能多赚 2。
* **最多 1 次** = 5；**最多 2 次** = 7；**最多 100 次** 也只是 7（天数就这么多，没有更多的好机会）。

所以答案随「允许的次数」变化。这就是第 3 层要处理的东西。

---

## 2. 前置知识

### 2.1 复杂度：这题为什么不能暴力

沿用 `oa01_job_chain.md` 2.3 节的约定：n 是天数，`O(n)` 表示步数和 n 成正比，`O(n²)` 表示每一天都和每一天比一次。
n = 10 万时 `O(n)` 约 10 万步，`O(n²)` 约 100 亿步（几十秒以上）。面试官说「数据很大」，就是在告诉你 `O(n²)` 过不了。

### 2.2 动态规划（dynamic programming, DP）—— 从一个和股票无关的例子讲起

#### 2.2.1 是什么

动态规划是一种解题套路：**把大问题拆成一串小问题，小问题的答案存起来、反复用，不重复算。**

先用一个最小的例子体会「为什么需要它」。

#### 2.2.2 例子：斐波那契数列

定义：`fib(0) = 0`，`fib(1) = 1`，之后 `fib(n) = fib(n-1) + fib(n-2)`。数列是 0, 1, 1, 2, 3, 5, 8, 13, ……

直接把定义抄成代码：

```java
static long fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
```

对不对？对。快不快？看 `fib(5)` 的调用树：

```
                      fib(5)
                 /              \
            fib(4)              fib(3)
           /      \            /      \
       fib(3)    fib(2)     fib(2)    fib(1)
       /   \     /   \      /   \
   fib(2) fib(1) ...  ...  ...
```

`fib(3)` 被算了 2 次，`fib(2)` 被算了 3 次……规模一大就爆炸：`fib(40)` 一共要调用函数约 3.3 亿次，`fib(50)` 约 400 亿次。
问题不在「难」，而在**同一个小问题被反复重新算**。

**改进 1（记忆化，memoization）**：算过的存进一个数组，下次直接用。

```java
static long fib(int n, long[] memo) {
    if (n < 2) return n;
    if (memo[n] != 0) return memo[n];            // 算过了，直接拿
    return memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
}
```

每个 `fib(i)` 只算一次，总共 n 次 → `O(n)`。

**改进 2（自底向上的表，tabulation）**：干脆从小到大一个个填表，不用递归：

```java
long[] f = new long[n + 1];
f[1] = 1;
for (int i = 2; i <= n; i++) f[i] = f[i - 1] + f[i - 2];
```

**改进 3（滚动数组，rolling array）**：算 `f[i]` 只需要前两个，更早的没用了。那就只留两个变量：

```java
long a = 0, b = 1;                 // a = f[i-2], b = f[i-1]
for (int i = 2; i <= n; i++) { long c = a + b; a = b; b = c; }
```

空间从 `O(n)` 降到 `O(1)`。

这三步合起来就是动态规划的全部「形状」：

1. 找出**小问题**是什么（这里：「第 i 项是多少」）；
2. 写出**小问题之间的关系**（这里：`f[i] = f[i-1] + f[i-2]`），叫**转移**（transition）；
3. 确定**起点**（`f[0]`、`f[1]`）；
4. 按依赖顺序**从小到大填**，存下来；
5. 答案是表里的某一格（这里 `f[n]`）；
6. 如果新的一格只依赖最近几格，旧的可以丢（滚动数组）。

斐波那契的关系是白送的。**真正难的是：别的题里，「小问题」和「关系」要你自己发明。**

#### 2.2.3 术语：状态、转移、最优子结构

* **状态**（state）：描述「现在处于什么局面」的一小撮信息。判断标准——**知道了状态，就足够决定「接下来能做什么、能得到什么」，不需要再回头看是怎么走到这一步的。**
  斐波那契里，状态就是「现在算到第几项」。
* **转移**（transition）：从一个（或几个）旧状态走到新状态的规则，以及值怎么更新。
* **最优子结构**（optimal substructure）：大问题的最优解，是由小问题的最优解拼出来的。对我们这题的具体含义见 2.2.4。
* **重叠子问题**（overlapping subproblems）：同一个小问题会被很多大问题用到，所以存起来才划算。

#### 2.2.4 DP 为什么是对的：以股票为例的「优势论证」

这是整篇讲义最重要的一个想法，请慢慢读。

我们要给股票题定义状态。想一想：今天结束时，**为了决定明天能做什么，我需要知道什么？**

* 手里有没有股票（有 → 明天只能卖或休息；没有 → 明天只能买或休息）；
* （Part 3）已经用掉几次交易额度（决定还能不能再买）；
* （Part 4）今天是不是刚卖出（冷却期不能买）。

**我不需要知道**：是哪天买的、买入价是多少之外的任何历史细节——买入价已经体现在「我手里现金是多少」里了。

于是我们把状态定成「（有没有股票，已用次数，是否冷却）」这样几个**有限的**情形，并对每个状态记一个数：**「到今天结束，处于这个状态时，手里最多有多少现金」**。

为什么只记「最多」就够？**优势论证**：假设有两种不同的历史，都让你今天结束时处于同一个状态，但一个现金 100，一个现金 80。
未来的任何操作序列，对两种历史都同样可行（因为可行性只取决于状态）；而且每个操作序列带来的现金变化量相同。
所以现金 100 的那个历史，不管未来怎么走，都比现金 80 的多 20。**现金 80 的历史永远没有机会成为最优，可以直接丢掉。**

这就是为什么 DP 只记每个状态下的**最优值**，而不记全部历史——而历史的数量是指数级的，状态的数量是很小的常数。这是从指数降到多项式的原因。

> 一句话版本：**状态 = 能决定未来的最小信息；值 = 到达这个状态的最优结果；转移 = 一天一天地更新。**

### 2.3 状态机（finite state machine）：把「每天做什么」画成图

**是什么**：一张图，圈代表状态，箭头代表「一天里做了某个动作后，状态怎么变」。

**为什么需要它**：DP 的难点是「状态定义」和「转移写全」。先画图，转移就是**把每一条箭头翻译成一行代码**；漏箭头、多箭头一眼就能看出来。面试里先在白板上画这张图，面试官会觉得你思路很清楚。

**一次交易（Part 1/2 的情形）**——只有两个状态：

```
              休息                      休息
            ┌──────┐                  ┌──────┐
            ▼      │                  ▼      │
          [ FREE ] ───── 买入 ─────▶ [ HOLD ] 
            ▲                          │
            └─────────── 卖出 ─────────┘
```

* `FREE`：手里**没有**股票（可以买）。
* `HOLD`：手里**有**一股（可以卖）。
* 每天有三种选择：休息（留在原状态）、买（FREE → HOLD，现金减去价格）、卖（HOLD → FREE，现金加上价格）。

**加上冷却（Part 4）**——多一个状态 `COOL`（今天刚卖出，明天只能休息）：

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

**加上「最多 k 次」（Part 3）**：给每个状态再加一个下标 j = 「到目前为止用了几次买入」。每次买入 j 加 1。图的形状不变，只是复制成 k+1 层，买入的箭头从第 j−1 层指向第 j 层。

**Java 里怎么写**：用 `enum` 表示状态，每个箭头一个方法（这就是 reference 里的 `State`，第 5 节会读它）：

```java
public enum State {
    FREE, HOLD, COOL;
    public State afterRest() { return this == COOL ? FREE : this; }
    public State afterBuy()  { if (this != FREE) throw new IllegalStateException(...); return HOLD; }
    public State afterSell(Rules r) { if (this != HOLD) throw ...; return r.cooldown() ? COOL : FREE; }
}
```

### 2.4 滚动数组（rolling array）与「更新顺序」

**是什么**：DP 表原本是「天数 × 状态」一张大表；因为明天只依赖今天，所以只保留「今天」这一行，每天原地更新成「明天」。

**为什么需要它**：n = 400 万天、k = 100 时，完整的表是 4 亿格，装不下；滚动之后只有 k+1 格。

**怎么工作 / 最容易出错的地方——更新顺序。** 原地更新时，你写的每个新值，可能覆盖了后面某个新值还需要的旧值。举个迷你例子：

```java
// 想要：b' = a（用旧的 a），a' = a + 1
a = a + 1;
b = a;      // ❌ 这里的 a 已经是新的了，b 得到的是 a'，不是 a
```

正确做法是**先算依赖旧值的，再算会覆盖旧值的**，或者用临时变量暂存旧值。Part 3 里 `hold[j]` 依赖 `free[j-1]`（旧的），所以 `j` 要**从大到小**更新：处理 j 的时候，`free[j-1]` 还没被今天的值覆盖。第 4 节会把这个讲透。

### 2.5 回溯（backtracking）：怎么从最优值还原出最优方案

DP 表算完，你只知道「最多赚多少」，不知道「怎么赚的」。要还原，有两种办法：

1. 正向填表时，**每一格顺手记下「这个最优值是从哪个旧状态来的」**（叫父指针 / 决策记录）；
2. 填完后，从终点**倒着走**：看每一格的决策记录，跳回上一格，直到起点。沿途经过的「买」「卖」箭头，就是方案。

代价：不能再用滚动数组（要保留每一天的决策），空间变成 O(n · 状态数)。本题只记 2 个比特/格，所以也不算贵。

### 2.6 哨兵值（sentinel）、溢出与「从源头消灭」

* **哨兵值**：有些状态一开始**不可能到达**（还没买过，不可能 HOLD）。我们给它一个「极小的数」，意思是「这条路走不通」，这样 `max` 会自动忽略它。
  代码里是 `NEG = Long.MIN_VALUE / 4`。为什么除以 4？如果直接用 `Long.MIN_VALUE`，对它做 `- price` 就**下溢**绕回成一个巨大的正数（见 `oa01_job_chain.md` 2.7 节），反而成了「最优」。除以 4 留足余量。
* **溢出**：`long` 最大约 9.2 × 10¹⁸。如果价格和天数都不设上界，利润可能溢出。本题的做法是在入口处规定 `0 ≤ price ≤ 2⁴⁰`、`n ≤ 2²²`，于是利润 ≤ 2²¹ × 2⁴⁰ = 2⁶¹ < 2⁶³，整个 DP 里**任何中间值都不可能溢出**，内循环里就不用到处写 `Math.addExact`。
  这叫「从源头消灭」：检查一次入口，比在热路径里检查一百万次便宜；而且「接受或拒绝」比「静默回绕」安全。

### 2.7 `enum`、`record`、`sealed` 的最小介绍

* `enum`：一个只有固定几个取值的类型（`FREE`/`HOLD`/`COOL`）。比起用 `int` 常量（0/1/2），它不会被传进一个「3」，而且能带方法。
* `record`：不可变的数据类（`Trade(buyDay, sellDay)`）。细节见 `oa01_job_chain.md` 第 6 节。
* `sealed` 接口：规定「只有这几种实现」，配合 `switch` 让编译器检查你有没有处理全。第 6 节讲。

---

## 3. 从最笨的解法开始

### 3.1 Part 1 的暴力：试遍所有（买入日，卖出日）

```java
long best = 0;                                  // 0 = 一笔也不做
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)             // 卖出日必须在买入日之后
        best = Math.max(best, prices[j] - prices[i]);
```

* 对不对：对。每一对都试了。
* 复杂度：约 n²/2 对，`O(n²)`。
* **具体在哪个输入上慢**：n = 10 万的随机价格表，约 50 亿次比较，要几十秒。本机实测（`reference` 里的 `maxProfitBrute`）：
  3 万天 **186 ms**；对照 O(n) 的 `maxProfitOnce`：3 万天 **0.018 ms**（预热后取 7 次最好值）。
  按 n² 外推，100 万天的暴力要 3 分钟以上（外推值，不是实测）。

### 3.2 如果有「最多 k 次」，暴力更惨

暴力要枚举「所有互不重叠的 (买, 卖) 区间的集合」。n 天里选 2k 个分割点，方案数是组合数 C(n, 2k)，n=1000、k=10 就是天文数字。
所以到 Part 3，**必须**用 DP，暴力连用来对拍的价值都只剩 n ≤ 10 的小数据（测试里就是这样做的：用暴力枚举当「标准答案」去对拍 DP）。

---

## 4. 一步一步改进

### Part 1：从 O(n²) 到 O(n)

**发现问题**：内层循环在为每个卖出日 j 重复回头找最好的买入日 i。

**想法**：对一个固定的卖出日 j，最好的买入日是 j 之前**价格最低**的那天。而「j 之前的最低价」随着 j 往后移，可以边走边更新，不用每次重新找。

**为什么对**：对固定的 j，`prices[j] - prices[i]` 在 `prices[i]` 最小时最大——一个减数越小差越大。

```java
long minSoFar = Long.MAX_VALUE, best = 0;
for (long p : prices) {
    if (p < minSoFar) minSoFar = p;         // 今天比以前所有天都便宜：更新最低价
    else best = Math.max(best, p - minSoFar); // 否则假设今天卖
}
```

用 `[7, 1, 5, 3, 6, 4]` 手算：

| 天 | 价格 | minSoFar | 今天卖的利润 | best |
|---|---|---|---|---|
| 0 | 7 | 7 | — | 0 |
| 1 | 1 | 1 | — | 0 |
| 2 | 5 | 1 | 4 | 4 |
| 3 | 3 | 1 | 2 | 4 |
| 4 | 6 | 1 | 5 | 5 |
| 5 | 4 | 1 | 3 | 5 |

**新复杂度**：`O(n)` 时间，`O(1)` 空间。

**换个角度看——这其实是只有两个状态的 DP**。令 `hold` = 「手里有股票时的最大现金」（买股票花了钱，所以是负的），`free` = 「已经卖出后的最大现金」。
每天：`hold = max(hold, 0 - p)`（要么早就买了，要么今天买：现金 0 减去价格）；`free = max(free, hold + p)`（要么早就卖了，要么今天卖）。
注意 `hold = max(-p 的历史) = -(历史最低价) = -minSoFar`。所以 `free = max(free, p - minSoFar)`——和上面一模一样。
这个视角很重要：Part 2、3、4 就是把它一步步扩展。

> 小警告（常见误区）：不能写成「全局最大价 − 全局最小价」。`[10, 9, 8, 1]` 的全局最大 10、最小 1，但最小值在最大值**后面**，答案是 0 不是 9。

### Part 2：次数不限

**发现问题**：Part 1 的 `hold = max(hold, 0 - p)` 里，买入用的现金是「0」，因为只能买一次，买之前现金一定是 0。次数不限时，买之前的现金可能是前几笔赚的钱。

**想法**：把「0」换成「现在的 `free`」：

```
hold' = max(hold,  free - p)      // 休息 或 今天买（用 free 里的全部现金）
free' = max(free,  hold + p)      // 休息 或 今天卖
```

（`'` 表示「今天结束时」的值，右边是「昨天结束时」的值。）

这就是第 2.3 节第一张状态机图的逐箭头翻译：休息箭头 → 两个 `max` 的第一项；买入箭头 → `free - p` 进 `hold`；卖出箭头 → `hold + p` 进 `free`。

手算 `[7, 1, 5, 3, 6, 4]`（初始 `free = 0`，`hold = −∞`）：

| 天 | 价格 | free | hold | 说明 |
|---|---|---|---|---|
| 0 | 7 | 0 | −7 | 第 0 天买入，现金 −7 |
| 1 | 1 | 0 | −1 | 改成第 1 天买更划算：−1 |
| 2 | 5 | 4 | −1 | 第 2 天卖：−1 + 5 = 4 |
| 3 | 3 | 4 | 1 | 用赚到的 4 现金买入：4 − 3 = 1 |
| 4 | 6 | 7 | 1 | 卖：1 + 6 = 7 |
| 5 | 4 | 7 | 3 | 买入 7 − 4 = 3，但不会比 7 更好 |

答案是最后一天的 `free = 7` ✓。

**更简单的写法**：这个 DP 化简后，答案其实等于「所有『今天比昨天贵』的差之和」：

```java
for (int i = 1; i < n; i++) if (prices[i] > prices[i-1]) sum += prices[i] - prices[i-1];
```

**为什么**：把任何一个方案想成「每个相邻日对 (i−1, i) 要么持有、要么不持有」。持有的日对，赚到 `prices[i] − prices[i−1]`（可能为负）。
* **上界**：一个方案赚的钱 = 它持有的那些日对的差之和，不可能超过「所有正差之和」；
* **可达**：只持有差为正的日对即可。连续几个正差的日对会合并成一笔交易（买在最低点、卖在最高点，中间的上涨相当于一段一段赚）。

**注意**：这个贪心 (greedy) 的化简只在「次数不限、没有冷却、没有手续费」时成立。一旦有任何限制，必须回到状态机。**面试里建议两种都讲**：先说状态机（通用），再说「这里可以化简成累加正差」（炫技，但要能证明）。

**新复杂度**：`O(n)`，`O(1)` 空间。

### Part 3：最多 k 次

**发现问题**：现在买入次数受限，状态里必须记「已经用了几次」，否则不知道还能不能买。

**想法**：给 `free`、`hold` 各加一个下标 j（0..k）：

* `free[j]`：手里没股票、**最多**做过 j 笔交易时的最大现金；
* `hold[j]`：手里有一股、这一股的买入算在第 j 笔之内（所以买它之前至多做过 j−1 笔）时的最大现金。

转移（对每个 j ≥ 1，每天价格 p）：

```
hold'[j] = max(hold[j],  free[j-1] - p)    // 休息；或今天买（买之前只能做过 j-1 笔）
free'[j] = max(free[j],  hold[j]   + p)    // 休息；或今天卖
```

初始：`free[j] = 0`（对所有 j：什么都没做，现金 0；「最多」j 笔，所以 0 笔也算）；`hold[j] = −∞`。答案是 `free[k]`。

**为什么用「最多 j 笔」而不是「恰好 j 笔」**：「最多」的定义下，`free[k]` 就直接是答案，不用再对 j 取最大。而且初始值全是 0，不需要特殊处理。

手算 `k = 2`，`prices = [3, 3, 5, 0, 0, 3, 1, 4]`（LeetCode 123，答案 6）。每格是 `[j=0, j=1, j=2]`；`hold[0]` 永远是 −∞（买不起第 0 笔），省略：

| 天 | 价格 | free[0..2] | hold[1], hold[2] |
|---|---|---|---|
| 0 | 3 | 0, 0, 0 | −3, −3 |
| 1 | 3 | 0, 0, 0 | −3, −3 |
| 2 | 5 | 0, 2, 2 | −3, −3 |
| 3 | 0 | 0, 2, 2 | 0, 2 |
| 4 | 0 | 0, 2, 2 | 0, 2 |
| 5 | 3 | 0, 3, 5 | 0, 2 |
| 6 | 1 | 0, 3, 5 | 0, 2 |
| 7 | 4 | 0, 4, 6 | 0, 2 |

逐格验证几处：
* 第 2 天（价格 5）：`free[1] = max(0, hold[1] + 5) = max(0, −3 + 5) = 2`——第 0 天买 3，第 2 天卖 5，赚 2 ✓。
* 第 3 天（价格 0）：`hold[2] = max(−3, free[1] − 0) = max(−3, 2) = 2`——「已经赚了 2，再用这 2 块现金（不花钱，价格 0）买第二笔的股票」，现金是 2 ✓。
* 第 7 天（价格 4）：`free[2] = max(5, hold[2] + 4) = max(5, 6) = 6`——第二笔在价格 0 买、价格 4 卖，加上第一笔赚的 2 = 6 ✓。

**更新顺序（接 2.4 节）**：第 d 天的新 `hold[j]` 需要「昨天的 `free[j-1]`」。所以：

```java
for (int j = k; j >= 1; j--) {                              // j 从大到小
    free[j] = Math.max(free[j], hold[j] + p);               // 先用「昨天的 hold[j]」
    hold[j] = Math.max(hold[j], free[j - 1] - p);           // free[j-1] 还没被今天覆盖：仍是昨天的
}
```

若写成 j 从小到大：处理 j 时，`free[j-1]` 已经被今天更新过，等于允许「同一天先卖、再用卖出的钱买入」，违反「一天一个动作」。
**有意思的是，对 Part 3 这个具体公式，两种顺序的答案其实一样**（我用 n ≤ 5、价格 0..3 的全部输入验证过）：同一天按同一个价格「卖了又买」，现金一分不变，
所以多出来的那条路径不会产生更好的值。但这是「碰巧」：它依赖「同一天买卖价格相同、没有手续费、没有冷却」。
一旦加上冷却（下面 Part 4），读了「今天已更新的 free」去买入就会得到错误答案（见 Part 4 的例子）。**所以养成习惯：每个转移只用「昨天的值」，写法上要么 j 倒序，要么先把旧值存进局部变量。**

**k 很大时怎么办**：`k = Integer.MAX_VALUE` 时 `new long[k + 1]` 会 `OutOfMemoryError`。观察：n 天里每笔交易至少占两天（买一天、卖一天），所以**最多完成 n/2 笔**。
`k ≥ n/2` 时，次数限制等于没有限制 → 直接用 Part 2。

```java
if (k >= n / 2) return maxProfitUnlimited(prices);
```

**新复杂度**：时间 `O(n · min(k, n/2))`，空间 `O(min(k, n/2))`。n = 20 万、k = 50 实测 3.6 ms（预热后）。

### Part 4：冷却、手续费、还原交易

#### 手续费（LC 714）：只改一处

手续费是「每次卖出扣 fee」。唯一的变化是卖出箭头：`hold + p` 变成 `hold + p − fee`。状态机不变。
一个细节：手续费让「买了又立刻卖」亏钱，所以 DP 自动不会做无意义的交易。

#### 冷却（LC 309）：多一个状态

卖出之后的下一天不能买。「今天是不是刚卖出」会影响明天能不能买，所以它必须是状态的一部分——按 2.2.4 的判断标准：它决定了未来能做什么。新增状态 `COOL`（对应 2.3 节第二张图）：

```
hold'[j] = max(hold[j],  free[j-1] - p)    // 买入只能从 FREE 来（不能从 COOL 买！）
cool'[j] = hold[j] + p - fee                // 今天卖出 → 进入 COOL
free'[j] = max(free[j], cool[j])            // 休息；或冷却结束（昨天卖的，今天自动变回 FREE）
```

没有冷却时，卖出直接回到 FREE：`free'[j] = max(free[j], hold[j] + p - fee)`。

手算 LC 309：`prices = [1, 2, 3, 0, 2]`，不限次数（`j` 这一维压成 1 格）。答案 `max(free, cool)`：

| 天 | 价格 | free | hold | cool | 说明 |
|---|---|---|---|---|---|
| 0 | 1 | 0 | −1 | −∞ | 买入 |
| 1 | 2 | 0 | −1 | 1 | 昨天的 hold(−1) + 2 = 1：第 1 天卖出，进入 COOL |
| 2 | 3 | 1 | −1 | 2 | free = max(0, 昨天的 cool=1) = 1：冷却结束；今天不能用这笔钱买（买入只看**昨天**的 free = 0）|
| 3 | 0 | 2 | 1 | −1 | free = max(1, 昨天的 cool=2) = 2；hold = max(−1, 昨天的 free(1) − 0) = 1 |
| 4 | 2 | 2 | 1 | 3 | cool = 昨天的 hold(1) + 2 = 3 |

最终 `max(free=2, cool=3) = 3` ✓（第 0 天买、第 1 天卖赚 1；第 2 天冷却被迫休息；第 3 天价格 0 买入、第 4 天价格 2 卖出赚 2；合计 3）。

如果错把买入写成 `hold' = max(hold, free' - p)`（用今天**已更新**的 free'，其中已包含「昨天卖出、今天冷却结束」的钱），同一份数据会得到 **4** 而不是 3：它在第 2 天卖出、第 3 天立刻买入价格 0 的股票，刚好跳过了冷却。这是冷却题最常见的错，样例 `[1,2,3,0,2]` 就能抓到。

#### 还原交易：回溯（接 2.5 节）

**发现问题**：现在只有一个数字。要报出买卖日，必须记下每一格是怎么来的。

**想法**：每个 (天, j) 格子记 2 个比特：
* bit0：`hold` 这一格是不是「今天买入」得来的（`free[j-1] − p > hold[j]` 严格成立）；
* bit1：`free` 这一格是不是不是「休息」得来的（来自卖出，或来自冷却结束）。

**平局时选「休息」**（比较用严格 `>`）。好处：不会产生净利润为 0 的废交易；方案更稳定。

倒着走：从终点状态（`FREE` 或 `COOL`，看谁的现金多）出发，每一天看当前状态对应的比特：

* 当前是 `COOL`：这一天卖出了 → 记下卖出日，状态变成 `HOLD`（回到昨天持有的情形）；
* 当前是 `HOLD`：bit0 = 1 → 这一天买入了 → 配对记一笔 `(买入日, 刚才记下的卖出日)`，状态变成 `FREE`（j 减 1）；bit0 = 0 → 昨天也持有，原地不动；
* 当前是 `FREE`：bit1 = 1 → 有冷却时意味着「昨天才卖，今天冷却结束」→ 状态变成 `COOL`；没有冷却时意味着「今天卖出」→ 记卖出日，状态变成 `HOLD`；bit1 = 0 → 休息，原地不动。

对 `[1, 2, 3, 0, 2]`（冷却，不限次数）走一遍。正向填表时每天记下的 bits（bit0 = 今天买入，bit1 = free 不是休息得来的）依次是：第 0 天 `01`，第 1 天 `00`，第 2 天 `10`，第 3 天 `11`，第 4 天 `00`（二进制，bit1 在左）。倒着走：

```
终点：cool=3 > free=2  →  状态 COOL
第 4 天，COOL        →  这天卖出            记 sell=4，状态 → HOLD
第 3 天，HOLD, bit0=1 →  这天买入            记 Trade(3,4)，状态 → FREE
第 2 天，FREE, bit1=1 →  冷却在这天结束      状态 → COOL
第 1 天，COOL        →  这天卖出            记 sell=1，状态 → HOLD
第 0 天，HOLD, bit0=1 →  这天买入            记 Trade(0,1)，状态 → FREE   ← 回到起点 FREE，一致
```

倒着得到的是 `[Trade(3,4), Trade(0,1)]`，反转后 `[Trade(0,1), Trade(3,4)]` ✓（这正是测试里的期望）。

**回溯的自检**：走到起点时状态必须是 `FREE`（初始状态）。如果不是，说明决策记录写错了。reference 里用 `AssertionError` 把这个检查留了下来。

**更强的自检——`replay`**：不要只信 DP 给出的数字。再写一个**独立的检查器**，把方案逐天回放一遍：按状态机一天天走（有动作按动作，没动作就休息），非法就报错，最后算利润。
`plan(...).profit()` 必须等于 `replay(...)` 的结果。这是「验证」与「计算」分开的好习惯：DP 的错误和检查器的错误很难恰好抵消。

**新复杂度**：`maxProfit`：时间 `O(n·min(k, n/2))`，空间 `O(min(k, n/2))`。`plan`：多 `O(n·min(k, n/2))` 字节的决策记录；超过 2²⁸ 字节就拒绝。

---

## 5. 逐段讲参考解

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

* `Trade` 的紧凑构造器保证「买入日 < 卖出日」：一个非法的 `Trade` 构造不出来，后面的代码不需要再检查。
* `Plan` 的紧凑构造器给 `trades` 赋成 `List.copyOf(...)`：一个**不可变的拷贝**。外部拿到 `Plan` 之后不可能改它里面的列表，`Plan` 才算真的不可变。
* `Rules` 把 k / fee / cooldown 打包成一个值。LC 121 = `atMost(1)`，122 = `unlimited()`，188 = `atMost(k)`，309 = `unlimited().withCooldown(true)`，714 = `unlimited().withFee(f)`——**六道题是同一个函数的六组参数**。

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

三个方法 = 状态机图上的三类箭头。非法的箭头（比如在 `COOL` 买入）抛 `IllegalStateException`。
这个状态机**不参与** DP 的计算（DP 的转移是手写在数组更新里的），它的用途是 `replay`：用「同一份规则的另一种表达」独立检查方案。

### 5.3 输入校验与 Part 1/2

```java
private static void check(long[] prices) {
    Objects.requireNonNull(prices, "prices");
    if (prices.length > MAX_DAYS) throw new IllegalArgumentException("too many days: " + prices.length);
    for (int i = 0; i < prices.length; i++)
        if (prices[i] < 0 || prices[i] > MAX_PRICE) throw new IllegalArgumentException(...);
}
```

每个公共入口第一行调用 `check`。`Objects.requireNonNull` 抛 `NullPointerException` 并带一个信息，比让它在后面某行意外崩溃更好定位。

`maxProfitBrute`、`maxProfitOnce`、`maxProfitUnlimited` 就是第 3、4 节里的代码，没有额外技巧。

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

* `new long[k + 1]` 默认全 0 → `free` 的初值正好是 0，不用填。
* `hold[j] + p`：`hold[j]` 可能是 `NEG`（`Long.MIN_VALUE/4`），加一个不超过 2⁴⁰ 的 p 仍然是极负数，`max` 会忽略它，且不会溢出。
* 内层循环里没有任何分配，也没有分支预测不友好的跳转，所以 20 万天 × 50 的实测只要几毫秒。

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

* `unbounded`：次数不限（或大到等于不限）时，j 这一维没有意义，压成 1 格。此时「买入的钱来自哪一格」从 `free[j-1]` 变成 `free[j]`（同一格），所以有 `src = unbounded ? j : j - 1`。
* 三个数组 `free` / `hold` / `cool`，对应三个状态。

```java
    for (int i = 1; i <= n; i++) {
        long p = prices[i - 1];
        for (int j = bound; j >= 0; j--) {
            int src = unbounded ? j : j - 1;
            long oldHold = hold[j], oldFree = free[j], oldCool = cool[j];
            long buy = src >= 0 ? free[src] - p : NEG;
            long sell = oldHold + p - fee;
```

* 开头先把三个「旧值」存进局部变量（`oldHold` 等），这样后面不管先写谁，别的转移用的都是昨天的值。`free[src]` 当 `src = j-1` 时在 j 递减循环里仍是昨天的值（2.4 节）。
* `buy`：今天买入后的现金 = 昨天 FREE 的现金 − 今天价格。`src < 0` 表示「第 0 笔不能买」，给 `NEG`。
* `sell`：今天卖出后的现金 = 昨天 HOLD 的现金 + 价格 − 手续费。

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

* 四个 `if` 就是状态机的四类带值的箭头：「买」「休息(HOLD)」「卖」「冷却结束 / 休息(FREE)」。严格 `>` = 平局选休息。
* `how` 为 `null` 时（只要利润）完全不记录，所以 `maxProfit` 和 `plan` 共用同一段引擎，答案必然一致。
* 为什么 `cool[j] = sell` 而不是 `max(cool[j], sell)`？`COOL` 的含义是「**今天刚**卖出」，只有今天卖出才算，昨天的 COOL 今天就变成 FREE 了。

```java
    if (rules.cooldown() && cool[bound] > free[bound]) return new Solved(cool[bound], State.COOL);
    return new Solved(free[bound], State.FREE);
}
```

终点状态：最后一天结束时，没股票的两种情形里取现金多的。（不会停在 `HOLD`：没卖出的股票不算利润。）

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

和 4 节的倒走一一对应。注意读 `bits` 用的是**当前的 j**，j 在买入分支里才减 1。
最后：

```java
for (Trade t : reversed.reversed()) { ... if (net > 0) trades.add(t) ... }
if (sum != solved.profit()) throw new AssertionError(...);
```

`reversed.reversed()`：第一个 `reversed` 是变量名（倒着收集的交易），第二个是 Java 21 的 `List.reversed()` 方法，返回倒序视图（第 6 节）。
最后一行把「各笔净利润之和」与 DP 的数字对账——两者不等就是有 bug，直接 `AssertionError`。

### 5.7 `replay`

```java
state = switch (moves.get(day)) {
    case null -> state.afterRest();
    case Buy(var d) -> { cash = Math.subtractExact(cash, prices[d]); yield state.afterBuy(); }
    case Sell(var d) -> { cash = Math.addExact(cash, prices[d] - rules.fee()); yield state.afterSell(rules); }
};
```

* `moves` 是 `TreeMap<Integer, Move>`：天 → 那天的动作。`get(day)` 没有动作返回 `null`（休息）。
* `case null`：Java 21 的 `switch` 可以显式处理 `null`；以前对 `null` 做 `switch` 会直接 `NullPointerException`。
* `case Buy(var d)`：record 模式，同时判断类型和取出字段。
* 状态机方法抛出的 `IllegalStateException` 在外面被包成 `IllegalArgumentException("illegal plan: ...")`——对调用者来说，传入一个非法方案是参数错误。

---

## 6. Java 21 特性小课

### 6.1 `enum` + `switch` 表达式（J05）

旧写法（Java 7）：

```java
switch (state) {
    case FREE: ... break;     // 忘了 break 就会「掉」到下一个 case
    case HOLD: ... break;
}
```

新写法：箭头 `->`，没有 fallthrough；`switch` 可以**直接产生值**；对 enum 的 `switch` 表达式要求覆盖所有取值，漏一个**编译失败**。块分支里用 `yield 值` 返回。
`State` 里 `this == COOL ? FREE : this` 是更小的写法；复杂一点的转移用 `switch` 表达式更清楚。

### 6.2 `sealed` 接口 + record（J02）+ 模式匹配 `switch`（J03）+ record 模式（J04）

```java
public sealed interface Move permits Buy, Sell {}
public record Buy(int day) implements Move {}
public record Sell(int day) implements Move {}
```

`sealed` 告诉编译器：`Move` 只有 `Buy` 和 `Sell` 两种。所以 `switch (move) { case Buy(var d) -> ...; case Sell(var d) -> ...; }` 不需要 `default`：
编译器知道已经覆盖全部。以后新增 `Rest`，所有没处理它的 `switch` 立刻编译失败——这是「让编译器帮你找遗漏」。

`case null`（J03 的一部分）：Java 21 允许 `switch` 里直接写 `case null ->`，不再需要先 `if (x == null)`。

什么时候**不该**用：枚举值只有几个、没有各自的数据时，用 `enum` 就够了（如 `State`）；`sealed` + `record` 适合「每种情形带不同的数据」（买带日期、卖带日期、将来可能有的取消带原因……）。

详细课本：`study/10-java21/J02_sealed.md`、`J03_pattern_switch.md`、`J04_record_patterns.md`（待写）。

### 6.3 Sequenced Collections（J09）

旧写法：要倒着遍历一个 `List`，要么 `Collections.reverse(list)`（修改原列表）要么写倒着的下标循环。

```java
for (Trade t : reversed.reversed()) { ... }
```

Java 21 的 `List.reversed()` 返回一个**倒序视图**（不拷贝、不修改原列表）。同一批新方法还有 `getFirst()` / `getLast()` / `addFirst()`……统一定义在 `SequencedCollection` 接口上，`List`、`Deque`、`LinkedHashSet` 都实现了它。
旧代码里 `list.get(list.size() - 1)` 取最后一个，现在是 `list.getLast()`，空列表会抛 `NoSuchElementException` 而不是下标越界。

### 6.4 `record` 的紧凑构造器与「不可变拷贝」（J01）

`Plan` 里：

```java
public Plan { trades = List.copyOf(trades); }
```

紧凑构造器的参数就是 record 的组件，你可以在字段赋值**之前**重新给参数赋值。这里把调用者传进来的列表换成不可变拷贝：以后外部再改原列表，`Plan` 不受影响。
这叫**防御性拷贝**（defensive copy）。没有它，`record` 虽然字段是 `final`，里面的列表却仍可被外部修改，「不可变」就是假的。

### 6.5 数学小工具（J15）与 `var`（J08）

`Math.addExact` / `Math.subtractExact`：溢出时抛 `ArithmeticException`，而不是静默绕回。`replay` 里用它们是因为 `replay` 的输入（任意 `Trade` 列表）不如 DP 的内循环可控。
`var`：只在右边一眼看得出类型时用（`var reversed = new ArrayList<Trade>()`）。

---

## 7. 追问预演

**问：你的 DP 状态是什么？为什么这样定义就够了？**
* 思考：先说「状态 = 足以决定未来的信息」，再列出本题的：有没有股票、已用几笔、是否冷却。再说为什么不需要别的（买入价体现在现金里）。
* 答要点：每个状态记「最大现金」；优势论证——同一状态下现金多的历史永远不劣于现金少的。
* 说出口：「我把每天结束时的情形分成持有、空仓、冷却三类，再乘上已用的交易笔数。每个状态只记最大现金，因为未来的可行操作只取决于状态，现金多的历史总是更好。」

**问：k 很大怎么办？**
* 思考：O(n·k) 时间和 O(k) 空间在 k = 10⁹ 时都不行；n 天最多完成 n/2 笔。
* 答要点：`k ≥ n/2` 退化成不限次数，O(n)。
* 说出口：「交易至少占两天，所以有效的 k 不超过 n/2；超过就当作不限次数。」

**问：能不能再快？O(nk) 能降吗？**
* 答要点：这题有已知的更快解法——把价格序列拆成「波谷-波峰」对，用堆或分治做到 O(n log n)（利用「第 k 笔交易的边际收益递减」，即凹性）。面试中知道有这回事、能说出思路方向就够，一般不要求写出来。
* 说出口：「可以利用边际收益递减，用优先队列合并相邻的涨跌段，O(n log n)。我现在写的 O(nk) 在 k 小时已经足够。」

**问：怎么还原具体的买卖日？**
* 答要点：正向时每格记决策（2 个比特），倒着走；空间 O(n·k)；平局选休息避免零利润交易；走到起点必须回到初始状态做自检。
* 说出口：「我会记下每个格子的最优值是来自休息还是来自买/卖，最后从终点倒着走。如果只要日期而空间紧，可以用分治（Hirschberg 思路）把空间降到 O(k)，但代码复杂得多。」

**问：怎么保证你的答案是对的？**
* 答要点：对拍——写一个 n ≤ 10 的暴力枚举（枚举所有合法交易序列），和 DP 在几千组随机小数据上比较；再写独立的 `replay` 检查器验证 `plan`。
* 说出口：「我写了一个完全不用状态机的暴力枚举当标准答案，随机小数据对拍；还原出来的方案再用另一套检查器回放一遍。」

**问：价格是 `long`，利润会溢出吗？**
* 答要点：先问约束；没有约束就用 `Math.addExact` 或 `BigInteger`；有约束就从界限算出最大利润（天数/2 × 最大价格）证明不溢出，在入口拒绝越界输入。
* 说出口：「我先在入口限制价格和天数，保证最大利润小于 2⁶³，这样内循环里不用检查溢出。」

**问：流式输入、不能存下全部价格怎么办？**
* 答要点：只要利润——滚动数组本来就是一遍扫描，O(k) 内存，直接逐个价格更新；要还原则需要保存决策，内存随之增长。
* 说出口：「只要数字的话我这个实现本来就是在线的，每来一个价格更新一次。」

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 全局最大 − 全局最小（Part 1） | 最小值可能在最大值之后，`[10, 9, 8, 1]` 答案是 0 | 边扫边维护「到目前为止的最低价」 |
| Part 3 里 `j` 从小到大更新，并以为「反正答案一样」 | 纯 Part 3 里碰巧一样（同价卖了再买现金不变），但加上冷却 / 手续费就错；依赖「碰巧」的写法一改规则就炸 | 每个转移只用昨天的值：`j` 从大到小，或先存旧值 |
| `new long[k + 1]` 不判断 k 的大小 | `k = Integer.MAX_VALUE` 直接 `OutOfMemoryError` | `k ≥ n/2` 时退化为不限次数 |
| 用 `Long.MIN_VALUE` 当「不可达」，然后 `- price` | 下溢绕回成巨大正数，被 `max` 当成最优 | `NEG = Long.MIN_VALUE / 4` 留余量 |
| 冷却用「今天已更新的 free」去买入 | 等于允许冷却期里买入：`[1,2,3,0,2]` 得到 4 而不是 3 | 买入只能用「昨天结束时」的 FREE |
| 手续费在买入、卖出各扣一次 | 题面是每笔交易扣一次（LC 714） | 只在卖出（或只在买入）扣 |
| 回溯时读错了 j（买入前先把 j 减了） | 读到别的格子的决策，还原出错的方案 | 先用当前 j 读 `bits`，买入分支里再 `j--` |
| DP 的数字直接信，不对拍 | DP 的 bug 往往只在特定输入暴露 | 小数据暴力对拍 + 独立的 `replay` 检查器 |
| 把平局算成「也做交易」 | 方案里出现净利润为 0 的废交易，tie-break 不稳定 | 比较用严格 `>`，平局选休息 |

---

## 9. 自测题

1. 用自己的话说：DP 里的「状态」要满足什么条件？为什么「只记最优值」不会丢掉更好的解？
2. 画出「最多 k 次、有冷却」的状态机（至少画出 j=0 和 j=1 两层），在每条箭头上标出现金怎么变。
3. `prices = [2, 1, 4, 5, 2, 9, 7]`，`k = 2`，手算 `free[2]` 的最终值，并说出是哪两笔交易。
4. 把 `maxProfitAtMost` 的内层循环改成 `j` 从小到大，纯 Part 3 的答案会变吗？为什么？如果同时加上「冷却」会怎样？
5. 写代码：在不改动 `run` 的前提下，用 `Rules` 解决「每笔交易买入时扣手续费，而不是卖出时」。需要改什么？结果和卖出时扣有区别吗？
6. （挑战）只要利润数字，空间能降到 O(1) 吗（不限次数 + 冷却）？写出三个变量的更新式。

<details><summary>答案</summary>

1. 状态要满足：知道状态就足以决定接下来能做什么、每个动作带来的现金变化——和「怎么到达的状态」无关。因此到达同一状态的两个历史，现金多的永远不会比现金少的差（未来对两者完全一样，只是起点差一个常数）；少的可以丢。
2. 每层有 FREE、HOLD、COOL 三个圈。FREE→HOLD（买入，现金 −p，j 层 +1）；HOLD→COOL（卖出，现金 +p −fee）；COOL→FREE（被迫休息，现金不变）；FREE→FREE、HOLD→HOLD（休息，现金不变）。j=0 层没有 FREE→HOLD 的箭头指向自己，买入的箭头从 j=0 的 FREE 指向 j=1 的 HOLD。
3. 最优是：价格 1 买、价格 5 卖（赚 4）；价格 2 买、价格 9 卖（赚 7）；合计 11。`free[2] = 11`。（另一种分法 1→9 一笔赚 8，再加不了第二笔，不如两笔。）
4. 纯 Part 3 里答案不变：从小到大时 `hold[j]` 会用到今天已更新的 `free[j-1]`，相当于同一天「卖出再买入」，但价格相同、无手续费，现金不变，不产生更优值。
   加上冷却后会变：`hold` 读到了包含「昨天卖出、今天冷却结束」的钱，等于冷却期内买入（本讲义 Part 4 的例子：`[1,2,3,0,2]` 得到 4 而不是 3）。结论：每个转移只用昨天的值。
5. 把 `sell = oldHold + p - fee` 改成 `sell = oldHold + p`，把 `buy = free[src] - p` 改成 `buy = free[src] - p - fee`。结果相同：每笔**完成**的交易恰好扣一次，而最终答案只看 `free` / `cool`（还持有的股票不计入），所以没有区别；`plan` 里每笔的净利润公式也不变。
6. 不限次数 + 冷却：`free' = max(free, cool)`；`hold' = max(hold, free - p)`；`cool' = hold + p`（都用昨天的值，所以先存旧值再更新）。答案 `max(free, cool)`。这就是 LC 309 的标准 O(1) 空间解。

</details>

---

## 10. 延伸阅读

* Cormen 等《算法导论》第 14 章（第 4 版，原第 15 章）「动态规划」—— 从「钢条切割」讲起，把「最优子结构」「重叠子问题」讲得最清楚，读前两节就够。
* Skiena《算法设计手册》第 10 章 动态规划 —— 习题多，尤其「状态定义」的练习。
* LeetCode 188 官方题解 https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/ ——本题的原型；注意看它是怎么用「买入 / 卖出」两个数组定义状态的（和这里一致）。
* JEP 395 Records / JEP 409 Sealed Classes / JEP 441 Pattern Matching for switch / JEP 431 Sequenced Collections（openjdk.org/jeps/）—— 本题用到的语言特性的设计文档。
* `java.lang.Math` Javadoc（`addExact`、`subtractExact`、`clamp`）—— 溢出检测的标准做法。
