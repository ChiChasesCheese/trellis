---
id: hl-cx-arraydeque-vs-arraylist
node: foundations.complexity
type: qa
step: 45
---
## Q
`ArrayDeque.addFirst` 摊还 O(1)，而 `ArrayList.add(0, x)` 是 O(n)。要频繁在头部插入，为什么 `ArrayDeque` 可以而 `ArrayList` 不行？

## A
`ArrayList` 是普通数组，元素必须从下标 0 紧密排列，头部插入要把所有元素后移一位，O(n)。

`ArrayDeque` 是**环形数组**，用 `head`、`tail` 两个下标，头部插入只需 `head` 回退一格（对容量取模），不挪元素；满了才扩容，摊还 O(1)。
