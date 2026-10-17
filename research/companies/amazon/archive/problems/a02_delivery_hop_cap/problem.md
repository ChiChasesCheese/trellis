> **Reconstruction.** Shape reported as "cheapest route with a hop cap" in Amazon OA write-ups. Not a LeetCode statement. Wording is ours.

# a02 · Delivery hop cap

**Type:** Amazon OA coding · **Clock:** one of two problems in 70–90 min
**Family:** graph · **Confidence:** medium (wording) / high (family)

Fulfillment centers are connected by directed legs with a positive cost. Given `src`, `dst`, and hop cap `k`, return the cheapest path that uses **at most `k` edges**. No path → `-1`. A center to itself with `k ≥ 0` costs `0`.

## Input
```
C
<cid>
…
E
<from> <to> <cost>
…
Q
<src> <dst> <k>
```

`C` center ids, `E` directed legs, then one query.

## Output
A single integer: cheapest cost, or `-1`.

## Constraints
C ≤ 200, E ≤ 2000, k ≤ C. Costs fit in 32-bit ints.
