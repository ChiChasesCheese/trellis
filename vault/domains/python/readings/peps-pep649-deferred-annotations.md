---
nodes:
- types.gradual-typing
title: PEP 649：注解的延迟求值
corpus: peps
section: 18-pep-0649
url: https://peps.python.org/pep-0649/
tags:
- canonical
---

# PEP 649：注解的延迟求值

讲的是 TYPE_CHECKING 这个常见变通手段背后真正的问题，以及它未来可能被替代的方式。注解默认在函数/类绑定时立即求值，如果类 C 的方法标注了后定义的类 D、D 又反过来标注 C，就会遇到无法解开的循环引用；PEP 563（from __future__ import annotations）用把注解整体转成字符串的办法绕开，但代价是运行时想用注解就得手动 eval，字符串化也不总能准确还原表达式。这篇提出第三条路：把注解表达式编译进一个独立函数 __annotate__，直到真正访问 __annotations__ 时才调用求值，从而在不牺牲运行时可用性的前提下解决前向引用和循环导入问题。理解这段历史，能解释 TYPE_CHECKING 这种 hack 为什么存在、以及它未来可能不再必要的方向。
