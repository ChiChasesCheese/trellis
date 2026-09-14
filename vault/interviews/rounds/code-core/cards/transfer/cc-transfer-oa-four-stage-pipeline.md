---
id: cc-transfer-oa-four-stage-pipeline
node: transfer.stripe-oa
type: qa
---
## Q
The bespoke-spec assessment always has the same four stages. Name them, and say what you gain by keeping them as separate functions.

## A
**Parse → model → apply rules → render**, with `main` doing nothing but wiring the four together.

- **Parse**: bytes to typed records; one validator; normalization done once, at the boundary.
- **Model**: dicts keyed by id, exactly one place holding each entity's state.
- **Rules**: pure functions over that state — this is where the hidden tests live.
- **Render**: formatting in exactly one function, so a format change is a one-line change.

What it buys: every stage is testable with plain data; part N+1 usually adds a rule instead of forcing a rewrite; and a failing test tells you which stage to open from the shape of the diff. A solution that interleaves parsing with arithmetic has to be re-read in full for every bug.

## Q zh
定制题面型笔试永远是同样的四个阶段。说出它们，并说明把它们保持为分离的函数能得到什么。

## A zh
**解析 → 建模 → 应用规则 → 渲染**，而 `main` 只负责把这四段接起来。

- **解析**：字节到带类型的记录；一个校验器；规范化只在边界做一次。
- **建模**：按 id 作键的字典，每个实体的状态恰好只有一处持有。
- **规则**：作用在该状态上的纯函数 —— 隐藏测试住在这里。
- **渲染**：格式化恰好在一个函数里，于是改格式就是改一行。

收益：每个阶段都能用普通数据测试；part N+1 通常是加一条规则而不是被迫重写；测试失败时，从 diff 的形状就能看出该打开哪个阶段。把解析和算术揉在一起的方案，每出一个 bug 都得整份重读。
