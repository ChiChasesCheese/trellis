# interviews/ — 面试的完整文件夹

> 原 `Quick_Check/`（Stripe OA 起家）于 2026-09-13 重构为此目录。Trellis 的 `stripe` domain（`skeleton/stripe.yaml` + `vault/stripe/`）仍是 Stripe OA 的卡片面；这里是它背后的**原始研究、题库、演练、故事库与简历**——不进 Anki，按公司整体消费。

## 目录约定：company → phase，外加一个 core

```
interviews/
  README.md                 本文件：方法论 + 约定 + 新公司接入流程
  core/                     核心能力：与公司无关，跨公司持续打磨（越用越厚）
    resume/                 resume.tex（唯一源）+ 投递 PDF + CHANGELOG
    stories/                evidence-base.md（S1–S9 旗舰故事）+ resume-evidence-map/（学习画像）
    answers/                逐题行为面答案手册 dim1–dim6（技术深度 / 影响 / 领导力 / 带教 / HR）
    playbooks/              按轮次的通用打法：AI 语音筛选 / recruiter / HM / 电面 / onsite …
  companies/                每家公司一个自包含 kit（题库 + 测试 + 演练器 + 研究 + 学习面）
    stripe/                 = github.com/ChiChasesCheese/stripeoa 全量镜像：problems/（54 题带测试）· loop/rounds/（recruiter→onsite 全轮次 39 题）· catalog/ · study/ · tools/ · drill.py · loop/mock.py
    snowflake/              同一骨架：AI 轮 dossier（00–07, CARD, fit）+ 正在建的全轮次 kit；进度见 CHECKPOINT.md / LEDGER.md / tasks/plan.md
  _template/company/        新公司 dossier 骨架，cp -r 即可开工
```

**为什么是 company → phase 而不是 phase → company**：临考前一家公司的材料是被整体消费的（今晚只看 snowflake/），而不是横向比较各家的电面；跨公司复用的东西（故事、答案、简历、轮次打法）全部下沉到 `core/`，公司目录里只留「这家公司特有的」——流程证据、题库、fit 话术、反问。两者用相对链接互指，不复制。

## 跑一个 kit

```bash
cd vault/interviews/companies/stripe
python3 drill.py list / start q01 / test q01 / ref q01 / status      # OA 60 分钟演练
python3 loop/mock.py list / start ps01 / test ps01 / bq hm -n 3        # OA 之后各轮
uv run --project ../../../.. --with pytest python -m pytest problems -q -m "not perf"
python3 loop/tree/check_tree.py --strict                                 # 知识树 ↔ 目录一致
python3 tools/summary.py --run                                           # 重建 TEST_SUMMARY
```

`.py` 文件对 Obsidian 不可见、对 trellis 无影响（它只读 `*.md`）；仓库根的 `pytest` 只跑 `tests/`。每个公司 kit 自带 `CONVENTIONS.md`（题目目录结构与测试要求）。

## 方法论（Stripe 尽调沉淀下来的六步，Snowflake 沿用）

1. **raw/ 先行**：把论坛 / 题库 / 官方页 / 邮件原文按来源分文件存进 `companies/<co>/raw/`，每条带 URL + 日期。不整理，只收集。
2. **CATALOG / process**：从 raw 汇总成一张表——轮次、时长、形式、通过线、挂点；题目按 `#refs`（独立来源数）和置信度（high / medium / low）排序。**每个结论都能回溯到 raw 里的一条**。
3. **fit 话术**：Why <company> / 自我介绍 / 对业务的理解——从 `core/stories/evidence-base.md` 取材，只写这家公司特有的桥接点。
4. **答案库**：把这家公司会问的题映射到 `core/answers/` 的既有答案（不重写），只补公司特定题和价值观映射。
5. **演练**：可计时的 mock（Stripe 是 `loop/mock.py`；非编码轮是题库 + 计时口述）。
6. **回写 core**：面完把新故事 / 新答案 / 新教训写回 `core/`，公司目录保持只读归档。

## 新公司接入

```bash
cp -r vault/interviews/_template/company vault/interviews/companies/<company>
```

然后按 `_template/company/00-README.md` 里的清单填。第一天只需要 `01-company-brief.md` + `02-process.md` + `raw/`；答案库和 mock 在拿到具体轮次邀请后再写。

## 与 Trellis 其它部分的关系

- `vault/stripe/`（domain）里的 40 张卡片是从 `companies/stripe/study/` 提炼出来的**可复习面**；这里的东西不建卡。
- `code-core` domain 的 `transfer.*` 分支是「新公司的一轮面试 = 一个叶子」的接口；公司目录里的具体题目留在这里，通用规律升到那里。
- `skeleton/stripe.yaml` 头部注释指向 `companies/stripe/`。
