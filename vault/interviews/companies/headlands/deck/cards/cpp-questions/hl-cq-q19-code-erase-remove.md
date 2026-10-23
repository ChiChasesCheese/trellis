---
id: hl-cq-q19-code-erase-remove
node: cpp-questions.d-containers
type: qa
step: 13
---
## Q
补全代码：用 erase-remove 惯用法删掉 `vector<int> a` 里所有偶数；再用 C++20 `std::erase_if` 删除 `c` 里的偶数并接收被删个数。实测 `remove_if` 之后和 `erase` 之后的 size 各是多少（原 6 个、删 3 个）？

## A
```cpp
auto new_end = std::remove_if(a.begin(), a.end(), [](int x) { return x % 2 == 0; });
a.erase(new_end, a.end());                      // erase-remove

auto n = std::erase_if(c, [](int x) { return x % 2 == 0; });   // C++20，返回删除个数
```
- 实测：`remove_if` 之后 size 仍是 **6**，`erase` 之后变成 **3**。
- `remove_if` 返回的是新的逻辑末尾。
