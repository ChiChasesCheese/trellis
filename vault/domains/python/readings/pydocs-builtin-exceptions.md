---
nodes:
- runtime.exceptions
title: 内建异常完整参考
corpus: python-docs
section: 52-exceptions
url: https://docs.python.org/3/library/exceptions.html
tags:
- canonical
---

# 内建异常完整参考

这是所有内建异常类型的权威参考，最重要的是异常层级结构：BaseException 是所有异常的根，但 except Exception 不会捕获 KeyboardInterrupt（Ctrl+C）和 SystemExit（sys.exit()），因为它们特意被设计成 BaseException 的直接子类而不是 Exception 的子类，这样捕获所有异常的代码不会意外吞掉用户中断程序或正常退出的信号。文档详细列出了每个具体异常类的含义（OSError 及其一系列子类对应不同的系统调用失败原因）、异常上下文（__context__ 隐式记录、__cause__ 通过 raise from 显式记录）的区别，以及 3.11 引入的异常组（ExceptionGroup）及配套的 except* 语法，用于表示一批并发操作里同时发生了多个独立异常这种传统单异常模型表达不了的场景，正是 TaskGroup 失败后异常聚合的底层机制。
