%% trellis:begin %%
# 求值顺序与副作用
*名字、绑定与求值*

参数和操作数按什么顺序求值：Java 保证从左到右、Go 规定函数调用与通信的顺序、Rust 从左到右、C/C++ 未规定；顺序不确定时副作用如何变成 bug。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/binding.evaluation-strategy|求值策略：严格、惰性与短路]]

## Cards (9)
1. [[pl-binding-evaluation-order-principle]]
2. [[pl-binding-evaluation-order-foundation-java]]
3. [[pl-binding-evaluation-order-foundation-go]]
4. [[pl-binding-evaluation-order-foundation-assignment]]
5. [[pl-binding-evaluation-order-mechanism]]
6. [[pl-binding-evaluation-order-table]]
7. [[pl-binding-evaluation-order-philosophy-determinism]]
8. [[pl-binding-evaluation-order-best-practice]]
9. [[pl-binding-evaluation-order-pitfall-tuple-assign]]
%% trellis:end %%

## Notes
