---
id: problems-bounded-blocking-queue-while-not-if
node: problems.components.bounded-blocking-queue
type: qa
step: 1
tags: [grown]
---
## Q
手写一个有界阻塞队列时，`put` 等待非满、`take` 等待非空的循环，为什么必须写成 `while 谓词: cond.wait()`，写成 `if 谓词: cond.wait()` 会在什么场景下出错？

## A
`if` 只检查一次：`wait()` 返回后不再复核谓词，直接往下执行。这在两种情况下都会错：一是虚假唤醒（spurious wakeup）——`wait()` 允许在没有任何 `notify` 的情况下提前返回；二是即使确实被 `notify()` 唤醒，从『被唤醒』到『重新抢到锁、真正往下跑』之间，可能有另一个同类等待者抢先把条件又改了回去——比如队列只空出一个位置，两个 `put` 线程都被唤醒去检查，第一个抢到锁把位置填满，第二个如果用的是 `if` 就会在队列已满的情况下继续把元素塞进去，直接击穿容量上限。`while` 循环在每次被唤醒后都重新检查一遍谓词，只有条件真正成立才会退出循环，这是使用条件变量唯一安全的写法。
