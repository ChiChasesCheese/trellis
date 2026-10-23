---
id: hl-c06-selftest-accumulate-double
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 21
---
## Q
自测：`std::accumulate(v.begin(), v.end(), 0.0)` 与 `std::accumulate(v.begin(), v.end(), 0)` 对 `vector<double>` 有何不同？如何得到小顶堆 `priority_queue<int>`？

## A
- `0.0` 的累加器是 `double`，结果正确；`0` 的累加器是 `int`，对 `double` 元素**逐次截断**成整数。
- 小顶堆：`std::priority_queue<int, std::vector<int>, std::greater<int>>`。
