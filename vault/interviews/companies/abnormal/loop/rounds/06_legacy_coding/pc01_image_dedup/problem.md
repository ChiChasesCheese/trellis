# pc01 · Image dedup — 在一堆文件里找重复，弱哈希碰撞怎么办，怎么安全地删

> Abnormal 的"旧流程"编码轮（电面 / 第一轮，"20 min 讨论 + 30 min 写"）：不是 LeetCode，是一道会
> 一路追问到 system design 的文件系统题。先讨论方案（内存有限怎么办、哈希碰撞怎么办），再写
> `main`，最后聊"海量照片怎么办"。

## 背景

一手原话（1point3acres 帖 1059585 / 1072363 / 1074077 / 1137132，2024-04 → 2025-07，四帖互相印证，
置信度中）：

- "给你一堆图片，找出 duplicate 的图片；如果 memory 有限怎么做；如果要 hashing 怎样做；如果有 hashing collision……"
- "写出 main function，我写的 python，给了 `os.walk` 的用法提示，直接 call 他给的 `_calculate_hash`
  会有 hash collision，问解决方法，最后问 system design"
- "如果你的 file system 里面有很多照片，如何删除重复的照片"
- PracHub 2025-07 另有两个标题："Design a duplicate-file removal algorithm" / "Design a scalable photo deduplication service"

四帖没有给出完整题面。本题据此重建：Part 1（找重复）、Part 2（给定的 `_calculate_hash` 会碰撞）
是一手原话的直接落地；Part 3（删除策略）与 Part 4（近似重复）**(reconstructed)**。给定的
`_calculate_hash` 的具体弱法（"前 1 KiB 的 CRC32，用文件大小做种子"）也是 **(reconstructed)**——
帖子只说"会碰撞"。

## API 契约（英文签名）

```python
DEFAULT_CHUNK = 1 << 16

def _calculate_hash(path: str) -> int: ...          # GIVEN, deliberately weak (see Part 2)

@dataclass
class ScanResult:
    groups: list[list[str]]
    skipped: int                                    # unreadable files

def files_equal(a: str, b: str, chunk_size: int = DEFAULT_CHUNK) -> bool: ...
def scan_duplicates(root: str, chunk_size: int = DEFAULT_CHUNK,
                    hash_fn: Callable[[str], object] | None = None) -> ScanResult: ...
def find_duplicates(root: str, chunk_size: int = DEFAULT_CHUNK) -> list[list[str]]: ...
def find_duplicates_verified(root: str, hash_fn=_calculate_hash,
                             chunk_size: int = DEFAULT_CHUNK) -> list[list[str]]: ...

def plan_deletions(groups: list[list[str]], policy: str = "oldest",
                   prefer_dir: str | None = None, dry_run: bool = True) -> list[str]: ...

def average_hash(matrix: list[list[int]]) -> int: ...
def hamming(a: int, b: int) -> int: ...
def group_similar(images: dict[str, list[list[int]]], threshold: int = 5) -> list[list[str]]: ...
```
只用标准库（`os`、`hashlib`、`zlib`、`tempfile`）；不依赖 PIL。

## 规则

### Part 1 — `find_duplicates(root, chunk_size)`
- `os.walk(root)` 遍历（**不跟随**符号链接：文件符号链接、目录符号链接、悬空链接都既不进入也不计入）。
- **先按文件大小分桶**：大小唯一的文件不可能有重复，**根本不读取**。
- 同大小的文件再按**完整内容**的哈希（SHA-256）分桶，哈希必须**流式**：每次 `read(chunk_size)`，
  不能一次把整个文件读进内存（测试用 `tracemalloc` 卡 4 MiB 文件的峰值 < 1 MiB）。
- 输出 `list[list[str]]`：每组至少 2 个路径；**组内路径排序，组按首路径排序**。
- 空文件（0 字节）彼此就是重复，成一组。
- 不可读文件（`OSError`）跳过，计入 `scan_duplicates(...).skipped`，其余文件照常处理。
- `chunk_size <= 0` → `ValueError`。

### Part 2 — 给定的 `_calculate_hash` 会碰撞
- `_calculate_hash(path)` 是面试官给的：对文件**前 1 KiB** 做 CRC32，用文件大小做种子。两个同样大小、
  前 1 KiB 相同的文件**必然碰撞**（比如照片被改了末尾的元数据）。
- `find_duplicates_verified(root, hash_fn=_calculate_hash, chunk_size)`：哈希相同**只代表候选**。
  同一哈希桶里用 `files_equal(a, b, chunk_size)`（逐块字节比较，遇到第一个不同块就停；大小不同
  直接 False）把桶切成真正的**内容等价类**；等价类大小 ≥ 2 才输出。
