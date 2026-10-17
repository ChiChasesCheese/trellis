# Task: amazon.amz-linux-find

- **Leaf id**: `amazon.amz-linux-find`   **slug**: `amz-linux-find`   **kind**: problem
- **题目**: Linux find 命令 API（File Search API）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- Hello Interview `file-search-api` 'Design a Linux Find Command API' — 'search files across directories based on criteria like size, format, and name … filters like "files >5MB" or "all XML files" through a clean, extensible interface' (11 reports overall; one 2026-10-01 mid-level USA) https://www.hellointerview.com/community/questions?company=Amazon (question slug `file-search-api`) [medium–high]
- 1p3a question bank `file-search-by-size-and-suffix` (onsite-coding, 4 sources, 2026-07-25..09-18; tags filesystem, oop-design, testing, cycle-detection) [medium]

## (reconstructed) — not in any visible report

- AND/OR/NOT composition order of follow-ups, symlink-cycle follow-up (the qbank tag 'cycle-detection' suggests it)

## Reuse / link (our own repo first)

- `vault/interviews/companies/amazon/lld/file_search.md` + `vault/interviews/companies/amazon/lld/code/file_search.py` (our own; adapt)
- bank [[solution-in-memory-file-system]] for the tree itself
- HI file system breakdown (in-memory FS, for contrast): /Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/hi_lld/file-system.txt
- concept leaves patterns.structural (Composite / Specification), oop.interfaces

## Card ladder notes

- ladder; step 4 = the Specification/Composite filter tree; step 8 = walking a real directory lazily (generators) and symlink loops
