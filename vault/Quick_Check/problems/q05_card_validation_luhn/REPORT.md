# q05 Payment Card Validation — report

## Summary
Luhn checksum + network detection (VISA / MASTERCARD / AMEX by length and prefix), then two
"real-world" twists: count the valid completions of a redacted card (`*` digits) and recover all
valid originals of a card with exactly one typo (digit change or adjacent swap). Stripe asks it
because it is domain-literate string work (BIN, check digit) plus a small combinatorics step,
with byte-exact output and an order-of-checks trap (shape before checksum).

## Sources & confidence
high — femisowems/stripe-interview-questions question6 (verbatim statement + sample_input /
expected_output, reproduced byte-for-byte by the io test), linkjob 2025-09 and extrabrain
2026-02 (identical 4-part spec with test-case ranges), Blind gdmiywlu 2025-08, 1point3acres
677770/677836, 1024bbs. Conflict resolved: the brief/cn retellings write Part 3 as
`NETWORK: count`; the repo's expected_output uses `NETWORK,count` — the verbatim form wins.
Both stdin protocols (`PART n` + one card per line; HackerRank `Q` + `Pk card`) are supported.

## Approach by part
1. `luhn_ok`: walk from the right, double odd indices, −9 if > 9, sum % 10 == 0.
2. `classify`: `network_of` (length + per-position prefix digit sets) first → `UNKNOWN_NETWORK`;
   then Luhn → `INVALID_CHECKSUM`; else the name.
3. `count_completions`: DP over positions with state = running Luhn sum mod 10; masked positions
   branch over the allowed digits (prefix positions restricted to the network's digit set:
   AMEX `3`,`47`; MC `5`,`12345`; VISA `4`). O(16·10·10) per network, independent of the number
   of `*`. Verified against an independent brute-force oracle on 200 random masks + a 5-star case.
4. `recover`: generate 9·L digit changes + ≤ L−1 adjacent swaps (skip equal digits), drop the
   observed card, keep `network_of` ∧ `luhn_ok`, sort (same length → string order = numeric).

## Pitfalls hidden tests target
- checksum checked before shape (Luhn-valid `2223…`/`6011…` must be `UNKNOWN_NETWORK`)
- MC `50`/`56`, AMEX `35`, 15-digit `4…`, 13/17-digit inputs; masked prefix digits
- Part 3 zero counts printed, wrong alphabetical order, brute force on 5 stars timing out
- Part 4 duplicates (change vs swap coincide), listing the observed card, identity swaps of equal
  digits, originals on a different network than the observed prefix, non-numeric ordering

## Complexity & measured cost
P1/P2 O(L); P3 O(L·100) per network; P4 O(L·10·L). 1 500 five-star P3 + 1 500 P4 queries:
0.46 s, 18 MB RSS (budget 2 s / 256 MB).
Measured: 0.46s, 18 MB

## Test inventory
21 tests — part1: 4 · part2: 4 · part3: 5 · part4: 8 (incl. io ×3, perf ×1 across parts); edge 11 · fmt 2 · io 3 · perf 1.
`IMPL=starter`: 18 fail / 3 pass (the three that expect empty output; the DP-vs-brute test now uses
an independent oracle in the test, so the empty template fails it).

## Skills exercised
S02 parsing (two protocols) · S05 order of checks · S08 numeric sort · S09 exact format ·
S14 Luhn digit walking + wildcard expansion · S15 masked-input combinatorics (mod-10 DP) and
single-edit enumeration · S19 incremental design (P1 ⊂ P2 ⊂ P3/P4 share `network_of`/`luhn_ok`)
