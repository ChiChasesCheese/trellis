---
id: cc-algorithms-binary-search-monotone-check
node: algorithms.binary-search
type: qa
---
## Q
Before searching an answer space, what must you establish — and what does failing to do so look like?

## A
**That the predicate is monotone in the searched variable**: once true, true forever (or once false, false forever).

- Say the sentence out loud: "if capacity C finishes in time, so does C + 1." If you cannot say it, the search is invalid even though it will return a number.
- A non-monotone predicate returns *a* boundary of *some* true region. It is silently wrong on exactly the inputs that have more than one region — which are the interesting hidden tests, never the sample.
- Typical breakage: a per-unit cost *plus* a discount above a threshold; a feasibility check that itself depends on an ordering you also choose; an objective that improves and then worsens.
- When monotonicity fails, the fallbacks are a scan, a DP, or a different parameterisation — never a "tweaked" binary search with extra conditions bolted on.

## Q zh
在答案空间上二分之前，你必须先确立什么 —— 没做会是什么样子？

## A zh
**谓词对被搜索变量是单调的**：一旦为真就永远为真（或一旦为假就永远为假）。

- 把这句话说出来：「如果运力 C 能按时完成，那么 C + 1 也能。」说不出来，这个搜索就是无效的，尽管它照样会返回一个数。
- 非单调的谓词返回的是*某个*为真区域的*某个*边界。它恰好在有多个区域的输入上悄悄出错 —— 那正是有意思的隐藏测试，而绝不会是样例。
- 典型的破坏方式：按件计价*外加*超过阈值的折扣；可行性检查本身依赖于一个同样由你选择的顺序；目标先变好再变坏。
- 单调性不成立时，退路是扫描、DP 或换一种参数化 —— 绝不是在二分上硬加条件「微调」一下。
