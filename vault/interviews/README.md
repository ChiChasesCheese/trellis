# interviews/ —— 面试的完整文件夹

这里只放你要读、要练的东西：每家公司的备考入口、各轮的练习题、故事库和简历。查来源、打分排序、跑验证的材料不在这里，在仓库的 `research/companies/<公司>/`。打开一家公司的文件夹，先读它的 `README.md`。

## 目录

```
interviews/
  README.md            本文件
  core/                跨公司通用，越用越厚
    resume/            简历源文件、投递 PDF、修改记录
    stories/           S1…S11，一个故事一个文件；Core.md 是目录页
    Answers.md         行为面标准答案 Q1–Q24
    playbooks/         按轮次的通用打法
    coding/ system-design/ low-level-design/ cpp/ java/ foundations/
                       通用专题，按公司分子目录：core/<专题>/<公司>/
    leetcode/          LeetCode 公司题单工具和各公司映射
  rounds/              与公司无关的轮次能力（有卡片，进 Anki）
    code-core/ leetcode/ narrative/
  companies/<公司>/    一家公司一个文件夹，只放学习页和练习代码
  _template/company/   新公司的骨架
```

公司文件夹里只留这家公司特有的内容：入口 `README.md`、`LOOP_GUIDE.md`、LP 和行为面页面、只有这家公司才考的轮次，以及练习用的题目文件夹。系统设计、低层设计、编码套路和语言课程是通用专题，放到 `core/<专题>/<公司>/` 或对应的卡片领域分支，公司入口页用链接指过去。

文件夹里不放来源、目录表、验证脚本。这些在 `research/companies/<公司>/`，其中的 `README.md` 说明里面有什么、学习页在哪。

## 跑练习

只用公司入口页告诉你的命令，在该公司文件夹里运行。常见的几种：

```bash
cd vault/interviews/companies/<公司>
python3 drill.py list / start q01 / test q01 / ref q01 / status    # 限时编码演练
python3 loop/mock.py list / start ps01 / test ps01 / bq hm -n 3    # 其他轮次的模拟
uv run --project ../../../.. --with pytest python -m pytest problems -q -m "not perf"
```

`.py` 文件在 Obsidian 里看不到，也不影响卡片；仓库根目录的 `pytest` 只跑 `tests/`。

## 备考方法

1. **GitHub 先行**：先看别人整理过的这家公司的题单和面试记录，再去论坛和聚合站。
2. **建题目目录**：一行一个题目，写清轮次、考几次、最近一次是什么时候。按「轮次 × 次数 × 新近度」排序，前 20% 的题要覆盖大约 80% 的出现次数，并写下这条分界线。
3. **每一轮写一份打法**：形式、考什么、通过线、常见失败点、准备动作。
4. **fit 话术**：Why 这家公司、自我介绍、对业务的理解。从 [[Core]] 取材，只写这家公司特有的衔接点。
5. **答案库**：把这家公司会问的题对应到 [[Answers]] 里已有的答案，只补公司特有的题和价值观。
6. **演练**：编码轮用限时练习代码，非编码轮用题库加计时口述。
7. **回写 core**：面完，把新故事、新答案和新教训写回 `core/`。

写学习页要遵守仓库的写作规则，用 `python3 scripts/plain_style.py <页面>` 检查（LP 页加 `--outline`）；文字图用 `python3 scripts/phone_diagrams.py <页面或目录>` 检查是否能在手机上读；失效链接用 `python3 scripts/check_wikilinks.py`。

## 新公司

```bash
cp -r vault/interviews/_template/company vault/interviews/companies/<公司>
mkdir -p research/companies/<公司>/catalog/raw
```

然后按 `_template/company/README.md` 的清单填。第一天只需要 `01-company-brief.md` 和 `02-process.md`；答案库和模拟在拿到具体轮次邀请后再写。

## 和卡片的关系

- 公司文件夹里的内容按公司整体阅读，不逐条建卡；要进 Anki 的部分放在对应的卡片领域（例如低层设计的 `amazon` 分支）。
- `code-core` 领域的 `transfer.*` 分支是「新公司的一轮编码面试 = 一个叶子」的接口：公司的具体题目留在公司文件夹，通用规律升到那里。
