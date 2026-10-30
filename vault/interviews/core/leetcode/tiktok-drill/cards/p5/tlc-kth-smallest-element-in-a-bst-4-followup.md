---
id: tlc-kth-smallest-element-in-a-bst-4-followup
node: p5.kth-smallest-element-in-a-bst
type: qa
step: 4
---
## Q
**LC 230 二叉搜索树中第 K 小的元素**｜追问

面试官接着问：（1）树经常被修改，又要频繁查第 `k` 小，怎么办？（2）第 `k` **大**怎么改？（3）想一次一个地按升序取元素（不一次读完整棵树）？

## A
1. **顺序统计树（order-statistic tree）**：每个节点额外存「以它为根的子树节点数」`size`。查询时看左子树大小 `left`：`k <= left` 去左边；`k == left + 1` 命中当前节点；否则 `k -= left + 1` 去右边。每层一次比较，`O(h)`；插入 / 删除沿路径更新 `size`，同样 `O(h)`。平衡树（红黑树、AVL）能保证 `h = O(log n)`。

```python
def kth_by_size(root: TreeNode | None, k: int, size: dict[TreeNode, int]) -> int:
    node = root
    while node:
        left = size.get(node.left, 0)          # 左子树节点数；None 查不到，按 0 算
        if k <= left:
            node = node.left
        elif k == left + 1:
            return node.val
        else:
            k -= left + 1
            node = node.right
    raise ValueError("k 超过节点数")
```

`size` 是「节点 → 子树大小」的字典；`[5,3,6,2,4,null,null,1]`、`k = 3` → `3`。
2. **第 `k` 大**：镜像中序（右、根、左），代码里把 `left` / `right` 互换；或者先数出 `n`，再找第 `n - k + 1` 小。
3. **按需取**：用栈保存当前位置，每次调用 `next()` 做一步中序，就是 BST 迭代器（LC 173）；摊销 `O(1)`，空间 `O(h)`。

**Python 提醒**：`dict.get(None, 0)` 对 `None` 键返回默认值 `0`，所以空孩子不用特判；用节点对象当字典键靠的是对象的 `id` 哈希，树被改动时要同步更新字典，否则 `size` 会过期。
