# study/30-articles — 每题一篇中文题解

> **先做题再读**：题解是验收用的，不是读着爽的。格式见 `_TEMPLATE.md`；每篇的代码骨架与该题 `solution.py` 一致（简化，不矛盾）。本表由 `tools/articles_readme.py` 生成，勿手改。

| 文章 | 题目目录 | 轮次 | 最值得带走的一个模式 |
|---|---|---|---|
| [pc01_grouped_aggregation](pc01_grouped_aggregation.md) | `../../loop/rounds/01_first_round/pc01_grouped_aggregation/` | R1 coding | **只要聚合函数满足结合律（sum/count/max 都满足），"分块算局部结果再合并" |
| [pc02_async_paginated_ingestion](pc02_async_paginated_ingestion.md) | `../../loop/rounds/01_first_round/pc02_async_paginated_ingestion/` | R1 coding | **并发时"谁先完成"和"最终顺序"是两件事**——按索引写入预先留好的位置， |
| [pc03_decorators](pc03_decorators.md) | `../../loop/rounds/01_first_round/pc03_decorators/` | R1 coding | 可测试性靠"注入"——真实时钟/真实 `sleep` 换成参数 `clock`/`sleep`， |
| [pc04_big_integer_strings](pc04_big_integer_strings.md) | `../../loop/rounds/01_first_round/pc04_big_integer_strings/` | R1 coding | 加、减、乘三个运算共用同一套"数字字符 ↔ 数值"映射表和"数量级比较" |
| [pc05_subarray_sums_div_k](pc05_subarray_sums_div_k.md) | `../../loop/rounds/01_first_round/pc05_subarray_sums_div_k/` | R1 coding | **任何"子数组和满足某条件"的题，先写出前缀和数组，再看条件变成了前缀和之间的什么关系** |
| [pc06_water_problems](pc06_water_problems.md) | `../../loop/rounds/01_first_round/pc06_water_problems/` | R1 coding | **双指针收缩类问题，正确性不是靠试出来的，是靠"移动另一侧不可能更优"的论证** |
| [pc07_anagram_store](pc07_anagram_store.md) | `../../loop/rounds/01_first_round/pc07_anagram_store/` | R1 coding | **"按某种等价关系分组"的题，核心动作永远是"把等价类映射成一个可哈希的 key"，剩下的都是在这个 `dict[key, list]` 上做增删查改** |
| [pc08_lru_ttl_median](pc08_lru_ttl_median.md) | `../../loop/rounds/01_first_round/pc08_lru_ttl_median/` | R1 coding | **"两个独立机制作用在同一个数据结构上"时，第一件事是想清楚它们各自的触发条件是不是互相干扰——LRU 淘汰和 TTL 过期是两条完全不相交的规则** |
| [pc09_price_data_store](pc09_price_data_store.md) | `../../loop/rounds/01_first_round/pc09_price_data_store/` | R1 coding | **任何"写入乱序到达、按时间查询"的存储题，先维护一个始终有序的 key 列表（`bisect.insort`），查询全部变成二分/切片** |
| [pc10_sql_drill](pc10_sql_drill.md) | `../../loop/rounds/01_first_round/pc10_sql_drill/` | R1 coding | **任何"找出从未出现过的 X"的题，先问自己"NOT IN 的子查询里会不会混进 NULL"，混进就换 NOT EXISTS** |
