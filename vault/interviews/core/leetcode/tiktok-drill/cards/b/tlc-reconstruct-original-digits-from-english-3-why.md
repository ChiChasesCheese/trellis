---
id: tlc-reconstruct-original-digits-from-english-3-why
node: b.reconstruct-original-digits-from-english
type: qa
step: 3
---
## Q
**LC 423 从英文中重建数字**｜正确性

为什么识别 0~9 必须按 `0, 2, 4, 6, 8, 3, 5, 7, 1, 9` 的顺序，而不能按 `0, 1, 2, …`？每一步「识别字母的计数就是该数字个数」依赖什么不变量？

## A
**不变量。** 轮到数字 `d` 时，计数 `cnt` 里已经扣掉了之前所有已识别数字的单词，此刻字母 `key` 只出现在 `d` 的单词里；所以 `cnt[key]` 恰好等于 `d` 的个数（识别单词里 `key` 只出现一次）。

**为什么这个顺序成立。**
- 第一批 `z, w, u, x, g` 在原始计数里就是唯一的，`zero, two, four, six, eight` 先处理。
- `h` 只在 `three` 和 `eight` 里，8 已扣掉后唯一；`f` 只在 `five` 和 `four` 里，4 已扣掉后唯一；`s` 只在 `six` 和 `seven` 里，6 已扣掉后唯一。
- `o` 在 `zero, one, two, four` 里，0、2、4 都扣掉后只剩 `one`；`i` 在 `five, six, eight, nine` 里，5、6、8 扣掉后只剩 `nine`。

**反例（先数 1）。** `"owoztneoer"`（正确 `"012"`）里有 3 个 `o`。先用 `o` 数 `one`，得到 1 的个数是 `3`，再按 `zero`（`z` 有 1 个）、`two`（`w` 有 1 个）识别，输出 `"01112"`：多出了两个 `1`，因为那两个 `o` 其实属于 `zero` 和 `two`。按正确顺序，`o` 在 0 和 2 被扣掉后只剩 1 个，得到 `"012"`。
