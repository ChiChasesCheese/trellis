---
id: hl-cq-q10-concepts-ranges-expected
node: cpp-questions.b-standards
type: qa
step: 28
---
## Q
三个追问：concepts 解决了模板的什么问题？ranges 的 view 是惰性的吗？`std::expected` 相比异常有什么好处？

## A
- **concepts**：模板过去是“鸭子类型”，传错类型会在模板体深处报错；concepts 在**调用处**检查要求。
- **ranges**：view 是惰性且不拥有数据的，遍历时才计算。
- **`std::expected` vs 异常**：错误在函数签名里显式可见、没有栈展开成本、强制调用者去看错误。
