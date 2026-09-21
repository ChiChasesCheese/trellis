---
nodes:
- model.numbers
- engineering.money-time
title: decimal 模块：精确十进制运算
corpus: python-docs
section: 53-decimal
url: https://docs.python.org/3/library/decimal.html
tags:
- canonical
---

# decimal 模块：精确十进制运算

decimal 模块提供了不会有二进制浮点误差的十进制定点/浮点运算，是处理金额等要求精确的场景的标准选择。文档开篇的快速上手教程就点出了最容易用错的地方：直接用浮点数构造 Decimal 会把 float 本身已经存在的二进制近似误差原样带进来，正确做法是用字符串构造，即 Decimal(str(x))，从字符串构造才能得到真正精确的值。Context 对象控制精度和舍入模式，四舍五入（ROUND_HALF_UP）等舍入模式需要显式指定，因为默认的银行家舍入（ROUND_HALF_EVEN）和日常直觉的四舍五入不一致，财务场景搞混这一点会导致对账差一分钱的诡异 bug。文档还讲了如何在多线程环境下给每个线程设置独立的精度上下文（localcontext()）。这是回答金额计算该用什么类型这一常见问题时的标准依据。
