# CLAUDE.md — 在这个仓库里干活之前先读完

这是一个**自建的 Stripe 面试备考题库**，不是产品代码。使用者一个人（仓库主），
目标面试时间 **2026-09**，2026-09-04 起进入全力冲刺。所以这里的"质量"标准是：
**练完能在面试里做出来**，以及**这份材料本身可信、可回溯**。

---

## 0. 赛道（已定，不要自己扩）

> **只准备 SWE backend。** 2026-09-04 仓库主明确：其他岗位不考虑。

具体含义：

- 镜像 / 面经里出现的 **MLE · 前端 · mobile/Android · Security · Data Scientist / DA(SQL)**
  素材，**记录进台账即可，不立项建题**。它们正确地不在覆盖率分母里。
- 这条撤销了 `HANDOFF.md` §3 P4 的"要不要建 DS/DA 赛道"这个待决问题——答案是**不建**。
- 如果将来仓库主改主意，要**由他明说**才动，不要从"素材存在"推出"应该建"。

---

## 1. 权威顺序（结论冲突时按这个排）

```
git 历史  >  CLAUDE.md（本文件，长期规矩）  >  HANDOFF.md（当前断点）
          >  loop/CHECKPOINT.md  >  loop/tasks/todo.md
```

- **`HANDOFF.md`**：现在做到哪、下一步做什么、站点可达性台账。**接手先读它。**
- **本文件**：不随进度变的规矩。改进度不要改这里，改规矩才改这里。

---

## 2. 三条记账纪律（这份题库能不能长期可信，全在这）

1. **不编 URL。** 只写实际抓取过、或搜索真实返回过的链接。
2. **不把猜测写成事实。** 找不到就写"未找到"，并记下试过的检索式。
3. **转引要标明。** 复用旧材料标"复用 + 原采集日期"，**不冒用今天的访问日期**。

配套的一条硬边界——**重建题（reconstruction）**：
题面来源不足时可以自拟，但必须在 `problem.md` 顶部写**警示块**，说清哪些有据、哪些自拟。
`tools/mirror.py scaffold` 会按 FULL/SUMM/TITLE 档位**自动写**对应措辞，**不要手写**。

> **练里面的技能，不背输出格式。** 把自拟格式当真题背，比不练更糟。

还有一条同样重要：**发现自己写错了就留下更正记录，不要把错的悄悄删掉。**
`catalog/discovery/2026-09-03b/coverage_analysis.md` 顶部的更正块、
`catalog/SOURCES.md` 里两条推翻自己的记录、`loop/study/00-prereq/templates/patterns.py`
里那个 off-by-one 的自述，都是**故意留着的**，不要"清理"。

---

## 3. 目录地图

```
problems/qNN_slug/          OA 库（q01–q42 自建 · qA01–qA14 LeetCode 对标）
loop/rounds/<轮次>/<id>/    面试各轮题库（ps 电面 · bs bug squash · int integration
                            · cd VO coding · sd system design · 01/02/08 非技术轮题库）
loop/study/                 学习材料：00-prereq 前置 · 10-rounds 八章打法 · 20-cards 速查卡
                            · 30-articles 逐题文章
catalog/                    CATALOG.md 题目主键 · SOURCES.md 站点台账 · discovery/ 尽调报告
catalog/raw/mirror_1p3a_stripe/   1point3acres 的 GitHub 镜像副本（168 条，.py 已改名 .txt）
tools/                      harvest(收割) · mirror(镜像→题目) · refresh_check(来源复验)
                            · progress · summary · build_report_html
drill.py / loop/mock.py     两个演练器（OA 库 / 轮次库），都有 start·test·time·ref·status
loop/tree/check_tree.py     结构自检：跑完必须 errors=0 warnings=0
```

**六件套约定**（`problems/`）与 **bug squash 版式**见 `CONVENTIONS.md`。新建题必须照抄版式。

---

## 4. 常用命令

```bash
python3 drill.py start q22          # OA 库：打印全文 + 重置 starter + 60 分钟计时
python3 loop/mock.py start ps01 -m 45   # 轮次库：拷到 loop/work/ 用 IDE 打开
python3 drill.py test q22 -k part1  # 先锁 part1 再动 part2
python3 drill.py status --all       # 跨题进度板
python3 loop/tree/check_tree.py     # 结构自检（改完题必跑）
python3 tools/mirror.py gaps        # 镜像里还没立项的条目（粗筛，需人工判重）
python3 tools/refresh_check.py stale   # 哪些来源该复验了
make test                           # 全部参考解 + 全部测试
```

**`pytest.ini` 已经带 `-q`，命令行别再加 `-q`**——会把汇总行吞掉，
然后你就会用 grep 去数字符串，然后就会数错。（这个坑真的踩过。）

---

## 5. 协作约定（仓库主定的，按时间最新为准）

- **并行子代理 ≤ 3。** 这是默认值，只有仓库主当次明确要求才可突破。
- **频繁存盘防 usage limit。** 每完成一个可验收单元就 commit + push，不要攒着。
  长时间运行的收割任务必须**增量落盘 + 能从磁盘续跑**，不能只在结尾写文件。
- 产出型子代理用 `sonnet`；**每个代理只写自己名下目录**；协调者独立验收后才 commit。
- **`git add <目录>` 会扫进代理还没写完的文件。** 这个坑踩过两次。
  多代理并行时，用 `.git/info/exclude`（本地，不污染 `.gitignore`）挡住在建目录，验收后再放开。
- 语言：**材料中文，代码与专有名词英文**。
  但 `problems/` 的 `problem.md` **正文保持英文**——真实 OA 是英文，
  读长英文题面本身就是被打分的能力。警示块 / Sources / REPORT.md 用中文。
- **不放宽任何 perf 预算**去让容器看起来绿。预算是按开发机定的。

---

## 6. 已知的红，不要"修"

跑测试看到这几条红是**正常状态**，先于当前工作存在：

1. `loop/lint.sh` 的 black 失败（13 文件）——容器里 black 版本比仓库当初用的严，不是代码问题。
2. `loop/study/00-prereq/exercises/` 的 flake8 + 测试红——**仓库主自己的作答文件**，
   函数体还是 `# TODO`。红是它应该有的样子。
3. `tools/build_report_html.py` 的 4 条 flake8——先于本轮工作。
4. `q07::test_perf_100k`（单独跑也红）、`cd06::test_perf_1m_rows`（单独跑绿，
   只在全量并跑、CPU 被抢时超时）——**perf 预算不放宽**。

bug squash 五题的正常状态是"**打补丁前 2 红**"——那是题目本身，不是坏了。

---

## 7. 抓数据之前先看台账

`catalog/SOURCES.md` 和 `HANDOFF.md` §2 记了每个站**实测能不能进、走哪条路径**。

贯穿三轮尽调的教训，代价是几百条一手材料：

> **一次抓取失败不能给一个站定终身。要具体到"哪条路径"失败。**

teamblind、reddit、1point3acres 都被我们先判死、后推翻过。
所以台账里记的是"HTML 403 但 `.rss` 通"这种粒度，不是"这站不行"。

`lodely.com` / `vervecopilot.com` 已判定为 **AI 题目农场，一律不采信**；
CSDN 可达但混有内容农场（日期造假），逐条辨伪。
