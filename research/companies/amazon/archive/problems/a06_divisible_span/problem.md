> **Reconstruction.** Shape reported as "longest contiguous fulfillment batch whose units are divisible by k." Not a LeetCode statement. Wording is ours.

# a06 · Divisible span

**Type:** Amazon OA coding · **Clock:** one of two problems in 70–90 min
**Family:** prefix remainder · **Confidence:** medium (wording) / high (family)

Given a list of unit counts and modulus `k`, return the **longest** contiguous span whose sum is divisible by `k`. Empty / none → `0`.

## Input
```
N
<x1> <x2> …
K
```

## Output
A single integer: the length.

## Constraints
N ≤ 10^5. Units are ints (may be negative). k is a positive int.
