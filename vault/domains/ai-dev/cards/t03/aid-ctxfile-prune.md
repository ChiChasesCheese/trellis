---
id: aid-ctxfile-prune
node: t03.context-file-claude-md-agents-md
type: qa
step: 2
tags: [考点]
---
## Q
**Context file · 哪些行该删**｜考点 · 必会

下面是某个仓库 CLAUDE.md 里的六行。哪些该删，哪些该留？

```text
1. We use TypeScript with React and Vite.
2. Components live in src/components, one folder each.
3. Run one test: pnpm vitest run <file>
4. Write clean, well-structured, maintainable code.
5. Don't copy patterns from src/legacy/, still live but deprecated.
6. IMPORTANT: ALWAYS write unit tests!!!
```

## A
| 行 | 处理 | 理由 |
|---|---|---|
| 1 | 删 | 读 `package.json` 就知道 |
| 2 | 删 | 读目录就知道 |
| 3 | **留** | 测试命令是"怎么确认做对了" |
| 4 | 删 | 空话，没法检验，agent 本来就在努力 |
| 5 | **留** | 读代码读不出来：老代码到处都是，agent 会学它 |
| 6 | 改 | 去掉大写和感叹号：现行模型照普通措辞就会做，强调只会让它过度套用；如果真是没有例外的规则，就做成 hook（harness 执行的脚本，下一叶讲）或检查 |

**结果：** 六行剩两行，还有更好的信噪比。

**时效（2026-11 官方）：** 官方"可以不再做的事"列表里有：给 agent 一再忽略的指令加 IMPORTANT 或全大写、在 CLAUDE.md 里描述架构和文件布局。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Keep CLAUDE.md short；What you can stop doing）

</details>
