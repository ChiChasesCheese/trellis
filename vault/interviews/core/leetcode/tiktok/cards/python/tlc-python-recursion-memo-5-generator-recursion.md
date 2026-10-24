---
id: tlc-python-recursion-memo-5-generator-recursion
node: python.recursion-memo
type: qa
step: 5
---
## Q
**Python 递归｜生成器递归与 `yield from`**

中序遍历、排列枚举这类「一个一个产出结果」的递归，写成生成器有什么好处？`yield from` 做了什么？

## A
递归生成器每次 `yield` 一个结果后暂停，调用方用多少取多少；不用先把所有结果存进列表。

```python
from collections.abc import Iterator
from itertools import islice
def inorder(n: TreeNode | None) -> Iterator[int]:
    if n:
        yield from inorder(n.left)     # 把左子树产出的值逐个转发出去
        yield n.val
        yield from inorder(n.right)
bst = TreeNode(5, TreeNode(3, TreeNode(2), TreeNode(4)), TreeNode(8, None, TreeNode(9)))
print(list(inorder(bst)), list(islice(inorder(bst), 2))[-1])   # [2, 3, 4, 5, 8, 9] 3
```

- `yield from g` 等价于 `for x in g: yield x`，并且正确转发 `send` / `return`。
- 第 2 小的元素只推进到第二个值就停：**提前终止**不访问剩下的节点，而返回完整列表的写法一定走完整棵树。LC 230 二叉搜索树中第 K 小的元素、LC 173 二叉搜索树迭代器（要求 `next` 摊还 `O(1)`，可以用显式栈或生成器）都适用。
- 递归生成器同样受递归深度限制，而且每个值要穿过 `depth` 层 `yield from`，总成本 `O(n * depth)`，不是 `O(n)`；树很深时改成显式栈。
- 排列枚举：

```python
def perms(a: list[int]) -> Iterator[list[int]]:
    if not a:
        yield []
        return
    for i, x in enumerate(a):
        for p in perms(a[:i] + a[i + 1:]):
            yield [x] + p
print(list(perms([1, 2, 3]))[:3], sum(1 for _ in perms([1, 2, 3, 4])))   # [[1,2,3],[1,3,2],[2,1,3]] 24
```

- **坑**：生成器只能消费一次；需要多次使用就 `list(...)`；函数里一旦出现 `yield`，它就是生成器函数，直接 `return value` 不会返回值给调用者。
