---
id: hl-c05-selftest-address
node: cpp-lessons.c05-stl-containers
type: qa
step: 24
---
## Q
自测：什么时候 `v.push_back(x)` 之后 `v[0]` 的地址不变？`unordered_map` rehash 之后旧迭代器和旧元素引用，哪个还能用？

## A
- `size < capacity`（容量有余）时不重分配，`v[0]` 地址不变。
- `unordered_map` rehash 之后：旧的**引用/指针仍有效**（节点没有被搬动），旧的**迭代器失效**。
- 订单簿最优卖价如何 O(1) 取到？卖盘用 `std::map<price, qty>`（升序），`begin()` 就是最低卖价；买盘用 `std::greater` 排序（或 `rbegin()`）。
