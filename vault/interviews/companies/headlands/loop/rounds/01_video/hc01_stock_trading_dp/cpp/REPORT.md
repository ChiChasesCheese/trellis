# hc01 · 思路与追问（C++20 版）

买卖股票是电面里最典型的 DP 题：一道经典题加一串 follow-up。面试官看的是你加规则时改一条箭头还是重写整个解法，以及在 C++ 里整数边界有没有踩雷。下面按 Part 写清怎么写、面试官在探什么、该说出口的话。逐行的实现和可运行的示例在讲义 [[hc01_stock_trading_dp_cpp]]。

## 30 秒版本

- **一次交易**：对固定的卖出日，最好的买入日是此前的最低价，一次扫描维护 `min_so_far`。
- **不限次数**：所有正差之和；通用说法是两个状态 `free / hold`。
- **最多 k 笔**：每个状态加一个下标 j，滚动数组，`j` 从大到小；`k >= n/2` 直接按不限次数做。
- **冷却 / 手续费**：手续费是卖出箭头多减一个 `fee`；冷却是多一个 `COOL` 状态，买入只能读昨天的 `free`。
- **还原交易**：正向记每格 2 个比特的决定，倒着走，走完必须回到 `FREE`，各笔净利润之和必须等于 DP 的数字。
- **C++ 的雷**：`size() - 1`、`k + 1`、哨兵上的加减、`(n+1)*(k+1)`，全是有符号或无符号的边界问题。

## Part 1 · 一次交易

**写法**

```cpp
long long min_so_far = LLONG_MAX, best = 0;
for (long long x : p) {
    if (x < min_so_far) min_so_far = x;
    else best = std::max(best, x - min_so_far);
}
```

先写 O(n²) 的暴力当标准答案，再改成一次扫描。入口先校验：天数超过 `MAX_DAYS` 或价格越界就抛 `std::invalid_argument`。

**面试官在探什么**

1. **为什么不是全局最大减全局最小**：买入必须在卖出之前。`[10,9,8,1]` 得 0，`[5,1,5,0,4]` 得 4。
2. **为什么有价格上界**：天数 ≤ 2^22、价格 ≤ 2^40，利润最多 2^21 · 2^40 = 2^61，小于 2^63。由此内层循环不需要检查溢出，检查只放在入口。没有上界就得用 `__builtin_add_overflow`。
3. **空输入**：`p.size()` 是无符号数，`p.size() - 1` 在空 span 上是 `SIZE_MAX`，`i < p.size() - 1` 会读越界。循环写成 `for (x : p)`，或者下标从 1 开始、条件写 `i < p.size()`。
4. **`span` 的好处**：不拷贝、不会是 null、vector / `std::array` / C 数组都能转进来，Java 里的 `NullPointerException` 这一类错误不存在。
5. **价格用什么类型存**：2^40 超过 `int`，差值也要用 `long long`。

**该说出口的话**：「对每个卖出日，最好的买入日是它之前的最低价，所以一遍扫描维护最低价。价格有上界，我在入口校验，内层不用查溢出。」

## Part 2 · 次数不限

**写法**：`for (i = 1; i < n; ++i) if (p[i] > p[i-1]) sum += p[i] - p[i-1];`。

**面试官在探什么**

1. **为什么求正差之和是对的**：每笔交易的利润等于它覆盖的每日差之和，所以上界是所有正差之和；取每一段上涨就达到这个上界。
2. **和状态机的关系**：`hold' = max(hold, free - p)`，`free' = max(free, hold + p)`。先说通用状态机，再说化简，因为 Part 3 和 4 要在状态机上改。
3. **溢出**：1000 笔 × 2^40 约 2^50，远小于 2^63。

**该说出口的话**：「不限次数时每段上涨都拿，利润就是所有正差之和；这等价于两状态 DP，后面加规则我还回到状态机。」

## Part 3 · 最多 k 笔

**写法**

```cpp
// dp[j] = {idle, held}，j 从大到小
idle = std::max(idle, held + price);                       // 卖：读昨天的 held[j]
held = std::max(held, dp[j - 1][0] - price);               // 买：读昨天的 idle[j-1]
```

初值 `idle = 0`、`held = NEG`；答案是 `dp[k][0]`。入口先分流：`k == 0` 或 n < 2 得 0；`k >= n / 2` 调 `max_profit_unlimited`。

**面试官在探什么**

1. **状态是什么**：「已经买了几次 × 手里有没有股」。同一状态下现金多的历史永远不差，所以只记最大现金。
2. **`j` 为什么倒序**：买入要读昨天的 `idle[j-1]`；倒序时 `dp[j-1]` 还没被今天覆盖。正序会读到今天已更新的值，等于允许同一天卖出再买入。没有冷却时这个错误不改变结果（同一天卖了又买，现金不变），所以测试发现不了；加上冷却后同一类错误会改变结果（见 Part 4 第 1 条）。
3. **`k` 很大**：`std::vector dp(k + 1)` 在 `k == INT_MAX` 时 `k + 1` 是有符号溢出，是 UB，不是回绕；就算不溢出也会去分配几十 GB。n 天最多完成 n/2 笔，所以 `k >= n/2` 要在任何分配之前分流成 Part 2。
4. **`NEG` 取多少**：不可达状态要参与 `+ price`、`- price`、`- fee`。`LLONG_MIN` 上再减就是有符号溢出，所以取 `LLONG_MIN / 4`，留足余量。
5. **复杂度**：时间 O(n · min(k, n/2))，空间 O(min(k, n/2))。为什么不能贪心：有 k 的限制后，哪几段上涨值得占名额取决于全局。有 O(n log n) 的做法（谷峰段 + 堆合并），知道方向即可。
6. **验证方法**：写一个枚举所有「买 < 卖 < 买 < 卖……」序列的朴素解，随机小输入对拍；再加性质：k 增大时利润不下降，`k = 1` 等于 Part 1。

