# q38 Feature Flags — report

## Summary
"User Feature System": decide `is_enabled(flag, user)` from a flag definition that combines a
kill switch, allow/deny lists, attribute targeting, a deterministic percentage rollout and
dependencies on other flags. The interview content is the *evaluation order* and determinism of
the bucket, not data structures.

## Sources & confidence
medium — adonais0's 2021 phone-screen write-up gives the concrete rules (location-restricted
features; A/B features only for even user IDs); InterviewDB and a 1point3acres prep list confirm
the title "User Feature System" is still asked (2026) without content. Parts 2 and 4 and the
option mini-language are reconstructions; the even-ID rule is kept as `ab=even`.

## Approach by part
1. `Flag` NamedTuple; `off` → OFF for everyone (beats allow); `deny` → OFF; `allow` → ON.
2. `bucket = zlib.crc32(f"{flag}:{user}") % 100`, ON iff `bucket < rollout` (strict: 0 = nobody,
   100 = everyone); the flag name is part of the hash so buckets differ per flag.
3. rules dict `key -> accepted values`: AND across keys, OR within; missing attribute fails;
   `ab=even` checks the digits of the id.
4. `requires`: recursive `is_enabled` with a `seen` frozenset (cycle → OFF), checked before
   deny/allow so an allowlisted user still needs the prerequisite.

## Pitfalls hidden tests target
- allowlist is a bypass, not an audience (`vip,carol` → ON); `off` and `deny` beat `allow`
- rollout boundary: bucket 54 OFF at `rollout=54`, ON at 55; per-flag buckets
- missing attribute; OR-within/AND-across; `ab=even` for ids without digits
- dependency chain, missing required flag, self/2-cycle; re-declared flag replaces options

## Complexity & measured cost
O(depth of `requires`) per check. Measured: 0.41s, 38 MB (10k users, 10-deep chain,
100k checks; budget 2 s / 256 MB).

## Test inventory
16 tests — part1: 3 · part2: 6 (incl. 1 io) · part3: 4 · part4: 3 (incl. 1 perf); edge 8 · fmt 0.

## Skills exercised
S02 parsing · S03 domain modeling · S05 threshold semantics · S11 determinism · S18 validation/error paths · S19 incremental design
