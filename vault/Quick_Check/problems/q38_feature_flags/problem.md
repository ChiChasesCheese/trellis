# q38 · Feature Flags — allowlists, percentage rollout, attribute rules, dependencies

**Type:** phone screen (live coding, ~35 min) · **Stage:** Stripe phone interview ("User Feature System") · **Last asked:** 2026 (InterviewDB / 1point3acres phone titles); 2021-06 (adonais0 write-up with content)
**Frequency:** 3 sources (adonais0 write-up with rules; InterviewDB phone-screen title "User Feature System"; 1point3acres 1025478 prep list "User Feature") · **Confidence:** medium

## Context
Stripe ships dashboard features behind flags: a feature can be limited to some countries or
plans, rolled out to a percentage of users, force-enabled for internal testers, and may depend on
another feature being on. The dashboard asks one question per feature per user:
`is_enabled(flag, user)`. The answer must be **deterministic** (the same user always lands in
the same rollout bucket) and cheap.

## Input (stdin)
Commands, one per line, processed in order (one accumulating program; no `PART` line):
```
FLAG,<name>,<on|off>[,<option>]...     options (any order, each at most once):
    allow=<id>|<id>...   deny=<id>|...   rollout=<0..100>   requires=<flag>|<flag>...
    country=<C>|<C>...   plan=<p>|<p>...   ab=even
USER,<id>[,<key>=<value>]...            e.g. USER,u1,country=US,plan=pro
CHECK,<flag>,<user>
```
Re-declaring a `FLAG` or `USER` replaces it. A `CHECK` for an unknown user treats the user as
having no attributes.

## Output
One line per `CHECK`: `<flag>,<user>,ON|OFF`.

## Rules — evaluated in this order, first decisive step wins
### Part 1 — boolean flags, allowlist, denylist
1. unknown flag → `OFF`; `off` → `OFF` for everyone (kill switch, beats the allowlist).
2. user in `deny` → `OFF`. 3. user in `allow` → `ON` (skips Parts 2–3, **not** Part 4).

### Part 2 — percentage rollout
`bucket = zlib.crc32(f"{flag}:{user}".encode()) % 100`; the user is in the rollout iff
`bucket < rollout` (`rollout=100` → everyone, `0` → nobody; default 100). The bucket depends on
the flag name too, so different flags roll out to different users. Evaluated after Part 3's
attribute rules (a user outside the target segment is `OFF` regardless of bucket).

### Part 3 — attribute rules
`country=US|CA` and `plan=pro|enterprise` are **AND**ed across keys, **OR**ed within a key. A user
missing the attribute fails the rule. Variant (source): `ab=even` enables the feature only for
users whose numeric id (digits of the id) is even — exposed as an ordinary rule key.

### Part 4 — dependencies
`requires=a|b`: every required flag must itself be `ON` for the same user (recursively, with all
of its own rules). A missing required flag, or a dependency cycle, → `OFF`. Dependencies are
checked **after** the kill switch and before the deny/allow lists, so even allowlisted users
cannot use a feature whose prerequisite is off for them.

## Worked examples
Buckets used below (`crc32("newui:<user>") % 100`): alice 13, bob 43, carol 5, dave 98, u1 54.
```
FLAG,dark,on
FLAG,killed,off,allow=alice
FLAG,vip,on,allow=alice|bob,deny=bob
CHECK,dark,alice            -> dark,alice,ON
CHECK,killed,alice          -> killed,alice,OFF
CHECK,vip,alice             -> vip,alice,ON
CHECK,vip,bob               -> vip,bob,OFF
CHECK,vip,carol             -> vip,carol,ON       (an allowlist is a bypass, not a filter)
CHECK,nope,alice            -> nope,alice,OFF
```
```
FLAG,newui,on,rollout=50
CHECK,newui,alice -> ON   CHECK,newui,bob -> ON   CHECK,newui,carol -> ON   CHECK,newui,dave -> OFF
```
```
USER,alice,country=US,plan=pro
USER,bob,country=DE,plan=pro
USER,carol,country=US
FLAG,tax,on,country=US|CA,plan=pro|enterprise
CHECK,tax,alice             -> tax,alice,ON
CHECK,tax,bob               -> tax,bob,OFF        (country)
CHECK,tax,carol             -> tax,carol,OFF      (no plan attribute)
FLAG,ab,on,ab=even
CHECK,ab,u2 -> ON   CHECK,ab,u3 -> OFF
```
```
FLAG,base,on,country=US
FLAG,addon,on,requires=base,allow=bob
USER,alice,country=US
USER,bob,country=DE
CHECK,addon,alice           -> addon,alice,ON
CHECK,addon,bob             -> addon,bob,OFF      (allowlisted, but base is OFF for bob)
FLAG,x,on,requires=y
FLAG,y,on,requires=x
CHECK,x,alice               -> x,alice,OFF        (cycle)
```

## Edge cases hidden tests are known to target
- allowlist present but user not on it → **not** automatically OFF: Parts 2–3 still decide
  (`vip,carol` → ON because `vip` has no other rule)
- rollout boundary: bucket 54 is OFF at `rollout=54`, ON at `rollout=55`; `rollout=0` / `100`
- `off` beats `allow`; `deny` beats `allow`
- attribute missing on the user; OR within key / AND across keys
- `requires` chain of three; missing required flag; two-flag cycle; allowlisted user with failing prerequisite
- unknown user on CHECK; re-declared flag replaces the old options

## Variants seen in the wild
- adonais0 (2021): features limited to a location apply only to users in that location; A/B
  features apply only to users with **even IDs** → `ab=even` here.
- Some phrasings treat an allowlist as the *only* audience (users not listed are OFF). This repo
  treats it as a bypass (testers see the feature early); the kill switch / attributes / rollout
  decide for everyone else. Under the "audience" reading `vip,carol` would be OFF.

## What this tests
skills: S02 parsing · S03 domain modeling · S05 threshold semantics · S11 determinism/idempotency (stable hash buckets) · S18 validation/error paths · S19 incremental design

## Sources
- https://adonais0.github.io/20210603/interview-stripe/ (phone screen write-up, 2021-06-03: location restrictions + A/B even-ID rule)
- https://www.1point3acres.com/bbs/thread-1025478-1-1.html (电面 prep list: "User Feature")
- InterviewDB phone-screen title "User Feature System" (title only; see catalog/raw/en_forums.md §B)
