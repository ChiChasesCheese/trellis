%% trellis:begin %%
# 生成器管线与显式栈：惰性遍历 + pairwise / islice
*编码功力（Coding Craft） / 高级写法（Idioms）*

遍历写成 yield 的生成器，用显式栈替代递归：取第一个结果不必走完整棵树，深目录不撞递归上限。

**Requires:** [[domains/python/map/iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]], [[domains/python/map/iteration.itertools|`itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`]], [[domains/python/map/iteration.iterator-protocol|可迭代对象与迭代器：`__iter__`、`__next__`、`StopIteration`]]

## Cards (6)
1. [[craft-generators-lazy-traversal-1-lazy-vs-eager]]
2. [[craft-generators-lazy-traversal-2-explicit-stack]]
3. [[craft-generators-lazy-traversal-3-single-use]]
4. [[craft-generators-lazy-traversal-4-itertools]]
5. [[craft-generators-lazy-traversal-5-across-problems]]
6. [[craft-generators-lazy-traversal-6-scales-cursor]]
%% trellis:end %%

## Notes
