---
id: hl-cq-q21-emplace-vs-push-numbers
node: cpp-questions.e-templates
type: qa
step: 8
---
## Q
`v.push_back(Order("MSFT", 1))` 和 `v.emplace_back("MSFT", 1)` 各经历几次构造、拷贝、移动？为什么？

## A
```cpp
v.push_back(Order("MSFT", 1));   // 先构造临时 Order，再移动进 vector
v.emplace_back("MSFT", 1);       // 参数转发给 Order 的构造函数，在 vector 内存里直接构造
```
- `push_back(Order(...))`：ctor=1 copy=0 **move=1**。
- `emplace_back(args...)`：ctor=1 copy=0 **move=0**。
- 同理 `make_unique`、`make_shared` 也是靠转发构造。
