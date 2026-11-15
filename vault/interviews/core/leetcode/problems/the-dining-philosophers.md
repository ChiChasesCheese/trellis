---
slug: the-dining-philosophers
---
## Q
**LC 1226 哲学家进餐**｜Medium

5 位哲学家围圆桌，相邻两人之间一把叉子。吃饭要同时拿起左右两把叉子。设计 `wantsToEat`，使任意线程调度下不死锁、相邻的哲学家不会同时吃饭。

## A
**一句话。** 给叉子编号，每个人总是先拿编号小的叉子再拿大的：全局统一的加锁顺序破坏了循环等待，不会死锁。

```python
class DiningPhilosophers:
    def __init__(self):
        self.forks = [threading.Lock() for _ in range(5)]

    def wantsToEat(self, philosopher,
                   pickLeftFork, pickRightFork,
                   eat, putLeftFork, putRightFork):
        left, right = philosopher, (philosopher + 1) % 5
        first, second = sorted((left, right))   # 先拿编号小的
        with self.forks[first]:
            with self.forks[second]:
                pickLeftFork()
                pickRightFork()
                eat()
                putLeftFork()
                putRightFork()
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 每人先拿左边叉子：五个人同时拿起左叉，谁都等不到右叉，循环等待造成死锁。
- 只用一把全局锁：不死锁，但同时只有一人吃饭，没有并发。
- 释放顺序出错：用 `with` 嵌套，离开作用域自动按相反顺序释放。

**追问。**
- 另一种防死锁办法？：用信号量限制最多 4 人同时拿叉子，至少有一人能拿到两把。
- 为什么统一顺序就不死锁？：死锁需要环形等待，所有人按同一全序拿锁时，等待关系不会成环。

**同模式。** LC 1114 按序打印、LC 1188 设计有限阻塞队列
