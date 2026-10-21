> **Reconstruction.** Shape reported in 2025–2026 Amazon OA write-ups (nearest feasible resource). Not a LeetCode statement. Wording is ours.

# a01 · Fulfillment assignment

**Type:** Amazon OA coding · **Clock:** one of two problems in 70–90 min
**Family:** heap · **Confidence:** medium (wording) / high (family)

Assign each incoming order to the **nearest warehouse that still has capacity**. Distance is Euclidean. Ties break by warehouse id, string ascending. If none fit, reject.

## Input
```
W
<wid> <x> <y> <capacity>
…
N
<oid> <x> <y> <size>
```

## Output
One line per order, input order: `oid,wid` or `oid,REJECT`

## Constraints
W, N ≤ 10^4. Coordinates fit in 32-bit ints. Capacity and size are positive ints.
