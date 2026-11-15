---
slug: nested-list-weight-sum-ii
---
## Q
**LC 364 嵌套列表加权和 II**｜Medium

嵌套列表里的元素是整数或列表。与 LC 339 相反：整数的权重是「最大深度 - 自己的深度 + 1」，即最浅的整数权重最大。返回加权和。接口：`isInteger()`、`getInteger()`、`getList()`。

## A
**一句话。** 按层剥开：每剥一层，把已累计的「整数之和」再加进总和一次；这样最外层的整数被加了「总层数」次，最深层的只被加 1 次，正好是逆序权重。

```python
def depth_sum_inverse(nested_list):
    total = level_sum = 0
    level = nested_list
    while level:
        nxt = []
        for ni in level:
            if ni.isInteger():
                level_sum += ni.getInteger()
            else:
                nxt.extend(ni.getList())    # 下一层
        total += level_sum       # 之前的数再多算一次
        level = nxt
    return total
```

**复杂度。** 时间 `O(n)`（`n` 为元素总数），空间 `O(n)`。

**易错点。**
- `total += level_sum` 放在循环外：必须每处理完一层累加一次。
- 把 `level_sum` 每层重置：它要保持累计，才能让浅层的数被重复计入。
- 先求最大深度再二次遍历：可以，但多一遍遍历；这个写法一遍就行。

**追问。**
- 为什么这样累加得到逆序权重？：深度为 `d` 的整数从第 `d` 层起每层都被加一次，共 `最大深度 - d + 1` 次。
- 用 DFS 怎么做？：先 DFS 求最大深度，再 DFS 按 `最大深度 - 深度 + 1` 乘权重。

**同模式。** LC 339 嵌套列表加权和、LC 341 扁平化嵌套列表迭代器、LC 102 二叉树的层序遍历、LC 690 员工的重要性
