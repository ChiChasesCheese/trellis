---
id: hl-cq-q21-code-wrong-right-forward
node: cpp-questions.e-templates
type: qa
step: 7
---
## Q
有重载 `sink(const std::string&)`（拷贝）和 `sink(std::string&&)`（移动）。写出两个包装模板 `wrong` 与 `right`，其中一个永远走拷贝，另一个保持值类别。为什么？

## A
```cpp
void sink(const std::string&) { puts("  sink(const&)  -> copy"); }
void sink(std::string&&)      { puts("  sink(&&)      -> move"); }

template <class T> void wrong(T&& x) { sink(x); }                    // x 有名字 -> 左值 -> 永远拷贝
template <class T> void right(T&& x) { sink(std::forward<T>(x)); }   // 保持原本的值类别
```
实测：给 `wrong` 传临时对象也走了拷贝；`right` 才走移动。
