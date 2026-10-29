%% trellis:begin %%
# 采样：top-k 与 top-p
*AI 工程里的数据结构与算法*

模型每步给出整个词表的概率，怎样挑下一个 token：top-k 只取最大的 k 个（部分排序或找阈值，不必全排序）；top-p 先按概率排序，再累加到 p 为止（排序 + 前缀和）；温度怎样改变分布。

## Cards (4)
1. [[uth-ai-sampling-1-temperature]]
2. [[uth-ai-sampling-2-top-p]]
3. [[uth-ai-sampling-3-partial-sort]]
4. [[uth-ai-sampling-4-draw]]
%% trellis:end %%

## Notes
