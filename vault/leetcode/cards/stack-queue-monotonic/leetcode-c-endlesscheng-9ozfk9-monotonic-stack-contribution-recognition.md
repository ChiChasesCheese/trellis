---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-contribution-recognition
node: stack-queue-monotonic.monotonic-stack-contribution
type: cloze
anki: 1788743827535
tags: [concept-cloze, leetcode, recall, recognition]
---
求所有子数组最小值或最大值之和时，应把“枚举子数组”改成 {{c1::枚举元素贡献}}。

将所有子数组的聚合值改为逐元素计数贡献。若 nums[i] 作为某类极值可覆盖 L 种左端点和 R 种右端点，则它对总和贡献 nums[i] × L × R；单调栈用于找唯一归属的左右边界。

**Evidence**

三、贡献法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.03%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E8%B4%A1%E7%8C%AE%E6%B3%95)
