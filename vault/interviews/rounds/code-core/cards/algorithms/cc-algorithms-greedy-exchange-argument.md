---
id: cc-algorithms-greedy-exchange-argument
node: algorithms.greedy
type: cloze
---
A greedy is justified by an **exchange argument**: take any optimal solution that {{c1::differs from the greedy choice}} and show you can swap the greedy choice in {{c2::without making the solution worse}}; induction then gives optimality. If you cannot state that swap in one sentence you do not have a proof — and the fastest way to find out is {{c3::to hunt for a counterexample}} on the smallest input that offers a real choice, which is usually {{c4::2 or 3}} items.

## zh
贪心靠**交换论证**来证明：取任意一个与{{c1::贪心选择不同}}的最优解，证明可以把贪心选择换进去而{{c2::不会让解变差}}；再用归纳法即得最优性。如果你没法用一句话说出这个交换，那你就没有证明 —— 而最快的验证办法是 {{c3::去找反例}}，在最小的、确实存在选择的输入上找，通常 {{c4::2 或 3}} 个元素就够了。
