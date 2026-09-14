---
nodes: [rules.money, output.formatting]
url: https://docs.stripe.com/currencies#zero-decimal
tags: [docs]
---
# Zero-decimal currencies (Stripe docs)

A short reference with an outsized effect on how you model money. Amounts are
integers in the currency's smallest unit — but JPY, KRW and about two dozen
others have no minor unit at all, so "divide by 100 to display" is wrong for
them, and three-decimal currencies exist too. Reading the list once is what
stops you from hard-coding a factor of 100 into a formatter and then discovering
it in the one hidden test that uses yen.

**Extract on read:**
- Amounts as integer minor units, always — never a float, in any currency.
- The zero-decimal list, and the special-cased three-decimal currencies.
- Why the display factor belongs in one table keyed by currency, next to the
  single formatting function ([[cc-python-io-exact-stdout]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.stripe.com/currencies#zero-decimal)

## Archived copy
![[stripe-zero-decimal-currencies-clip]]
%% trellis:end %%
