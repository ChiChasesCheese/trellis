---
id: python-typing-not-enforced
node: python.typing
type: qa
step: 1
tags: [grown]
---
## Q
给函数参数写了类型注解（比如 `def charge(amount: float) -> None`），运行时调用 `charge("100")` 会报错吗？类型注解的价值体现在哪？

## A
不会报错——CPython 从不在运行时检查函数注解，`amount` 照样会被绑定成字符串 `"100"`，直到代码内部真正做数值运算才可能出错（甚至可能不报错就悄悄产生 bug）。注解的价值在于**静态**工具链：mypy/pyright 能在写代码、代码评审阶段就标红这次调用，注解本身也是给下一个读者的、不会过期的契约文档——这正是设计评审里愿意花时间写注解的原因：把接口契约显式化，而不是指望调用方读实现。
