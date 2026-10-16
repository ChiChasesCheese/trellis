# Amazon · SDE, AWS Data Services（2026 US）—— 从这里开始

> 岗位：Software Development Engineer, AWS Data Services – 2026 (US)，job 10414316，挂的是 SDE I。
> **本 kit 一律按 senior 标准准备**（Chi：「不要调整 bar，我们永远准备的内容对标 senior」）。全部材料是教科书模式。
> Onsite：西雅图现场，约 10/20–21（根据机票推断，以 recruiter 邮件为准）。

## 地图

| 想做什么 | 去哪 |
|---|---|
| 这一场怎么面、5 天怎么排 | [LOOP_GUIDE.md](LOOP_GUIDE.md) |
| **LP**：原理 → 故事 → 题库 → 练习 | [lp/00_how_lp_works.md](lp/00_how_lp_works.md) · [lp/story_matrix.md](lp/story_matrix.md) · `lp/stories/` · [lp/question_bank.md](lp/question_bank.md) · [lp/drill.md](lp/drill.md) |
| **GenAI 这一轮** | [lp/genai/00_what_they_ask.md](lp/genai/00_what_they_ask.md) · [stories](lp/genai/stories.md) · [question_bank](lp/genai/question_bank.md) · [primer](lp/genai/primer.md) |
| **编码**（Python，16 个模式、81 道题） | [coding/plan.md](coding/plan.md) · [coding/amazon_bar.md](coding/amazon_bar.md) · [coding/top_list.md](coding/top_list.md) · `coding/patterns/01–16` |
| **LLD / OOD** | [lld/route.md](lld/route.md) · 文件搜索、计费、人数追踪、**[内存数据库（Chi 亲历 + LC 2408）](lld/in_memory_database.md)**（附可运行代码 `lld/code/`） |
| **系统设计** | [sd/00_ddia_refresh.md](sd/00_ddia_refresh.md) · [sd/00_how_to_run_the_round.md](sd/00_how_to_run_the_round.md) · `sd/problems/`（5 道 AWS 数据题）· [sd/route.md](sd/route.md) · [sd/hld_sketches.md](sd/hld_sketches.md) |
| 证据原文 | `catalog/raw/official.md`（官方）· `catalog/raw/forums.md`（110 条 2025–2026 面经）· `catalog/raw/github_repos.md` |

## 面试前必须处理

1. **简历数字**：`core/resume/resume.tex` 已在 2026-10-15 改成证据口径：S1 是「tens of millions of Amex transactions (billions of dollars) a year」，S5 是「Owned the interchange-fee track … 13.7M rows, >99.9% parity」。但 PDF 还没重新生成（本机没有 TeX），而且**投给 Amazon 的那版还写着 $600B+**。面试官手里是旧版。【待 Chi 确认 $600B 的真实出处】，然后按情况选一句：
   - 如果它是平台级口径：*"That's the platform-level volume; the pipeline I built handles tens of millions of Amex transactions a year — billions of dollars."*
   - 如果找不到出处：*"Let me correct a number on my resume: the figure I can stand behind for my pipeline is tens of millions of Amex transactions a year, billions of dollars."*
   主动纠正，比被追问出来强。
2. **`lp/stories/` 里的【待 Chi 补】**：先补 matrix 标出的高风险 LP，也就是只靠一个故事撑着的、或者完全没有故事的。
3. **Disagree and Commit 缺一个「争论输了、最后照样执行」的故事**；LP16 没有故事。

## 检查命令

```bash
python3 -I coding/run_all.py          # 81 道题 + 讲义代码块全部跑通、逐字一致
python3 lp/coverage.py                # LP 覆盖率
for f in lld/code/*.py; do python3 -I "$f"; done
```
