---
id: leetcode-c-endlesscheng-v2rxsn-backtracking-enumeration-template
node: backtracking-search.backtracking-enumeration
type: cloze
anki: 1787272463779
tags: [concept-cloze, leetcode, recall, template]
---
保存回溯路径到答案时使用 {{c1::path[:]}}，避免后续修改污染结果。

```
def subsets(nums):
    ans = []
    path = []
    def dfs(i):
        if i == len(nums):
            ans.append(path[:])
            return
        dfs(i + 1)
        path.append(nums[i])
        dfs(i + 1)
        path.pop()
    dfs(0)
    return ans
```

**Evidence**

一、技巧类题目：回溯

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.04%20-%20%E5%9B%9E%E6%BA%AF%E4%B8%8E%E4%BA%8C%E8%BF%9B%E5%88%B6%E6%9E%9A%E4%B8%BE)
