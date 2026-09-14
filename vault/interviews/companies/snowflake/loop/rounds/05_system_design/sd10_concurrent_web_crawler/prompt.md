# Concurrent Web Crawler（去重/礼貌性/分片/扩展）

请设计一个并发网络爬虫：给定一批种子 URL，爬虫要不断抓取网页、从网页里提取出新的链接、把这些新链接也加入抓取队列，如此持续下去，把整个可达的网页集合都爬下来。这个系统要能高并发地跑（同时对成百上千个不同的域名发起抓取请求），但也要讲"礼貌"——不能对同一个域名在极短时间内发起大量请求把对方服务器打垮或者触发对方的反爬限制，需要有 per-domain 的请求节流。爬取过程中会不断发现新的 URL，其中很多是重复的（不同页面互相链接到同一个地址，或者同一个页面被不同的路径链接到），所以需要一个高效的去重机制防止对同一个 URL 重复抓取——但要考虑到这个系统运行一段时间之后，见过的 URL 总量会非常大，去重结构本身不能无限占用内存。最后，这套系统需要能水平扩展——当抓取的网页规模从百万级涨到百亿级的时候，架构上应该怎么把工作分摊到多台机器上，同时依然保持"去重不重复抓取"和"礼貌性"这两条约束在多机环境下依然成立。请设计这个系统。

---

**面试环境说明**：这是 Snowflake 技术电面或 onsite 的 System Design 轮，时长 45–60 分钟。白板工具未证实；面试官风格两极分化。这道题也有对应的 coding 版本（BFS + Queue + HashSet/Bloom Filter 去重的单机实现），如果面试官先给了 coding 版本再要求"现在把它做成分布式的"，可以直接从"单机去重结构在多机环境下会遇到什么问题"这个角度切入展开本题。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.13）：
- **Coding 版**：用 BFS + Queue + HashSet/Bloom Filter 去重；也有 DFS 记录深度的变体，"follow-up discussion on how to scale the solution" —— WebSearch 综合多个聚合站（PracHub、Educative 等）（**低-中**）。
- **SD 版**："Design a Concurrent Web Crawler"（Hard），题面 "Concurrent web crawler that starts from a given URL"；归类页标签 "Web-Crawler/Distributed-Systems/Queueing/Scaling"（单篇报告）—— PracHub / staffengprep.com（**低-中**）。
- **复用材料**：`../../raw/process_research.md` §3.2 #11 引用 linkjob 收录的 "Web Crawler (BFS)"（**低**，复用）。
- 整体置信度 **LOW-MED**（没有一手候选人报告留下具体追问，属于该题库里证据相对薄弱的一题，但题型本身是经典分布式系统设计题，可以按行业标准打法准备）。
