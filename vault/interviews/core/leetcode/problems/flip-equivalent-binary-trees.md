---
slug: flip-equivalent-binary-trees
---
## Q
**LC 951 翻转等价二叉树**｜Medium

可以任选若干结点交换其左右子树。判断二叉树 `root1` 能否经过若干次这样的翻转变成 `root2`（结点值互不相同）。

## A
**一句话。** 两根值相等后，要么左对左右对右，要么左对右右对左，两种配对有一种递归成立即可。

```python
def flip_equiv(a, b):
    if not a or not b:
        return a is b            # 两个都空才相等
    if a.val != b.val:
        return False
    return (flip_equiv(a.left, b.left)
            and flip_equiv(a.right, b.right)
            or flip_equiv(a.left, b.right)
            and flip_equiv(a.right, b.left))
```

**复杂度。** 时间 `O(min(n, m))`（值互不相同，每对结点至多被比较常数次），空间 `O(h)`。

**易错点。**
- `not a or not b` 时返回 `False`：两棵都空应为 `True`，所以用 `a is b`。
- 先比左右再比值：值不等时白白递归。

**追问。**
- 值可以重复吗？：那两种配对都可能成立，最坏指数级；改为给每个子树算规范形（孩子的规范形排序后拼接）再比较。
- 为什么复杂度不是指数？：值互不相同时，一个结点只可能与值相同的那个结点配对，另一种配对在值比较时立刻失败。

**同模式。** LC 100 相同的树、LC 101 对称二叉树、LC 572 另一个树的子树、LC 226 翻转二叉树
