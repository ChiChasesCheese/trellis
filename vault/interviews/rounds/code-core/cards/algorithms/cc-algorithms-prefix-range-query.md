---
id: cc-algorithms-prefix-range-query
node: algorithms.prefix
type: cloze
---
With `pre[0] = 0` and `pre[i] = pre[i-1] + a[i-1]`, the sum of the half-open slice `a[l:r]` is {{c1::`pre[r] - pre[l]`}}, so `pre` has {{c2::n + 1}} entries and every range query costs {{c3::O(1)}} after an O(n) build. For an *inclusive* range `[l, r]` the same expression is {{c4::`pre[r+1] - pre[l]`}} — the off-by-one lives entirely in the index convention, so write which one you chose {{c5::in a comment above the array}}.

## zh
取 `pre[0] = 0`、`pre[i] = pre[i-1] + a[i-1]`，则半开切片 `a[l:r]` 的和是 {{c1::`pre[r] - pre[l]`}}，所以 `pre` 有 {{c2::n + 1}} 个元素，构建 O(n) 之后每次区间查询是 {{c3::O(1)}}。对*闭*区间 `[l, r]`，同样的表达式是 {{c4::`pre[r+1] - pre[l]`}} —— off-by-one 完全存在于下标约定里，所以把你选的那种 {{c5::写在数组上方的注释里}}。
