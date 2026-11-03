%% trellis:begin %%
# 用 dataclasses.replace 整体替换，而不是原地改（immutable record swap）
*编码功力（Coding Craft） / 高级写法（Idioms）*

状态变化 = 造新对象换进字典；交出去的旧快照永远不变，「检查再替换」可以做成锁内比较并交换。

**Requires:** [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]], [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]]

## Cards (6)
1. [[craft-replace-for-state-change-1-swap-not-mutate]]
2. [[craft-replace-for-state-change-2-replace-as-cas]]
3. [[craft-replace-for-state-change-3-post-init-reruns]]
4. [[craft-replace-for-state-change-4-when-mutable]]
5. [[craft-replace-for-state-change-5-across-problems]]
6. [[craft-replace-for-state-change-6-scales-optimistic-lock]]
%% trellis:end %%

## Notes
