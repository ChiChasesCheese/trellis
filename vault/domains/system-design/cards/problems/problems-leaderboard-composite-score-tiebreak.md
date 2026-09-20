---
id: problems-leaderboard-composite-score-tiebreak
node: problems.realtime.leaderboard
type: qa
step: 4
tags: [grown]
---
## Q
Relying on a sorted set's default tie-break (lexicographic ordering of the member string) when two players have the same score produces an ordering unrelated to who actually achieved that score first. How can a leaderboard encode "earliest achiever ranks first" directly into the numeric score, and why does the precision of a standard double comfortably support it?

## A
Encode both the primary metric and a time-based tiebreaker into one number: composite_score = raw_score × 10^6 + (period_length_in_seconds − seconds_elapsed_in_period_when_achieved). Because seconds_elapsed is smaller for an earlier achievement, the subtraction produces a larger value for players who reached the same raw_score sooner, so higher composite scores naturally sort first without any special-case logic. This works because a standard double (as used for Redis sorted-set scores) represents integers exactly up to 2^53 (about 9.007×10^15); with a raw score capped at 10^9 and a 10^6 multiplier leaving room for a tiebreak component up to 999,999 (comfortably covering an 86,400-second day), the largest composite score is about 10^15 — well inside the exact-integer range, so no rounding error can corrupt the ordering.

## Q zh
两名玩家分数相同时，如果依赖有序集合的默认并列打破规则（按成员字符串的字典序），排出的顺序和「谁真正先达成这个分数」毫无关系。排行榜要如何把「先达成者排前面」直接编码进数值分数本身？为什么标准双精度浮点数的精度足以支撑这样做？

## A zh
把主指标和一个基于时间的打破并列指标编码进同一个数字：组合分数 = 原始分数 × 10^6 + (周期总秒数 − 达成时本周期内已过秒数)。因为更早达成的玩家「已过秒数」更小，减法结果对他们来说更大，所以在原始分数相同的情况下，更早达成的玩家组合分数更高，自然排在前面，不需要任何特殊逻辑分支。这之所以可行，是因为标准双精度浮点数（Redis 有序集合分数所使用的类型）能精确表示到 2^53（约 9.007×10^15）以内的整数；原始分数上限设为 10^9，乘数 10^6 给打破并列部分留出到 999,999 的空间（足够覆盖一天 86,400 秒），最大组合分数约为 10^15——完全落在精确整数范围之内，不会有舍入误差破坏排序。
