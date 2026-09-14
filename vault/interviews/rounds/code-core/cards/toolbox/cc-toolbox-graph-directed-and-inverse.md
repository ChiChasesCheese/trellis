---
id: cc-toolbox-graph-directed-and-inverse
node: toolbox.graph-repr
type: qa
---
## Q
A rate table gives `USD:EUR:0.9`. Does that give you `EUR:USD`? A shipping leg gives `UK:US:UPS:4`. Does that give you `US:UK`?

## A
**Only if the domain says so — direction is data, not decoration.**

- Shipping legs are **directed**: the reverse leg exists only if it is listed. Adding it "for symmetry" invents routes and produces a cheaper-than-real answer that no test expects.
- Exchange rates *are* invertible, so `1/rate` is a legitimate reverse edge — but a **direct quote must win** over the inverse of the opposite quote when both exist. Build in two passes: all direct edges first, then `setdefault` the inverses.
- Inconsistent pairs (`USD:AUD:1.4` alongside `AUD:USD:0.8`) must not be allowed to compound into a profit cycle — restrict paths to simple ones, or cap the hop count ([[cc-algorithms-shortest-path-product-weights]]).
- A duplicate ordered pair means "last one wins" unless the spec says otherwise. Decide, and put it in a comment.

## Q zh
汇率表给出 `USD:EUR:0.9`。它是否也给了你 `EUR:USD`？运输航段给出 `UK:US:UPS:4`。它是否也给了你 `US:UK`？

## A zh
**只有领域规则这么说时才成立 —— 方向是数据，不是装饰。**

- 运输航段是**有向的**：反向段只有被列出时才存在。为了「对称」而加上它就是凭空造出航线，得到一个比真实更便宜、任何测试都不期待的答案。
- 汇率*确实*可逆，所以 `1/rate` 是合法的反向边 —— 但当两者都存在时，**直接报价必须优先**于反向报价的倒数。分两趟构建：先加所有直接边，再用 `setdefault` 补倒数。
- 互相矛盾的报价对（`USD:AUD:1.4` 与 `AUD:USD:0.8` 并存）不能被复利放大成套利环 —— 把路径限制为简单路径，或限制跳数（[[cc-algorithms-shortest-path-product-weights]]）。
- 重复的有序对默认「后者胜出」，除非 spec 另有规定。做出决定，并写进注释。
