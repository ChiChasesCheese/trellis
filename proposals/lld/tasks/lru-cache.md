# Task: problems.components.lru-cache

- **Leaf id**: `problems.components.lru-cache`   **slug**: `lru-cache`   **family**: 基础组件
- **题目**: LRU / LFU 缓存
- **范围**: O(1) 的 get/put：哈希表加双向链表，LFU 变体，线程安全版本。
- **Taught by 10 independent sources** in the survey.

## Concept leaves it stands on (wikilink these in the article; their cards may be grading-point links)
- `[[python.data-model|数据模型与特殊方法（Data Model）]]`
- `[[structure.api|进程内 API 设计]]`

## A drill already exists: `vault/domains/low-level-design/drills/lru-cache.md`
It is in English and predates this bank. Rewrite that file in the drill format of PROBLEM_AGENT.md (keep its file name), add your leaf to `nodes:`. Do not create a second drill.

## Free treatments found by the survey (Python ones first; read two or three, then design your own)
- https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/lru_cache  — donnemartin/system-design-primer (object_oriented_design folder only) (code (Python))
- https://github.com/abhaypaswan/lld-python/tree/main/problems/lru-cache  — abhaypaswan/lld-python (code (Python))
- https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/lru-cache.md  — ashishps1/awesome-low-level-design (code)
- https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/017-lru-cache  — jkaus324/machine-coding-interview-questions (code (5 languages))
- https://leetcode.com/problems/lru-cache/description/  — 4. GitHub — prsnt558908/CodeZymSolutions (mirrors codezym.com) (outline; reported at Microsoft and Salesforce and Walmart, 2026)
- https://leetcode.com/problems/lfu-cache/description/  — 4. GitHub — prsnt558908/CodeZymSolutions (mirrors codezym.com) (outline; reported at Salesforce and Walmart, 2026)
- https://algomaster.io/learn/lld  — AlgoMaster — LLD (Ashish Pratap Singh) (—)

## Commercial / paywalled treatments (link as `no-archive` readings if you use them; never copy)
- https://www.tryexponent.com/questions  — 1. Exponent (tryexponent.com) question bank (paywalled)
- https://www.tryexponent.com/questions  — 1. Exponent (tryexponent.com) question bank (paywalled)
- https://www.tryexponent.com/questions  — 1. Exponent (tryexponent.com) question bank (paywalled)
- https://codemia.io/object-oriented-design  — Codemia — Object-Oriented / Low-Level Design (paywalled)

## Python documentation worth citing when you use the facility
- https://docs.python.org/3/library/dataclasses.html · https://docs.python.org/3/library/enum.html · https://docs.python.org/3/library/typing.html#typing.Protocol
- https://docs.python.org/3/library/threading.html · https://docs.python.org/3/library/queue.html · https://docs.python.org/3/library/heapq.html · https://docs.python.org/3/library/collections.html
