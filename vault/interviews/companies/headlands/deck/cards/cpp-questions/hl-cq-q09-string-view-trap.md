---
id: hl-cq-q09-string-view-trap
node: cpp-questions.b-standards
type: qa
step: 20
---
## Q
C++17 的 `std::string_view` 是什么？它的主要陷阱是什么？什么场合可以放心用？

## A
- 它是“指针 + 长度”，**不拥有数据，不拷贝**。
- 陷阱是**生命周期**：指向的字符串先销毁，视图就悬空（AddressSanitizer 会报 `heap-use-after-free`）。
- 作函数参数时用最合适；作成员或返回值要小心它指向的数据能活多久。
