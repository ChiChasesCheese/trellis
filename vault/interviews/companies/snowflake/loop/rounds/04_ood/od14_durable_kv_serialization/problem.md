# od14 · Durable Key-Value Store Serialization — 长度前缀编码 + 分块落盘 + 崩溃原子性

> TrueInterview 同步清单第 71 题 "Durable Key-Value Store Serialization"（LLD，2025-11 报告）；
> 1point3acres 问题库另有一条同名标题 "Durable Key-Value Store Serialization"
> （`https://www.1point3acres.com/interview/problems/post/7100062`，仅标题）。题面付费，确认的
> 骨架只有："`put/get/shutdown/restore`，不许用 `json`/`pickle`，键值可以包含任意字符（含换
> 行、冒号、unicode）——用长度前缀编码"。分块落盘的具体机制、元数据格式、崩溃原子性全部
> **(reconstructed)**。

## 背景

一个"优雅关闭时落盘、重启时恢复"的内存 KV store。真实约束是：① 不能用 `json`/`pickle`（键值
可能包含任何字节，包括这两种格式的转义字符本身）；② 底层文件系统（这里用一个内存 fake 模拟）
对单个文件大小有上限（本题设定 1024 字节），所以大 store 必须自己切块；③ 落盘不是原子的——
进程可能在写到一半时崩溃，重启后 `restore()` 不能读到"一半新快照 + 一半旧快照"的损坏状态。

## API 契约（英文签名）

```python
class FileSystem:                                    # 提供的内存 fake，Part 1 起就是这个接口
    def save_blob(self, filename: str, data: bytes) -> None: ...   # 超过 1024 字节抛 ValueError
    def get_blob(self, filename: str) -> bytes: ...                # 不存在抛 FileNotFoundError
    def list_files(self) -> list[str]: ...

class KVStore:
    def __init__(self, fs: FileSystem) -> None: ...
    def put(self, key: str, value: str) -> None: ...
    def get(self, key: str) -> str | None: ...
    def shutdown(self) -> None: ...     # 序列化并落盘当前全部数据
    def restore(self) -> None: ...      # 从 fs 读回最近一次成功落盘的快照，覆盖内存状态
```

## 规则

### Part 1 — 长度前缀编码（禁止 `json`/`pickle`）

- 编码格式（netstring 风格）：把每个 `(key, value)` 编码成
  `<len(key的UTF-8字节数)>:<key字节><len(value的UTF-8字节数)>:<value字节>`，按 key 排序后依次
  拼接。长度永远写在数据前面，所以**键值可以包含任何字符（换行、冒号、unicode）而不需要任何
  转义**——不存在"分隔符出现在数据里怎么办"这个问题，因为解析方永远先读长度、再原样取那么多
  字节，根本不去找分隔符。
- `shutdown()` 序列化当前全部键值对并落盘；`restore()` 从 fs 读回上一次成功落盘的快照，**覆
  盖**当前内存状态（不是合并）。`restore()` 在 fs 从未 `shutdown()` 过时（没有任何快照）安全
  地得到一个空 store，不报错。

### Part 2 — 分块落盘（每个文件 ≤ 1024 字节）**(reconstructed)**

- `FileSystem.save_blob` 本身强制单个 blob ≤ 1024 字节（模拟真实 blob 存储的限制）——这意味着
  `KVStore` 必须**自己**把序列化后的完整字节流切成多个 ≤1024 字节的分块，分别调用
  `save_blob("chunk_g<gen>_<i>", chunk)` 落盘，`gen` 是本次快照的生成号（Part 3 引入，Part 2
  单独使用时可以理解成"当前唯一版本号"）。
- **UTF-8 边界**：切块发生在**编码后的原始字节流**上，可能切在一个多字节 UTF-8 字符的中间——
  这完全没问题，因为解码只发生在 `restore()` 把所有分块重新拼接成完整字节流**之后**，任何一
  个分块单独拿出来解码都可能是非法 UTF-8，但这从未被要求过（本题的选择：先分块存字节，重装后
  再解码一次；另一种选择是"分块前先按字符边界切"，但那样切块大小就不再精确等于 1024 字节，权
  衡取舍见"追问"）。
- 元数据：一个额外的 `"meta"` blob 记录 `<generation>\n<num_chunks>\n<total_len>\n`；
  `restore()` **只**按元数据声明的 `num_chunks` 去读 `chunk_g<generation>_0 .. chunk_g<generation>_(num_chunks-1)`，
  **从不**扫描 fs 里所有以 `chunk_` 开头的文件——这正是"陈旧分块不能污染 restore"的关键：如果
  上一份快照有 5 个分块、这一份缩小到只需要 1 个分块，旧的 4 个分块文件会原样留在 fs 里，但
  `restore()` 根本不会去看它们。
