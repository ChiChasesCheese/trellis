---
id: cc-round-debug-minimal-repro
node: round.debugging
type: qa
---
## Q
You have bisected to a failing 40-line input. Why keep shrinking it, and how far?

## A
**Shrink until every remaining line is necessary — the minimal input *is* the diagnosis.** Delete a line; if it still fails, keep it deleted. Three or four rounds usually take 40 lines to three, and at three lines the bug is often visible without running anything.

Then keep the minimal case as a test, named for the rule it violates. It costs nothing to re-run after each later part, and it is the only defence against fixing this bug and silently re-introducing it while writing the next part.

## Q zh
你已经二分到一个 40 行的失败输入。为什么还要继续缩，缩到什么程度？

## A zh
**缩到每一行都不可或缺 —— 最小输入本身**就是**诊断。** 删掉一行；如果仍然失败，就保持删除。三四轮通常能把 40 行缩到 3 行，而到了三行，常常不用运行就能看出 bug。

然后把这个最小用例留作测试，用它违反的规则来命名。以后每做完一部分重跑一次几乎不花钱，而这也是唯一能防止"修好这个 bug 又在写下一部分时悄悄引回来"的手段。
