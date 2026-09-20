---
id: problems-food-delivery-10x-mip-degrades-heuristic
node: problems.geo.food-delivery
type: qa
step: 8
tags: [grown]
---
## Q
In a food delivery dispatch design, if order volume grows 10x so a single dense market's dispatch batch grows from roughly 120 orders to roughly 1,200 orders per window, why might the dispatch service need to shift from solving the batch as an exact mixed-integer program to a pre-filtered heuristic instead?

## A
The time an exact mixed-integer programming solver needs to find the optimal assignment tends to grow much faster than linearly with the number of orders and couriers being jointly considered, so a batch that was comfortably solvable within the dispatch cycle's time budget at 120 orders may no longer fit that budget at 1,200 orders. The standard response is to first use cheap rules to narrow the candidate order-courier pairings down to a smaller, more tractable set, then run the exact solver only on that reduced subproblem — trading a small amount of solution quality for keeping the whole batch inside the time budget as scale grows, the same pattern combinatorial-optimization systems generally follow as their input size increases.

## Q zh
在一个外卖调度设计中，如果订单量涨到 10 倍，导致单个稠密市场一次调度窗口内的订单数从约 120 涨到约 1,200，为什么调度服务可能需要从把这一批精确求解为混合整数规划问题，转向使用预筛选的启发式方法？

## A zh
混合整数规划求解器找到最优指派所需的时间，通常随联合考虑的订单和骑手数量增长得远比线性更快，所以一个在 120 单规模下能舒服地在调度周期时间预算内求解的批次，到了 1,200 单规模下可能就超出这个预算了。标准的应对方式是先用低成本的规则把候选的订单-骑手配对缩小到一个更小、更容易处理的子集，再只对这个缩小后的子问题跑精确求解——用一点解的质量换取整个批次能随规模增长仍然留在时间预算之内，这是组合优化系统在输入规模增长时普遍遵循的模式。
