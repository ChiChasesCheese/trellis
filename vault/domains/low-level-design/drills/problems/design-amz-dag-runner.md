---
nodes: [amazon.amz-dag-runner, concurrency.patterns]
tags: [problem]
---
# Drill：DAG 执行器与依赖安装（DAG Runner）

一批任务（或软件包）里，一些必须等另一些做完才能开始。要算出合法的执行顺序、发现死结就报错，再把互不相关的任务同时跑起来。
规模很小，但每一关都在检验同一件事：入度怎么数、环怎么报、并行时状态归谁。
输入输出的细节开场向面试官确认，下面各关是一套自洽的默认约定。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：`install_order(deps)`，`deps[x]` 是 x 的前置依赖；返回安装顺序，有环抛 `CycleError` 并带上环本身。想清楚只出现在依赖里的名字、重复依赖、平局顺序。
- 第 2 关（约 10 分钟）：不看题解，读 `vault/domains/low-level-design/problems/amz-dag-runner/buggy_runner.py`，找出三个 bug，各写一个最小输入，再修好。
- 第 3 关（约 15 分钟）：`Workflow.add(name, fn, needs)` 与 `run()`：按依赖顺序执行，上游结果以 `{依赖名: 结果}` 传给下游，失败就停并指出步骤。
- 第 4 关（选做）：`run_parallel(max_workers)`：独立步骤用线程池同时跑；一个失败只让它的后代跳过，其他分支照常完成；测试不能用 sleep。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-dag-runner/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-dag-runner -q`。

**评分点**
- 开场问了依赖方向、是否报出环、平局规则（[[amz-dag-runner-how-asked-and-three-questions]]）。
- 图的算法与执行分开，对象职责清楚（[[amz-dag-runner-objects-and-their-jobs]]）。
- 第 1 关用 Kahn 算法，只在依赖里出现的名字也登记，排完核对数量（[[amz-dag-runner-stage1-kahn-in-code]]）。
- 环报告是具体的环而不是所有卡住的节点（[[amz-dag-runner-cycle-report-walk-prerequisites]]）。
- 说得出 Kahn 与 DFS 的取舍（[[amz-dag-runner-decision-kahn-vs-dfs]]）。
- 结果传递只新增 Step 与 Workflow，不改图（[[amz-dag-runner-followup-results-flow-between-steps]]）。
- 评审时能给出重复边入度错误的最小输入（[[amz-dag-runner-code-review-duplicate-edge-indegree]]）。
- 并行时调度状态只由一个线程持有，失败只跳过后代（[[amz-dag-runner-parallel-failure-skips-descendants]]）。
- 不忘记排完核对数量（[[amz-dag-runner-common-mistake-no-length-check]]）。

**题解**：[[solution-amz-dag-runner]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
