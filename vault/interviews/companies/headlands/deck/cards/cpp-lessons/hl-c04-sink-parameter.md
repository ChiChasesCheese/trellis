---
id: hl-c04-sink-parameter
node: cpp-lessons.c04-move-semantics
type: qa
step: 11
---
## Q
什么是 sink 参数（sink parameter）？写出一个存储 `std::string name_` 的构造函数，并说明传左值和右值各花多少。

## A
sink 参数：构造函数要**存下**字符串，就**按值接收，然后 `std::move` 进成员**。

```cpp
class Person {
    std::string name_;
public:
    explicit Person(std::string name) : name_(std::move(name)) {}
};
```
- 传**右值**：1 次移动。
- 传**左值**：1 次拷贝（形参初始化）+ 1 次移动。
- 简单、够快，不必写两个重载或模板。只读不存的参数仍用 `const std::string&` 或 `string_view`。
