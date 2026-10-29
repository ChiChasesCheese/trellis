%% trellis:begin %%
# 背包这类问题在生产里为什么用贪心
*考点补全：后端系统里的算法*

把容器装进机器、把请求塞进一批推理，本质都是装箱或背包问题，规模大了精确求解太慢；Kubernetes 调度器给节点打分取最高，vLLM 按 token 预算逐个放入请求：用简单贪心换速度。

## Cards (4)
1. [[uth-gaps-heuristics-1-filter-score]]
2. [[uth-gaps-heuristics-2-sample-nodes]]
3. [[uth-gaps-heuristics-3-vllm-budget]]
4. [[uth-gaps-heuristics-4-spread-vs-pack]]
%% trellis:end %%

## Notes
