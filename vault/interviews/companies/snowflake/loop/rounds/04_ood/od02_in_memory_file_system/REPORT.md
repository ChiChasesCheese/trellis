# od02 In-Memory File System — report

## Summary
LC 588 的类设计变体：一棵 `_Dir`/`_File` 节点树，从基础 `ls/mkdir/add_content_to_file/
read_content_from_file` 出发，逐步加 `rm`/`rmdir`、大文件分块存储（避免 O(n²) 字符串拼接）、
以及 per-path 锁而非全局大锁的并发模型。Snowflake 把这题当"数据结构 + API 设计"考，重点是候选人
是否会主动指出 `mkdir` 与 `add_content_to_file` 在"父目录不存在时怎么办"上应该不对称、以及全局锁
在高并发命名空间下的吞吐问题。

## Sources & confidence
HIGH-MED——4 个独立来源交叉：fastprep（Phone Screen，Hard）、GitHub/darkinterview.com 训练笔记
（明确称"a common Snowflake interview question around data structures and API design"，并列出
`rm`/`rmdir`、分块、锁、WAL+快照四个追问方向）、prachub、techprep.app 的 low-level-design 分类。
四个来源规模不同（GitHub 版 ≤300 次调用/内容≤50字符，fastprep 电面版 ops≤2000/内容≤1000字符），
本题 perf 预算取电面版规模。

## Approach by part
1. 路径统一解析成组件列表（`_split`），根路径对应空列表；`_get_node` 沿途逐级检查类型，缺失/
   类型不符分别抛 `FileNotFoundError`/`NotADirectoryError`。`mkdir` 的"父目录自动创建"与
   `add_content_to_file` 的"父目录必须已存在"是刻意的不对称设计点。
2. `rm`/`rmdir` 各自校验"目标类型是否匹配操作"（`rm` 拒绝目录、`rmdir` 拒绝文件）、"目录是否为空"
   （`rmdir` 拒绝非空），以及根目录的 `PermissionError` 兜底。
3. `_File` 内容存成 `chunks: list[str]`，`add_content_to_file` 只 `append`，从不 `+=` 拼接；
   `total_len` 随每次 append 增量维护，`size()` 因此是 O(1) 而不需要 `"".join(chunks)`。
4. 并发模型：一把 `_tree_lock` 只在"遍历/修改树结构"这段 O(depth) 临界区内持有（包括为新文件插入
   `_File` 节点的那一刻）；一旦拿到具体的 `_File` 引用就释放 `_tree_lock`，改用该文件自己的
   `threading.Lock` 做内容追加——不同路径的写入因此不会互相排队等同一把全局锁。

## Pitfalls hidden tests target
- `mkdir` 对已存在目录幂等、对已存在文件抛 `FileExistsError`
- `add_content_to_file` 父目录缺失时**不会**像 `mkdir` 一样自动创建，而是 `FileNotFoundError`
- `rm`/`rmdir` 的错误类型必须精确匹配"操作 vs 目标类型"的四种组合，外加根目录的
  `PermissionError`
- `size()` 必须是维护的累加值，不是每次 `len("".join(chunks))`（perf 测试用 2 万次小追加检测
  O(n²) 拼接）
- 并发追加到同一文件：不丢更新 + 每个线程自己写入的多个 chunk 保持相对顺序（用 `re.findall` 按
  线程分组校验，而不是断言跨线程整体顺序）
- `main()` 的 `ADD` 行解析规则（`split(" ", 2)`）：路径后连续两个空格时第二个空格是 content 的
  一部分，这是刻意的解析陷阱

## Complexity & measured cost
`ls`/`mkdir`/`rm`/`rmdir`/`add_content_to_file`/`read_content_from_file`/`size` 均为 O(depth) 树
遍历 + O(1) 或 O(内容长度) 的文件级操作。perf 测试：2 万次 50 字符追加到同一文件，测得
~0.02s（远低于 2s 预算），`size()` 全程 O(1)。

## Test inventory
22 tests — part1: 11（含 1 io、1 fmt）· part2: 5（含 1 io）· part3: 4（含 1 perf）· part4: 2；
edge 12 · fmt 1 · io 3 · perf 1。

## Skills exercised
S09 类设计先定 API 契约（不对称的错误策略要主动讲清楚）· S10 并发正确性（per-path 锁粒度，
而非一把全局锁）· S11 持久化与恢复（WAL + 快照，追问层面）· S12（间接，分块存储与缓存分页思路
相通）
