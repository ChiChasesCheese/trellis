---
id: cc-rules-round-once-at-the-edge
node: rules.rounding
type: qa
---
## Q
A hundred rows each attract a 2.1% fee and the output is the total. Round per row, or round the total?

## A
**Whatever the statement says — and the two answers differ, so the sentence has to be found rather than assumed.**

Per row is the norm when each row is itself billable (an invoice line, a per-transaction fee that a merchant sees) — a hundred roundings, each up to half a cent, and the total is whatever they sum to. Rounding once at the end is the norm when the total is the billed quantity and rows are just inputs.

The tell is where the money is *charged*. If you must guess, follow the granularity of the output: a per-row output implies per-row rounding, and a single total implies rounding once.

## Q zh
一百行各自产生 2.1% 的手续费，输出是总额。按行取整，还是对总额取整？

## A zh
**按题面说的做 —— 而两种答案不同，所以那句话必须找出来，而不是假设。**

当每一行本身就是可计费单位时（发票行、商户能看到的每笔交易手续费），按行取整是常态 —— 一百次取整、每次最多半分，总额就是它们的和。当总额才是被计费的量、各行只是输入时，最后取整一次是常态。

线索在于钱是在哪一层被**收取**的。如果必须猜，就跟随输出的粒度：按行输出意味着按行取整，单一总额意味着只取整一次。
