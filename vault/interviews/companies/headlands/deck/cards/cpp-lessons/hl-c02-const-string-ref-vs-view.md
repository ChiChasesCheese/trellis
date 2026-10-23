---
id: hl-c02-const-string-ref-vs-view
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 10
---
## Q
面试问：为什么字符串参数以前常写 `const std::string&`，现在又推荐 `std::string_view`？
Interview question: Why prefer `std::string_view` over `const std::string&` for read-only string parameters?

## A
- `const std::string&` 避免了复制，但**只接受 `std::string`**：传字面量会临时构造一个 `string`，可能触发分配。
- `string_view` 接受任何字符序列（字面量、`string`、字符数组），**零分配**。
- 代价：①不保证以 `\0` 结尾；②**不拥有**数据；③有悬空风险。
- 规则：视图可以当**参数**，当成员变量或返回值时，必须保证被引用的数据活得更久。
