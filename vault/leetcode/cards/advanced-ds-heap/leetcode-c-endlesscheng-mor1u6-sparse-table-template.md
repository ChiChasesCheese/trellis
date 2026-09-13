---
id: leetcode-c-endlesscheng-mor1u6-sparse-table-template
node: advanced-ds-heap.sparse-table
type: cloze
anki: 1787272423805
tags: [concept-cloze, leetcode, recall, template]
---
长度 L 的查询层数取 {{c1::floor(log2(L))}}。

```
def build_sparse_max(nums):
    st = [nums[:]]
    k = 1
    while (1 << k) <= len(nums):
        prev = st[-1]
        half = 1 << (k - 1)
        st.append([max(prev[i], prev[i + half]) for i in range(len(nums) - (1 << k) + 1)])
        k += 1
    return st

def query_sparse_max(st, left, right):
    k = (right - left).bit_length() - 1
    return max(st[k][left], st[k][right - (1 << k)])
```

**Evidence**

§8.7 ST 表（Sparse Table）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.20%20-%20ST%20%E8%A1%A8%EF%BC%88Sparse%20Table%EF%BC%89)
