%% trellis:begin %%
# 记忆化：lru_cache 要求参数可哈希、结果不可变
*编码功力（Coding Craft） / 高级写法（Idioms）*

query-condition-parser 把「条件字符串 → 语法树」用 lru_cache 缓存；之所以安全，是因为树节点全是 frozen。

**Requires:** [[domains/python/map/functions.functools|`functools`：`lru_cache`、`partial`、`singledispatch`、`cached_property`]], [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]], [[domains/python/map/classes.properties-descriptors|`property` 与描述符协议（`__get__`/`__set__`/`__set_name__`）]]

## Cards (5)
1. [[craft-memoize-on-frozen-1-cache-needs-immutable-results]]
2. [[craft-memoize-on-frozen-2-key-includes-everything]]
3. [[craft-memoize-on-frozen-3-not-compute-once]]
4. [[craft-memoize-on-frozen-4-cached-property-and-slots]]
5. [[craft-memoize-on-frozen-5-scales-compile-cache]]
%% trellis:end %%

## Notes
