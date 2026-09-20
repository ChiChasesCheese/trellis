# Task: problems.components.rate-limiter

- **Leaf id**: `problems.components.rate-limiter`   **slug**: `rate-limiter`   **family**: 基础组件
- **题目**: 限流器（Rate Limiter）
- **范围**: 令牌桶、滑动窗口的类设计，可注入时钟，按用户隔离与线程安全。
- **Taught by 6 independent sources** in the survey.

## Concept leaves it stands on (wikilink these in the article; their cards may be grading-point links)
- `[[patterns.strategy|策略模式与可替换算法（Strategy）]]`
- `[[concurrency.primitives|同步原语（threading）]]`

## Free treatments found by the survey (Python ones first; read two or three, then design your own)
- https://github.com/abhaypaswan/lld-python/tree/main/problems/rate-limiter  — abhaypaswan/lld-python (code (Python))
- https://github.com/InterviewReady/Low-Level-Design/tree/main/rate-limiter  — InterviewReady/Low-Level-Design (code (Java))
- https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/011-api-rate-limiter  — jkaus324/machine-coding-interview-questions (code (5 languages))

## Commercial / paywalled treatments (link as `no-archive` readings if you use them; never copy)
- https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/rate-limiter  — Hello Interview — Low-Level Design (paywalled)

## Python documentation worth citing when you use the facility
- https://docs.python.org/3/library/dataclasses.html · https://docs.python.org/3/library/enum.html · https://docs.python.org/3/library/typing.html#typing.Protocol
- https://docs.python.org/3/library/threading.html · https://docs.python.org/3/library/queue.html · https://docs.python.org/3/library/heapq.html · https://docs.python.org/3/library/collections.html
