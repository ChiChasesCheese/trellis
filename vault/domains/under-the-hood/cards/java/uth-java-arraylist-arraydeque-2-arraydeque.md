---
id: uth-java-arraylist-arraydeque-2-arraydeque
node: java.arraylist-arraydeque
type: qa
step: 2
---
## Q
**ArrayDeque 怎么两端 O(1)**｜Java · OpenJDK 25

`ArrayDeque` 用什么结构做双端队列？数组长度是 2 的幂吗？

## A
**结构。** 环形数组（circular array）：`head` 指向队首元素，`tail` 指向下一个空位，下标走到头就绕回 0。

**细节。**

- `addFirst` 把 `head` 减 1（小于 0 绕到末尾）再写入；`addLast` 写入 `tail` 再加 1；两者相遇就满了，立刻 `grow`。
- 长度不是 2 的幂：JDK 8 及以前是，用位与取模；JDK 9 起改用比较判断绕回。
- 初始长 17；长度小于 64 时扩为 `2n+2`，否则加 50%：`17 36 74 111 166 249`。

**为什么。** 环形数组两端都不需要搬动元素，也没有每个节点的对象头和指针。

**对应 LeetCode：** LC 641 设计循环双端队列 · LC 622 设计循环队列
