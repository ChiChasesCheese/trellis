---
id: uth-java-arraylist-arraydeque-3-vs-stack
node: java.arraylist-arraydeque
type: qa
step: 3
---
## Q
**栈和队列该用 Stack、LinkedList 还是 ArrayDeque**｜Java · OpenJDK 25

做栈或队列时，官方文档为什么推荐 `ArrayDeque`？它为什么不允许放 `null`？

## A
**结构。** `Stack` 继承 `Vector`，方法都带 `synchronized`；`LinkedList` 每个元素一个 `Node`（`item`、`next`、`prev`）；`ArrayDeque` 是一个连续数组。

**细节。**

- 文档原话：作栈时可能比 `Stack` 快，作队列时可能比 `LinkedList` 快。
- 数组不用逐个元素分配对象，遍历时内存连续、缓存友好；`Stack` 的每次调用还要加锁。
- `pollFirst` 靠「该槽为 `null`」判断空，所以 `addFirst(null)` 直接抛 `NullPointerException`。

**为什么。** 数组把分配成本摊到整块上，没有每个元素一个对象的开销。

**坑。** `Deque` 做栈要用 `push`、`pop`，别混用 `add`、`remove`，否则方向反了。

**对应 LeetCode：** LC 20 有效的括号 · LC 232 用栈实现队列
