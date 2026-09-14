# od14 · Durable Key-Value Store Serialization：生成号必须从持久层读，不能信任内存

> [!tldr]
> - 这题考的是：长度前缀编码 + 分块落盘 + 崩溃原子性的类设计——"内存状态"和"持久化状态"生命周
>   期不一样，这条判断决定了整题最容易踩的坑
> - 三步套路：netstring 风格长度前缀编码（键值含任意字符不需要转义）→ 单文件 ≤1024 字节强制
>   分块落盘 + 元数据只认自己声明的分块数 → 每次落盘用新生成号，元数据最后写，且生成号**从
>   fs 读，不是从内存读**
> - 最值得带走的一个模式：**任何"版本号/生成号"类的协调状态，如果只存在进程内存里，就会在"对
>   象被重建但没有走恢复流程"这个场景下归零，进而撞车覆盖掉持久层已经存在的数据——协调状态的
>   权威来源必须是持久层本身，不是内存计数器**

## 1. 题目在说什么（人话版）

一个内存 KV store，`shutdown()` 时把当前全部数据落盘，`restore()` 时从磁盘读回最近一次成功落
盘的快照。约束：不能用 `json`/`pickle`（键值可能包含任意字符）；单个文件大小上限 1024 字节，
大 store 必须自己切块；落盘不是原子的，进程可能写到一半崩溃，`restore()` 不能读到"一半新快照
+ 一半旧快照"的损坏状态。

三行小例子：
```
store.put("a", "1"); store.shutdown()
new_store = KVStore(同一个 fs); new_store.restore()
new_store.get("a") -> "1"
```

## 2. 读题：把文字变成模型

- **实体**：内存字典、`FileSystem` fake（`save_blob`/`get_blob`/`list_files`，单 blob ≤1024
  字节）、生成号（`generation`）、元数据 blob。
- **输入长什么样**：`put(key, value)`（任意字符，含换行/冒号/unicode）、`shutdown()`、
  `restore()`。
- **输出要什么**：`get(key)` 返回当前值或 `None`；`shutdown`/`restore` 无返回值，只改变
  fs/内存状态。
- **状态**：内存字典 + fs 里的若干 `chunk_g<gen>_<i>` blob + 一个 `"meta"` blob（记录
  `generation`/`num_chunks`/`total_len`）。
- **一句话建模**：这是一道**持久化与恢复**的类设计题——长度前缀编码解决"任意字符不需要转义"，
  分块解决"单文件大小限制"，生成号 + 元数据后写解决"崩溃原子性"。

> [!note] 为什么用长度前缀而不是转义
> `json`/`pickle` 被禁用是因为键值可能包含任何字节，包括这两种格式自己的转义字符本身。
> netstring 风格编码把长度写在数据前面（`<len>:<字节>`），解析方永远先读长度、再原样取那么多
> 字节，根本不需要去找分隔符——不存在"分隔符出现在数据里怎么办"这个问题。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`_encode_entries`/`_decode_entries` 实现 netstring 编解码；`KVStore` 只有
   `put`/`get`/内存字典，`shutdown`/`restore` 先直接存/取一个大 blob（暂不管 1024 字节限制）。
2. **Part 1 最小可用**：验证键值含换行/冒号/unicode 的往返正确性。
3. **Part 2 叠加**：`shutdown` 把编码后的**原始字节流**（不是解码后的字符）切成 ≤1024 字节的
   分块分别落盘；写一个 `"meta"` blob 记录分块数；`restore` 只按元数据声明的分块数去读，从不
   扫描 fs 里所有 `chunk_*` 文件——这是"陈旧分块不能污染 restore"的关键。
4. **Part 3 叠加**：每次 `shutdown` 用一个**新生成号**写分块，元数据最后写；生成号从
   `_committed_generation()`（读 fs 当前 `"meta"`）算出，**不信任 `self._generation`**。
5. **收尾**：模拟 `save_blob` 写到一半抛异常，验证 `restore()` 精确返回上一次完整提交的快照；
   验证"从未 `restore()` 过的全新实例 `shutdown()`"不会撞车覆盖已提交的生成号。

## 4. 代码怎么组织

