---
id: pl-cpp-templates-concepts-found-sfinae
node: cpp.templates-concepts
type: qa
step: 3
---
## Q
SFINAE 是什么？C++20 之前的模板为什么需要它，又为什么报错那么难读？

## A
**SFINAE**（Substitution Failure Is Not An Error，替换失败不是错误）：编译器为重载候选的模板替换类型实参时，如果**签名**里的替换产生了无效类型，这个候选只是被悄悄丢弃，不报错；全部候选都被丢弃才报错。

**为什么需要**：C++98 的模板没有办法说"这个版本只对整数类型有效"。想为不同类型类别提供不同实现，只能利用 SFINAE，用 `std::enable_if` 在签名里放一个"条件满足才有效"的类型：

```cpp
template <class T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
std::string describe(T) { return "integral"; }
template <class T, std::enable_if_t<std::is_floating_point_v<T>, int> = 0>
std::string describe(T) { return "floating"; }
```

`describe(1)` 选第一个，`describe(1.5)` 选第二个。`describe("x")` 两个都被淘汰，真实报错（缩短）：`no matching function for call to 'describe'`，然后列出 `requirement 'std::is_integral_v<const char *>' was not satisfied`。

**为什么难读**：
1. **约束写在奇怪的位置**（默认模板参数、返回类型），读者要解码"这是个条件"。
2. **违反约束的错误发生在模板深处**。用 `std::sort` 排序 `std::list`（不支持随机访问），不会在调用点提示"需要随机访问迭代器"，而是在标准库内部某个 `<` 运算处失败，本机实测一次错误展开了 **126 行**，先是 `invalid operands to binary expression ('std::__list_iterator<int, void *>' ...)`，再是一串 `in instantiation of ...` 的嵌套回溯。

**根因**：C++98 模板是纯鸭子类型，没有"模板要求什么"的声明，编译器只能在实例化到使用点才发现不满足，看到的是内部实现的断裂，而不是接口的违约。

**历史意义**：SFINAE 是 C++ 最著名的"意外发现的技巧"。Boost 等库用它搭起了庞大的元编程设施。它能用，但是反映了语言缺一块：**给模板参数写接口约束**。C++20 的 concepts 正是对这块缺失的补齐。

**要记住的一点**：看到 `enable_if`，把它读作"这个模板只在条件成立时参与重载"；写新代码用 concepts。
