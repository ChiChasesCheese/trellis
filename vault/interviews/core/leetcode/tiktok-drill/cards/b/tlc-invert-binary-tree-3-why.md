---
id: tlc-invert-binary-tree-3-why
node: b.invert-binary-tree
type: qa
step: 3
---
## Q
**LC 226 翻转二叉树**｜正确性

为什么先翻转两个子树再换位是对的？如果把交换拆成两条赋值语句 `root.left = invert(root.right)`、`root.right = invert(root.left)`，会错在哪里？给出具体输出。

## A
**不变量（归纳假设）。** `invert_tree(t)` 返回 `t` 的镜像，且镜像的左子树是原右子树的镜像、右子树是原左子树的镜像。空树的镜像是空树。若两个子树的递归调用都返回正确的镜像，那么把它们对调后挂到同一个根下，整棵树就是镜像。

**为什么能对调。** 镜像把左右整体互换：原来在左边的一切（包括更深层的结构）都跑到右边，且自身也被镜像。递归保证了子树内部已镜像，对调只负责「谁在左谁在右」。

**反例：拆成两条赋值。**
```text
root.left  = invert_tree(root.right)   # 左指针已被覆盖
root.right = invert_tree(root.left)    # 这里读到的 left 是新值
```
- 输入 `[2,1,3]`：第一条后 `left = 3`，第二条算的是 `invert_tree(3)`，`right = 3`。
- 输出 `[2,3,3]`，原来的左孩子 `1` 丢了；正确是 `[2,3,1]`。
- 在 `[4,2,7,1,3,6,9]` 上输出 `[4,7,7,9,9,9,9]`，正确是 `[4,7,2,9,6,3,1]`。

元组赋值 `root.left, root.right = f(右), f(左)` 先完整算出右边两个值再赋值，避开了这个读写顺序问题。迭代写法 `node.left, node.right = node.right, node.left` 同理。
