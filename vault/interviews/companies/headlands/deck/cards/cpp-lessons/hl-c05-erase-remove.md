---
id: hl-c05-erase-remove
node: cpp-lessons.c05-stl-containers
type: qa
step: 5
---
## Q
写出从 `std::vector<int> v` 中删除所有值为 3 的元素的惯用法，以及 C++20 的写法；再写出删除所有偶数。

## A
```cpp
v.erase(std::remove(v.begin(), v.end(), 3), v.end());   // erase-remove 惯用法
std::erase(v, 3);                                       // C++20
std::erase_if(w, [](int x) { return x % 2 == 0; });     // C++20：删偶数
```
- `std::remove` 只是把保留的元素前移，返回新的逻辑末尾，**不真正缩小容器**；`erase` 才删掉尾部。
- 例：`{5,3,8,3,9,3,1}` 删 3 后得 `5 8 9 1`；`{1..6}` 删偶数后得 `1 3 5`。
