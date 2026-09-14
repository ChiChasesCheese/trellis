---
id: quality-null-returns
node: quality.errors
type: qa
---
## Q
Your repository's `findById` can miss. Rank the return-type options for "not found" and say when absence should be an exception instead.

## A
- **Best: `Optional<Order>`** — absence is in the signature; the compiler makes every caller decide (`orElseThrow`, `map`, default). For collections, return an **empty collection**, never null.
- **Acceptable: null object** (`GuestUser.ANONYMOUS`) — only when there's a genuinely sensible do-nothing/default behavior; a null object that silently absorbs real work hides bugs.
- **Worst: return `null`** — moves the check to every caller, and the NPE fires far from the cause.

Absence should **throw** when it violates an invariant — the caller holds an id the system itself issued (`getById` on a just-created order), so "missing" means corruption, not a normal outcome. Pattern: offer `findById → Optional` and `getById → throws NotFoundException`, and let callers state their expectation.

## Q zh
你的仓储 `findById` 可能找不到。给"未找到"的各种返回类型排序，并说明什么时候"不存在"反而应该抛异常。

## A zh
- **最好：`Optional<Order>`** —— 不存在这件事写在签名里，编译器逼着每个调用方做决定（`orElseThrow`、`map`、默认值）。对集合，返回**空集合**，永远不要返回 null。
- **可接受：null object**（`GuestUser.ANONYMOUS`）—— 仅当确实存在一个合理的"什么都不做/默认"行为时；一个默默吞掉真实工作的 null object 会把 bug 藏起来。
- **最差：返回 `null`** —— 把检查推给每一个调用方，而且 NPE 会在离病因很远的地方爆炸。

当"不存在"违反了一条不变量时，就该**抛异常** —— 调用方手里的 id 是系统自己发出去的（对刚创建的订单调 `getById`），那么"找不到"意味着数据损坏，而不是一个正常结果。惯用做法：同时提供 `findById → Optional` 和 `getById → throws NotFoundException`，让调用方自己表明预期。
