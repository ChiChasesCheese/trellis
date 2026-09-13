---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-contribution-invariant
node: stack-queue-monotonic.monotonic-stack-contribution
type: cloze
anki: 1788743827638
tags: [concept-cloze, invariant, leetcode, recall]
---
元素 i 的端点组合数是 {{c1::(i-left) * (right-i)}}，其中 left、right 是它的有效扩展边界。

为每个元素规定唯一的相等值归属规则，例如左边界找严格更小、右边界找小于等于。；左右边界之间的任意子数组都以当前元素为选定规则下唯一负责者。；贡献的端点组合数等于 (i - left) × (right - i)。

**Evidence**

三、贡献法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.03%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E8%B4%A1%E7%8C%AE%E6%B3%95)
