---
id: uth-devtools-regex-3-go-engines
node: devtools.regex
type: qa
step: 3
---
## Q
**Go 怎么做到既快又线性**｜Go · regexp · 1.25

保证线性，是不是意味着 Go 的正则每次都在慢速模拟 NFA？

## A
**结构。** 编译后按情况选三种引擎：onepass（模式无歧义，一遍扫完）→ 位状态回溯（bitstate backtracker）→ NFA 模拟。

**细节。**

- 回溯器给每个（指令, 位置）一位 `visited`，每个状态最多走一次，所以仍然是线性
- 只在指令数不超过 500、输入长度小于 262144 ÷ 指令数时才用它
- 否则落到 NFA，并行推进所有候选线程

**为什么。** 小输入上回溯常数小、速度快；大输入再用 NFA 保证上界。靠“记住走过的状态”，回溯也能变线性。

**对应 LeetCode：** LC 139 单词拆分 · LC 10 正则表达式匹配
