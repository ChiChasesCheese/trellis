---
id: craft-validate-then-commit-2-across-problems
node: craft.patterns.validate-then-commit
type: qa
step: 2
---
## Q
**先校验后提交 · 三道设计题里同一个骨架**｜模式

账本、电子表格、库存预留三种完全不同的状态，写代码时都会遇到「多处修改，中途失败」。它们的参考解是怎么把同一个骨架落到各自数据上的？哪些部分变了，哪些没变？

## A
**要点。** 骨架不变：校验段（只读，可抛异常）→ 一条分界线 → 提交段（只赋值）。变的只是「校验什么」和「分界线前算出的中间物」。

```python
# 账本 double-entry-ledger.post
self._validate(entry)                 # 先校验后修改：失败不留痕迹
self._check_reverses(entry)
self._check_floors(delta, freed)
self._journal.append(entry)           # 以下是提交：不会再失败

# 电子表格 spreadsheet-engine.set
node = parse_raw(raw)                 # 先解析：写错了表格没动过
if self._reaches(new_deps, cell):     # 先查环，再改任何状态
    raise CycleError(cell)

# 库存 inventory-management.reserve_many
plans = {sku: self._plan(sku, q) for sku in sorted(lines)}  # 先全部算好
return tuple(self._commit(sku, ...) for sku, plan in plans.items())
```

中间物各不相同：账本是 `delta` 字典，表格是解析后的语法树 `node`，库存是每个 sku 的 `plan`。共同点：它们都是「提交段需要的、已经算好的东西」，提交段不再做判断。

**见于。** double-entry-ledger、spreadsheet-engine、inventory-management、rate-limiter（组合限流）、amz-configurable-cache、battleship-game（齐射先整体检查）。

**信号。** 一个方法要改两处以上状态，或要对一批对象做「全有或全无」；你发现自己在写 `try: ... except: 撤销`。
