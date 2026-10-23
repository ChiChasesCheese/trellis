---
id: hl-cq-q42-division
node: cpp-questions.j-cross-language
type: qa
step: 17
---
## Q
`7/2`、`-7/2`、`-7%2` 在 Python 和 C++ 里各是多少？Python 的 `//` 呢？

## A
- **Python**：`7/2 = 3.5`；`//` **向下取整**，`-7//2 == -4`。
- **C++**：整数除法 `7/2 = 3`；**向零截断**，`-7/2 == -3`，`-7%2 == -1`。
- 这是从 Python 转到 C++ 最容易咬人的细节之一；另外 C++ 默认不做边界检查，无符号会回绕。
