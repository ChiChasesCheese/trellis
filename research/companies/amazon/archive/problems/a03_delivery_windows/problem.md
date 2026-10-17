> **Reconstruction.** Shape reported as "merge delivery / blackout windows." Not a LeetCode statement. Wording is ours.

# a03 · Delivery windows

**Type:** Amazon OA coding · **Clock:** one of two problems in 70–90 min
**Family:** intervals · **Confidence:** medium (wording) / high (family)

Each window is a half-open minute range `[start, end)`. Merge overlapping **or touching** windows. Report the merged ranges in start order, then the total covered minutes.

## Input
```
N
<start> <end>
…
```

## Output
One line per merged window: `start,end`
Last line: `COVERED <minutes>`

## Constraints
N ≤ 10^5. Minutes are non-negative ints. `start < end`.