```
_encode_entries(data) -> bytes / _decode_entries(blob) -> dict     # netstring 编解码
FileSystem.save_blob/get_blob/list_files                            # 提供的 fake，单 blob ≤1024B
KVStore._committed_generation() -> int                               # 每次都从 fs 读，不信任内存
KVStore.shutdown()                                                    # 编码 -> 分块 -> 新生成号落盘 -> 元数据最后写
KVStore.restore()                                                     # 读元数据 -> 只读它声明的分块 -> 解码
```

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def shutdown(self):
    # 生成号永远从 fs 当前的 meta 读出来，不信任 self._generation——见下方注释。
    current_generation = self._committed_generation()
    blob = _encode_entries(self._data)
    chunks = [blob[i:i + CHUNK_SIZE] for i in range(0, len(blob), CHUNK_SIZE)]
    new_generation = current_generation + 1
    for idx, chunk in enumerate(chunks):
        self._fs.save_blob(f"chunk_g{new_generation}_{idx}", chunk)
    meta = f"{new_generation}\n{len(chunks)}\n{len(blob)}\n".encode("ascii")
    self._fs.save_blob("meta", meta)     # 最后写：只有它落盘，这次快照才算"提交"
    self._generation = new_generation

def _committed_generation(self):
    # 一个从未调用过 restore() 的全新实例，如果信任 self._generation（永远是 0），
    # 会和 fs 里已经提交的生成号撞车，覆盖掉别人的分块文件——必须每次都读 fs 本身。
    try:
        meta_bytes = self._fs.get_blob("meta")
    except FileNotFoundError:
        return 0
    gen_s, _num_chunks_s, _total_len_s = meta_bytes.decode("ascii").splitlines()
    return int(gen_s)

def restore(self):
    try:
        meta_bytes = self._fs.get_blob("meta")
    except FileNotFoundError:
        self._data = {}
        return
    gen_s, num_chunks_s, _total_len_s = meta_bytes.decode("ascii").splitlines()
    generation, num_chunks = int(gen_s), int(num_chunks_s)
    parts = [self._fs.get_blob(f"chunk_g{generation}_{i}") for i in range(num_chunks)]
    self._data = _decode_entries(b"".join(parts))   # 只读元数据声明的分块，陈旧分块永不触碰
    self._generation = generation
```

## 6. 并发追问怎么答

- **为什么生成号不能只存在内存里**：`KVStore` 对象的生命周期和 fs 不一样——无状态服务里对象
  可能每次请求都重建；如果生成号只活在实例内存里，任何一次"重建对象但没调用 `restore()`"都会
  把计数器归零，下一次 `shutdown()` 就会和 fs 里已经存在的同名生成文件撞车。修复方式是每次
  `shutdown()` 都先从 fs 读当前已提交的生成号，永远算"当前 +1"，而不是自己维护的计数器。
- **两个进程同时对同一个 fs 调用 `shutdown()` 会怎样**：`_committed_generation()` 读取 + 写分
  块 + 写元数据这三步不是原子的——两个并发 `shutdown()` 可能读到同一个"当前生成号"，各自算出
  同一个"新生成号"，互相覆盖对方的分块文件。修复需要给"读生成号到写元数据"这一整段加锁，或者
  用乐观并发（生成号读的时候带一个版本号，写元数据时做 compare-and-swap，失败就重试）。
- **崩溃点如果发生在元数据写入之后（确认响应丢失）怎么办**：这个 fake 的 `save_blob` 要么完整
  成功要么完全不写，所以"写完但确认丢失"在这个语义下不存在；换成真实分布式存储时，调用方必须
  能安全重试同一次 `shutdown()`——重试时读到的仍是上一次成功的元数据，会用同一个生成号重新写
  一遍，这是幂等的，安全。

## 7. 常见跑偏（方法层面，含并发一条）

- 用 `json`/`pickle` 或手写转义方案处理任意字符的键值，而不是长度前缀编码——转义方案总有"转
  义字符本身又出现在数据里"的漏洞。
- `restore()` 扫描 fs 里所有以 `chunk_` 开头的文件而不是只读元数据声明的那几个，导致陈旧分块
  污染恢复结果。
- **并发相关（也是本题最容易被忽视的坑）**：生成号只存在 `KVStore` 实例的内存字段里，一个从
  未调用过 `restore()` 的全新实例第一次 `shutdown()` 就会撞车覆盖 fs 里已经提交的快照。

## 8. 同族题 / 延伸

- 与 `od13_dictionary_trie_codec` 的编码语法、`od15_json_parser` 的 JSON 语法同族，都是"先定
  长度/字符集约定再证明无歧义"。
- 与 `od02_in_memory_file_system`、`od05_cron_scheduler` 同族在"崩溃不丢触发/持久化恢复"这条
  技能线（S11）；与 `od11_dynamic_blacklist_filter` 同族在"并发正确性"（S10），一个靠"生成号
  权威来源在持久层"，一个靠"锁 + 线性化日志重放"。
- 练习命令：`python3 loop/mock.py start od14`
