---
id: debug-mode-four-ways-to-enable
node: asyncio.debugging
type: qa
source: cpython-internals
---
## Q
asyncio 默认运行在生产模式（production mode），有哪些方式可以打开它的调试模式（debug mode）？

## A
四种常见方式：设置环境变量 `PYTHONASYNCIODEBUG=1`；开启 Python 开发模式（Development Mode）；给 `asyncio.run(main(), debug=True)` 传参；或者直接调用 `loop.set_debug()`。此外通常还会配合把 asyncio 日志器（logger）的级别调到 `logging.DEBUG`，一起排查问题。
