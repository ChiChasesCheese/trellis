---
id: hl-cq-q27-avg-last-k-bug
node: cpp-questions.f-ub-debug
type: qa
step: 24
---
## Q
下面求“最近 k 个价格平均值”的函数，对 `px = {10, 20, 30, 40}`、`k = 2` 输出 20.00，期望 35.00。bug 在哪？怎么一步步查出来？

```cpp
double avg_last(const std::vector<double>& px, std::size_t k) {
    assert(k > 0 && k <= px.size());
    double sum = 0;
    for (std::size_t i = px.size() - k + 1; i < px.size(); ++i)
        sum += px[i];
    return sum / static_cast<double>(k);
}
```

## A
- **bug**：循环起点差 1，应是 `px.size() - k`，而不是 `px.size() - k + 1`。
- 排查步骤：
  1. **最小用例**：期望 (30+40)/2 = 35，实际 20 = 40/2，说明只加了一个元素，循环少跑一次。
  2. **缩小范围**：打印 `i` 的取值，或调试器单步，看到 `i` 从 3 开始。
  3. **找到起点错误**，改成 `size - k`。
  4. **补边界测试**：k = 1、k = size、k = 0（触发 `assert`）。
