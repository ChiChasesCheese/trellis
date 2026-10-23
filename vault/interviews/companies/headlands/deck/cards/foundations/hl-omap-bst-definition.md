---
id: hl-omap-bst-definition
node: foundations.ordered-maps-trees
type: qa
step: 3
---
## Q
二叉搜索树（BST）的性质是什么？写出在 BST 里查找 key 的 Java 代码。

## A
性质：**左子树的所有 key < 当前节点的 key < 右子树的所有 key**，对每个节点都成立。查找每一步丢掉一半：例如根 50，查 60，60 > 50 只看右边；到 70，60 < 70 看左边；到 60 找到，共 3 步。

```java
static Node find(Node root, int key) {
    Node cur = root;
    while (cur != null) {
        if (key == cur.key) return cur;
        cur = key < cur.key ? cur.left : cur.right;
    }
    return null;
}
static final class Node {
    final int key;
    Node left, right;
    Node(int key) { this.key = key; }
}
```
查找最多走「树高」步。
