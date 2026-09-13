# q38 · Feature Flags — allowlists, percentage rollout, attribute rules, dependencies

## Context
Stripe ships dashboard features behind flags: a feature can be limited to some countries or
plans, rolled out to a percentage of users, force-enabled for internal testers, and may depend on
another feature being on. The dashboard asks one question per feature per user:
`is_enabled(flag, user)`. The answer must be **deterministic** (the same user always lands in
the same rollout bucket) and cheap.

## Input (stdin)
Commands, one per line, processed in order (one accumulating program; no `PART` line):
| 格式 | 说明 |
|---|---|
| `FLAG,<name>,<on\|off>[,<option>]...` | options (any order, each at most once): `allow=<id>\|<id>...`; `deny=<id>\|...`; `rollout=<0..100>`; `requires=<flag>\|<flag>...`; `country=<C>\|<C>\|...`; `plan=<p>\|<p>...`; `ab=even` |
| `USER,<id>[,<key>=<value>]...` | e.g. `USER,u1,country=US,plan=pro` |
| `CHECK,<flag>,<user>` | |
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

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s11-idempotency-dedup|S11 幂等 / 去重]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
