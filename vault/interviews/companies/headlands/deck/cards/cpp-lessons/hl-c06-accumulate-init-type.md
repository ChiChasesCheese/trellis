---
id: hl-c06-accumulate-init-type
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 4
---
## Q
```cpp
std::vector<int> big(10, 1'000'000'000);
long long s = std::accumulate(big.begin(), big.end(), 0);
```
结果为什么错？怎么修？UBSan 会说什么？

## A
- `std::accumulate` 的**累加器类型 = 初值的类型**，不是元素类型，也不是目标变量类型。
- 初值 `0` 是 `int`，每个部分和都是 `int`；2000000000 + 1000000000 超出 `int`，**有符号溢出 = UB**。
- UBSan 报：`runtime error: signed integer overflow: 2000000000 + 1000000000 cannot be represented in type 'int'`。
- 修法：初值写 `0LL`，得 10000000000。
- 同理对 `double` 元素用 `0` 作初值会逐步截断成整数，要写 `0.0`。
