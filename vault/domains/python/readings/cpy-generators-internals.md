---
nodes:
- iteration.generators
- iteration.yield-from
- runtime.frames-eval
title: 生成器对象怎么把一次函数调用变成可以反复挂起的执行
corpus: cpython-internals
section: 006-generators
url: https://github.com/python/cpython/tree/main/InternalDocs
tags:
- canonical
---

# 生成器对象怎么把一次函数调用变成可以反复挂起的执行

生成器对象（`PyGenObject`）内部直接嵌了一份自己的帧（frame），这就是“生成器为什么能挂起”的答案：普通函数返回后帧就销毁了，而 `RETURN_GENERATOR` 字节码在生成器第一次被调用时把当前帧复制一份，交给生成器对象持有；`yield` 对应的 `YIELD_VALUE` 指令把返回地址和异常状态存进这份帧再交还调用者，下次 `send()` 时解释器把同一份帧重新压回调用栈继续跑，局部变量原样还在。`yield from` 则是用 `SEND` 指令把值和异常在生成器链上转发，一层层委托子生成器，直到 `StopIteration`——这正是 async/await 底层复用的机制。读完能把“生成器只能消费一次”“yield 挂起后局部变量还在”这类现象从“记忆规则”变成“看得懂原理”，也顺带理解为什么生成器和协程会共用同一套 frame 基础设施。
