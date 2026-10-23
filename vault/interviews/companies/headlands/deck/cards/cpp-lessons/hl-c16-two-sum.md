---
id: hl-c16-two-sum
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 4
---
## Q
用 C++ 写出两数之和 `two_sum(a, target)`，返回 `std::optional<std::pair<int,int>>`（下标对）。

## A
```cpp
std::optional<std::pair<int, int>> two_sum(const std::vector<int>& a, int target) {
    std::unordered_map<int, int> seen;                    // 值 -> 下标
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
        if (auto it = seen.find(target - a[i]); it != seen.end())
            return std::pair{it->second, i};
        seen.emplace(a[i], i);
    }
    return std::nullopt;
}
```
- 哈希只需点查 → `unordered_map`，平均 O(1)，整体 O(n)。
- 测试：`{2,7,11,15}` 目标 9 得 `(0,1)`；`{1,2}` 目标 100 得空；空输入得空。