**该说出口的话**：「状态是已买次数加是否持股，滚动数组 j 倒序，保证买入读的是昨天的值；k 超过 n/2 就退化成不限次数，所以永远不会按 k 分配空间。」

## Part 4 · 冷却 / 手续费 / 还原 / 回放

**写法**：三个状态 `free / hold / cool`，加一个可选的决策记录。

- 手续费：卖出多减 `fee`，`sell = hold + price - fee`。
- 冷却：卖出进 `cool`，`free' = max(free, cool)`；买入读的是**昨天**的 `free`。
- 没有冷却：卖出直接回 `free`。
- 只要数字（`max_profit`）不传决策记录，`plan` 传一个 `vector<unsigned char>`，每格 2 个比特：bit 0 表示今天的 hold 来自今天买入，bit 1 表示今天的 free 不是单纯休息。两者共用一个引擎，不写两份。

**回溯**：从终点倒着走，终点要比较 `cool` 和 `free`；`COOL` 记卖出日，`HOLD` 且 bit 0 记买入日，`FREE` 且 bit 1 表示冷却结束或当天卖出。有限制 k 时，先读决定位再 `--j`。走完必须回到 `FREE`，各笔净利润之和必须等于 DP 的数字。平局选休息，所以不会产生零利润交易。

**面试官在探什么**

1. **冷却的读取顺序**：买入读今天已更新的 `free`（把今天的 `cool` 并进去）会得到 `[1,2,3,0,2]` → 4，正确答案是 3。买入必须只读昨天的 `free`。
2. **手续费 == 价差**：净利润 0 的交易不应该出现。更新用严格大于，平局偏向休息。
3. **`plan` 为什么和 `max_profit` 分开**：只要数字就不该付 O(n · k) 字节的决策表。`try_plan` 在格子数超过 `MAX_PLAN_CELLS`（2^28）时返回 `std::nullopt`，让调用者决定怎么退化；价格越界是调用者的错，仍然抛异常。
4. **格子数怎么算**：`(n + 1) * (k + 1)` 用 `int` 算会越界，n = 100 000、k = 49 999 约 5·10⁹。两个因子先转成 `long long` 再乘。
5. **`std::optional` 的取值**：回溯里的「待配对的卖出日」用 `std::optional<int>`，取值用 `.value()`，DP 和回溯不一致时抛异常；`*opt` 在空时是 UB。
6. **`replay` 为什么单独写**：用 `State` 状态机逐天回放，是对 `plan` 的第二道独立检查。非法方案（重叠、冷却期买入、超过 k 笔、同一天两个动作、日期越界、没持股就卖）靠 `after_buy` / `after_sell` 抛 `IllegalState`，再包成 `std::invalid_argument`。
7. **`IllegalState` 为什么不继承 `invalid_argument`**：前者是状态转移用错，后者是参数不对；继承后一个 `catch` 会把两种错误吞在一起。
8. **`enum class` 可以装任何整数**：`static_cast<State>(7)` 不能当下标用，也不能假设只有三个值；`after_buy` / `after_sell` 对它抛 `IllegalState`，`after_rest` 原样返回。
9. **`std::variant` 的动作类型**：`Move = variant<Buy, Sell>`，`std::visit` 要求处理所有类型，以后加一种动作，编译就失败；`holds_alternative` 链不会提醒你。
10. **追问**：买卖价差（bid-ask）→ 买用 ask、卖用 bid，状态机不变；价格是 `double` → 累积舍入误差，平局判断不可靠，金融里用整数 tick；流式输入 → 只要数字，滚动数组天然在线，要还原则要保存决策。

**该说出口的话**：「手续费是卖出箭头多减 fee，冷却是多一个 COOL 状态，买入只读昨天的 free。还原靠记决策位再倒着走，最后用 replay 独立回放验证。」

## C++ 专属陷阱

1. `i < p.size() - 1`：空输入回绕成 `SIZE_MAX`。
2. `dp(k + 1)` 且 `k == INT_MAX`：有符号溢出。
3. `NEG = LLONG_MIN` 再加减价格：有符号溢出。
4. `(n + 1) * (k + 1)` 用 `int` 算。
5. 用 `*opt` 解引用空 `optional`。
6. `j` 正序更新，或冷却下买入读了今天的值。
7. 平局偏向「买 / 卖」，产生零利润交易或同一天又卖又买。
8. 用 `int` 装价格差。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 输入 | `long[]`，可为 `null`，要抛 `NullPointerException` | `std::span<const long long>`，不会是 null，不拷贝 |
| 溢出 | `Math.addExact` 抛 `ArithmeticException` | 有符号溢出是 UB，用 `__builtin_add_overflow`，或像这里一样用输入上界保证不溢出 |
| `k + 1` | 回绕成负数，`NegativeArraySizeException` | UB；先用 `k >= n/2` 分流 |
| 长度 | `int length` | `size_t`，无符号，`size() - 1` 回绕；格子数用 `long long` |
| 表太大 | 抛异常 | `try_plan` 返回 `std::optional`，输入非法才抛 |
| 状态机 | `enum` + 方法，`IllegalStateException` | `enum class` + 自由函数，自定义 `IllegalState`；`enum class` 里可以出现非法值 |
| 动作类型 | `sealed interface` + `record` + 模式匹配 | `std::variant` + `std::visit`，同样编译期穷尽 |
| 待配对的卖出日 | 哨兵整数 `-1` | `std::optional<int>`，`.value()` |
| 倒序遍历 | `list.reversed()` | `reversed \| std::views::reverse` |
