# od02 · In-Memory File System — LC 588, rm/rmdir, chunked content, per-path locks

**类型：** 电面/技术筛（PS，45–60 min，4 part + 追问）· **最近：** 2026-08
**置信度：** HIGH-MED（4 个独立来源交叉，见文末）

## 背景
"设计一个内存文件系统" 是 Snowflake 电面里被四个独立信息源（fastprep、GitHub/darkinterview 训练
笔记、prachub、techprep）反复提到的题，功能上等价于 LC 588，但 Snowflake 的版本明确把它当"数据
结构 + API 设计"题来考，而不是纯算法题——面试官会在候选人写完基础版之后，逐步加 `rm`/`rmdir`、
超大文件的分块存储、以及并发/持久化。这与 Snowflake 自己的元数据服务（一个巨大的、支持并发读写
的层级命名空间）在形状上是一致的。

## API 契约（英文签名）
```python
class FileSystem:
    def ls(self, path: str) -> list[str]: ...
    def mkdir(self, path: str) -> None: ...
    def add_content_to_file(self, file_path: str, content: str) -> None: ...
    def read_content_from_file(self, file_path: str) -> str: ...
    def rm(self, path: str) -> None: ...
    def rmdir(self, path: str) -> None: ...
    def size(self, file_path: str) -> int: ...
```
路径都是以 `/` 开头的绝对路径，用 `/` 分隔组件（根目录 `/` 本身不作为参数传入其他方法，只在
`ls("/")` 时出现）。

## 规则

### Part 1 — LC 588 基础 API
- `ls(path)`：如果 `path` 是文件，返回 `[文件名]`；如果是目录，返回其直接子项名字的**升序排序
  列表**（文件与子目录混在一起统一按字符串排序，不分文件/目录）。
- `mkdir(path)`：递归创建路径上所有缺失的目录（类似 `mkdir -p`）。路径已存在（无论是目录还是
  文件）视为幂等/未定义行为的边界，本题约定：路径已经是目录 → 无操作；路径已经是文件 → 抛
  `FileExistsError`。
- `add_content_to_file(file_path, content)`：文件不存在则创建（其父目录必须已经存在，否则抛
  `FileNotFoundError`——这与 `mkdir` 的"自动创建父目录"不同，故意制造一个候选人常见的踩坑点）；
  文件存在则把 `content` **追加**到已有内容之后。
- `read_content_from_file(file_path)`：返回该文件当前的全部内容（一个字符串）；路径不存在或指向
  目录抛 `FileNotFoundError`/`IsADirectoryError`。

### Part 2 — `rm` / `rmdir`
- `rm(path)`：删除一个文件。路径不存在抛 `FileNotFoundError`；路径是目录抛 `IsADirectoryError`
  （用 `rmdir` 删目录，不允许 `rm` 误删目录）。
- `rmdir(path)`：删除一个**空**目录（没有任何子项）。路径不存在抛 `FileNotFoundError`；路径是
  文件抛 `NotADirectoryError`；目录非空抛 `OSError`（模拟真实文件系统 `rmdir` 拒绝删非空目录的
  行为——本题不提供递归删除）。
- 根目录 `/` 永远不能被 `rm`/`rmdir`，无论是否为空，抛 `PermissionError`。

### Part 3 — 大文件分块存储
真实系统不会把一个文件的内容存成一整个 Python 字符串反复拼接（`content += new_chunk` 是 O(n)
的，重复 `add_content_to_file` 调用 n 次会退化成 O(n²)）。本题要求文件内容内部存成**分块列表**
（每次 `add_content_to_file` 追加一个新的 chunk，而不是拼接进已有 chunk），并新增：
```python
def size(self, file_path: str) -> int: ...  # 总字节数，O(1)：全程维护一个累加的总长度计数器
```
`read_content_from_file` 仍然返回拼接后的完整字符串（`"".join(chunks)`），语义不变；但内部实现
和 `size()` 的存在，是为了让候选人证明自己确实避免了 O(n²) 重复拼接（Part3 有一条 perf 测试，
`add_content_to_file` 10^4 次、每次 100 字符，若内部用 `+=` 拼接会明显超时/超内存）。

