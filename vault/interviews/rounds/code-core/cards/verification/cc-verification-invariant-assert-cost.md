---
id: cc-verification-invariant-assert-cost
node: verification.invariants
type: qa
---
## Q
You want assertions everywhere, and you also have to pass a 2-second performance test. Reconcile the two.

## A
**Assert at the boundary, not in the hot loop.**

- O(1) checks stay inline: a parsed field is in range, a counter did not go negative, a lookup key exists.
- Anything O(n) — recomputing a sum to compare against a maintained total — belongs in a test, or behind an explicit `if DEBUG:` that is `False` in the submitted file.
- `assert` is stripped by `python -O`, so never put a side effect or a check you actually depend on inside one; a validation that must always run is an `if ... raise`.
- Give every assert a message carrying the offending value: `assert total >= 0, (acct, total)`. An assertion without context costs you the minute you saved writing it.

## Q zh
你想到处放断言，同时又必须通过 2 秒的性能测试。把两者调和一下。

## A zh
**在边界处断言，不要在热点循环里断言。**

- O(1) 的检查可以内联：解析出的字段在范围内、计数器没有变负、查找的键存在。
- 任何 O(n) 的检查 —— 重算一个总和去比对增量维护的值 —— 都属于测试，或者放在一个显式的 `if DEBUG:` 后面，而提交的文件里它是 `False`。
- `assert` 会被 `python -O` 剥掉，所以绝不要在里面放副作用或你真正依赖的检查；必须始终执行的校验要写成 `if ... raise`。
- 每个断言都带上出错的值：`assert total >= 0, (acct, total)`。没有上下文的断言会把你写它省下的那一分钟还回去。
