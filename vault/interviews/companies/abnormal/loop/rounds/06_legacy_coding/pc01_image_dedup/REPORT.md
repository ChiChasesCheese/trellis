# pc01 Image dedup — report

## Summary
Abnormal 旧流程编码轮（电面 / 第一轮，"20 min 讨论 + 30 min 写"）的重复文件题：找重复 → 给定的
`_calculate_hash` 会碰撞，怎么办 → 怎么删 → system design。4-part：Part 1 `find_duplicates`
（大小分桶 + 流式完整哈希）→ Part 2 `find_duplicates_verified`（弱哈希只当候选，字节比较确认）→
Part 3 `plan_deletions`（保留策略、默认 dry-run）**(reconstructed)** → Part 4 `average_hash` /
`hamming` / `group_similar`（近似重复，8×8 矩阵）**(reconstructed)**。

## Sources & confidence
中。1point3acres 1059585 / 1072363 / 1074077 / 1137132（2024-04 → 2025-07）四帖互相印证，一手原话覆盖
"内存有限 / hashing / collision / `os.walk` 提示 / 给定 `_calculate_hash` 会碰撞 / 最后问 system design /
文件系统里很多照片怎么删重复"；PracHub 2025-07 两个标题只作旁证。给定哈希的具体弱法、Part 3、Part 4、
所有 worked examples 与测试规模为重建（已在 `problem.md` 标注）。条目：`catalog/raw/questions_reported.md` Q16。

## Approach by part
1. `os.walk(followlinks=False)`，符号链接用 `os.path.islink` 先排除；`size -> [paths]` 分桶，单元素桶
   不读取；同大小桶内 SHA-256 流式（`read(chunk_size)` 循环）；输出统一经 `_finish`（组内排序、组按首路径排序、
   丢掉单元素组）。`OSError` 记入 `bad` 集合，最终 `skipped = 遍历期失败数 + len(bad)`。
2. 同一份 `scan_duplicates`：传入 `hash_fn` 时桶键是弱哈希，桶内用等价类划分（逐个与各类代表做
   `files_equal`），所以对恒 0 的哈希也正确；`files_equal` 先比大小，再逐块比较，第一个不同块即返回。
3. `plan_deletions`：`min(key=(mtime, len(path), path))` 选保留者；`prefer_dir` 用 `os.path.commonpath`
   按目录边界判断；先 `lexists` 过滤已消失文件；`dry_run=False` 时在计划完成后才删。
4. `average_hash` 用整数比较 `v * 64 > sum` 避免浮点；`group_similar` 用并查集求汉明图的连通分量。

## Pitfalls hidden tests target
- 大小唯一的文件被打开（测试监听 `builtins.open`）；整文件 `read()`（`tracemalloc` 峰值 < 1 MiB）
- 弱哈希碰撞被当成重复（同大小、同前 1 KiB、尾部不同）；同桶里真重复与假重复混合没有拆成多个等价类
- 恒 0 哈希下结果与强哈希版不一致；差异只在最后一个字节、`chunk_size` 为 1 / 恰好等于 / 大于文件大小
- 符号链接（文件、目录、悬空）被跟随或被算作重复；空文件被漏掉
- 不可读文件中断整次扫描或没有计数
- `plan_deletions` 默认不是 dry-run、某组被删光、`originals_backup/` 被误判为在 `originals/` 之下、
  平局顺序不确定
- `average_hash` 用浮点均值、纯色图不为 0；`group_similar` 不传递（a~b、b~c 却没合并）

## Complexity & measured cost
设 n 个文件、总字节 B：遍历 + `stat` O(n)；只有同大小桶内的文件被读取，最坏 O(B)；字节比较在碰撞桶内最坏
O(k·B_bucket)，k 为桶内等价类数。`python3` 实测（本机）：2 万个小文件（0–40 字节，分在 50 个目录）+ 3 个
2 MiB 大文件，`find_duplicates` 0.39 s，`find_duplicates_verified` 0.39 s（预算 2 s）；
4 MiB × 3 个文件、`chunk_size=4096` 的流式测试 tracemalloc 峰值 < 1 MiB。

## Test inventory
34 test functions（`grep -c "def test"` = 34）；
`python3 tools/verify_suites.py . "loop/rounds/06_legacy_coding/pc01*"` → `solution: 33 passed, 1 skipped`
（跳过的是依赖 `chmod 000` 的用例，root 下权限不生效；同一场景由"读时抛 `PermissionError`"的用例覆盖）；
`IMPL=starter` → `27 failed, 6 passed, 1 skipped`（通过的 6 个是对"空结果 / 抛不出 `ValueError` 以外的
默认值"本就成立的断言，例如无重复时返回 `[]`）。按 marker（`grep -c "mark.<m>"`）：part1 10 · part2 8 ·
part3 7 · part4 6；edge 13 · perf 2 · io 3。

## Skills exercised
`os.walk` / `stat` / 符号链接语义 · 分层过滤（size → hash → bytes）· 流式 IO 与内存意识 · 哈希碰撞与"哈希只做
剪枝"· 破坏性操作的安全设计（dry-run、保留一份、TOCTOU）· 并查集 · 感知哈希入门 · 从单机到分布式 / 对象存储的
system design 过渡。
