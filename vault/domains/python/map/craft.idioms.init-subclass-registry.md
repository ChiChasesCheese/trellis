%% trellis:begin %%
# __init_subclass__ 注册表 vs 手写 dict（create_cache 的取舍）
*编码功力（Coding Craft） / 高级写法（Idioms）*

按名字创建实现（'lru'、'file'）时，注册表可以靠 __init_subclass__ 自动维护，也可以手写一个 dict。

**Requires:** [[domains/python/map/classes.metaprogramming|类装饰器、`__init_subclass__` 与元类（metaclass）]], [[domains/python/map/classes.inheritance-mro|继承、多重继承、MRO（C3 线性化）与 `super()`]]

## Cards (5)
1. [[craft-init-subclass-registry-1-hand-written-registry]]
2. [[craft-init-subclass-registry-2-init-subclass-auto-register]]
3. [[craft-init-subclass-registry-3-import-order-trap]]
4. [[craft-init-subclass-registry-4-explicit-decorator-and-test-isolation]]
5. [[craft-init-subclass-registry-5-scales-fail-fast-config]]
%% trellis:end %%

## Notes
