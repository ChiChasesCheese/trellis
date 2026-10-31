# 回溯

枚举所有方案的 DFS：子集、组合、排列、分割、N 皇后。选择 / 递归 / 撤销三步，剪枝和去重决定快慢。加上记忆化就变成动态规划。

**先做（TikTok P1–P4 与经典题单，24 道）**

- [[tlc-longest-substring-without-repeating-characters-0-whole|LC 3 无重复字符的最长子串]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-subsets-0-whole|LC 78 子集]]（中等）· TikTok P2 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-jump-game-0-whole|LC 55 跳跃游戏]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-word-search-0-whole|LC 79 单词搜索]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-restore-ip-addresses-0-whole|LC 93 复原 IP 地址]]（中等）· TikTok P3
- [[tlc-permutations-0-whole|LC 46 全排列]]（中等）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-combination-sum-0-whole|LC 39 组合总和]]（中等）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-word-search-ii-0-whole|LC 212 单词搜索 II]]（困难）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · Top Interview 150
- [[tlc-generate-parentheses-0-whole|LC 22 括号生成]]（中等）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-n-queens-0-whole|LC 51 N 皇后]]（困难）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-valid-parenthesis-string-0-whole|LC 678 有效的括号字符串]]（中等）· TikTok P3 · NeetCode 150
- [[tlc-combinations-0-whole|LC 77 组合]]（中等）· TikTok P4 · Amazon · Top Interview 150
- [[tlc-unique-paths-0-whole|LC 62 不同路径]]（中等）· TikTok P4 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100
- [[tlc-stickers-to-spell-word-0-whole|LC 691 贴纸拼词]]（困难）· TikTok P4
- [[tlc-palindrome-partitioning-0-whole|LC 131 分割回文串]]（中等）· TikTok P4 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-24-game-0-whole|LC 679 24 点游戏]]（困难）· TikTok P4
- [[tlc-maximum-length-of-a-concatenated-string-with-unique-characters-0-whole|LC 1239 串联字符串的最大长度]]（中等）· TikTok P4
- [[tlc-letter-combinations-of-a-phone-number-0-whole|LC 17 电话号码的字母组合]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-combination-sum-ii-0-whole|LC 40 组合总和 II]]（中等）· TikTok B · NeetCode 150
- LC 52 N 皇后 II（困难）· Top Interview 150
- [[tlc-subsets-ii-0-whole|LC 90 子集 II]]（中等）· TikTok B · NeetCode 150
- [[tlc-coin-change-0-whole|LC 322 零钱兑换]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-partition-equal-subset-sum-0-whole|LC 416 分割等和子集]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-target-sum-0-whole|LC 494 目标和]]（中等）· TikTok B · NeetCode 150

**再做（其余牌组里的题，16 道）**

- LC 37 解数独（困难）· Amazon
- [[tlc-permutations-ii-0-whole|LC 47 全排列 II]]（中等）· TikTok B
- [[tlc-unique-binary-search-trees-ii-0-whole|LC 95 不同的二叉搜索树 II]]（中等）· TikTok B
- [[tlc-path-sum-ii-0-whole|LC 113 路径总和 II]]（中等）· TikTok B
- [[tlc-word-ladder-ii-0-whole|LC 126 单词接龙 II]]（困难）· TikTok B · Amazon
- [[tlc-word-break-ii-0-whole|LC 140 单词拆分 II]]（困难）· TikTok B · Amazon
- LC 282 给表达式添加运算符（困难）· TikTok C
- LC 291 单词规律 II（中等）· TikTok C
- LC 294 翻转游戏 II（中等）· TikTok C
- [[tlc-remove-invalid-parentheses-0-whole|LC 301 删除无效的括号]]（困难）· TikTok B
- [[tlc-additive-number-0-whole|LC 306 累加数]]（中等）· TikTok B
- [[tlc-matchsticks-to-square-0-whole|LC 473 火柴拼正方形]]（中等）· TikTok B
- LC 489 扫地机器人（困难）· TikTok C
- [[tlc-partition-to-k-equal-sum-subsets-0-whole|LC 698 划分为k个相等的子集]]（中等）· TikTok B
- [[tlc-letter-case-permutation-0-whole|LC 784 字母大小写全排列]]（中等）· TikTok B
- [[tlc-minimum-moves-to-spread-stones-over-grid-0-whole|LC 2850 将石头分散到网格图的最少移动次数]]（中等）· TikTok B