### Part 4 — 线程安全：按路径加锁
多个线程可能同时操作文件系统。要求：
- 对**同一个文件路径**的并发 `add_content_to_file` 调用，最终内容必须包含所有线程写入的全部
  chunk（不丢更新），且每个线程自己写入的多个 chunk 之间保持它调用的相对顺序。
- 对**不同路径**的操作不应该被同一把全局大锁串行到"必须排队"的程度——用每个路径（或每个目录
  节点）各自的锁，而不是一把全局锁包住所有方法。允许 `mkdir`/`rm`/`rmdir` 这类改变目录树结构的
  操作使用一把较粗的"目录树结构锁"，但对已存在文件的内容追加应该只锁该文件自己。

## Worked examples

**例 1（Part1，LC 588 经典序列）**
```
mkdir /a/b/c
add_content_to_file /a/b/c/d hello
ls /
ls /a/b/c
read_content_from_file /a/b/c/d
add_content_to_file /a/b/c/d world
read_content_from_file /a/b/c/d
```
→
```
['a']
['d']
hello
helloworld
```
（两次 `add_content_to_file` 是**追加**，不是覆盖：`"hello"` 后追加 `"world"` 得到
`"helloworld"`。`main()` 的行解析规则见下方"边界清单"：content 是路径之后**恰好一个分隔空格**
之后的整行剩余部分，因此如果调用方想让 content 自带前导空格，需要在路径后连续打两个空格——这是
一个刻意的解析陷阱，见边界清单最后一条。）

**例 2（Part2，`rm`/`rmdir` 的错误分支）**
```
mkdir /x
add_content_to_file /x/f hi
rm /x
rmdir /x/f
rmdir /x
rm /x/f
rmdir /x
ls /
```
→
```
ERROR:IsADirectoryError
ERROR:NotADirectoryError
ERROR:OSError
(no output)
(no output)
[]
```
（`rm /x` 对目录抛 `IsADirectoryError`；`rmdir /x/f` 对文件抛 `NotADirectoryError`；`rmdir /x`
此时目录非空抛 `OSError`；`rm /x/f` 成功删除文件后 `rmdir /x` 成功删除空目录；最终 `ls /` 为
空列表。）

**例 3（Part3，分块与 O(1) `size`）**
```
mkdir /d
add_content_to_file /d/big aaaa
add_content_to_file /d/big bbbb
size /d/big
read_content_from_file /d/big
```
→
```
8
aaaabbbb
```

**例 4（Part4，并发追加不丢更新——测试文件里用线程验证，不是 `main()` 命令流）**
50 个线程各自对同一个新建文件 `add_content_to_file` 100 次，每次写入形如 `"t{tid}-{i} "` 的
定长 token；结束后 `size()` 必须恰好等于 `50 * 100 * len(token)`，且 `read_content_from_file`
按 token 切分后，每个线程写入的 100 个 token 相对顺序不变（用正则或 split 校验，而不是要求
跨线程整体顺序确定）。

## `main()` 命令流
```
MKDIR <path>
ADD <path> <content...>          -- content 是本行剩余部分，允许包含空格；用行内第一个空格后的
                                     全部原文（不再 split/strip）作为 content
LS <path>
READ <path>
RM <path>
RMDIR <path>
SIZE <path>
```
`MKDIR`/`ADD`/`RM`/`RMDIR` 成功无输出；失败输出 `ERROR:<ExceptionClassName>`。`LS` 输出
`repr(sorted_list)`（Python list 字面量形式，例如 `['a', 'b']`，空列表输出 `[]`）。`READ`/`SIZE`
成功输出其值（`SIZE` 输出整数的字符串形式），失败输出 `ERROR:<ExceptionClassName>`。

## 边界清单
- `ls("/")` 在没有任何 `mkdir`/文件的初始状态下返回 `[]`
- `ls` 一个文件路径返回 `[文件名]`（长度为 1 的列表），不是文件内容
- `mkdir` 已存在的目录 → 无操作（幂等）；`mkdir` 已存在的文件路径 → `FileExistsError`
- `add_content_to_file` 到一个父目录不存在的路径 → `FileNotFoundError`（不会像 `mkdir` 那样自动
  建父目录——这是本题刻意设计的不对称点，测试专门验证）