- 空 store：`shutdown()` 落盘 `num_chunks=0`，`restore()` 直接得到 `{}`，不需要任何分块文件。

### Part 3 — 崩溃原子性 **(reconstructed)**

- 每次 `shutdown()` 都在一个**全新的生成号**（`generation`）下写分块（文件名带 `gen` 编号，
  绝不覆盖旧生成号的文件），**元数据永远是最后一次写**——只有元数据成功落盘，这次快照才算"提
  交"。如果 `save_blob` 在写分块的过程中（元数据落盘之前）抛异常（模拟崩溃），元数据仍然指向
  上一个生成号，`restore()` 读到的还是上一次**完整**提交的快照，新生成号写了一半的分块文件永
  远不会被任何 `restore()` 引用到。
- **生成号从 fs 读，不从内存读**：`shutdown()` 每次都先读 fs 当前的 `"meta"` 来确定"下一个生
  成号"，而不是信任 `KVStore` 实例自己内存里维护的计数器——否则一个**从未调用过 `restore()`
  的全新进程**（比如崩溃重启后新建的 `KVStore` 对象）会从生成号 0 开始，直接和 fs 里已经提交
  的生成号 1 撞车，覆盖掉分块文件，造成数据损坏。这是本题最容易被面试官问到的坑，见"边界清单"
  与"追问"。

### 命令流

```
PUT <key> <value>     无输出（命令行协议里 value 不含空格/换行，富字符场景走类 API 直接测试）
GET <key>             输出 value，不存在输出字面量 None
SHUTDOWN              无输出
RESTORE               无输出
FILES                 Part 2/3：输出 fs.list_files() 空格拼接，空 → -
```

## Worked examples（全部由 `solution.py` 实际运行得出）

```
PART 1
PUT a 1
PUT b hello
SHUTDOWN
GET a          → 1
RESTORE
GET a          → 1
GET missing    → None
```

```
直接调用类 API（验证任意字符）：
store.put('key:with:colons', 'val\nwith\nnewlines')
store.put('unicode', '你好世界🎉')
store.shutdown()
新建 KVStore(同一个 fs).restore() 后：
  get('key:with:colons') == 'val\nwith\nnewlines'
  get('unicode') == '你好世界🎉'
```

```
编码示例：
_encode_entries({'a': '1', 'b': 'hello world'}) == b'1:a1:11:b11:hello world'
落盘后 fs.list_files() == ['chunk_g1_0', 'meta']   （数据很小，只需要 1 个分块）
```

```
分块（100 个 40 字节的 value）：
fs.list_files() 里 chunk_g1_0 .. chunk_g1_4 共 5 个分块 + meta；restore 后全部 100 个键值往返
一致。
```

```
陈旧分块不污染 restore：
第一次 shutdown（5 个分块，含 k0..k99）之后，第二次用一个全新的 KVStore(同一个 fs) 实例
（从未 restore 过）只 put('only','x') 就 shutdown：
  生成号从 fs 读到 1，本次落盘为 gen2；fs.list_files() 里 chunk_g1_0..4 依然都在，但新增
  chunk_g2_0 + meta 被覆盖指向 gen2。
第三个 KVStore(同一个 fs).restore() 之后：get('only') == 'x'，get('k0') is None
  （旧快照的分块文件还在磁盘上，但 restore 完全不看它们）。
```

```
崩溃原子性：
storex.put('a','1'); storex.shutdown()          # gen1 提交成功
# 模拟：fs.save_blob 在第 2 次调用起开始抛异常
storex.put('b','2')
storex.shutdown()                                # 抛 OSError（分块写到一半"崩溃"）
用同一个 fs 新建 KVStore.restore()：get('a') == '1'，get('b') is None
  （gen2 的元数据从未成功落盘，gen1 仍是唯一"已提交"的快照）。
```

## 边界清单

- 键值包含换行、冒号、unicode（多字节 UTF-8）：`shutdown`→`restore` 往返必须完全一致
- 空 store：`shutdown()` 落盘 0 个分块，`restore()` 得到 `{}`
- `restore()` 在 fs 从未 `shutdown()` 过（没有 `"meta"`）时：安全地得到空 store，不报错
- 大 store：分块数 > 1，`restore()` 必须完整重装所有分块再解码，且顺序正确
- 分块边界可能切在某个字符的 UTF-8 多字节序列中间——只要重装后再解码，往返必须正确
- 陈旧分块：新快照的分块数少于旧快照时，旧快照多出来的分块文件必须被完全忽略，不能污染
  `restore()` 的结果
- 崩溃原子性：`save_blob` 在写分块阶段（元数据落盘之前）抛异常，`restore()` 必须精确返回**上
  一次完整提交**的快照，新数据的任何部分都不能出现
