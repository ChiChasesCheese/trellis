---
id: uth-devtools-diff-2-preprocess
node: devtools.diff
type: qa
step: 2
---
## Q
**diff 先做了哪些预处理**｜Git · xdiff · 2.56

真正跑 Myers 之前，git 怎么先把问题变小？

## A
**结构。** 先把每一行映射成一个整数（`minimal_perfect_hash`），之后比较两行只是比较两个整数。

**细节。**

- `xdl_trim_ends`：先剪掉开头和结尾完全相同的行
- `xdl_cleanup_records`：在另一个文件里根本没出现的行，直接判为增或删，不进入主算法
- 在另一文件里出现次数过多的行（上限约为行数的平方根，最多 1024），夹在可丢弃的行中间时也会被丢弃

**为什么。** 典型的改动只占文件一小段，剪掉两头和“注定不匹配”的行，核心算法面对的就小得多。

**坑。** 丢弃高频行是启发式，结果可能不是最短；`--minimal` 会把这个上限取消。

**对应 LeetCode：** LC 49 字母异位词分组 · LC 1143 最长公共子序列
