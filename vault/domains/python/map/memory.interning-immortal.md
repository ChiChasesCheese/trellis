%% trellis:begin %%
# 驻留（interning）与不朽对象（immortal objects，PEP 683）
*内存管理与垃圾回收*

理解字符串驻留与小整数缓存如何省内存与加速比较，3.12 引入不朽对象让 `None`/`True`/小整数免于引用计数写入，以及这对多核与写时复制（fork）的意义。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]]

## Readings
- [[cpy-string-interning|字符串驻留与不朽对象：is 比较为什么能又快又准]]
- [[cpyint-05-objects-types|CPython Internals · 对象与类型]]
- [[peps-pep683-immortal-objects|PEP 683：用固定引用计数实现不朽对象（Immortal Objects）]]
- [[pydocs-free-threading|自由线程 Python（无 GIL 构建）]]
- [[pydocs-sys-module|sys 模块：解释器内部状态入口]]

## Cards (6)
1. [[immortal-objects-benefits]]
2. [[immortal-objects-what-and-why]]
3. [[immortal-refcount-inspection-huge-value]]
4. [[mortal-interned-refcount-bookkeeping]]
5. [[string-interning-purpose]]
6. [[string-interning-two-mechanisms]]
%% trellis:end %%

## Notes
