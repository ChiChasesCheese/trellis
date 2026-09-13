# ps11 Factory Cost — report

## 摘要
本题是**重建题（非真题）**。已知线索只有 `catalog/discovery/2026-09/C_batchA.md` `## C4` 里记录的
一句话概述——PracHub 词条《Minimize total factory cost with distance penalties》(Stripe ·
Phone/Technical Screen · Medium · 2026-03-29 最后更新)：**"累计建厂成本 + 相邻工厂距离惩罚 +
可跳过一个工厂"的动态规划题**。本轮（2026-09-03）在写这道题之前，用 WebFetch 重新抓了一次
PracHub 那条 URL 的原始页面，返回内容和 `C_batchA.md` 记录的完全一致——仍然只有这句 Quick
Overview，规则、输入输出格式、函数签名、样例**一个都没有拿到**（页面需要登录/未完全加载完成）。
interviewdb.io 上有裸标题「Factory Cost」的独立词条（Coding/Phone，约 2026-08），1point3acres
有标题「Factory Cost Optimizer」（全站 403，正文拿不到）。三个标题不完全一致，是否为同一题
**未证实**。

因此本题的具体规则——建厂成本怎么累加、距离惩罚怎么分档、"跳过"的确切语义（跳一个 vs 跳 k 个）、
输入输出格式、4 个 part 怎么切——**全部是本仓库自拟**，只保留了"DP + 建厂成本 + 相邻惩罚 + 跳过"
这个主题方向。做成了 Stripe 基建选址（沿一条走廊建结算枢纽机房，机房离太近有冗余对等成本）的业务
包装，核心仍然是线性序列 DP。

## Sources & confidence
**置信度：低**——见上，仅题目主题方向有依据，题面细节 100% 自拟。来源列表见 `problem.md` 底部
"Sources" 一节（`catalog/discovery/2026-09/C_batchA.md` `## C4`、PracHub 原始 URL 二次抓取记录、
interviewdb.io / 1point3acres 的标题存在性确认）。

## 各 part 设计思路
1. **Part 1**：所有候选工厂全部建设，`TOTAL = sum(build_cost)`。纯累加，建立货币解析基础
   （`parse_money_to_cents`，整数分，禁止浮点）。
2. **Part 2**：在 Part 1 基础上加"相邻建成工厂之间的距离惩罚"——按走廊顺序看每一对相邻建成工厂，
   查一张距离分档表（闭区间 `[min_dist,max_dist]`，`max_dist` 可以是字面量 `inf`）。分档表本身
   顺序不可信，要先按 `min_dist` 排序（复用 ps02 的纪律）。距离落在分档表的"缺口"里是一个显式的、
   有断言的错误路径，而不是让它崩溃。
3. **Part 3**：允许跳过**至多一个**工厂来降低总成本。没有对每个候选 j 都重新 O(n) 扫一遍，而是
   预计算 n-1 条相邻惩罚的**前缀无效计数 + 前缀金额和**，让每个候选 j（"跳过 j"）的总成本变成
   O(1) 增量计算——这正是 skills_matrix.md 里 **A01**（前缀和 + argmin 带 tie-break，对应
   LC 2483）的模式。跳过端点工厂（第一个/最后一个）不需要"桥接惩罚"，跳过中间工厂需要新查一次
   `position[j+1]-position[j-1]` 的桥接距离惩罚。
4. **Part 4**：把"至多跳 1 个"推广成"至多跳 k 个"，退化为标准 DP：`dp[i][s]` = 最后建成的工厂是
   `i`、且在 `i` 之前已经跳过 `s` 个的最小成本；转移要额外做"回溯重建"——不仅要算出最优总成本，
   还要还原出具体跳过了哪些工厂（这是"求最优 / 回溯选中的方案"那一步）。

## Tie-break 设计（S08 的核心落点）
Part 3：候选集合是 `{skip-none} ∪ {skip-j : j=0..n-1}`（排除无效项），比较 key 是
`(total_cost, rank)`，`rank=-1` 给 skip-none，`rank=j` 给 skip-j——Python 的 `min()` 元组比较
天然实现了"总成本最低优先，同成本 skip-none 优先于任何 skip-j，同成本的 skip-j 之间取最小 j"
这个三级 tie-break，不需要额外分支。

