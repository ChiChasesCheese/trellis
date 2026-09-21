---
nodes:
- runtime.exceptions
title: PEP 654：异常组与 except*
corpus: peps
section: 21-pep-0654
url: https://peps.python.org/pep-0654/
tags:
- canonical
---

# PEP 654：异常组与 except*

解决的是解释器一次只能传播一个异常这个根本限制。动机部分给了很有说服力的真实案例：asyncio.gather() 只能选择“抛第一个异常”或“把异常放进结果列表”两种笨办法；atexit 注册的多个回调如果都失败，只有最后一个被重新抛出；TemporaryDirectory.__exit__ 清理时的异常会掩盖用户代码本来抛出的异常。Rationale 说明了为什么不能靠一个普通容器异常类型（如 Trio 的 MultiError）解决——调用方必须手动拆包才能按类型分别处理，还得小心保留每个异常自己的 __traceback__/__cause__/__context__。也解释了为什么不修改 except 的语义而是新增 except*：两者语义差异太大，硬改会破坏向后兼容。理解这段能回答“并发场景下多个任务同时失败该怎么处理”这个 asyncio 高频追问。
