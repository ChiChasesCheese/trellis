# Object Store with Deduplication（带内容去重的对象存储）

我们要做一个简化版的云对象存储服务，给内部的数据平台用：用户按 `bucket/key` 上传文件、按 `bucket/key` 下载、可以覆盖同名对象、可以删除，也能列出某个前缀下的对象。上传的内容里有大量重复——同一份 Parquet 文件被不同团队复制到各自的 bucket，查询结果被反复导出，备份任务每天上传几乎不变的快照——所以存储成本里很大一块是在为重复字节付钱。希望你设计的系统在用户完全无感的前提下对内容做去重：两个不同的 key 指向相同内容时，物理上只存一份；删除一个 key 不能影响另一个 key 还能读到数据；覆盖一个 key 之后旧内容如果没人再引用，要能最终被回收。单个对象从几 KB 到几百 GB 不等，大对象上传可能中途断开需要续传；整体规模是每天新增 PB 级、对象数百亿，读多于写，读延迟要低。另外，安全团队提了一个要求：不同租户之间不能通过"上传一份内容看看是不是秒传成功"来推断别的租户是否存过某个文件。请设计这个系统。

---

**面试环境说明**：Snowflake onsite 或技术电面的 System Design 轮，45–60 分钟。白板工具未证实；面试官风格两极，沉默时要自己推进。

**题目原始报告与来源**：
- **LOW（聚合站自建题库，无一手印证）**：PracHub "Object Store with Deduplication"（Medium，"Simplified cloud object storage service" for upload/download，内容去重，420 人做过，2025-12-15）；staffengprep 归类为 "Blob Storage De-duplication"。见 `../../../catalog/raw/system_design.md` §1.14 与 §3 第 5 条（该文件明确把这题归为"聚合站自建题库，练习价值仅供覆盖面"）。
- 进入建题批次是因为它落在 28 法则 cut line 内（`../../../catalog/PARETO.md` 第 28 行）。**按覆盖面练，不按真题押。**
- 与 Snowflake 的关系：micro-partition 不可变、clone 共享底层分区、Time Travel 与 Fail-safe 决定何时能真正删除——都是"多引用共享一份不可变数据 + 延迟回收"的问题。**[推断]**