- 对**任何** `hash_fn` 都必须正确，包括恒返回 0 的哈希（正确性来自字节比较，哈希只是剪枝）。
- 不可读文件规则同 Part 1。

### Part 3 — `plan_deletions(groups, policy, prefer_dir, dry_run)` **(reconstructed)**
- 每组保留一个，返回要删的路径（排序后的 `list[str]`）。保证**每组恰好保留一个**，绝不删光。
- `policy`：`"oldest"`（最早 mtime 保留）· `"shortest_path"`（路径最短保留）· `"prefer_dir"`
  （保留位于 `prefer_dir` 之下的一份；该组在 `prefer_dir` 下没有副本就回落到 `"oldest"`）。
- 平局：先路径更短，再字典序。`prefer_dir` 的"之下"按目录边界判断（`originals_backup/` 不在
  `originals/` 之下）。
- `dry_run=True` 是**默认值**，只返回计划不动文件；`dry_run=False` 真删并返回删掉的列表。
- 未知 policy、`prefer_dir` 策略没给目录 → `ValueError`；一组中只剩 1 个还存在的文件（另一个已消失）
  → 该组不产生删除；空输入 → `[]`。

### Part 4 — 近似重复：average hash **(reconstructed)**
- 视觉相同但字节不同（重新压缩、改亮度）：输入是 8×8 灰度矩阵（不依赖 PIL）。
- `average_hash(matrix)`：64 位整数，行优先、最高位在前，像素 **严格大于** 均值记 1。
  形状不是 8×8 → `ValueError`。用整数比较 `v * 64 > sum`，不引入浮点。
- `hamming(a, b)`：不同的位数。
- `group_similar(images, threshold)`：汉明距离 ≤ `threshold` 视为相似，**传递闭包**（a~b、b~c 则
  同组，即使 a≁c，用并查集）；只输出 ≥ 2 的组；组内与组间均按名字排序；`threshold < 0` → `ValueError`。

## Worked examples（全部由 `solution.py` 实际运行得出）

`main()` 把命令流描述的文件树建在临时目录里再调用对应 API（`FILE <相对路径> <内容> [mtime]`，
内容无空格，缺省为空文件；`LINK <相对路径> <目标相对路径>` 建符号链接）。Part 1/2 用 `chunk_size=4`。

**Part 1**
```python
part1(["FILE a/x.jpg cat", "FILE b/y.jpg cat", "FILE c/z.jpg dog", "FILE d/w.jpg cat",
       "FILE e/e1.jpg", "FILE e/e2.jpg", "LINK f/l.jpg a/x.jpg", "FILE g/u.jpg lonely"])
```
→ `["a/x.jpg b/y.jpg d/w.jpg", "e/e1.jpg e/e2.jpg"]`
（三份 `cat` 一组；两个空文件一组；`dog` 与 `lonely` 大小唯一；`f/l.jpg` 是符号链接，被忽略）

**Part 2**（`H` = 1024 个 `H` 字符）
```python
part2(["FILE a.bin H…HA", "FILE b.bin H…HB", "FILE c.bin H…HA", "FILE d.bin H…HB"])
```
→ `["a.bin c.bin", "b.bin d.bin"]`
（四个文件大小相同、前 1 KiB 相同，`_calculate_hash` 全部碰撞成一个桶；字节比较把它拆成 `A` 组与 `B` 组）

**Part 3**
```python
part3(["POLICY oldest", "FILE a/x.jpg cat 300", "FILE b/y.jpg cat 100",
       "FILE c/long_name_z.jpg cat 200", "FILE d/q.jpg dog 5", "FILE d/r.jpg dog 5"])
```
→ `["a/x.jpg", "c/long_name_z.jpg", "d/r.jpg"]`
（`cat` 组保留 mtime=100 的 `b/y.jpg`；`dog` 组 mtime 与路径长度都相同，字典序决定保留 `d/q.jpg`）

**Part 4**（`a` 上半黑下半白；`b` 与 `a` 只差 1 个像素；`c` 是上下颠倒）
```python
part4(["THRESHOLD 2", "IMG a 0,…,255", "IMG b …", "IMG c …"])
```
→ `["a b"]`（`hamming(a, b) = 1 ≤ 2`；`c` 与它们差 64 位 / 63 位）

## `main()` 命令流

