---
id: hl-hc04-followups-precision
node: problems.hc04-queue-mean-snapshot
type: qa
step: 17
---
## Q
追问：均值返回 `double` 不够精确怎么办？128 位够吗？如果元素是 `double`，怎么做滑动窗口均值？

## A
- **精度**：两类误差——累积误差、最后除法的舍入。总和用整数（精确），只有最后一步可能舍入。口述：「累积误差靠整数总和消除；分子分母都能精确表示时 IEEE 除法本身正确舍入，保证最近 double。」需要精确时返回约分分数 `numerator/denominator`，需要十进制让调用者选舍入。我的 `getMean` 保证返回最接近精确值的 `double`；`mean()` 精确。
- **128 位够吗**：n 个 `long` 之和绝对值 ≤ n·2⁶³；n ≤ 2³¹（Java 数组长度上限）→ < 2⁹⁴ < 2¹²⁷，绝对安全。要「任意多」就 `BigInteger`。
- **`double` 元素的滑动窗口均值**：running sum 会累积误差。办法：补偿求和（Kahan），或定期重新求和，或 Welford 在线算法；**NaN / Inf** 进入窗口之后，running sum 再也回不到有限值，需要单独计数处理。同一思路：滚动统计 + 数值稳定性。
- **C++ 追问**：`get_mean` 返回 `double` 还是分数？分数精确可比较；`double` 方便但有舍入。我给两个：`mean()` 精确，`get_mean()` 对精确值只舍入一次。C++ 版用 `__int128` 累加器，不用 `long double`（Apple arm64 上就是 64 位 `double`，尾数最多 64 位，装不下 2¹²⁷ 范围的精确和）。
- 快照该拷贝还是共享：拷贝简单 O(k)；共享需要持久化结构，每版本 O(log n)；取决于快照频率和大小。
