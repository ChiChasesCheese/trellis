%% trellis:begin %%
# GIL 与并发：线程、进程与 asyncio
*Python 内置类型与标准库*

GIL 让同一时刻只有一个线程执行 Python 字节码：CPU 密集的多线程不会变快，I/O 密集的可以；多进程绕开 GIL 的代价；3.13 起的自由线程构建（PEP 703）。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-python-gil-concurrency-1-why-gil]]
2. [[uth-python-gil-concurrency-2-switch-io]]
3. [[uth-python-gil-concurrency-3-not-atomic]]
4. [[uth-python-gil-concurrency-4-processes]]
5. [[uth-python-gil-concurrency-5-free-threading]]
%% trellis:end %%

## Notes
