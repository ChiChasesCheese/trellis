---
id: cc-algorithms-binary-search-on-answer
node: algorithms.binary-search
type: qa
---
## Q
"The minimum capacity that finishes the work within D days." There is no closed form. What do you search, and what does it cost?

## A
**Binary search the answer space, not an array**, whenever `feasible(x)` is monotone: false, false, …, true, true.

- Write `feasible(x)` as a plain O(n) simulation. That is the part you can get right under time pressure, and it is where all the domain rules live.
- Total cost is O(n · log(range)); with a range of 10^9 that is 30 evaluations — the log factor is essentially free.
- The cue that names this technique is "minimise the maximum" or "maximise the minimum" ([[cc-algorithms-recognition-cue-to-technique]]).
- For "the **maximum** x that is feasible", flip the predicate and search the first infeasible, then subtract one — do not maintain two different loop shapes ([[cc-algorithms-binary-search-loop-shape]]).
- Confirm monotonicity first; the loop happily returns something either way ([[cc-algorithms-binary-search-monotone-check]]).

## Q zh
「在 D 天内完成工作所需的最小运力。」没有闭式解。你二分什么，代价多少？

## A zh
**只要 `feasible(x)` 是单调的（假、假、……、真、真），就在答案空间上二分，而不是在数组上。**

- 把 `feasible(x)` 写成朴素的 O(n) 模拟。那是限时压力下你能写对的部分，也是所有业务规则所在之处。
- 总代价是 O(n · log(值域))；值域 10^9 时也就 30 次求值 —— log 因子几乎是免费的。
- 点名这项技术的线索是「最小化最大值」或「最大化最小值」（[[cc-algorithms-recognition-cue-to-technique]]）。
- 求「可行的**最大** x」时，把谓词反过来找第一个不可行再减一 —— 不要维护两套不同的循环形态（[[cc-algorithms-binary-search-loop-shape]]）。
- 先确认单调性；不管单不单调，这个循环都会照样返回一个值（[[cc-algorithms-binary-search-monotone-check]]）。
