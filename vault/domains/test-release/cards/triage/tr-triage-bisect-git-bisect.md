---
id: tr-triage-bisect-git-bisect
node: triage.bisect
type: qa
step: 1
---
## Q
`git bisect` 是怎么在一段提交区间里找到引入回归的那个提交的？在 1,000 个提交里要试几次？`git bisect run` 的退出码约定是什么？

## A
**原理：二分查找**。已知一个"好"提交（没有问题）和一个"坏"提交（有问题），并假设问题出现后一直存在。每次检出区间中点测试：好就说明问题在后半段，坏就在前半段。每一步把候选减半。

例：提交 0 是好、16 是坏，问题由 11 引入；阴影是剩下的候选，粗框是这次检出的中点：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<g font-family="sans-serif" font-size="11" fill="currentColor">
<g stroke="currentColor" stroke-width="0.6">
<path fill-opacity="0.18" d="M52,22h15v20h-15zM69,22h15v20h-15zM86,22h15v20h-15zM103,22h15v20h-15zM120,22h15v20h-15zM137,22h15v20h-15zM154,22h15v20h-15zM171,22h15v20h-15zM188,22h15v20h-15zM205,22h15v20h-15zM222,22h15v20h-15zM239,22h15v20h-15zM256,22h15v20h-15zM273,22h15v20h-15zM290,22h15v20h-15zM307,22h15v20h-15zM188,68h15v20h-15zM205,68h15v20h-15zM222,68h15v20h-15zM239,68h15v20h-15zM256,68h15v20h-15zM273,68h15v20h-15zM290,68h15v20h-15zM307,68h15v20h-15zM188,114h15v20h-15zM205,114h15v20h-15zM222,114h15v20h-15zM239,114h15v20h-15zM222,160h15v20h-15zM239,160h15v20h-15z"/>
<path fill="none" d="M52,68h15v20h-15zM69,68h15v20h-15zM86,68h15v20h-15zM103,68h15v20h-15zM120,68h15v20h-15zM137,68h15v20h-15zM154,68h15v20h-15zM171,68h15v20h-15zM52,114h15v20h-15zM69,114h15v20h-15zM86,114h15v20h-15zM103,114h15v20h-15zM120,114h15v20h-15zM137,114h15v20h-15zM154,114h15v20h-15zM171,114h15v20h-15zM256,114h15v20h-15zM273,114h15v20h-15zM290,114h15v20h-15zM307,114h15v20h-15zM52,160h15v20h-15zM69,160h15v20h-15zM86,160h15v20h-15zM103,160h15v20h-15zM120,160h15v20h-15zM137,160h15v20h-15zM154,160h15v20h-15zM171,160h15v20h-15zM188,160h15v20h-15zM205,160h15v20h-15zM256,160h15v20h-15zM273,160h15v20h-15zM290,160h15v20h-15zM307,160h15v20h-15z"/>
</g>
<path fill="none" stroke="currentColor" stroke-width="2.5" d="M171,22h15v20h-15zM239,68h15v20h-15zM205,114h15v20h-15zM222,160h15v20h-15z"/>
<path fill-opacity="0.6" stroke="currentColor" d="M222,206h15v20h-15z"/>
<text x="60.5" y="14" text-anchor="middle">1</text>
<text x="315.5" y="14" text-anchor="middle">16</text>
<text x="4" y="36">第1次</text>
<text x="178.5" y="56" text-anchor="middle">测8：好</text>
<text x="4" y="82">第2次</text>
<text x="246.5" y="102" text-anchor="middle">测12：坏</text>
<text x="4" y="128">第3次</text>
<text x="212.5" y="148" text-anchor="middle">测10：好</text>
<text x="4" y="174">第4次</text>
<text x="229.5" y="194" text-anchor="middle">测11：坏</text>
<text x="4" y="220">结果</text>
<text x="243" y="220">第一个坏提交11</text>
</g>
</svg>
```

**次数**：约 log₂(N) 次。1,000 个提交约 10 次（2¹⁰ = 1024）；100 个约 7 次。如果每次构建加测试要 20 分钟，10 次就是 3 个多小时，比人工逐个看快得多，而且可以完全自动。

**手动用法**：

```bash
git bisect start <坏提交> <好提交>   # 例如 HEAD v1.7.0
# git 检出中点后，测试，然后告诉它结果
git bisect good        # 或 git bisect bad
git bisect skip        # 这个提交没法测（例如编译不过）
git bisect reset       # 结束，回到原来的分支
```

**自动用法**：`git bisect run ./check.sh`，git 在每个中点运行脚本，按退出码判断：
- **0**：好；
- **1–127（125 除外）**：坏；
- **125**：这个提交无法测试，跳过；
- **其他值**（例如 128 以上，包括被信号杀死）：中止整个二分。

注意 `exit(-1)` 在 shell 里会变成 255，会让二分直接中止，而不是判为"坏"。

**其他有用的命令**：
- `git bisect log` 保存过程，`git bisect replay <文件>` 重放，用于标错了某一步之后修正；
- `git bisect start --term-old fast --term-new slow`：找"从什么时候开始变慢"这类不是对错的问题，术语换成自己的；
- `--first-parent`：只沿主干的第一父提交走，遇到合并提交时把整个合并当成一步，避免掉进被合并分支里那些本来就编译不过的中间提交。

结束时 git 打印"第一个坏提交"，这就是嫌疑提交，还需要用"在它和它的父提交上各跑一次"来确认。
