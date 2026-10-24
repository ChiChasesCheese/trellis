---
id: tlc-python-classes-design-4-iterator
node: python.classes-design
type: qa
step: 4
---
## Q
**Python 设计题｜迭代器类：二叉搜索树迭代器（LC 173）**

`next()` 摊还 `O(1)`、空间 `O(h)` 的 BST 迭代器怎么设计？Python 的迭代器协议（`__iter__` / `__next__`）和这类题的方法式接口是什么关系？

## A
中序遍历的显式栈版本，**暂停在栈里**：栈里存「还没访问、但左子树已展开」的节点。

```python
class BSTIterator:
    def __init__(self, root: TreeNode | None) -> None:
        self.st: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, n: TreeNode | None) -> None:
        while n:                       # 一路向左压栈，栈顶就是当前最小
            self.st.append(n)
            n = n.left

    def next(self) -> int:
        n = self.st.pop()
        self._push_left(n.right)       # 访问完，展开右子树的左链
        return n.val

    def hasNext(self) -> bool:
        return bool(self.st)

bst = TreeNode(7, TreeNode(3), TreeNode(15, TreeNode(9), TreeNode(20)))
it, out = BSTIterator(bst), []
while it.hasNext():
    out.append(it.next())
print(out)     # [3, 7, 9, 15, 20]
```

- 每个节点入栈、出栈各一次，`n` 次 `next` 总计 `O(n)`，摊还 `O(1)`；栈最多 `h`（树高）个元素，空间 `O(h)`，不需要把整棵树先展平成 `O(n)` 的列表。
- Python 自己的协议：`__iter__` 返回迭代器，`__next__` 返回下一个值并在结束时 `raise StopIteration`。**最省事的实现是在 `__iter__` 里写生成器**：

```python
class Countdown:
    def __init__(self, n: int) -> None: self.n = n
    def __iter__(self):
        n = self.n
        while n > 0:
            yield n; n -= 1
print(list(Countdown(3)), list(Countdown(3)))   # [3, 2, 1] [3, 2, 1]：每次 iter 都是新迭代器
```

- 带 `peek` 的迭代器（LC 284）：额外存一个「已取出但未消费」的值。
- 展平嵌套列表迭代器（LC 341）：栈里存迭代器，遇到子列表就压入其迭代器。
