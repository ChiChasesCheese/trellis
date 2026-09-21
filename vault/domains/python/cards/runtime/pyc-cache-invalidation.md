---
id: pyc-cache-invalidation
node: runtime.compile-bytecode
type: qa
source: cpython-internals
---
## Q
Python 怎么判断 `__pycache__` 里的 `.pyc` 缓存是否过期需要重新编译？哪两种情况永远不查缓存？

## A
默认比较源文件 `.py` 的修改时间戳与 `.pyc` 里记录的时间戳，不一致就重新编译（3.7 起也支持按源码哈希校验）。两种情况永远不查缓存：①直接从命令行运行的顶层脚本（`__main__`）每次都重新编译、不落盘缓存；②只有编译产物、没有源文件的「纯字节码分发」——没有源文件可比对，只能信任已有的 `.pyc`。
