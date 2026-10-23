---
id: hl-c06-top-k-heap
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 8
---
## Q
面试问：怎么求 top-k（例如成交额最大的 3 笔）？用什么堆、复杂度多少？
Interview question: How do you compute the top-k elements?

## A
- **小顶堆**维护 k 个：每来一个元素就 `push`，堆大小超过 k 就 `pop`（弹掉堆顶，即目前最小的），最后堆里就是最大的 k 个。复杂度 **O(n log k)**。
- 或 `nth_element`，平均 O(n)。

```cpp
auto cmp = [](const Trade& a, const Trade& b) { return a.qty*a.px > b.qty*b.px; };
std::priority_queue<Trade, std::vector<Trade>, decltype(cmp)> top3(cmp);
for (auto& t : ts) { top3.push(t); if (top3.size() > 3) top3.pop(); }
```
- 例：四笔成交里 `top3.top()` 是这三个最大里最小的 NVDA 9000。
