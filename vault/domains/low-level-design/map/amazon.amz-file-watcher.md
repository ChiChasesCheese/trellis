%% trellis:begin %%
# 文件监听器（File Watcher）
*Amazon 专项（Amazon OOD）*

监听目录的创建 / 修改 / 删除并回调：快照比对、去抖、递归目录、回调线程与关闭。（重建）

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.observer|观察者与事件（Observer）]], [[domains/low-level-design/map/concurrency.primitives|同步原语（threading）]]

## Readings
- [[solution-amz-file-watcher|设计题解：文件监听器（File Watcher）]]
- [[src-1p3a-amz-file-watcher|一亩三分地：Amazon SDE II 电面（先 tech 再 LP）]]
- [[src-pydocs-amz-file-watcher|os.scandir（Python 标准库文档）]]
- [[src-pydocs-threading-amz-file-watcher|threading — Event Objects（Python 标准库文档）]]

## Drills
- [[design-amz-file-watcher|Drill：文件监听器（File Watcher）]]

## Cards (9)
1. [[amz-file-watcher-how-asked-and-three-questions]]
2. [[amz-file-watcher-objects-and-their-jobs]]
3. [[amz-file-watcher-stage1-poll-and-diff-in-code]]
4. [[amz-file-watcher-snapshot-diff-mtime-and-size]]
5. [[amz-file-watcher-decision-polling-vs-os-notification]]
6. [[amz-file-watcher-followup-debounce-by-stability]]
7. [[amz-file-watcher-edge-callback-failure-isolation]]
8. [[amz-file-watcher-concurrency-callback-thread-and-stop]]
9. [[amz-file-watcher-common-mistake-sleep-tests-and-first-scan-events]]
%% trellis:end %%

## Notes
