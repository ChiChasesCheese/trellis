---
id: tlc-construct-binary-tree-from-preorder-and-inorder-traversal-2-code
node: a.construct-binary-tree-from-preorder-and-inorder-traversal
type: qa
step: 2
---
## Q
**LC 105 从前序与中序遍历序列构造二叉树**｜写出 Python 实现

已知一棵二叉树的前序遍历 `preorder` 和中序遍历 `inorder`（长度相同，至多 3000，元素互不相同，范围 `[-3000, 3000]`），还原并返回这棵树的根节点。要求 `O(n)`。

## A
**思路。** 字典 `index` 记每个值在中序里的下标，定位根 `O(1)`。递归函数只接收中序区间 `[lo, hi)`；根永远是前序迭代器的下一个值，先建左子树再建右子树，消费顺序和前序一致。

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    index = {v: i for i, v in enumerate(inorder)}   # 值 -> 中序下标
    pre = iter(preorder)                            # 前序序列只会被顺序消费一次

    def build(lo: int, hi: int) -> TreeNode | None:  # 还原中序区间 inorder[lo:hi]
        if lo == hi:
            return None
        val = next(pre)                              # 前序的下一个值就是这段的根
        mid = index[val]
        node = TreeNode(val)
        node.left = build(lo, mid)                   # 必须先建左再建右，顺序和前序一致
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder))
```

运行：`[3,9,20,15,7]` 加 `[9,3,15,20,7]` → `[3, 9, 20, None, None, 15, 7]`；`[-1]` 加 `[-1]` → `[-1]`；`[1,2]` 加 `[2,1]` → `[1, 2]`；`[1,2]` 加 `[1,2]` → `[1, None, 2]`。深度 3000 的链状树在默认递归上限下抛 `RecursionError`，`sys.setrecursionlimit(10000)` 后返回正常。

**复杂度。** 时间 `O(n)`：建字典 `O(n)`，每个节点只创建一次、查一次字典；空间 `O(n)`：字典 `O(n)`，递归栈最坏（链状）`O(n)`。

**写法要点。**
- `iter(preorder)` 加 `next(pre)`：不用维护前序下标变量，也不用 `nonlocal`，闭包里直接消费。
- 字典推导式 `{v: i for i, v in enumerate(inorder)}` 一行建好值到下标的映射。
- 递归传区间 `[lo, hi)` 而不是切片：切片每层复制数组，会让总复杂度退化成 `O(n^2)`。
- 空区间用 `lo == hi` 判断，左闭右开让左右子树的区间 `[lo, mid)` 与 `[mid + 1, hi)` 不需要再 `±1` 修正。
