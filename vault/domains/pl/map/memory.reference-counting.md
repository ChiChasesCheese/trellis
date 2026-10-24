%% trellis:begin %%
# 引用计数
*内存管理*

计数归零即释放、循环引用问题；CPython 引用计数 + 循环检测、Rust Rc/Arc 与 Weak、Swift ARC；与追踪式 GC 的对比。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/memory.manual-raii|手动管理与 RAII]]

**Unlocks:** [[domains/pl/map/concurrency.gil|Python GIL 与自由线程]]

## Cards (9)
1. [[pl-memory-reference-counting-principle]]
2. [[pl-memory-reference-counting-foundation-cpython]]
3. [[pl-memory-reference-counting-foundation-rc-arc-weak]]
4. [[pl-memory-reference-counting-mechanism]]
5. [[pl-memory-reference-counting-table]]
6. [[pl-memory-reference-counting-rc-vs-arc]]
7. [[pl-memory-reference-counting-best-practice]]
8. [[pl-memory-reference-counting-pitfall-refcell]]
9. [[pl-memory-reference-counting-history]]
%% trellis:end %%

## Notes
