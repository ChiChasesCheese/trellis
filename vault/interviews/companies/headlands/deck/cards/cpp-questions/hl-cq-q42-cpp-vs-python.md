---
id: hl-cq-q42-cpp-vs-python
node: cpp-questions.j-cross-language
type: qa
step: 15
---
## Q
面试题：详细比较 C++ 和 Python，什么时候各用哪个？
C++ vs Python: compare them in detail. When would you use each?

## A
- **Python**：动态类型、解释执行、整数无限精度、有 GIL，开发快。
- **C++**：静态类型、编译成机器码、整数固定宽度会溢出 / 回绕，速度快几十倍并能控制内存。
- 选择：研究、脚本、胶水、测试用 Python；延迟敏感的在线系统用 C++；两者经常配合（Python 调 C++ 扩展，C++ 核心加 Python 绑定）。
