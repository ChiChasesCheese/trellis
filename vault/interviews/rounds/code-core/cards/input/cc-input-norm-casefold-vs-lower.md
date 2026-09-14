---
id: cc-input-norm-casefold-vs-lower
node: input.normalization
type: qa
---
## Q
For a case-insensitive lookup key, when is `str.lower()` not enough?

## A
**When the input can be non-ASCII: `casefold()` is the case-insensitive-comparison operation, `lower()` is the display transformation.**

`"STRASSE".lower()` is `strasse` but `"straße".lower()` stays `straße`; `casefold()` maps both to `strasse`. For ASCII identifiers they are identical, so the cost of preferring `casefold()` for keys is zero.

Two rules that matter more than the choice: fold on the way into the key, never in the comparison itself (`a.lower() == b.lower()` scattered through the code drifts), and never fold a value you must print back.

## Q zh
做大小写不敏感的查找 key 时，什么时候 `str.lower()` 不够用？

## A zh
**当输入可能是非 ASCII 时：`casefold()` 才是大小写无关比较的操作，`lower()` 是显示用的变换。**

`"STRASSE".lower()` 是 `strasse`，但 `"straße".lower()` 仍是 `straße`；`casefold()` 把两者都映射成 `strasse`。对 ASCII 标识符两者完全一样，所以 key 上优先用 `casefold()` 的代价为零。

比选哪个更重要的两条规则：在生成 key 时折叠，而不是在比较时折叠（散落各处的 `a.lower() == b.lower()` 会漂移）；以及绝不折叠你还要原样打印的值。
