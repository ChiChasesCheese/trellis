---
id: hl-hc01-cpp-followups
node: problems.hc01-stock-trading-dp
type: qa
step: 23
---
## Q
C++ 版股票题的追问：`plan` 和 `max_profit` 为什么分开？价格用 `double` 行吗？`std::visit` 比 `holds_alternative` 好在哪？

## A
- **`plan` 与 `max_profit` 分开**：只要数字就别付 O(n·k) 字节的决策表；`try_plan` 在格子数超限时返回 `nullopt`，让调用者决定退化策略。
- **价格是 `double`**：利润加减累积舍入误差，「严格大于才改变」的平局判断不再可靠。金融里用整数 tick 或定点数，这也是题目用 tick 的原因。
- **`std::visit`**：编译器检查穷尽，漏掉一个类型、或以后给 `Move` 增加类型都会编译失败；`holds_alternative` 链不会提醒你，还容易忘写 `else`。
- **`NEG` 为什么取 `LLONG_MIN / 4`**：`NEG` 还要参与 `+price`、`-price`、`-fee`，对 `LLONG_MIN` 减正数是有符号溢出（UB）。
- **`try_plan` 为什么返回 `optional`**：决策表过大是「这次给不出答案」，不是输入错误；价格越界是调用者的错，仍抛异常。
- **证明 DP 对**：写一个枚举所有（买<卖<买<卖……）序列的朴素解随机对拍，再加性质检查。
