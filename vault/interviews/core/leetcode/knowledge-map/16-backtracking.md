# 回溯

枚举所有方案的 DFS：子集、组合、排列、分割、N 皇后。选择 / 递归 / 撤销三步，剪枝和去重决定快慢。加上记忆化就变成动态规划。

**先做（TikTok P1–P4 与经典题单，24 道）**

- [[lct-longest-substring-without-repeating-characters|LC 3 无重复字符的最长子串]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-subsets|LC 78 子集]]（中等）· TikTok P2 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-jump-game|LC 55 跳跃游戏]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-word-search|LC 79 单词搜索]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-restore-ip-addresses|LC 93 复原 IP 地址]]（中等）· TikTok P3
- [[lct-permutations|LC 46 全排列]]（中等）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-combination-sum|LC 39 组合总和]]（中等）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-word-search-ii|LC 212 单词搜索 II]]（困难）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · Top Interview 150
- [[lct-generate-parentheses|LC 22 括号生成]]（中等）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-n-queens|LC 51 N 皇后]]（困难）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-valid-parenthesis-string|LC 678 有效的括号字符串]]（中等）· TikTok P3 · NeetCode 150
- [[lct-combinations|LC 77 组合]]（中等）· TikTok P4 · Amazon · Top Interview 150
- [[lct-unique-paths|LC 62 不同路径]]（中等）· TikTok P4 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100
- [[lct-stickers-to-spell-word|LC 691 贴纸拼词]]（困难）· TikTok P4
- [[lct-palindrome-partitioning|LC 131 分割回文串]]（中等）· TikTok P4 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-24-game|LC 679 24 点游戏]]（困难）· TikTok P4
- [[lct-maximum-length-of-a-concatenated-string-with-unique-characters|LC 1239 串联字符串的最大长度]]（中等）· TikTok P4
- [[lct-letter-combinations-of-a-phone-number|LC 17 电话号码的字母组合]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-combination-sum-ii|LC 40 组合总和 II]]（中等）· TikTok B · NeetCode 150
- LC 52 N 皇后 II（困难）· Top Interview 150
- [[lct-subsets-ii|LC 90 子集 II]]（中等）· TikTok B · NeetCode 150
- [[lct-coin-change|LC 322 零钱兑换]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-partition-equal-subset-sum|LC 416 分割等和子集]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-target-sum|LC 494 目标和]]（中等）· TikTok B · NeetCode 150

**再做（其余牌组里的题，16 道）**

- LC 37 解数独（困难）· Amazon
- [[lct-permutations-ii|LC 47 全排列 II]]（中等）· TikTok B
- [[lct-unique-binary-search-trees-ii|LC 95 不同的二叉搜索树 II]]（中等）· TikTok B
- [[lct-path-sum-ii|LC 113 路径总和 II]]（中等）· TikTok B
- [[lct-word-ladder-ii|LC 126 单词接龙 II]]（困难）· TikTok B · Amazon
- [[lct-word-break-ii|LC 140 单词拆分 II]]（困难）· TikTok B · Amazon
- [[lct-expression-add-operators|LC 282 给表达式添加运算符]]（困难）· TikTok C
- [[lct-word-pattern-ii|LC 291 单词规律 II]]（中等）· TikTok C
- [[lct-flip-game-ii|LC 294 翻转游戏 II]]（中等）· TikTok C
- [[lct-remove-invalid-parentheses|LC 301 删除无效的括号]]（困难）· TikTok B
- [[lct-additive-number|LC 306 累加数]]（中等）· TikTok B
- [[lct-matchsticks-to-square|LC 473 火柴拼正方形]]（中等）· TikTok B
- [[lct-robot-room-cleaner|LC 489 扫地机器人]]（困难）· TikTok C
- [[lct-partition-to-k-equal-sum-subsets|LC 698 划分为k个相等的子集]]（中等）· TikTok B
- [[lct-letter-case-permutation|LC 784 字母大小写全排列]]（中等）· TikTok B
- [[lct-minimum-moves-to-spread-stones-over-grid|LC 2850 将石头分散到网格图的最少移动次数]]（中等）· TikTok B
