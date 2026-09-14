---
id: leetcode-c-endlesscheng-wr1mjp-dynamic-programming-memo-to-tabulation-recognition
node: dp-linear-knapsack.dynamic-programming-memo-to-tabulation
type: cloze
anki: 1787272471380
tags: [concept-cloze, leetcode, recall, recognition]
---
暴力递归反复求解相同参数的子问题时，应改为 {{c1::记忆化搜索/动态规划}}。

先定义状态代表“从当前局面到答案”的子问题，用记忆化搜索验证转移；确定状态依赖方向后，再改写为递推以节省栈或便于优化。

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.07%20-%20%E8%AE%B0%E5%BF%86%E5%8C%96%E6%90%9C%E7%B4%A2%E4%B8%8E%E9%80%92%E6%8E%A8%20Dynamic%20Programming)
