---
id: hl-c16-top-k
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 5
---
## Q
用 C++ 写出按成交额（`qty * px_cents`）取 top-k 的 `top_k(trades, k)`，最大的排最前。

## A
```cpp
std::vector<Trade> top_k(const std::vector<Trade>& trades, std::size_t k) {
    auto notional = [](const Trade& t) { return t.qty * t.px_cents; };
    auto worse = [&](const Trade& a, const Trade& b) { return notional(a) > notional(b); };
    std::priority_queue<Trade, std::vector<Trade>, decltype(worse)> heap(worse);
    for (const auto& t : trades) {
        heap.push(t);
        if (heap.size() > k) heap.pop();      // 丢掉 k+1 个里最小的
    }
    std::vector<Trade> out;
    while (!heap.empty()) { out.push_back(heap.top()); heap.pop(); }
    std::reverse(out.begin(), out.end());     // 最大的在前
    return out;
}
```
- `greater` 语义的比较器得**小顶堆**，堆顶是目前最小。
- 复杂度 O(n log k)；k 很小用堆，k 接近 n 用排序 / `nth_element`。
