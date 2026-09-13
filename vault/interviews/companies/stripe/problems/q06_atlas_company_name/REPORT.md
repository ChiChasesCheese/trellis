# q06 Atlas Company Name Availability — report

## Summary
Delaware-style "distinguishable name" check for Stripe Atlas: canonicalize a company name
(case, `&`/`,`, entity suffixes, leading article, inner `And`), compare against a registry, then
make the registry persistent and add owner-only `RECLAIM`. Stripe asks it because it is a
string-canonicalization pipeline with an order-sensitive rule list plus a tiny stateful
registry — cheap to specify, easy to get subtly wrong (`And` first vs inner, `The Inc.` → empty,
reclaim by the wrong account).

## Sources & confidence
high — femisowems/stripe-interview-questions question1 (verbatim statement + 12-line sample and
expected output, reproduced byte-for-byte by the io test), linkjob 2025-09, extrabrain 2026-02,
Blind ijfwtgl0, programhelp (low-confidence variant, not implemented).
Reconstructed: the stdin section protocol (`REGISTERED` / `REQUESTS` blocks, `PART n`); the
"other punctuation → space" step (brief) — sources only name `&` and `,`, so it is a flag
`normalize(name, strip_punctuation=True)` applied *after* suffix stripping so `L.L.C.` still
matches. Conflict resolved: the repo's Part 1 text already says "register it immediately" —
Part 1 here is the stateless check (the distinct part-1 rule of linkjob/extrabrain) with
`part1(lines, persist=True)` giving the repo behaviour; Part 2 is the persistent registry.

## Approach by part
1. `normalize`: lower → `&`,`,` → space → split → pop trailing suffix tokens while present →
   drop one leading article → drop `and` unless index 0 → punctuation → space → join. Empty → Not
   Available. `part1` checks each request against the normalized `REGISTERED` block only.
2. `run(persist=True)`: registry `dict[normalized] -> account`; accepted names are stored, and any
   later hit (same account included) is Not Available; rejected requests store nothing.
3. `run(reclaim=True)`: `RECLAIM,acct,name` splits on the first two commas; delete only when
   `registry.get(key) == acct`; block names (registrant `None`) and unknown names are ignored.

## Pitfalls hidden tests target
- treating `Inc.`/`The`/`&` alone as available (empty normalized form); registering an empty key
- stripping only one suffix; stripping suffix words in the middle; shredding `L.L.C.` before
  matching it; dropping a leading `And`; article removed after `and` handling
- same-account re-request expected to be available (it is not); reclaim by non-registrant;
  reclaim matched on raw spelling instead of normalized form; printing something for `RECLAIM`
- names with commas inside `RECLAIM,…`; whitespace around `account_id`

## Complexity & measured cost
O(total characters); dict lookups per request. 100 000 requests (10 % reclaims, 500 accounts):
0.16 s, 49 MB RSS (budget 2 s / 256 MB).
Measured: 0.16s, 49 MB

## Test inventory
34 tests — part1: 22 (17 parametrized normalize cases) · part2: 5 · part3: 7 (incl. 1 io, 1 perf);
edge 10 · fmt 1 · io 1 · perf 1. `IMPL=starter`: 29 fail / 5 pass (empty-output cases).

## Skills exercised
S02 parsing (two record shapes, commas in names) · S03 registry keyed by canonical name ·
S09 exact `id|Name Available` format · S11 idempotent registration · S14 string canonicalization ·
S18 ignored/invalid requests · S19 incremental design (`run(persist, reclaim)`)
