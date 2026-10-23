---
id: hl-omap-rotation
node: foundations.ordered-maps-trees
type: qa
step: 7
---
## Q
平衡树里的旋转（rotation）是什么？为什么它不会破坏 BST 的有序性？

## A
旋转是平衡树调整形状的基本动作。右旋（在 y 处）：y 的左孩子 x 上来成为父节点，y 变成 x 的右孩子，x 原来的右子树 B 转交给 y 当左子树；左旋是它的逆操作。

旋转前后的**中序遍历都是 A x B y C**：顺序没变，只是 x 和 y 的上下关系换了。所以随时可用来调整形状而不破坏 BST 性质，而且只改常数个指针，O(1)。
