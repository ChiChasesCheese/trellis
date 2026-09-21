---
nodes:
- model.numbers
title: 浮点数运算：问题与限制
corpus: python-docs
section: 19-floatingpoint
url: https://docs.python.org/3/tutorial/floatingpoint.html
tags:
- canonical
---

# 浮点数运算：问题与限制

这篇简短但权威的文档用一句话点明了几乎所有初学者都会遇到的困惑：0.1 + 0.2 != 0.3，原因不是 Python 的 bug，而是绝大多数十进制小数根本无法用二进制浮点数精确表示，就像十进制无法精确表示 1/3 一样。文档展示了 0.1 在计算机里实际存储的是一个非常接近但不完全等于 0.1 的二进制近似值，repr() 显示的位数已经是能唯一还原该近似值的最短表示。这解释了为什么直接用 == 比较浮点数是危险的，应该用误差范围比较（如 math.isclose()），也解释了为什么涉及金额的计算必须用 Decimal 或者干脆用整数分而不是 float 累加。这是任何做数值计算或金额处理的人都该精读一遍的文档，而不是道听途说浮点数不精确就够了。
