%% trellis:begin %%
# 描述符：什么时候值得（共享字段规则），什么时候不值得
*编码功力（Coding Craft） / 高级写法（Idioms）*

同一条字段规则（正整数、非空、范围）在三个以上的类里重复时，才值得写一个 __set_name__ 描述符。

**Requires:** [[domains/python/map/classes.properties-descriptors|`property` 与描述符协议（`__get__`/`__set__`/`__set_name__`）]], [[domains/python/map/classes.attribute-lookup|属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`]]

## Cards (5)
1. [[craft-descriptors-where-they-earn-1-one-rule-many-classes]]
2. [[craft-descriptors-where-they-earn-2-store-on-the-instance]]
3. [[craft-descriptors-where-they-earn-3-descriptor-with-dataclass]]
4. [[craft-descriptors-where-they-earn-4-shared-function-post-init]]
5. [[craft-descriptors-where-they-earn-5-scales-declare-in-schema]]
%% trellis:end %%

## Notes
