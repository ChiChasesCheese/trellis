---
slug: binary-tree-level-order-traversal-ii
---
## Q
**LC 107 二叉树的层序遍历 II**｜Medium

返回二叉树自底向上的层序遍历：从叶子所在层到根所在层，每层从左到右。

## A
**一句话。** BFS 按层收集（自顶向下），最后把各层整体反转。

```python
def level_order_bottom(root):
    ans, level = [], [root] if root else []
    while level:
        ans.append([n.val for n in level])
        level = [c for n in level
                 for c in (n.left, n.right) if c]
    return ans[::-1]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 空树返回 `[[]]`：应为 `[]`，`level = [root] if root else []` 让空树跳过循环。
- 反转整条 BFS 序列：`[3,9,20,15,7]` 反转成 `[7,15,20,9,3]`，丢了分层，层内顺序也反了。
- 展开孩子时漏掉 `if c`：`None` 混进下一层，`n.val` 报 `AttributeError`。

**追问。**
- 不想最后反转？：用 `deque`，每收集一层就 `appendleft`。
- 之字形、右视图怎么改？：之字形奇数层反转该层；右视图每层只取最后一个。

**同模式。** LC 102 二叉树的层序遍历、LC 103 之字形层序遍历、LC 199 二叉树的右视图、LC 429 N 叉树的层序遍历
