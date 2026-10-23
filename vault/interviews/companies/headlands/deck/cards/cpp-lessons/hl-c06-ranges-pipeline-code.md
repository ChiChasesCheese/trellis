---
id: hl-c06-ranges-pipeline-code
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 15
---
## Q
用 ranges 写出：取 `{1..10}` 中偶数的平方的前三个；再写出 1 到 1,000,000 中 3 的倍数之和（不建 100 万元素的 vector）。

## A
```cpp
namespace rv = std::views;
auto pipeline = v | rv::filter([](int x) { return x % 2 == 0; })
                  | rv::transform([](int x) { return x * x; })
                  | rv::take(3);
for (int x : pipeline) std::cout << x << ' ';   // 4 16 36

long total = 0;
for (long i : rv::iota(1, 1'000'001)
              | rv::filter([](long i) { return i % 3 == 0; })) total += i;
// total == 166666833333
```
- 管线定义时**什么都没运行**，在 `for` 遍历时逐元素计算，没有临时 vector。
