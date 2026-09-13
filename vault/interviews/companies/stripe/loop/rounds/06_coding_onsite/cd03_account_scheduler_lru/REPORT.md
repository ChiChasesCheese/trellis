# cd03 AccountScheduler — 报告

## 概要
一个带定时锁的固定沙盒账户池(`is_available` → `acquire` → LRU
`acquire_any`),是 `problems/q26_account_scheduler_lru` 的现场面试版姐妹题。整道题
本质上是一次 60 分钟时限下的类设计:一个 `locked_until` 字典、明确的
异常策略(未知 id 用 `KeyError`,`duration <= 0` 用 `ValueError`)而不是
布尔哨兵值,以及一个刻意使用**构造顺序**而非 id 字符串顺序的 LRU 平局裁决——
这是最容易让照搬 q26 模式的人栽跟头的细节。

## 来源与置信度
中等 —— 1point3acres 题库 "AccountScheduler LRU"(现场面试,最近一次 2026-03-27),
`loop/raw/en_forums.md` §6.2 (C4),linkjob 2025-12-07/2026 现场面试报告。三方法递进
结构证据充分;确切的构造函数形态、异常 vs 哨兵值的选择,以及构造顺序平局裁决
是本轮重建的内容,并在 problem.md 中做了标注——刻意与 q26 的动态池 / id 顺序
约定不同,以免两道题收敛成同一个解法。

## 分 Part 思路
1. `AccountScheduler(accounts)` 去重后存为列表(保留首次出现的顺序),并建立
   `id -> index` 映射以支持 O(1) 的平局裁决查找。`is_available` 先检查成员关系
   (不存在则 `KeyError`),再判断 `locked_until.get(id) is None or t >= locked_until[id]`
   (锁定结束是排它的)。
2. `acquire` 在委托给 `is_available`(它负责为未知 id 抛出 `KeyError`)**之前**
   先校验 `duration > 0`——这是文档规定的检查顺序,之所以选它是因为 `duration`
   是纯参数检查,不需要查状态,运行成本最低,所以放在最前面。
3. `acquire_any` 先把固定池过滤成 `t` 时刻可用的账户,再按
   `(has_been_used, last_used_or_0, construction_index)` 取 `min()`——从未使用的
   账户(标记为 0)永远排在已使用的账户(标记为 1)之前;同组内由第二、第三个
   分量决定顺序。加锁时复用了和 `acquire` 完全相同的 `locked_until`/`last_used` 写入。
4. `run_commands` 解析必需的 `ACCOUNTS ...` 头部行,然后分发
   `AVAIL`/`ACQ`/`ANY`;任何 `KeyError`/`ValueError`(包括 `t`/`duration` 的
   `int()` 转换失败)或未知动词/参数个数错误只在这一层被捕获并打印为 `ERROR`——
   类本身从不吞掉异常。

## 隐藏测试针对的坑
- 排它的锁定结束时刻(`t0+d` 时空闲,`t0+d-1` 时不空闲);恰好在到期时刻重新加锁
- 三个公开方法都会为未知 id 抛出 `KeyError`,不只是 `is_available`
- `duration <= 0` → `ValueError`,即使是"双重错误"调用也要在未知 id 检查之前检查
- 从未使用的账户排在已使用的之前,无论"多久没用"对从未使用的账户毫无意义
- 从未使用账户的平局裁决是**构造顺序**(`ACCOUNTS c b a` → `c, b, a`),不是字母顺序——
  这是与 q26 分歧最大的一处,用刻意非字母顺序的池来测试
- 已使用账户之间 `last_used` 相等时同样回退到构造顺序
- 失败的 `acquire` / 单纯的 `is_available` 调用绝不会改动 `last_used`
- 全部锁定 → `None`;恰好有一个到期的那一刻 → 就是它,按排它性结束时刻比较
- 跨调用非单调的 `t` 纯粹靠比较来回答,没有隐含的"经过时间"状态

## 复杂度与实测成本
`is_available`/`acquire` 为 O(1)。`acquire_any` 每次调用是 O(n)(线性扫描 + `min`),
遍历整个固定池——对于本题设定的规模是可接受的,problem.md 的追问部分已明确指出
如果被问到 10^4+ 账户且持续高负载,应当升级为双堆 + 延迟失效设计(类似 q26)。
性能测试:50 万条混合命令(50% `AVAIL`,40% `ACQ`,10% `ANY`)在 500 账户的池上
通过 `run_script` 运行约 1.1 秒 / 约 30MB——远低于 2 秒 / 256MB 的预算。更密集的
`ANY` 混合比例(例如 2,000 账户池上占 20%)在临时测试中测得约 7.6 秒,证实
`acquire_any` 的 O(n) 追问是真实存在的,而非纯理论上的谈资。

## 测试清单
18 个测试——part1:3 个 · part2:4 个 · part3:11 个(含 2 个 io、1 个 perf、1 个 fmt);
edge 8 个 · fmt 1 个 · io 2 个 · perf 1 个。

## 涉及技能点
S03 类 + 字典建模 · S05 严格/非严格时间比较 · S08 确定性平局裁决
(构造顺序,而非"显而易见"的 id 顺序) · S10 事件流上的状态 · S18
校验/异常策略 · S19 增量式设计 · S20 自测

## 复盘（2026-09-02）
**改了什么**
- `loop/lint.sh` 在改动前对本题 4 个文件全部报 "would reformat"（未跑过 black -l 110）：`--fix` 后
  `solution.py`/`starter.py`/`starter_template.py`/`test_cd03.py` 全部格式化通过，纯格式改动（多余空行、
  行内注释多空格、`test_cd03.py` 里两条 worked-example 列表从单行挤在一起改成一行一个元素），无语义变化——
  用 `git diff` 核对过，且格式化前后跑三条 worked examples 逐字核对输出不变。
- `solution.py`：`acquire` 和 `acquire_any` 原本各自重复写 `locked_until[...] = t + duration` /
  `last_used[...] = t` 这两行；抽成私有方法 `_lock(account_id, t, duration)`，两个公共方法末尾都调用它。
  公共 API（`__init__`/`is_available`/`acquire`/`acquire_any` 的签名）完全未变，`starter_template.py`/
  `starter.py`/`test_cd03.py` 不需要跟着改。
**为什么**：lint 未过是 F 项（checklist "F `loop/lint.sh <dir>` 通过"），必须修。`_lock` 抽取是 S 项
（checklist "后 part 复用前 part 的函数"）——原来 `acquire_any` 是重写一份写状态逻辑而不是复用 `acquire`
已经验证过的路径，两处逻辑分离后续容易改一处漏一处；抽取后两个公共方法的加锁写入只有一条代码路径。
`REPORT.md` 原有的 Summary/Sources/Approach/Pitfalls/Complexity/Test inventory/Skills 六节在改动前已经
符合 CONVENTIONS 要求，未改动正文，只追加本节。
**遗留**：`acquire_any` 仍是 O(pool size) 的线性扫描，problem.md 的追问 2 已经把"两个堆 + 版本号懒删除"
的优化路线写清楚，本轮按题面要求不实现，只在文章第 6 节讲清楚怎么口头带过。
