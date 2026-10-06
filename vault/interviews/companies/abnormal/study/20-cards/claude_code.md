# 速记卡 · Claude Code 面试操作（AI Technical Screen 用）

> 官方门户点名：plan mode（Shift+Tab）、`claude --resume` / `/resume`。其余是 Claude Code 的常用功能；**考前在本地每个都按一次**，面试环境是浏览器 VS Code 的终端。

1. **启动**：终端里 `claude`。第二个终端跑测试与 CLI（`Ctrl/Cmd+\``，`+` 开新终端）。新终端接回会话：`claude --resume` 或会话内 `/resume`；`claude -c` 继续最近一次。
2. **Plan mode**：`Shift+Tab` 循环切换权限模式（普通 → 自动接受编辑 → plan）。plan 模式下它只读代码、给方案，不改文件——**写代码前先用它对齐方案**。
3. **打断与回退**：`Esc` 停止当前生成；`Esc Esc` 回到之前的消息改写；改坏了用 git（`git diff`、`git checkout -- <file>`）。
4. **引用文件**：`@path/to/file.py` 把文件放进上下文；比"看看 rules 目录"更准。
5. **跑命令**：`!pytest -q` 在会话里直接跑 shell 并把输出给它看。
6. **上下文**：`/context` 看用量；换任务 `/clear`；长会话 `/compact`（Shrivu 偏好 `/clear` + 让它重读改动文件）。
7. **项目说明**：`CLAUDE.md` 是它每次都读的约定；面试库若有，先读；没有可 `/init` 生成一份（≈1–2 分钟，产物可当架构摘要念）。
8. **提示词模板**（复制即用）：
   - 地图："Map this repo: entry points, main data flow, core models, extension points. Cite files. ≤ 25 lines."
   - 约定："What conventions does this codebase follow for config, persistence, errors, logging, tests? One canonical example each. Flag deprecated code."
   - 歧义："Given this ticket and this codebase, what's ambiguous? List decisions with the option you'd pick. No code."
   - 计划："Plan the smallest change for M1: <…>. Reuse <X> (pattern in <file>), tests next to <test file>, don't touch <legacy>. List files and test cases. Stop after M1."
   - 自审："Review this diff against the conventions you found. List deviations and risks, not style nits."
9. **审 AI 输出的三问**：挂在正确的扩展点上吗？配置/存储/注册/审计走已有的路吗？误报样本、租户隔离、缺字段覆盖了吗？
10. **手写的时机**：一行注册、一个配置键、一个断言——自己敲。AI 连续两次改错——自己接手。