Part 4 的 DP 回溯多一层复杂度：DP 转移时同成本优先"跳得更少的那一步"（即更大的前驱 `j`）；
最终在所有满足预算的终止状态里，先比总成本，再比"总跳过数更少"，最后比"最后建成的下标更大"。
`test_dp_tie_break_prefers_larger_j_at_equal_cost` 专门构造了一个人工同分场景验证第二条规则
真的生效（而不是任意一个同分方案都能通过测试）。

## Hidden tests 会考的坑
- Part 2：分档表乱序；距离恰好卡在某档的上/下边界（闭区间两端都要覆盖）；一条工厂链里有两个
  独立的"缺口"时必须报**第一个**（下标最小的那个）。
- Part 3：跳过端点工厂永远不需要桥接惩罚，这个规则会让"跳端点"在非零成本下几乎总是不劣于
  "全建"——因此"skip nothing 本身最优"这个边界只能通过**平局**触发（构造端点 build_cost=0 且
  相关惩罚也是 0，逼成三路平局，靠 tie-break 规则 1 选出 skip-none），而不是靠严格更优；
  `problem.md` 和测试都把这一点显式地写清楚，不留给候选人自己猜。
- Part 4：`k=0` 必须和 Part 2 的成功/报错行为逐字一致（本题专门测试了两种情况）；"只建一个最便宜
  的工厂"这种极端跳过预算；两个非相邻工厂都要跳才能达到最优（不是简单地跳连续一段）。
- 格式：三种错误文案（`no penalty band for distance=<d>`、`no valid configuration`、
  `no valid configuration within skip budget k=<k>`）逐字匹配；`SKIPPED` 列表按走廊顺序、逗号
  连接、不额外加空格。

## Complexity & measured cost
Part 1/2：`O(n)`。Part 3：`O(n)`（前缀和预处理 + 每个候选 O(1)，A01 的关键收益）。Part 4：
`O(n^2 * k)`（`n,k` 均 ≤ 100，按题面本身的约束），加上每次转移一次分档表线性扫描
（≤20 条，可忽略）。实测：100 个工厂、20 条分档、`k=40` 的随机输入，`solution.py` 直接调用
（不经过子进程）耗时约 0.02 秒；`test_perf_100_factories_dp` 通过 `run_script` 子进程测量，
预算 2s / 256MB，实测远低于预算。

## 测试清单
29 个测试——part1: 4 · part2: 6 · part3: 7 · part4: 8；其中 edge: 17 · fmt: 1 · io: 3 ·
perf: 1（part1/part2/part3/part4 markers 与 edge/fmt/io/perf markers 按 pytest 惯例可以叠加，
上面按主 part marker 计数）。

## 本题覆盖的知识点
- **A01**（前缀和 + argmin，带 tie-break）：Part 3 的核心算法——预计算前缀无效计数与前缀金额和，
  把每个"跳过 j"候选的总成本降到 O(1)，再用显式三级 tie-break 做 argmin，直接对应
  LC 2483 Minimum Penalty for a Shop 的解题模式。
- **S06**（整数最小单位金额、显式舍入）：全程用整数分（`parse_money_to_cents`/`fmt_cents`），
  金额字符串最多 2 位小数、多一位直接拒绝而不是四舍五入——显式声明了"没有舍入规则，因为输入本身
  不带超过分的精度"这条规则，而不是隐式假设。
- **S13**（区间/off-by-one）：距离惩罚分档是闭区间 `[min_dist,max_dist]`，测试专门覆盖两端边界
  （`dist==min_dist` 和 `dist==max_dist` 分别落在不同档时的正确性），以及"缺口"距离的显式报错
  路径（含"多个缺口，报第一个"的 off-by-one 式下标测试）。
- **S08**（确定性排序与 tie-break）：Part 3/Part 4 的多级 tie-break 规则全部显式写在 `problem.md`
  里并逐条测试到（skip-none 优先、最小下标优先、DP 同分优先更大的前驱下标、终止状态优先更少的
  总跳过数），`SKIPPED` 的输出顺序也固定为走廊顺序而非任何排序。
