---
slug: design-circular-deque
---
## Q
**LC 641 设计循环双端队列**｜Medium

设计容量固定为 `k` 的循环双端队列，支持 `insertFront`、`insertLast`、`deleteFront`、`deleteLast`、`getFront`、`getRear`、`isEmpty`、`isFull`，满了或空了的操作返回 `False` / `-1`。

## A
**一句话。** 定长数组加队首下标 `front` 和元素个数 `size`，所有下标运算对容量取模，队尾位置由 `front + size` 推出。

```python
class MyCircularDeque:
    def __init__(self, k):
        self.a = [0] * k
        self.k = k
        self.front = 0              # 队首下标
        self.size = 0

    def insertFront(self, value):
        if self.isFull():
            return False
        self.front = (self.front - 1) % self.k
        self.a[self.front] = value  # 队首左移一格再写
        self.size += 1
        return True

    def insertLast(self, value):
        if self.isFull():
            return False
        self.a[(self.front + self.size) % self.k] = value
        self.size += 1
        return True

    def deleteFront(self):
        if self.isEmpty():
            return False
        self.front = (self.front + 1) % self.k
        self.size -= 1
        return True

    def deleteLast(self):
        if self.isEmpty():
            return False
        self.size -= 1              # 队尾由 size 决定，减一即删
        return True

    def getFront(self):
        return -1 if self.isEmpty() else self.a[self.front]

    def getRear(self):
        if self.isEmpty():
            return -1
        return self.a[(self.front + self.size - 1) % self.k]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k
```

**复杂度。** 时间每个操作 `O(1)`，空间 `O(k)`。

**易错点。**
- 用 `front` 与 `rear` 两个下标判空满：相等时分不清是空还是满，存个数 `size` 最省事。
- 往前插时 `front - 1` 不取模：Python 里负下标不报错却写到数组末尾以外的错位置，须 `% k`。
- 队尾下标用 `front + size`：取最后一个元素是 `front + size - 1`，别混。

**追问。**
- 不存 `size`，用 `k+1` 的数组怎么判空满？：空为 `front == rear`，满为 `(rear+1) % cap == front`，牺牲一格。
- 多线程使用呢？：加锁，或用 CAS 的环形缓冲区（单生产者单消费者可无锁）。

**同模式。** LC 622 设计循环队列、LC 707 设计链表、LC 232 用栈实现队列、LC 225 用队列实现栈
