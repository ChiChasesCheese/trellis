---
nodes: [python.stdlib, input.structured]
url: https://docs.python.org/3/library/json.html
tags: [docs]
---
# json — JSON encoder and decoder

Short page, three things to take from it. `json.loads` on a line at a time is
the whole of JSON-lines parsing. `sort_keys=True` and explicit `separators=`
are what make serialized output deterministic and byte-comparable. And the
conversion tables tell you what round-trips and what does not — a tuple comes
back as a list, an integer key comes back as a string, which is a quiet source
of key-lookup misses.

**Extract on read:**
- `loads` / `dumps` with `sort_keys=True` and `separators=(",", ":")` for
  deterministic, compact output ([[cc-verification-determinism-repeatable-runs]]).
- The decode conversion table: object to `dict`, array to `list`, integer keys
  become strings.
- `object_pairs_hook` when duplicate keys in the input must not silently collapse.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/json.html)

## Archived copy
![[python-json-clip]]
%% trellis:end %%
