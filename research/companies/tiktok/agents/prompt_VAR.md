# Revise agent — TikTok pattern problem-list cards: put every tier-A problem under a pattern (group V)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Edit only the problem-list
cards `vault/interviews/core/leetcode/tiktok/cards/patterns/tlc-patterns-*-problems.md`. Scratch in `/tmp/var_V/`.
`git checkout uv.lock` whenever uv touches it. Card rules: `research/companies/tiktok/CARDS.md`.

Chi (2026-10-31) wants every tier-A problem reachable from a pattern card.

1. Add these six LeetCode problems to the list card of the pattern they fit (put each in the matching variant group,
   marked 「（高频）」): LC 572 另一个树的子树 and LC 101 对称二叉树 (tree DFS), LC 83 删除排序链表中的重复元素 (linked
   list), LC 470 用 Rand7() 实现 Rand10() and LC 1247 交换字符使得字符串相同 (math), LC 311 稀疏矩阵的乘法 (hashing).
2. These 39 TikTok custom problems (slugs; whole cards at `vault/interviews/core/leetcode/tiktok/cards/*/tlc-<slug>-0-whole.md`):
   tt-lru-cache-ttl（带 TTL 的 LRU 缓存（含 LFU / 加权 / 线程安全追问））; tt-islands-follow-ups（岛屿数量及其追问集合）; tt-course-schedule-output-path（课程表：输出可行学习路径 / 最短路径）; tt-reverse-k-group-variants（K 个一组翻转链表的变体（尾部、从尾部起、偶数长度组））; tt-largest-number-below-n-from-digits（用给定数字组成小于 N 的最大数）; tt-rate-limiter-implementation（手写限流器（滑动窗口 / 令牌桶））; tt-basic-calculator-ladder（计算器梯度题（无括号 -> 括号与一元负号，先校验再求值））; tt-concurrency-limited-runner（限制并发数的异步任务执行器）; tt-deep-merge-nested-json（合并两个嵌套 JSON）; tt-max-path-sum-with-path（二叉树最大路径和并还原 / 打印路径）; tt-path-sum-n-ary-prefix-sum（N 叉树路径和计数（暴力被拒，要前缀和））; tt-fixed-array-deque-o1（定长数组实现双端队列 / 列表（全部操作 O(1)））; tt-grid-min-cost-fuel-recharge（网格最小代价路径（障碍 / 加油站 / 油量 K））; tt-kv-store-snapshot-restore（内存 KV 存储：快照与恢复（序列化））; tt-array-min-heap（用数组手写最小堆（并用它按先修关系排课））; tt-ring-walk-count（环上走 n 步回到起点的方案数）; tt-delete-window-balance-even-odd（删除长度 k 的窗口使奇偶下标和相等）; tt-nested-comment-tree（由扁平记录构建嵌套评论树）; tt-valid-parenthesis-string-print-all（含星号的有效括号 + 输出所有合法字符串）; tt-currency-conversion-queries（汇率换算查询（多跳 / 无解返回 -1））; tt-fish-decaying-ponds（鱼塘捕鱼：产量递减时的最大收获）; tt-seller-task-scheduler（卖家任务调度器（轮转 + VIP + 优先级））; tt-all-simple-paths（枚举有向图中的所有简单路径（含环的情况））; tt-agent-tool-call-tracer（Agent 工具调用的事件追踪）; tt-removable-timestamp-task-scheduler（可删除任务的时间戳调度器（popTask））; tt-pythagorean-triple-in-array（整数数组中的勾股三元组）; tt-idempotent-versioned-update（幂等、带版本号的数据更新）; tt-ai-assisted-order-validator（AI 辅助编码：OrderValidator（规则 DAG））; tt-most-frequent-ties-smaller（出现次数最多的元素（并列取较小的））; tt-sorted-array-more-than-n-over-3（有序数组中出现次数超过 n/3 的数）; tt-longest-zigzag-grid-path（网格中最长的之字形递增路径）; tt-contiguous-memory-allocator（连续内存分配器（first-fit、拆分与合并））; tt-water-jug-shortest-operations（水壶问题：输出最短操作序列）; tt-die-beats-probability（一个骰子掷出更大点数的概率）; tt-spiral-matrix-constant-space（螺旋矩阵：O(1) 额外空间且不修改输入）; tt-login-count-per-user-per-day（日志流中统计每个用户每天登录次数）; tt-flatten-multilevel-list-skip-empty（展平多级链表（值为空的嵌套节点要排除））; tt-subarray-max-min-plus-max（长度至少为 2 的子数组，最大化 min + max）; tt-inorder-string-iterator（二叉树中序字符迭代器）
   For each, choose the pattern its main solution really uses (one card; two only when the solution truly combines
   two, e.g. LRU with TTL = design + heap) and add it under a group 「TikTok 变体」 at the end of that card's list, as
   「<中文名>（一句话：用到的结构）」.
3. For every problem added, append a folded block after the card's existing blocks:
   `**例题：** <LC n 名字 | 中文名>`, one or two sentences of statement, then the main solution from its whole card
   (comments / blank lines may go, logic unchanged; classes stay whole). Verify each block on the first example of its
   statement in a scratch harness (design classes: replay the example operations).
4. Never delete or rewrite existing content.

Gate: `uv run python research/companies/tiktok/tools/gate_cards.py <changed files>` (0 problems),
`uv run python scripts/plain_style.py <changed files>` ok, `uv run trellis --domain tiktok-lc validate` 0 errors.

Reply (≤ 8 lines): which card got which problems, anything you could not place, gate results.
