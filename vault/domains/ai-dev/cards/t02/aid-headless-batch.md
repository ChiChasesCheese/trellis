---
id: aid-headless-batch
node: t02.headless-batch-scheduled-event-triggered
type: qa
step: 1
tags: [实践]
---
## Q
**Headless 与 batch**｜实践 · 追问

你要让 agent 在 CI 或脚本里对 200 个文件做同一种迁移，没有人盯着。要加哪些保险？

## A
**headless（无头）：** `claude -p "prompt"` 运行一次就退出，适合 CI、git hook、shell 循环。

```bash
for file in $(cat files.txt); do
  claude --bare -p "Migrate $file to the new logger API and commit. Reply OK or FAIL." \
    --allowedTools "Read,Edit,Bash(git add *),Bash(git commit *)" \
    --permission-mode dontAsk \
    --max-turns 20
done
```

| 参数 | 作用 |
|---|---|
| `--allowedTools` | 预先批准这些工具 |
| `--permission-mode dontAsk` | 其余本来要问的一律拒绝 |
| `--max-turns` / `--max-budget-usd` | 回合或花费上限 |
| `--output-format json` | 输出单个可解析的结果 |

**无人值守前的五问：** 它知道什么叫完成吗？能自检吗？能碰什么？什么让它停？结果交给谁签字？

**做：** 先在 3 个文件上试，看哪里出错，改好 prompt，再跑其余。
**别做：** 直接对全部 200 个文件放权运行。

**时效：** 参数名以官方文档为准（2026-11 的写法）。

**出处：** Claude Code docs《Best practices》（Let Claude run without you：Run Claude from a script）
