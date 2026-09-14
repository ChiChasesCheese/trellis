---
nodes: [rules.money, rules.fees]
url: https://martinfowler.com/eaaCatalog/money.html
tags: [canonical]
---
# Money (Patterns of Enterprise Application Architecture)

The catalogue entry that names the pattern: money is an amount plus a currency,
represented as an integer in the smallest unit, wrapped in a type that refuses
to add dollars to euros. Short, but it contains the one operation people
implement wrong — allocation. Splitting 100 cents three ways must produce 34,
33, 33 and never 33.33 three times, and the entry gives the algorithm that
distributes the remainder deterministically.

**Extract on read:**
- Amount as a whole number of minor units, with the currency carried alongside it.
- `allocate` — splitting so the parts sum back to the total exactly, with the
  remainder assigned by a stated rule ([[cc-verification-invariant-conservation]]).
- Why arithmetic on money belongs behind a type rather than scattered through
  the rules.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/eaaCatalog/money.html)
%% trellis:end %%
