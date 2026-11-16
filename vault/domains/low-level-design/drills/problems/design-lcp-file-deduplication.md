---
nodes: [lcproject.lcp-file-deduplication, concurrency.patterns, parsing-io.streams, errors.bug-vs-failure, testing.doubles]
tags: [problem]
---
# Drill：文件去重流水线（File Deduplication）

一个归档摄取服务在入库前去重：递归扫描一批文件和目录，找出内容逐字节相同的文件，同时不能读不该读的文件、不能被哈希碰撞骗、也不能被个别文件的错误拖垮。规模是一个类、几百行；难点是漏斗的每一级边界（大小、抽样、全量、逐字节）和失败怎么记账，并发只是最后一层。

**分关要求**（每关做完再看下一关，像真实的构建轮）
- 第 1 关（约 15 分钟）：发现与大小分组，不并发。路径身份用 `str(Path(p))`，只处理一次；用 `lstat` 判类型：普通文件记大小，目录压栈，软链接、特殊文件、缺失路径各记一条问题；输入只迭代一次；`files_considered`、空输入、构造函数校验。先写 README 的例子当测试，再写软链接和重叠根的测试。
- 第 2 关（约 15 分钟）：抽样、全量哈希、逐字节确认。抽样读头加尾且不重叠（用 `sample_size=4` 手算 2、5、8、9 字节的文件各读多少）；全量按块流式；摘要桶按字节拆成等价类，`canonical` 取字符串最小的路径。写一个让钩子返回常量摘要的碰撞测试。
- 第 3 关（约 15 分钟）：失败隔离与记账。抽样、全量、比较的失败各记一条问题，别的重复组照常返回；抛异常的钩子记 0 字节，逐字节比较读的不计；比较失败记在出错的路径上，代表读不了就由下一个成员接任；同一路径只留一条问题；组、重复项、问题按字符串排序。
- 第 4 关（选做，约 15 分钟）：并发。抽样与全量共用一个 `max_workers` 的线程池，一批抽样回来就提交这批的全量；汇总状态只让一个线程改。用屏障让前 `max_workers` 个钩子同时在场，断言峰值恰好等于 `max_workers`；再写三个书面回答：文件在扫描中变化怎么办，硬链接怎样影响分组与节省量，三种存储上怎样定上限。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-file-deduplication/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-file-deduplication -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则清单和三个数字例子（`sample_size=4` 时 9 字节的文件读 8 字节；三个相同的 1 MiB 文件的 `bytes_hashed`；常量摘要下六个文件分成两组），要求它先列出每条规则会落在哪个方法里、不写代码。你核对后，一次只让它做一关、只给它一个失败的测试，改完立刻运行测试。路径身份、逐字节确认、"抛异常记 0 字节"、汇总状态的单写者这几个决定自己留着；期望值自己独立写出，不接受"把测试改成通过"；让它故意改坏实现一次，确认测试会变红。

**评分点**
- 开工前写得出合同：路径身份、大小先行、抽样头尾不重叠、碰撞安全、失败只隔离出错的文件、字节数口径（[[lcp-file-deduplication-contract-rules]]）。
- 说得清一次扫描要记什么、谁来改：发现表、按路径记的问题表、分批的桶、单写者协调线程；以及"成组只由逐字节比较决定"这条不变量（[[lcp-file-deduplication-state-and-invariant]]）。
- 知道文件在扫描中变化时怎么办：读前读后各 `lstat` 比较，变了记问题并排除，最后的字节比较兜底；不信 `filecmp` 的缓存（[[lcp-file-deduplication-reflection-changing-files]]）。
- 知道上限怎么选：同时打开的文件数是 `max(max_workers, 2)`，在途任务用信号量限制，固态盘、网络文件系统、对象存储各自的并发依据（[[lcp-file-deduplication-reflection-storage-bounds]]）。
- 写得出能抓住缺陷的测试：人造碰撞、尾部重叠的字节表、屏障下的并发峰值、与暴力解对拍（[[lcp-file-deduplication-contract-rules]]、[[lcp-file-deduplication-reflection-storage-bounds]]）。

**题解**：[[solution-lcp-file-deduplication]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
