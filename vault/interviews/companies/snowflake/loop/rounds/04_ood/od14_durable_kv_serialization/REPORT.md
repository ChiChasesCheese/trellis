# od14 Durable Key-Value Store Serialization — report

## Summary
一个"关闭时落盘、重启时恢复"的内存 KV store：Part 1 长度前缀编码（禁用 json/pickle，键值可含
任意字符）→ Part 2 分块落盘（单文件 ≤1024 字节，元数据 + 陈旧分块隔离，reconstructed）→
Part 3 崩溃原子性（生成号必须从 fs 读而不是信任内存计数器，reconstructed）。两条来源
（TrueInterview、1point3acres）都只到标题级，分块/元数据/生成号机制全部重建。

## Sources & confidence
MED（TrueInterview 同步清单第 71 题，标题+格式标签+一句预览摘要）+ medium（1point3acres 问题
库同名标题，仅标题）。两条来源互相印证题目存在，但都没有给出规则文本。

## Approach by part
1. netstring 风格编码：`<len(key字节)>:<key字节><len(value字节)>:<value字节>`，按 key 排序
   拼接；长度永远在数据前面，键值可以包含任何字符而不需要转义。
2. `FileSystem.save_blob` 自身强制单 blob ≤1024 字节；`shutdown()` 把编码后的**原始字节流**
   （不是解码后的字符）切成 ≤1024 字节的分块——这样一个多字节 UTF-8 字符可能被切在两个分块中
   间也没关系，因为解码只发生在 `restore()` 把所有分块拼回完整字节流之后。一个额外的 `"meta"`
   blob 记录 `<generation>\n<num_chunks>\n<total_len>\n`；`restore()` 只按元数据声明的分块
   数去读，从不扫描 fs 里所有 `chunk_*` 文件，这就是陈旧分块不会污染 restore 的原因。
3. 每次 `shutdown()` 都在一个新生成号下写分块，元数据永远最后写——这是崩溃原子性的关键。更关
   键的一处修正：生成号必须每次都从 fs 当前的 `"meta"` 读出来（`_committed_generation()`），
   不能信任 `KVStore` 实例自己在内存里维护的计数器，否则一个从未调用过 `restore()` 的全新
   `KVStore` 实例会从生成号 0 开始，直接撞车覆盖掉 fs 里已经提交的生成号 1（这是实现过程中实
   际发现并修复的一个 bug，问题详见 problem.md 追问 1，测试
   `test_fresh_instance_never_calling_restore_does_not_collide_with_committed_generation`）。

## Pitfalls hidden tests target
- 键值含换行/冒号/unicode（含空字符串键、空字符串值）的往返正确性
- 空 store 的 shutdown/restore；从未 shutdown 过的 fs 上 restore 得到空 store，不报错
- 多分块的大 store 完整往返；每个分块文件都验证 ≤1024 字节
- UTF-8 多字节字符卡在分块边界中间，重装后解码依然正确
- 陈旧分块：大快照缩小成小快照后，旧分块文件仍在 fs 里但完全不影响 restore
- **生成号从 fs 读而不是从内存读**——从未调用 restore 的全新实例 shutdown 不能撞车覆盖已提交
  快照（这是本题最容易被忽视的坑，专门有一条测试覆盖）
- 崩溃原子性：`save_blob` 写到一半抛异常，restore 精确返回上一次完整提交的快照；崩溃后重试
  必须仍然能成功提交
- 连续 5 次生成号递增的 shutdown 不会互相污染

## Complexity & measured cost
`put`/`get` O(1)；`shutdown` O(总数据量)（编码 + 分块 + 落盘）；`restore` O(总数据量)（读回全
部分块 + 解码）。3000 个随机键值的端到端 PUT+SHUTDOWN+RESTORE 脚本远低于 2s 预算。

## Test inventory
21 tests — part1 6 · part2 5（含 1 perf）· part3 5 · fmt 2 · io 2；edge 8 · perf 1 · io 2 ·
fmt 2（跨 part 统计）。

## Skills exercised
S09 类设计先定契约（长度前缀而非转义的判断）· S11 持久化与恢复（分块、元数据、生成号、崩溃
原子性，与 od02/od05 的"崩溃不丢触发"同族）· 自定义序列化格式设计（与 od13 trie 编码、od15
JSON 解析同族）。
