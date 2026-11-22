---
id: aid-migration
node: t05.migration-refactoring
type: qa
step: 1
tags: [实践]
---
## Q
**大规模 migration 与 refactoring**｜实践 · 必会

要把 300 个文件从旧日志库迁到新日志库。怎么做才不会出现"改了一半、不知道哪里坏了"？

## A
**脚本化 + 分批验证 + 每批一个检查点。**

| 步骤 | 做法 |
|---|---|
| 1. 定规则 | 先在 2~3 个文件上和 agent 一起迁，确认规则和 prompt |
| 2. 脚本化 | 写成可重复的命令：每个文件一次无人值守的运行，输出 OK 或 FAIL |
| 3. 分批 | 一批 20~30 个，批内每个文件都要过测试 |
| 4. 每批一个提交 | 出问题只回退这一批 |
| 5. 失败的人工处理 | FAIL 的文件列出来单独看 |

```bash
for file in $(cat batch1.txt); do
  claude --bare -p "Migrate $file to the new logger API and commit. Reply OK or FAIL." \
    --allowedTools "Read,Edit,Bash(git add *),Bash(git commit *)" \
    --permission-mode dontAsk --max-turns 20
done
```

**官方原话的思路：** 先在 3 个文件上试，看出错在哪，改好 prompt，再跑其余。
**工具里的对应（2026-11）：** `/batch` 把大改拆成 5 到 30 个单元，展示计划，批准后每个单元一个独立工作目录并开 PR。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Run Claude from a script；Run sessions in parallel）

</details>
