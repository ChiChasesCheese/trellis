---
id: hl-c01-nested-member-copy
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 5
---
## Q
```cpp
struct Order { std::string symbol; Point where; long qty; };
Order o{"AAPL", {3, 4}, 100};
Order copy = o;
copy.symbol = "MSFT";
```
`o.symbol` 还是 "AAPL" 吗？为什么？成员在 `Order` 里是怎么存放的？

## A
还是 `"AAPL"`。
- `std::string` 和 `Point` 这类成员对象**直接嵌在 `Order` 内部**：没有指针、没有对象头（`string` 的字符可能在堆上，但 `string` 对象本身在 `Order` 里）。
- `Order copy = o;` 默认是**深拷贝**：逐成员复制，`symbol` 也被复制成独立字符串，所以改 `copy.symbol` 不影响 `o.symbol`。
- 例：此例中 `sizeof(Order)` 为 40 字节。
- 对比 Java：`Order` 里的 `symbol` 是引用，`copy` 若是引用复制则两者共享同一对象。
