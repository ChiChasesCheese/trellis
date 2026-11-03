%% trellis:begin %%
# 不可变快照 + 整体替换发布（copy-on-write publish）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

读者拿一次引用，之后读到的是完整的某一版；写者在锁里造新快照再换引用。读路径不加锁。

**Requires:** [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]], [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]], [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]

## Cards (5)
1. [[craft-immutable-snapshot-publish-1-publish-whole]]
2. [[craft-immutable-snapshot-publish-2-read-once]]
3. [[craft-immutable-snapshot-publish-3-writers-still-lock]]
4. [[craft-immutable-snapshot-publish-4-across-problems]]
5. [[craft-immutable-snapshot-publish-5-scales-hot-reload]]
%% trellis:end %%

## Notes
