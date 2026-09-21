---
nodes: [runtime.frames-eval, runtime.adaptive-jit]
url: https://realpython.com/products/cpython-internals-book/
tags: [book, no-archive]
title: CPython Internals · 求值循环
---
# CPython Internals · 求值循环

这一部分讲字节码是怎么被『跑』起来的：CPython 的主求值循环（ceval）逐条取出字节码指令、维护一个求值栈来执行；每次函数调用都会创建一个帧对象（frame）保存局部变量表和栈状态；也介绍了 3.11+ 引入的自适应解释器（specializing adaptive interpreter）如何为反复执行的指令生成更快的专用版本。

**读时提取：**
- 求值循环如何用一个栈式虚拟机逐条执行字节码指令
- 帧对象（frame）保存了什么：局部变量、求值栈、返回地址
- 自适应解释器如何在运行时把『通用但慢』的字节码替换成『针对具体类型更快』的版本

%% trellis:begin %%
## Source
[Open the original ↗](https://realpython.com/products/cpython-internals-book/)
%% trellis:end %%
