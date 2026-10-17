> **Reconstruction.** Shape reported as "two items under a spend cap." Not a LeetCode statement. Wording is ours.

# a05 · Budget pair

**Type:** Amazon OA coding · **Clock:** one of two problems in 70–90 min
**Family:** two pointers · **Confidence:** medium (wording) / high (family)

Pick **two distinct** prices whose sum is as close as possible to the budget **without exceeding it**. If several pairs share that sum, pick the pair with the smaller first price, then the smaller second price. Prices are printed in ascending order. No pair → `NONE`.

## Input
```
N
<p1> <p2> …
B
```

## Output
`lo,hi` or `NONE`

## Constraints
N ≤ 10^5. Prices and budget are positive ints.
