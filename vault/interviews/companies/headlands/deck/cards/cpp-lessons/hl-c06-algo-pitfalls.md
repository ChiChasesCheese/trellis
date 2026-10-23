---
id: hl-c06-algo-pitfalls
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 18
---
## Q
STL 算法、lambda、ranges 有哪七个常见的坑？

## A
1. 比较器不是严格弱序（用 `<=`、或比较浮点 NaN）→ `sort` 越界崩溃/死循环。
2. `accumulate` 初值类型决定累加类型（`0` vs `0LL` vs `0.0`）。
3. 对**未排序**区间用 `lower_bound`/`binary_search` = 结果无意义。
4. `remove`/`unique` 只前移保留的元素，不改变容器大小，必须配 `erase`。
5. lambda 按引用捕获后离开作用域再调用（线程、回调、返回值）→ 悬空。
6. `priority_queue` 的比较器方向与直觉相反。
7. 对临时容器用 ranges 算法返回 `dangling`。
