---
id: hl-oa01-cpp-followups
node: problems.oa01-job-chain
type: qa
step: 18
---
## Q
任务链报表的 C++ 版，面试官可能追问内存与时间、`string_view` 悬空、`unordered_map` 最坏情况，怎么答？

## A
- **百万行内存和时间**：`vector<string>` 每个 `string` 在 libc++ 里 24 字节，≤ 22 字符的串内联（SSO）不额外分配；`unordered_map` 每个节点一次堆分配，是最大开销。更快：id 排序去重得稠密下标，用 `vector` + 二分，或开放寻址哈希。时间 O(n) 期望加最后 O(c log c) 排序（c = 链数）。
- **能否边读边处理**：解析可流式（逐行 `getline`），但悬空、多前驱、环要看全部 job，所以 job 要存，省掉的只是原始字符串。
- **`string_view` 何时悬空**：指向临时对象（`string_view v = make_string();`）；view 存进长寿命容器而底层字符串先析构；`string` 被修改后重新分配。
- **`unordered_map` 最坏 O(n)**：所有 key 落进同一个桶时退化；`int` 的标准哈希是恒等，对抗输入可构造冲突，可换 splitmix64，或排序 + 二分得到确定的 O(n log n)。
- **测试**：单行规则、跨行规则、格式、边界（空、单条、`INT_MAX`、`LLONG_MAX`）、CRLF、随机大输入对照暴力解，全部在 `-fsanitize=address,undefined` 下跑。
