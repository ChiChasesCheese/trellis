---
id: cc-algorithms-dp-banded
node: algorithms.dp
type: cloze
---
When edit distance only has to be *compared against* a bound k, every cell with {{c1::`|i - j| > k`}} is already unreachable, so only a band of width {{c2::2k + 1}} matters and the cost drops from O(n·m) to {{c3::O(n·k)}}. Two shortcuts come first: if {{c4::`abs(len(a) - len(b)) > k`}} the answer is immediately "no", and identical strings have distance {{c5::0}} — which for the "exactly one edit" question means false, the single most common wrong answer.

## zh
当编辑距离只需要*与*上界 k *比较*时，所有满足 {{c1::`|i - j| > k`}} 的格子本就不可达，所以只有宽度为 {{c2::2k + 1}} 的带状区域有意义，代价从 O(n·m) 降到 {{c3::O(n·k)}}。有两条捷径要先走：若 {{c4::`abs(len(a) - len(b)) > k`}} 则答案立刻是「否」；而完全相同的字符串距离是 {{c5::0}} —— 对「恰好一次编辑」这个问题来说这意味着 false，也是最常见的错误答案。