```
PART 1                 PART 3                      PART 4
FILE a/x.jpg cat       POLICY oldest|shortest_path THRESHOLD 2
FILE b/y.jpg cat       |prefer:<dir>               IMG a <64 个逗号分隔整数>
LINK f/l.jpg a/x.jpg   FILE a/x.jpg cat 300        IMG b <...>
                       FILE b/y.jpg cat 100
→ a/x.jpg b/y.jpg      → a/x.jpg                   → a b
```
`PART 2` 与 `PART 1` 同格式但走 `find_duplicates_verified`。输出每组一行（空格分隔相对路径）；
无结果则不输出。

## 边界清单

- 空目录 / 没有重复 → `[]`；空文件互为重复；符号链接（文件 / 目录 / 悬空）不跟随
- 大小唯一的文件**不被打开**（测试用 `open` 的监听验证）
- 差异只在**最后一个字节**、或 `chunk_size` 恰好等于 / 大于文件大小时仍然正确
- 同桶里既有真重复又有碰撞的假重复：必须拆成多个等价类（`a1,a2,a3` / `b1,b2` / `c1` 单独不输出）
- `hash_fn` 恒为 0 时结果与强哈希版逐字相同
- 不可读文件：计数，不中断，不进入任何组（测试同时用 `chmod 000` 与"读时抛 `PermissionError`"两种方式；
  前者在 root 下会被跳过）
- `plan_deletions`：组只有 1 个、另一个已消失、未知策略、`prefer_dir` 的前缀兄弟目录
- `average_hash`：纯色图（没有像素严格大于均值）= 0；整体提亮不改变哈希

## 追问

1. **内存有限怎么办？** 只在内存里保存 `大小 → 路径列表` 与"同大小桶"的摘要；文件内容永远按
   `chunk_size` 流式读。路径列表本身太大（亿级）时落盘：先把 `(size, path)` 写成按 size 外排序的文件。
2. **为什么先按大小、再哈希、最后字节比较？** 代价递增、过滤力度递减：大小是 `stat`，免费；哈希要读
   整个文件；字节比较在碰撞桶里才做，且遇到第一个不同块就停。
3. **哈希冲突怎么办？** 加密哈希（SHA-256）的碰撞在实践中可忽略，但**"可忽略"不等于"可以删"**——
   删除不可恢复，成本不对称，所以删除前可以再做一次字节比较（belt and braces）；弱哈希则**必须**验证。
4. **只哈希前 1 KiB 有什么用？** 当作**廉价的第一道剪枝**（大文件上能省掉绝大多数完整读取），
   不能当作相等判据。常见分层：size → 头 4 KiB 哈希 → 完整哈希 → 字节比较。
5. **硬链接**：同一个 inode 的两个路径内容当然相同，但删一个不会释放空间，且可能破坏意图——
   `(st_dev, st_ino)` 相同的路径应折叠成一个，不算重复。
6. **TOCTOU**：`plan_deletions` 与真正 `os.remove` 之间文件可能被改——删除前重新比较 `size + mtime`
   （或再哈希一次）；永远先 dry-run，再让人确认。
7. **海量文件（分布式）**：按 `size` 或"头 4 KiB 哈希前缀"分片到不同 worker，同分片才可能重复
   （MapReduce 式两阶段：阶段 1 按廉价键 shuffle，阶段 2 每个分片内做完整哈希 + 字节比较）。
8. **对象存储**：S3 的 `ETag` 对 multipart 上传是"各分片 MD5 再取 MD5 加分片数"，同样内容、不同分片
   大小得到不同 ETag；SSE-KMS 加密对象的 ETag 也不是内容 MD5。不能直接拿 ETag 判重——要用上传时自己写的
   `x-amz-checksum-sha256` 或自维护的内容哈希索引。
9. **照片去重服务**：上传时算内容哈希（精确去重，内容寻址存储）+ perceptual hash（aHash / dHash / pHash），
   用 BK-tree 或把 64 位哈希切成 4 段做倒排索引（汉明距离 ≤ 3 时至少有一段完全相等）做近邻查询；
   "相似"只能提示、不能自动删。
10. **aHash 的局限**：对旋转、裁剪、镜像不鲁棒；对整体亮度不敏感（这是优点）；纯色图全是 0，会互相"相似"
    ——生产里要先过滤低方差图。

## 来源与置信度

中（四帖独立描述同一类题，2024-04 至 2025-07；是否同一人未知）。Part 1/2 的结构与追问链是一手原话；
`_calculate_hash` 的具体弱法、Part 3、Part 4 与全部测试规模均为重建。
证据：`../../../../catalog/raw/questions_reported.md` Q16。

## 这题考什么

分层过滤（便宜的先做）· 流式 IO 与内存意识 · 正确性不能押在哈希上（碰撞）· 破坏性操作的安全设计
（dry-run、保留至少一份、TOCTOU）· 从单机算法讲到分布式与对象存储的 system design 过渡。
