---
id: hl-hc02-cpp-priority-queue
node: problems.hc02-merge-k-streams
type: qa
step: 20
---
## Q
C++ 的 `std::priority_queue` 有哪四个事实？做 k 路合并时比较器怎么写？

## A
1. **它是大顶堆**：`top()` 是按比较器「最大」的元素。想让最小的先出，比较器要表达「a 排在 b **后面**」，所以写 `a.value > b.value || (a.value == b.value && a.stream > b.stream)`：值大的、编号大的靠后。
2. **它不稳定**：值相等的出堆顺序标准没规定，序列编号必须写进比较器。
3. **`top()` 返回 `const&`，`pop()` 之后引用悬空**：先把需要的小结构（如 16 字节的 `Head`）按值拷出来再 `pop()`。
4. **只能依赖 `<`**：元素可能只有 `operator<`；判断相等写 `!less(a,b) && !less(b,a)`，不要用 `==`、`>`，更不要用 `a - b`（有符号溢出是 UB）。

C++ 的做法：`priority_queue<int>` 只存序列下标，元素留在原处；`merge_longs` 也是不拷贝、不装箱。

陷阱：比较器方向写反；`Merger` 被拷贝或移动后比较器里的 `this` 指向旧对象（所以删掉拷贝构造）；倒着数的无符号循环 `i >= 0` 永远为真。
