---
id: leetcode-q-k-th-digit-in-infinite-string-pattern
node: topics.uncategorised
type: qa
anki: 1787102262882
tags: [lc::4022, leetcode, pattern, recall]
---
## Q
如何求无限数字串（按位数分段构造）中第k位数字？（如 Nth Digit / K-th Digit in Infinite String）

## A
核心模型：按数字位数d分段。d位数共有 9*10^(d-1) 个（普通版）或本题按'前(d-1)位相同'分组为 9*10^(d-2) 组、每组10个数（因为最后一位在组内变化）。步骤：
1. 先扣除1~9位数(k<=9直接返回)；
2. 循环用 total = 该段数字个数 * d 逐段减k，找到k所在的位数段d；
3. k-=1 转0-indexed；
4. 用 num = 起始值 + k//d 定位到具体数字，pos = k%d 定位到该数字内的第几位；
5. 本题额外的不变量：若前缀b（分组编号/十位数）为奇数，组内10个数按9,8,...,0倒序排列（之字形），偶数则正序，需要在计算num时按奇偶翻转组内偏移 j。

**Evidence**

笔记中给出的两版代码：K-th Digit in Infinite String（本题，含奇偶翻转 num = 10*b + (9-j if b&1 else j)）与 Related 里的 Nth Digit（标准版 num = start + n//d, pos = n%d），二者共享'按位数分段+定位数字+定位位'的模型。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F4022%20-%20K-th%20Digit%20in%20Infinite%20String)
