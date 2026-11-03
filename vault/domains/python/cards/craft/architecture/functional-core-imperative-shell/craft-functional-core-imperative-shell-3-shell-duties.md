---
id: craft-functional-core-imperative-shell-3-shell-duties
node: craft.architecture.functional-core-imperative-shell
type: qa
step: 3
---
## Q
**函数式核心 + 命令式外壳 · 外壳该薄到什么程度**｜架构

一个带锁、带通知的服务里，每个公开方法既要保证并发正确，又要做业务判断。如果两件事缠在一起，测并发时得带上整套业务，测业务时又得起线程。外壳和核心各自必须做什么、绝对不能做什么？

## A
**要点。** 外壳按固定顺序做五件事：拿锁 → 取时间等外部输入 → 调核心 → 把结果提交到真状态 → 放锁后通知。核心不拿锁、不取时间、不改对象字段、不发通知、不抛出和输入无关的异常。这样「并发对不对」只在外壳里验，「规则对不对」只在核心里验。

```python
def _seat_everyone_possible(self):
    now = self._clock()                         # 外部输入：外壳取，核心不知道时钟
    placed = _drain(self._queue, self._free,    # 调核心
                    self._sizes, self._max_overtakes)
    for w, table in placed:
        self._seated[w.id] = (table, now)       # 提交：只有外壳改真状态
    return [(w.id, table) for w, table in placed]
```

**为什么。** 时间是外壳取一次再传下去：核心拿到的是同一个 `now`，试跑与真实就能用同一个时间；测试给核心传固定的值，不用 mock 时钟。

**代价。** 外壳一旦变胖，比如在里面加 `if` 判断谁优先，规则就又散了两处，预测与真实会分叉。判断标准：外壳里出现业务名词（座位、额度）的分支，就该下沉进核心。

**信号。** 一个方法里同时出现 `with lock`、`self._clock()`、业务 `if` 和 `notify`，就该拆。
