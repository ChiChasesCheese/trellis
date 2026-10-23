---
id: hl-c16-read-errors-rule
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 8
---
## Q
编译器报了 20 个错误，从哪里开始读？`note:` 行有什么用？模板错误怎么读？

## A
- **从第一个 `error:` 往下读，只看前几行**；后面的错误常是第一个错误的连锁反应；先修第一个再重新编译。
- `note:` 行告诉你候选函数是什么、模板在哪里实例化。
- 模板错误的读法：报错来自标准库内部，但真正原因在**带你自己文件名的那一行**（`in instantiation of ... requested here`）。
- 不要和编译器较劲超过一两分钟：换更简单的写法（例如回退到传统 `for`）。
