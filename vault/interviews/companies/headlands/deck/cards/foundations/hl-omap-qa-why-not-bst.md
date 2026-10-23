---
id: hl-omap-qa-why-not-bst
node: foundations.ordered-maps-trees
type: qa
step: 35
---
## Q
面试题：为什么不直接用普通二叉搜索树？

## A
推荐答法：「高度取决于插入顺序，升序插入会退化成链表，O(n)。价格、时间戳、自增 id 恰好常常递增。实验：5000 个升序 key 高度就是 5000，随机的只有 28。」
