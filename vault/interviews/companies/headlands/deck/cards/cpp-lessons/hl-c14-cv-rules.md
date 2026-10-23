---
id: hl-c14-cv-rules
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 9
---
## Q
面试问：为什么 `condition_variable::wait` 一定要带谓词（或放在 `while` 里）？使用条件变量的三条规则是什么？
Interview question: Why must `condition_variable::wait` use a predicate?

## A
三条规则：
1. 条件本身是**被 mutex 保护的共享状态**（队列、标志）。
2. 等待用 `cv.wait(lock, predicate)`：线程先释放锁并睡眠，被唤醒时重新加锁并**重新检查谓词**。必须带谓词，因为有**虚假唤醒**（spurious wakeup）和「通知后条件又被别人改回去」。谓词版本等价于 `while (!pred()) wait(lock)`。
3. 修改状态后 `notify_one/notify_all`；通知可以在锁外发出（被唤醒的线程不用再立即阻塞在锁上）。

问题背景：忙等浪费 CPU，`condition_variable` 让线程**睡眠**直到被唤醒。
