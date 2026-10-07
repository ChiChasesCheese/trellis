# pc01 · Image dedup：找重复文件，弱哈希会碰撞，删之前先证明相等

> [!tldr]
> - 这题考的是：能不能把"找重复"拆成**代价递增的过滤层**，并且**不把正确性押在哈希上**。
> - 三步套路：按大小分桶（免费）→ 流式哈希（只读候选）→ 字节比较确认（只在碰撞桶里）。
> - 最值得带走的一个模式：**便宜的先做、昂贵的只对幸存者做；哈希是剪枝，不是证明。**

## 1. 题目在说什么（人话版）
一个目录里有成千上万张照片，很多是同一张被复制了多份。要找出哪些文件内容完全相同，分组列出；
然后问你：内存不够怎么办？哈希出现碰撞怎么办（面试官给了一个故意写得很弱的 `_calculate_hash`）？
真要删的时候怎么删才安全？最后一般会聊到"几亿张照片的服务怎么做"。

```
a/x.jpg = cat, b/y.jpg = cat, c/z.jpg = dog, d/w.jpg = cat
→ [["a/x.jpg", "b/y.jpg", "d/w.jpg"]]
```

## 2. 读题：把文字变成模型
- **实体**：文件（路径、大小、内容、mtime）、重复组、保留策略。
- **输入长什么样**：一个根目录；`os.walk` 给你 `(dirpath, dirnames, filenames)`。
- **输出要什么**：`list[list[str]]`，组内排序、组按首路径排序；至少 2 个成员才算一组。
- **状态**：`size -> [path]` 的桶，桶里再 `hash -> [path]`；不需要把内容留在内存。
- **一句话建模**：这是一个"**分层分组**"问题：用越来越贵的等价关系逐层细分同一个桶。

> [!note] 为什么先按大小
> 候选方案：①全部直接算哈希；②先按大小。选②：`stat` 不读内容，而大小不同的文件**必然**不同；
> 大小唯一的文件整个都不用打开。照片库里大小几乎都不同，这一层就能剔掉绝大多数 IO。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **先讨论 20 min 的内容，写下三层**：size → hash → bytes，以及每层为什么存在。
2. **Part 1 最小可用**：`os.walk` + `defaultdict(list)` 按大小分桶，`len>=2` 的桶流式 SHA-256，再按摘要分桶。
3. **Part 2**：给定的 `_calculate_hash` 当桶键；桶内再用 `files_equal` 把桶切成等价类。
4. **Part 3**：`plan_deletions` 默认 dry-run；先写"每组保留一个"的不变量。
5. **收尾**：排序 key 写全；符号链接、空文件、不可读文件三个边界各过一遍。

## 4. 代码怎么组织
```
_calculate_hash(path)                 # 面试官给的，不改
_strong_hash(path, chunk)             # 流式 SHA-256
files_equal(a, b, chunk)              # 逐块比较，先比大小
_size_buckets(root)                   # os.walk + islink 过滤
scan_duplicates(root, chunk, hash_fn) # 分层引擎；hash_fn=None 用强哈希，否则字节确认
find_duplicates / find_duplicates_verified   # 两个薄封装
plan_deletions(groups, policy, ...)   # 保留策略，dry-run 默认
```
`scan_duplicates` 一个引擎、两个入口，面试官看到"同一套流程，只是桶键换了"最容易跟上；
`hash_fn` 注入也让测试可以塞一个恒为 0 的哈希来证明正确性不依赖它。

## 5. 核心代码（骨架）
```python
buckets = defaultdict(list)
for dirpath, _, names in os.walk(root, followlinks=False):
    for name in names:
        p = os.path.join(dirpath, name)
        if not os.path.islink(p):
            buckets[os.path.getsize(p)].append(p)      # layer 1: free

for paths in buckets.values():
    if len(paths) < 2:
        continue                                       # unique size: never opened
    by_hash = defaultdict(list)
    for p in paths:
        by_hash[hash_fn(p)].append(p)                  # layer 2: stream the file
    for same in by_hash.values():
        classes = []                                   # layer 3: confirm bytes
        for p in same:
            for cls in classes:
                if files_equal(cls[0], p):
                    cls.append(p); break
            else:
                classes.append([p])
        groups += [c for c in classes if len(c) > 1]
groups = sorted((sorted(g) for g in groups), key=lambda g: g[0])
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「Before I code: can I assume exact byte-for-byte duplicates, and that I should not follow symlinks? Empty files count as duplicates of each other?」
- 写分层时：「I filter in order of cost: file size is free, hashing reads the file, byte comparison only runs inside a bucket where hashes collide.」
- 内存：「I never hold file contents; I read in fixed-size chunks, so memory is O(chunk size) plus the path index.」
- 碰撞：「A hash match is only a candidate. With a weak hash I confirm by comparing bytes; with SHA-256 a collision is practically impossible, but deletion is irreversible, so I would still verify before deleting.」
- 删除：「The tool defaults to dry run, always keeps one copy per group, and re-checks size and mtime right before removing to avoid a time-of-check/time-of-use race.」
- system design：「Shard by size or by a cheap prefix hash so each worker sees all candidates of a bucket; then full-hash and byte-compare inside the shard. For S3, ETag is not a content hash for multipart uploads, so I store my own SHA-256 at upload time.」

## 7. 常见跑偏（方法层面，3 条）
- 一上来对所有文件算完整哈希：没有利用"大小唯一就不可能重复"，IO 浪费几个数量级。
- 把"哈希相同"当成"内容相同"就输出：面试官给的 `_calculate_hash` 就是专门来踩这个的。
- 讨论删除时只说"删掉多余的"：没有 dry-run、没有"每组保留一个"的不变量、没提硬链接和并发修改。

## 8. 同族题 / 延伸
- 同一个"代价递增过滤"模式：`../../../snowflake/` 里的去重 / 分组聚合题；`../../millennium/study/30-articles/` 里的流式分组聚合题（只写目录，具体 ID 以目录为准）。
- 近似重复（Part 4）：aHash → dHash → pHash；大规模用 BK-tree 或分段倒排索引。
- 练习命令：`python3 loop/mock.py start pc01`；验收：`python3 tools/verify_suites.py . "loop/rounds/06_legacy_coding/pc01*"`。
