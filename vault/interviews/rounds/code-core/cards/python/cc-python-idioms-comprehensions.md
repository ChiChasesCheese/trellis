---
id: cc-python-idioms-comprehensions
node: python.idioms
type: qa
---
## Q
Write the four comprehension forms you reach for every round, plus the generator form that matters at 10^6 rows. Then say when a comprehension should go back to being a loop.

## A
```python
names = [r.name for r in rows if r.ok]        # list
by_id = {r.id: r for r in rows}               # dict (last duplicate wins)
ids   = {r.id for r in rows}                  # set
first = next((r for r in rows if r.ok), None) # first match, no list built
total = sum(r.amount for r in rows if r.ok)   # streams, O(1) extra memory
```

- A generator expression inside `sum` / `any` / `max` / `str.join` never materializes the list — the default choice on 10^6 rows.
- `{r.id: r for r in rows}` silently keeps the **last** duplicate; that is a policy decision, so make it deliberately.
- Turn it back into a loop the moment it needs two conditions plus an `else`, or must mutate state per row. A comprehension that needs a comment is a loop.

## Q zh
写出你每一轮都会用到的四种推导式形式，加上在 10^6 行规模上真正重要的生成器形式。然后说明推导式什么时候该变回循环。

## A zh
```python
names = [r.name for r in rows if r.ok]        # list
by_id = {r.id: r for r in rows}               # dict（重复时后者覆盖）
ids   = {r.id for r in rows}                  # set
first = next((r for r in rows if r.ok), None) # 首个匹配，不构造 list
total = sum(r.amount for r in rows if r.ok)   # 流式，额外内存 O(1)
```

- 放在 `sum` / `any` / `max` / `str.join` 里的生成器表达式不会物化列表 —— 在 10^6 行上这是默认选择。
- `{r.id: r for r in rows}` 会静默保留**最后**一个重复项；那是一个策略决定，要有意识地做。
- 一旦需要两个条件加一个 `else`，或者需要按行改状态，就变回循环。需要写注释的推导式就是一个循环。
