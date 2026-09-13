# core/resume — 简历的唯一源头

这里是简历的 **canonical source**。改简历只改 `resume.tex`，编译出 PDF，再把 PDF 复制到投递用的位置。
不要再在 JobWorkFlow / JobApply / Overleaf 里各改一份。

```
resume.tex               LaTeX 源（Source Sans Pro，10pt，单页）
resume.pdf               latexmk 编译产物（可提交；每次改 tex 后重编）
Chi_Zhang_SDE.pdf        当前对外投递版（= resume.pdf 的快照；与 iCloud/个人文件 同名文件保持一致）
leetcode-svgrepo-com.pdf 页眉 LeetCode 图标
CHANGELOG.md             每次改动记一行：日期 · 改了什么 · 为什么（哪家公司 / 哪条反馈）
```

## 编译

```bash
cd vault/interviews/core/resume
latexmk -pdf resume.tex          # TeX Live 在 /Library/TeX/texbin；首次约 10 s
latexmk -c                       # 清理 .aux/.log（.gitignore 已忽略）
```

单页检查：`uv run --with pypdf python -c "from pypdf import PdfReader;print(len(PdfReader('resume.pdf').pages))"` 必须打印 `1`。

## 发布

```bash
cp resume.pdf Chi_Zhang_SDE.pdf
cp Chi_Zhang_SDE.pdf "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Documents/个人文件/Chi_Zhang_SDE.pdf"
```

然后在 `CHANGELOG.md` 加一行，commit。

## 内容与证据的关系

- 每条 bullet 背后的真实证据在 `../stories/evidence-base.md`（S1–S9）和 `../stories/resume-evidence-map/`。
- 面试前对照 `evidence-base.md` §3「全局诚实红线」核对数字口径：
  - **$600B+**：evidence-base 里可辩护的是 $138.6B（2025 Amex volume，Impact Summary）；$600B 若为全平台/年化口径，先确认再说。
  - **Sentry**：evidence-base 六个来源里未见 Sentry，只见 Datadog + 自建 Streamlit + Splunk；`resume-evidence-map/03` 另有三处独立确认在用。面试里优先说 Datadog。
  - **Kafka in Kubernetes**（intern）：最弱的一条，见 `resume-evidence-map/04`。
- 简历改了某条 bullet，就同步改对应故事的「简历话术」段落，反之亦然。

## 定制版

按公司定制时 **不要 fork 整个 tex**：复制 `resume.tex` 为 `../../companies/<company>/resume-<company>.tex`，只改 bullet 顺序和措辞，并在该公司 dossier 的 `00-README.md` 里记录投递的是哪个版本。
