---
id: hl-c14-pitfalls-1
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 16
---
## Q
C++ 多线程里，关于 `join`/`detach`、条件变量 `wait`、“先判断后加锁”、返回受保护数据的引用、多把锁的加锁顺序，各有什么坑？

## A
1. **忘记 `join`/`detach`** → `std::terminate`。
2. **`wait` 不带谓词** → 虚假唤醒导致错误；通知先于等待时还可能永远睡眠。
3. **先判断后加锁**：`if (!q.empty()) { lock; q.pop(); }`——判断和操作之间被别人改了；判断必须在锁**内**。
4. **返回持锁保护的数据的引用**，出了锁就是数据竞争。
5. **按不同顺序加多个锁** → 死锁。
