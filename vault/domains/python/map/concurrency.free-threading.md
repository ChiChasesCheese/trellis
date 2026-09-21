%% trellis:begin %%
# 自由线程（PEP 703，3.13 实验版）与子解释器（PEP 734）
*并发模型：GIL、线程与进程*

理解 `--disable-gil` 构建如何用偏向引用计数与每对象锁替代 GIL、单线程约 1–8% 开销与 C 扩展兼容问题，以及子解释器提供的另一条多核路径。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]

## Readings
- [[cpy-qsbr-reclaim|自由线程构建里，读操作为什么能不加锁]]
- [[peps-pep703-free-threading|PEP 703：让 GIL 可选（Making the GIL Optional）]]
- [[peps-pep734-subinterpreters|PEP 734：标准库中的多解释器（Multiple Interpreters）]]
- [[pydocs-asyncio-free-threading|asyncio 与自由线程 Python]]
- [[pydocs-concurrent-interpreters|concurrent.interpreters：子解释器提供的另一条多核路径]]
- [[pydocs-free-threading|自由线程 Python（无 GIL 构建）]]

## Cards (6)
1. [[freethreading-biased-refcounting]]
2. [[freethreading-deferred-refcounting]]
3. [[freethreading-immortal-objects]]
4. [[freethreading-overhead-percent]]
5. [[qsbr-lock-free-reclamation]]
6. [[subinterpreters-vs-freethreading]]
%% trellis:end %%

## Notes
