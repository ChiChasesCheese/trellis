# Task: amazon.amz-file-watcher

- **Leaf id**: `amazon.amz-file-watcher`   **slug**: `amz-file-watcher`   **kind**: problem
- **题目**: 文件监听器（File Watcher）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- 1p3a 1189999 (2026-09-18, Amazon SDE II phone; see robot restaurant): 「…设计file watcher system」 https://www.1point3acres.com/bbs/thread-1189999-1-1.html [medium for the name; body hidden]

## (reconstructed) — not in any visible report

- the whole spec: watch a directory (recursive?), events created/modified/deleted (renamed?), callbacks, polling vs OS notifications, debounce, stop()

## Reuse / link (our own repo first)

- `vault/interviews/companies/amazon/lld/file_search.md` (walking a tree, filters — a watcher can take the same filter objects)
- bank [[solution-in-memory-file-system]] (inject a fake file system for tests)
- docs: os.scandir / os.stat https://docs.python.org/3/library/os.html#os.scandir, threading.Event
- concept leaves patterns.observer, concurrency.primitives

## Card ladder notes

- ladder; step 4 = snapshot diff (path → (mtime_ns, size)) and why mtime alone misses edits within one tick; step 8 = callback thread vs polling thread, stop() and a slow callback
