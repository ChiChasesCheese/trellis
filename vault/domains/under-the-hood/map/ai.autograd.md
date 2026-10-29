%% trellis:begin %%
# 自动求导：计算图上的拓扑排序
*AI 工程里的数据结构与算法*

PyTorch 前向时记下计算图，backward 从损失出发按拓扑逆序把梯度传回每个参数；一个张量被用了多次时梯度要累加；为什么要先数清依赖再执行。

## Cards (3)
1. [[uth-ai-autograd-1-record-replay]]
2. [[uth-ai-autograd-2-dependency-count]]
3. [[uth-ai-autograd-3-saved-tensors]]
%% trellis:end %%

## Notes
