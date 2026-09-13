---
id: leetcode-q-strobogrammatic-number-pattern
node: strings.string
type: qa
anki: 1787175410609
tags: [lc::246, leetcode, pattern, recall]
---
## Q
如何判断一个数字字符串是否为「对称数」（strobogrammatic number，旋转180度后与原数相同）？

## A
用哈希表记录旋转对应关系 {'0':'0','1':'1','8':'8','6':'9','9':'6'}；遍历字符串反转后的每个字符，若不在映射表中直接返回False，否则替换成对应字符收集到结果列表；最后判断结果列表是否等于原字符列表。核心思路：对称数等价于「反转字符串 + 逐位映射」后与原字符串相同。

**Evidence**

num2reversion = {'6':'9','9':'6','8':'8','1':'1','0':'0'}; 对 reversed(lst) 中每个字符做映射校验并比较 res == lst

[原文 ↗](obsidian://open?vault=lc&file=questions%2F246%20-%20Strobogrammatic%20Number)
