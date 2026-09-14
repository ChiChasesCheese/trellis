---
id: cc-algorithms-settlement-min-transfers
node: algorithms.settlement
type: cloze
---
With n non-zero net balances the minimum number of transfers is {{c1::n − (the maximum number of disjoint zero-sum subsets)}}, not {{c2::n − 1}}: each zero-sum group settles internally in `size − 1` transfers, so every extra group you find saves one transfer. Two ways to compute it — {{c3::DFS with pruning}} over which later party absorbs the first unsettled one, or {{c4::bitmask DP over subsets}} while n ≤ 20 — and both require {{c5::the zero nets dropped first}}.

## zh
在 n 个非零净额下，最少转账次数是 {{c1::n − （互不相交的零和子集的最大个数）}}，而不是 {{c2::n − 1}}：每个零和组内部用 `size − 1` 笔转账即可结清，所以每多找出一组就省一笔。两种算法 —— 对「由后面哪一方吸收第一个未结清者」做 {{c3::带剪枝的 DFS}}，或在 n ≤ 20 时做 {{c4::子集上的 bitmask DP}} —— 两者都要求 {{c5::先把净额为零的丢掉}}。
