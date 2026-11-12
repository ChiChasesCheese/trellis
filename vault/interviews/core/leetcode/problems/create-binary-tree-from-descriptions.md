---
slug: create-binary-tree-from-descriptions
---
## Q
**LC 2196 根据描述创建二叉树**｜Medium

`descriptions[i] = [parent, child, isLeft]` 表示 `child` 是 `parent` 的左（`1`）或右（`0`）孩子，节点值互不相同。构造二叉树并返回根。

## A
**一句话。** 字典按值按需建节点并连边，根是「当过父节点、从没当过孩子」的那个值。

```python
def create_binary_tree(descriptions):
    nodes = {}
    parents, children = set(), set()
    for p, c, is_left in descriptions:
        for v in (p, c):
            if v not in nodes:      # 第一次见才建节点
                nodes[v] = TreeNode(v)
        if is_left:
            nodes[p].left = nodes[c]
        else:
            nodes[p].right = nodes[c]
        parents.add(p)
        children.add(c)
    (root,) = parents - children
    return nodes[root]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 把第一条描述的父节点当根：示例 1 返回 `20`，应为 `50`。
- 每条描述都重新 `TreeNode(...)`：同一个值变成多个对象，树断开。

**追问。**
- 输入不保证有效怎么办？：校验 `parents - children` 恰好一个，同侧不重复，孩子不能有两个父亲。
- 怎么输出层序？：BFS，缺失的孩子记 `None`，去掉末尾的 `None`。

**同模式。** LC 105 从前序与中序遍历序列构造二叉树、LC 297 二叉树的序列化与反序列化、LC 1361 验证二叉树、LC 1110 删点成林
