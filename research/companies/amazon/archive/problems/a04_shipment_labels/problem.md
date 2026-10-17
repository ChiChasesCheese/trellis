> **Reconstruction.** Shape reported as "reorder letter vs digit shipment logs." Not a LeetCode statement. Wording is ours.

# a04 · Shipment labels

**Type:** Amazon OA coding · **Clock:** one of two problems in 70–90 min
**Family:** parsing · **Confidence:** medium (wording) / high (family)

Each log is `id` plus a payload. A **letter log** has a payload of words that are all letters. A **digit log** has a payload of words that are all digits.

Output letter logs first, sorted by payload, then by `id`. Digit logs keep **input order** and follow the letter logs.

## Input
```
N
<id> <word> <word> …
```

## Output
N lines, reordered.

## Constraints
N ≤ 10^4. Ids and words are non-empty tokens. Payload is never empty. A log is either all-letter or all-digit after the id.
