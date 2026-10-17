# Task: amazon.amz-dag-runner

- **Leaf id**: `amazon.amz-dag-runner`   **slug**: `amz-dag-runner`   **kind**: problem
- **题目**: DAG 执行器与依赖安装（DAG Runner）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- Hello Interview `package-installation-order` 2026-10-01 mid-level USA: 'Given a dependency adjacency list to install packages, return the installation order or throw an exception if a cycle is found.' (3 reports) https://www.hellointerview.com/community/questions?company=Amazon (question slug `package-installation-order`) [medium–high]
- Hello Interview `dag-execution-order` (CODE_REVIEW) 2026-09-20 mid-level: 'Interviewer gave long winded description of problem with table … problem basically boils down to Directed Acyclic graph and we need to find order of execution'; summary: 'Given Python code that determines the correct execution order of nodes in a DAG representing a step function, identify and fix the bug(s)' https://www.hellointerview.com/community/questions?company=Amazon (question slug `dag-execution-order`) [medium]
- 1p3a question bank `package-dependency-installation-build-order` (phone/onsite, 3 sources, 2026-08-04..09-18; topological-sort, dfs, cycle-detection, complexity) [medium]
- 1p3a 1192714 (2026-10-11, L5 phone ×3, AWS agentic-AI security team): 「第一轮 二姨已无(=LC 210) 是一个DAG 拓扑排序」 https://www.1point3acres.com/bbs/thread-1192714-1-1.html [high]; 1p3a 1193105 onsite: task and course scheduling [high]

## (reconstructed) — not in any visible report

- the buggy code (write a plausible buggy version with 3 realistic bugs and have the learner find them — label it 推断), the step-function semantics (Choice/Parallel), stage 4 parallel execution with a worker pool and failure propagation

## Reuse / link (our own repo first)

- `vault/interviews/companies/amazon/coding/solutions/207_course_schedule.py`
- bank [[solution-task-scheduler]], [[solution-thread-pool]] (link)
- graphlib.TopologicalSorter docs https://docs.python.org/3/library/graphlib.html
- concept leaf concurrency.patterns

## Card ladder notes

- ladder; step 3 = Kahn's algorithm in ≤ 15 lines; step 4 = cycle report (which nodes) with a concrete graph; step 7 = a code-review bug (e.g. in-degree counted per edge vs per unique edge with a duplicate dependency) and its concrete wrong output; step 8 = run independent nodes in parallel, one fails → cancel its descendants only
