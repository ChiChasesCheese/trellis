---
id: hl-cq-q19-code-erase-loop-swap-pop
node: cpp-questions.d-containers
type: qa
step: 14
---
## Q
补全代码：用迭代器循环删除 `vector<int> b` 里的偶数（正确处理 `erase` 的返回值）；再写顺序无关时的 swap-and-pop 删偶数循环（下标版，`d` 是 `vector<int>`）。

## A
```cpp
for (auto it = b.begin(); it != b.end();) {
    if (*it % 2 == 0) it = b.erase(it);   // 用返回值，不要再 ++
    else ++it;
}

for (std::size_t i = 0; i < d.size();) {  // swap-and-pop：O(1)，打乱顺序
    if (d[i] % 2 == 0) { d[i] = d.back(); d.pop_back(); }
    else ++i;
}
```
注意 swap-and-pop 换进来的元素还没检查，所以删除后不递增 `i`。