- `add_content_to_file` 空字符串内容（合法，等价于无操作但不报错）
- `rm`/`rmdir` 根目录永远 `PermissionError`
- `rmdir` 非空目录 `OSError`；`rmdir` 一个文件 `NotADirectoryError`；`rm` 一个目录
  `IsADirectoryError`
- 路径末尾有无冗余 `/`（如 `/a/b/`）：本题约定路径不带尾部斜杠（除根路径 `/` 本身），带尾部斜杠
  的输入未定义，测试不构造这类输入
- 大量小 chunk（10^4 次 `add_content_to_file`，每次 100 字符）在 2s 预算内完成，且不因为字符串
  拼接退化成 O(n²)
- 并发对同一文件追加不丢更新；并发对不同文件的操作互不阻塞到"整体退化为单线程"的程度（用一个
  计时对照测试：多路径并发明显快于人为强制串行的基线，允许一定误差余量，不做过严的绝对时间断言）
- `main()` 的 `ADD` 行解析：`"ADD /f  world"`（路径后两个空格）→ content 是 `" world"`（保留了
  第二个空格作为内容的一部分）；`"ADD /f world"`（一个空格）→ content 是 `"world"`；`"ADD /f "`
  （路径后只有一个空格、没有更多字符）→ content 是空字符串 `""`

## 并发追问
1. "为什么不干脆一把全局锁包住整个 `FileSystem`？" —— 期望候选人指出全局锁会让互不相关路径的
   操作互相阻塞，在元数据服务这种高并发场景下吞吐会被拖垮；per-path/per-node 锁让无关操作并行。
2. "两个线程同时 `mkdir` 同一条尚不存在的路径，会不会创建出两份重复的目录节点？" —— 期望候选人
   讨论"创建节点"这一步本身需要在父目录的锁下做"不存在则创建"的原子检查（check-then-create
   race），而不是先检查再在锁外创建。
3. "如果要支持崩溃恢复，怎么把这套分块内容结构做成 WAL + 快照？" —— 期望候选人提出"每次
   `add_content_to_file` 先写 WAL 再修改内存结构，定期把内存树整体快照落盘，恢复时先加载最近
   快照再重放快照之后的 WAL"，这是来源里明确点出的下一步追问方向。

## 变体
- GitHub/darkinterview 的训练版本约束很小（路径 ≤100 字符、内容 ≤50 字符、≤300 次调用），
  fastprep 的电面版本明显放大（ops ≤2000、内容 ≤1000 字符、总操作字符串长度 ≤200,000）——同一
  道题在不同候选人身上给的是不同规模，本题的 perf 预算取 fastprep 的电面规模。
- 一处来源提到"支持通配符路径查询"作为罕见的高阶变体，未见二次印证，不建入本题。

## 来源与置信度
- https://www.fastprep.io/problems/snowflake-design-in-memory-file-system （Hard, Phone Screen）
- https://raw.githubusercontent.com/harry-the-nerd/interview-notes-questions/main/snowflake/design-in-memory-file-system.md
  （引用 darkinterview.com："this is a common Snowflake interview question around data structures
  and API design"，明确列出 `rm`/`rmdir`、分块大文件、锁、快照+WAL 四个追问方向）
- https://prachub.com/interview-questions/design-an-in-memory-file-system （2026-08-24）
- https://www.techprep.app/companies/snowflake （"low-level design questions" 分类下列出）
- `catalog/raw/ood.md` #3、`catalog/CATALOG.md` Table B od02 行；置信度 **HIGH-MED**：4 个独立
  聚合来源 + 明确映射到 LC 588。

## 考什么
S09 类设计先定 API 契约（对称 vs 不对称的错误策略要讲清楚）· S10 并发正确性（per-path 锁粒度）·
S11 持久化与恢复（WAL + 快照追问）· S12（间接，分块存储与缓存分页思路相通）· S20 自测试
