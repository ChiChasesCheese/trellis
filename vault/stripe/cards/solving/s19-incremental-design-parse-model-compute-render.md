---
id: s19-incremental-design-parse-model-compute-render
node: stripe.solving
type: qa
---

## Q
多个 part 层层递进的题（Part 3 = Part 2 的结果 + 一条新规则），后面的 part 应该复制前面 part 的逻辑，还是直接调用它？

## A
见 `01-solving-framework.md` §3。这里补一条：

**后面的 part 应该调用前面的 part，而不是复制它。** 例如 Part 3 是
"Part 2 的结果 + 一条新规则"，那就 `def part3(lines): return apply_rule(part2(lines))`。
这样 Part 2 的 bug 修一次两处都对。
