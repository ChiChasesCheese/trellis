---
id: cc-transfer-playbook-card-the-rule
node: transfer.playbook
type: qa
---
## Q
A hidden test failed because you used `>` where the specification meant `>=`. What do you turn that into, and what would be worthless?

## A
**A card stating the general rule, answerable by someone who has never seen the original problem**: read "exceeds" as strict `>` and "at least" as `>=`, and always test `limit - 1`, `limit`, `limit + 1` ([[cc-verification-edge-exact-threshold-triple]]).

- Worthless: "in that fraud problem the threshold was `>=`". That tests recall of your own conclusion about one artefact, and it never fires again.
- The test of a good card: could a stranger answer it, and would it change what they type in a different company's round?
- One failure usually yields exactly one card. Two unrelated lessons are two cards, not one long one.

## Q zh
一个隐藏测试挂了，因为你写了 `>`，而规格的意思是 `>=`。你把它变成什么？什么样的东西毫无价值？

## A zh
**一张陈述通用规则、且从没见过原题的人也能作答的卡片**：把 "exceeds" 读成严格的 `>`，把 "at least" 读成 `>=`，并且永远测 `limit - 1`、`limit`、`limit + 1`（[[cc-verification-edge-exact-threshold-triple]]）。

- 毫无价值的：「那道欺诈题里的阈值是 `>=`」。它考的是你对某一件产物的结论的记忆，而且再也不会被触发第二次。
- 好卡片的检验标准：陌生人能不能答？它会不会改变那个人在另一家公司轮次里敲下的东西？
- 一次失败通常正好产出一张卡。两条无关的经验是两张卡，不是一张长的。