- **生成号必须从 fs 读，不能只信任内存计数器**：一个从未调用过 `restore()` 的全新
  `KVStore(同一个 fs)` 实例调用 `shutdown()`，不能与 fs 里已经提交的生成号相撞（这是本题设计
  上最容易被忽视的坑，见 worked example 与追问 1）
- 元数据本身损坏（无法解析生成号/分块数/长度）→ `restore()` 抛 `ValueError`，不静默返回部分
  数据
- 单个分块永远 ≤ 1024 字节（`FileSystem.save_blob` 自身强制这条不变量）

## 追问

1. **为什么生成号不能只存在 `KVStore` 实例的内存里？** 因为"内存状态"和"持久化状态"的生命周
   期不一样——`KVStore` 对象可能在每次请求后重建（无状态服务的常见模式），但 fs 是跨请求持久
   的；如果生成号只活在实例内存里，任何一次"重建 KVStore 对象但没调用 `restore()`"的场景都会
   把生成号计数器归零，下一次 `shutdown()` 就会覆盖掉 fs 里已经存在的同名生成文件。这个坑本题
   刻意设计成一个可测试的边界（"未 restore 的全新实例 shutdown 不能撞车"），因为它是候选人最
   容易一开始就写对、但换个测试顺序就暴露出来的隐藏 bug。
2. **分块要不要按字符边界切（而不是按字节数切）？** 按字符切能保证"单独拿出某个分块也能独立
   解码"，但代价是分块大小不再精确等于 1024 字节上限（一个字符可能正好卡在边界，逼你把它整个
   挪到下一块，某些分块因此明显小于上限，浪费"每个文件尽量填满"的空间效率）；本题选择"按字节
   切、整体重装后再解码"，把"分块"和"解码"完全解耦，简单且不浪费空间，代价是分块本身不能独立
   解码——这是候选人应该主动指出的权衡，而不是被问到才想起来。
3. **如果两个进程同时对同一个 fs 调用 `shutdown()`（真实场景是多副本/多线程共享一个持久化后
   端）会怎样？** `_committed_generation()` 读取 + 写入分块 + 写入元数据这三步不是原子的——两
   个并发 `shutdown()` 可能读到同一个"当前生成号"，各自计算出同一个"新生成号"，导致互相覆盖对
   方的分块文件（即使最终元数据只会指向其中一个的生成号，另一个的分块可能已经被部分覆盖，如
   果这时候又有第三次 `shutdown()` 用同一个撞车的生成号，正确性就无法保证）。修复需要给
   `_committed_generation()` 到写元数据这一整段加锁，或者用**乐观并发**（生成号读的时候顺带
   拿一个版本号，写元数据时做 compare-and-swap，失败就重新读生成号重试）。
4. **崩溃点如果发生在元数据写入**之后**（比如写完了但确认响应丢失），调用方怎么知道要不要重
   试？** 本题的元数据写入本身被视为原子操作（`FileSystem` fake 里 `save_blob` 要么完整成功
   要么完全不写），所以"元数据写完但确认丢失"在这个 fake 的语义下不存在——但如果换成真实的分
   布式存储（比如对象存储的 PUT 请求超时但实际已经落地），调用方必须能安全地重试同一次
   `shutdown()`（此时新生成号会被再次计算——如果重试时读到的仍是上一次成功的元数据，会尝试用
   同一个生成号重新写一遍，这是幂等的，安全）。

## 来源与置信度

- **MED**：kevin-2023-code/Tech-Interview-Questions（TrueInterview 同步清单）第 71 题
  "Durable Key-Value Store Serialization"，LLD，2025-11 报告；正文付费，只见标题、格式标签与
  "put/get/shutdown/restore，禁止 json/pickle，键值含任意字符——用长度前缀编码"这句预览摘要。
  见 `../../../catalog/raw/github_repos.md` §2 第 71 行、§3 "od14" 一条。
- **medium，标题级**：1point3acres 问题库同名标题 "Durable Key-Value Store Serialization"
  （`https://www.1point3acres.com/interview/problems/post/7100062`，仅标题），见
  `../../../catalog/raw/system_design.md` §1（KV store 系列汇总段落 38 行）。两条来源互相印证
  题目存在，但都没有给出规则文本。
- 分块落盘机制、元数据格式、生成号与崩溃原子性设计全部 **(reconstructed)**。

## 考什么

S09 类设计先定契约（"用长度前缀而不是转义"这条判断要在写代码前想清楚）· S11 持久化与恢复
（分块、元数据、生成号、崩溃原子性——与 od02/od05 的"崩溃不丢触发"同族）· 自定义序列化格式
（与 od13 的 trie 编码、od15 的 JSON 语法同族，都是"先定字符集/长度约定再证明无歧义"）。
