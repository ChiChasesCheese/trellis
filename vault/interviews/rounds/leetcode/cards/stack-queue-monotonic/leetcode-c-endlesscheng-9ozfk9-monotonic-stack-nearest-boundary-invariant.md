---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-nearest-boundary-invariant
node: stack-queue-monotonic.monotonic-stack-nearest-boundary
type: cloze
anki: 1787272403004
tags: [concept-cloze, invariant, leetcode, recall]
---
求左侧最近严格更大元素时，处理 nums[i] 前要弹出所有 {{c1::值小于等于 nums[i]}} 的栈顶。

栈内保存下标，且其对应值始终满足选定的严格单调性。；处理 x 前，弹出所有不可能作为 x 的目标边界、也不可能服务未来元素的栈顶。；弹栈完成后，若栈非空，栈顶就是当前方向上最近的合格边界。

**Evidence**

一、单调栈 > §1.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.01%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E6%B1%82%E6%9C%80%E8%BF%91%E6%94%AF%E9%85%8D%E8%BE%B9%E7%95%8C)
