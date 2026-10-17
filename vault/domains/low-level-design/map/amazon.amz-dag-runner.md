%% trellis:begin %%
# DAG 执行器与依赖安装（DAG Runner）
*Amazon 专项（Amazon OOD）*

依赖安装顺序与环检测，Step Function 式 DAG 执行顺序的 code review 找 bug，再到并行执行与失败传播。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/concurrency.patterns|并发模式]]

## Readings
- [[solution-amz-dag-runner|设计题解：DAG 执行器与依赖安装（DAG Runner）]]
- [[src-hellointerview-amz-dag-runner|依赖顺序与 DAG 执行：题目与要求]]
- [[src-pydocs-amz-dag-runner|graphlib — Functionality to operate with graph-like structures（Python 标准库文档）]]

## Drills
- [[design-amz-dag-runner|Drill：DAG 执行器与依赖安装（DAG Runner）]]

## Cards (9)
1. [[amz-dag-runner-how-asked-and-three-questions]]
2. [[amz-dag-runner-objects-and-their-jobs]]
3. [[amz-dag-runner-stage1-kahn-in-code]]
4. [[amz-dag-runner-cycle-report-walk-prerequisites]]
5. [[amz-dag-runner-decision-kahn-vs-dfs]]
6. [[amz-dag-runner-followup-results-flow-between-steps]]
7. [[amz-dag-runner-code-review-duplicate-edge-indegree]]
8. [[amz-dag-runner-parallel-failure-skips-descendants]]
9. [[amz-dag-runner-common-mistake-no-length-check]]
%% trellis:end %%

## Notes
