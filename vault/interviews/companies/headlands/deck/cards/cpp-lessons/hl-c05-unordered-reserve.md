---
id: hl-c05-unordered-reserve
node: cpp-lessons.c05-stl-containers
type: qa
step: 14
---
## Q
往 `unordered_map` 填 10 万个 `int` 键，不预留和 `reserve(100000)` 各发生什么？

## A
- 不预留：从空开始，桶数多次增长，一共十六次 rehash（1→2、3→5、6→11 … 51438→102877），每次所有元素重新分桶，迭代器失效。
- `r.reserve(100000)`：**一次建好桶**（100003），填充期间零 rehash。
- 规则：已知元素数就 `reserve(n)`，和 `vector::reserve` 同理。

```cpp
std::unordered_map<int, int> r;
r.reserve(100000);
for (int i = 0; i < 100000; ++i) r[i] = i;
```
