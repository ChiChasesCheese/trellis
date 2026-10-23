---
id: hl-hc02-naive-approaches
node: problems.hc02-merge-k-streams
type: qa
step: 4
---
## Q
合并 k 个有序 List 时，「拼接后排序」和「依次两两合并」的复杂度和实测差别是什么？面试里该怎么诚实评价它们？

## A
- **拼接后 `Collections.sort`**：O(N log N)，没用上各序列已有序。但 k=1000、每条 1000 个 `int`（N=10⁶）实测只要约 **50 ms**，比堆合并还快：TimSort 会识别已有序的 run 再归并，实际就是 k 路归并。
- **依次两两合并** `acc = mergeTwo(acc, list_i)`：第 i 次要拷贝已合并的 `acc`（约 `i·N/k`），总 `Σ ≈ N·k/2`，即 **O(N·k)**；同样数据约 **1230 ms**，是堆版本的 11 倍；k=10⁴ 时每个元素平均被拷贝 5000 次。
- **堆合并** `MergeK.merge`（装箱 `Integer`）约 110 ms；`mergeLongs`（`long[]` 无装箱）约 65 ms。

诚实结论：**内存里的 List 用拼接 + 排序在 Java 里很难被打败**。堆的价值在：(1) 流式 / 惰性——输入放不进内存或是无限的；(2) 只要前 m 个：O(k + m log k)；(3) 额外空间 O(k)；(4) 可以并发地边产生边合并。拼接排序不行的输入：数据是流，或只要合并后的前 10 个却要排完全部。
