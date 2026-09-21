---
id: logging-library-nullhandler-no-root
node: engineering.logging-config
type: qa
source: python-docs
---
## Q
写一个会被别人当依赖库使用的 Python 包，里面该怎么用 logging？为什么不能直接往根 logger（root logger）写日志、也不能在库代码里自己加 `FileHandler`/`StreamHandler` 这类处理器？

## A
库应该用带有清晰、可识别名字的 logger（通常是该库顶层包的 `__name__`），绝不能直接往根 logger 记日志——那样会让使用这个库的应用开发者没法单独调整这个库的日志详细程度或处理器，因为已经和应用自己的根 logger 日志混在一起了。库也不该自己加真正输出的处理器（除了什么都不做的 `NullHandler`），因为「配置处理器、决定日志去哪里」应该完全由使用这个库的应用开发者决定；库如果偷偷加了处理器，可能会干扰应用自己的单元测试或日志收集。如果不想在应用完全没配置 logging 时看到这个库默认打到 `sys.stderr` 的 WARNING 及以上消息，可以给库的顶层 logger 加一个 `NullHandler`。
