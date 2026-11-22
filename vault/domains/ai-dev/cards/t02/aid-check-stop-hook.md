---
id: aid-check-stop-hook
node: t02.agent-check-tests-type-check-lint-expected-outpu
type: qa
step: 2
tags: [实践]
---
## Q
**Check · 用 Stop hook 强制**｜实践 · 追问

prompt 里写"完成前一定跑 type check"，agent 多数时候照做，偶尔漏掉。怎么让它每次都不漏？

## A
**把"建议"换成"强制"：** 配置一个 Stop hook（hook：harness 在固定时点执行的脚本；Stop 在 agent 想结束时触发），在 agent 想结束时跑 type check，失败就把它送回去。

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [
        { "type": "command",
          "command": "pnpm tsc --noEmit 1>&2 || exit 2" }
      ]}
    ]
  }
}
```

**逐行意思：** hooks：登记要执行的 hook 的键；`tsc --noEmit` 只检查类型；`1>&2` 把编译器输出送到 stderr，这样会作为"为什么还不能结束"返回给 agent；`exit 2` 是"阻止结束"的退出码。

**边界：** 连续阻止 8 次且中间没有工具调用，Claude Code 会放行并结束（可调上限）。所以它是"强制重试"，不是无限循环。

**判断：** 一次偶尔漏掉也可以接受 → 留在 prompt 里；漏掉就出问题 → 用 hook。

**时效（2026-11）：** 这类配置的配置格式和字段名随版本变，上面是官方文档当时的写法。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Enforce the check with a Stop hook）

</details>
