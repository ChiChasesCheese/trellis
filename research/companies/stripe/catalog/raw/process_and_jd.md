# Stripe engineering hiring: what the process actually tests

Research date: 2026-08-25. Scope: the 60-minute language-agnostic multi-part HackerRank
"bespoke challenge", the rest of the Stripe SWE loop, 2025-2026 JD requirements, and the
Stripe product semantics most likely to appear inside OA prompts.

Confidence key: [S] = Stripe-official source (stripe.com / docs.stripe.com / support.stripe.com);
[C] = multiple independent candidate reports agree; [1] = single candidate/prep-site report.
Stripe's official "Candidate FAQ" / "candidate-info" pages returned 404 at fetch time, so OA-format
facts below are triangulated from candidate reports rather than an official Stripe page.

---

## (A) OA format facts (HackerRank "bespoke challenge")

| Fact | Detail | Confidence / source |
|---|---|---|
| Platform | HackerRank; recruiter emails a link ~4-5 days after applying | [C] Blind `stripe-hackerrank-rrt4pa6q`; interviewfox |
| Time | 60 minutes hard limit (some report ~45 min of real coding after setup + a short end survey question) | [C] Blind, interviewfox, programhelp, linkjob |
| Shape | ONE problem, split into 3-5 progressive parts (most reports: 3 or 4; intern/new-grad 2026: 5) | [C] interviewfox, linkjob, extrabrain, programhelp, Blind |
| Unlocking | Later parts appear only after the previous part's tests pass ("you have to solve Part 1 to unlock Part 2") | [C] interviewfox; linkjob ("each one based on what I had done in the previous part") |
| Parts build on each other | Each new part adds requirements to the same program/state; "bugs compound" | [C] Blind `how-are-you-guys-cracking-stripe-oa`; Blind `what-does-stripe-hackerrank-test-have` |
| Scoring | No numeric score shown; graded by test cases passed per part. Reported totals: 14/20, 18/20, 22/25, 6/14, 11/14, 13/19, 16/17, ~17 cases total incl. hidden | [C] interviewfox, Blind x2, programhelp |
| Pass bar | Unknown/undisclosed. 22/25 and 18/20 advanced; 14/20 poster expected rejection. Partial credit can advance | [C] |
| Hidden tests | Yes: visible sample cases + hidden cases; "approximately 17 (including multiple hidden cases)" | [C] programhelp; lodely |
| I/O model | Predominantly stdin parsing / string-formatted input lines (e.g. `CHARGE,charge_id,account_id,amount,code`, `account_id|proposed_name`) and exact-format stdout; some variants give a function stub. Output format errors (spacing, commas, ordering) cause test failures | [C] extrabrain problem set; oavoservice; programhelp |
| Question style | NOT LeetCode: "input parsing, creating classes, using proper data structures, and implementing business logic (which won't be algorithmically heavy)"; "real world production scenarios"; descriptions are long and take time to read | [C] Blind (Stripe employee +1'd), interviewfox, linkjob |
| Domain | Payments, fraud/disputes, billing/subscriptions, identity, card validation, company-name registry, ops data | [C] |
| Languages | Candidate's choice (HackerRank list; Python/Java/C++ explicitly reported). Stripe employees on Blind repeatedly advise against Java for speed ("Do not use Java, full stop" for the phone screen); no extra time for verbose languages | [C] Blind `stripe-phone-screen-march-2025`; programhelp |
| IDE | Browser IDE only; print-debugging, no breakpoints. Blind advice: "should use ide cause you are optimizing for speed" (i.e. write in your own editor and paste, if allowed). Whether external IDE is permitted is unresolved in threads; HackerRank logs tab/window focus loss | [C] interviewfox; Blind |
| Proctoring | HackerRank logs window/tab activity; webcam rarely on. HackerRank AI-plagiarism model uses tab-switch timeline, external paste, "suspicious code resetting", typing cadence; candidates must consent when AI detection is enabled; a single brief tab-out is below the flag threshold, a pattern is not | [S-HackerRank] hackerrank.com/blog plagiarism; support.hackerrank.com AI plagiarism; interviewfox proctoring |
| AI use | "AI use in Stripe interviews is strictly prohibited" (applies to the loop; treat the OA the same) | [S via interviewing.io] |
| Reapply cooldown | 12 months after a failed OA (reported) | [1] interviewfox; Blind |
| Question bank | Stripe reuses a small bank; the same problems recur (fraud/MCC, card validation, Atlas names, closing time, subscription emails, BIN ranges, merchant scoring) | [C] linkjob, extrabrain, interviewdb.io |

Reported OA problems (titles as circulated, each multi-part):
1. Merchant fraud detection by MCC (count threshold -> ratio threshold -> DISPUTE events reclassify -> dispute reversals -> edge cases: double disputes, zero-volume merchants). Output: lexicographically sorted account IDs. [C] extrabrain, interviewfox, leetcode-discuss intern OA.
2. Merchant fraud SCORING (base score; amount-multiplier rules with strict `>`; additive rule when customer has >=3 txns with merchant applied once per group; same-hour penalty by hour band 12-17 add / 9-11 & 18-21 subtract, times count). Output `merchant,score` sorted by name. [C] oavoservice, programhelp.
3. Stripe payment card validation (VISA 16 digits starting 4; MASTERCARD 16 starting 51-55; AMEX 15 starting 34/37; Luhn; redacted `*` digits -> count possibilities; corrupted `?` -> one digit changed or adjacent swap; sorted output). [C] extrabrain, linkjob.
4. Atlas company-name availability (normalize: case-insensitive, `&`/commas -> spaces, strip suffixes Inc./LLC/Corp, drop leading articles; then persistent registry; then RECLAIM by original registrant). [C] extrabrain, linkjob.
5. Card range obfuscation (fill gaps in BIN intervals over 0000000000-9999999999 offsets, inclusive endpoints, output zero-padded 16-digit numbers, sorted). [C] extrabrain.
6. Store closing-time penalty (Y/N hourly log; penalty = open hours with N + closed hours with Y; pick min penalty, smallest time on tie; then parse many logs between BEGIN/END, nested invalid). [C] extrabrain, codinginterview, pkafel gist.
7. Subscription notification scheduler (welcome on start, warning at -15 days, expiry on end; then plan changes; then renewals; chronological output with deterministic tie-break, `[Changed]`/`[Renewed]` tags). [C] extrabrain, linkjob.
8. Others listed on interviewdb.io as OA: Chat Billing, Collusion, Deployment, Join Dataset, Observability, Proximity Request Routing, Request Router, Stripepay Backend; prep sites also cite sliding-window rate limiter ("3 requests per 10 s"), credit/debit ledger balances from `{user_id} {event} {amount}` logs, email normalization (dots/plus-addressing), currency-conversion payouts. [1 each] interviewdb.io, programhelp.

Candidate-derived rubric hints for the OA: read the entire spec before typing ("biggest mistake was panic-implementing Part 1 then refactoring"); lock each part with edge cases before moving on ("checkpoint approach"); bank passing tests early; write modular code from the start so later parts extend rather than rewrite; use strict vs non-strict comparisons exactly as worded; match output format byte-for-byte. [C] Blind, interviewfox, oavoservice.

---

## (B) Full interview loop, round by round

Sources: interviewing.io Stripe guide (includes Stripe-employee input), Exponent, techinterview.org, IGotAnOffer, Blind threads, linkjob 8-round report, Medium 2025-26 report. New-grad/intern loops are leaner (often coding + integration + bug bash + HM, no standalone system design).

| Stage | Duration | Format | What is evaluated | Rules / notes |
|---|---|---|---|---|
| 0. Online assessment (some roles/regions; standard for university recruiting) | 60 min | HackerRank, 1 problem x 3-5 parts | Correctness on hidden tests per part; ability to finish under time; exact I/O formatting | See (A) |
| 1. Recruiter screen | 30 min | Call | Background, motivation, role fit, logistics; Stripe operating principles | Don't disclose comp/other-company progress (interviewing.io) |
| 2. Technical phone/"team" screen | 45-60 min | Live coding, own IDE + screen share or CoderPad/HackerRank pair mode; one multi-part practical problem (typically 3 parts, "3-4 problems linked to each other") | Extracting requirements from a dense prompt; clean, readable, correct code; testing instinct (run your code, add cases); communication; finishing. "Most failing candidates fail because they couldn't finish"; "time and space complexity carry little weight as long as correct and clear" | Language-agnostic ("questions play-tested per language"); boilerplate pre-written is fine; no extra time for verbose languages; interviewer answers clarifying questions. Reported problems: shipping cost calc (3 parts; corner cases = missing dict keys, invalid numbers, lambda sorts), user dedup by weighted similarity -> 1-hop -> transitive, currency conversion, transaction fee, card parsing, header (Accept-Language) parsing, merging transactions, payment invoices, user roles, wishlist, factory cost, shipping route |
| 3. Second recruiter call | 30 min | Prep call for onsite | n/a | |
| 4a. Onsite: General coding | 45-60 min | Same style as screen, more parts (e.g. AccountScheduler: is_available -> acquire(lock) -> LRU auto-select; subscription email schedule 3 parts) | Production-quality code "they'd approve in code review"; edge cases enumerated before coding; error handling; readability/testability; hash maps, parsing, strings, arrays dominate | Use most fluent language + editor; libraries allowed |
| 4b. Onsite: Bug Bash / debugging | 45-60 min | Unfamiliar real OSS repo (reported: SnakeYAML, Mako, others) with failing tests / GitHub issue; "generic version of a real Stripe bug"; 5-7 planted bugs in ~200 lines in some variants | Methodology: reproduce -> hypothesize -> small change -> re-test; narrate; a clear diagnosis often beats an incomplete fix; comfort with debugger/tooling in your language | Own IDE encouraged; Googling allowed |
| 4c. Onsite: Integration | 45-60 min | Private repo + API docs; stacked tasks: parse a file of requests, make HTTP calls, handle malformed responses/errors, persist results (reported: "Bikemap" ride JSON -> REST API -> render map; "read a file of request data, POST each, print responses"); ~30-40 min of coding after setup | Reading unfamiliar code/docs fast, following instructions precisely, HTTP/JSON handling, error handling, running early ("writing a lot before running anything" is the failure mode) | Googling allowed and encouraged; skipped for Infrastructure-org candidates |
| 4d. Onsite: System / API design | 45-60 min | Design a service + its API (ledger service, metrics counter, rate limiter, webhook system, subscriptions model, payments flow) | API as a product: idempotency, retries/duplicate requests, network failure mid-call, versioning, error model, data model that "holds up over time"; reliability/exactly-once/reconciliation; "correctness when things fail" | Often called the offer-deciding round for mid/senior; usually omitted for new grad |
| 4e. Onsite: Behavioral / HM | 45 min | Past-experience questions against Stripe operating principles (users first, ownership, rigor, written communication, transparency) | Concrete outcomes, ownership, disagreement handling, written clarity (Stripe is doc-heavy) | STAR |
| 4f. (Staff+) Presentation | 60 min | Past project with business context | | |
| Decision | Panel consensus; HM breaks ties | | | ~4-8 weeks end to end; down-leveling common |

Cross-round themes stated by multiple sources: "think out loud - silence is penalized"; "correctness and readability outrank optimization at every stage"; "treat the interviewer as a resource"; "read thoroughly before coding - prompts hide tasks in dense descriptions".

---

## (C) JD skill extraction (2025-2026 Stripe SWE listings)

JDs read: Software Engineer, Payments (7529787); Software Engineer, New Grad (57800855 / 7991718); Backend Engineer/API, Payments and Risk (4921361); Software Engineer (generalist, South SF, 73804609); Backend Engineer, Billing (7224418 / 5932585); Full Stack Engineer, Optimized Checkout & Link (38300794); Software Engineer, Backend / Money Movement (4205822); Staff SWE, Issuing (7369269); Software Engineer, Internal Systems (7543868). Several stripe.com listing URLs 404 (rotated); aggregator mirrors used where noted.

Frequency = number of the 9 JDs containing the requirement (approximate, from extracted text).

- Design/build/maintain APIs, services and systems; "own and solve problems end-to-end" - 9/9 (boilerplate in every Stripe SWE JD)
- Debug production issues "across services and several levels of the stack" - 7/9
- Collaborate cross-functionally (PM, design, other eng teams, global offices); strong written/verbal communication, empathy - 9/9
- "Strong coding skills in any programming language" / language-agnostic; Stripe stack named as Java, Ruby, JavaScript, Scala, Go (new grad), Ruby/Java/Go (generalist), Python/Java/Go (generalist minimums) - 6/9
- Large-scale distributed backend systems, reliability, scalability, low latency - 6/9
- Raise engineering standards: code review, testing, safe deploys, tooling, "high code quality standards" - 6/9
- Navigate ambiguity, clarify ownership, self-directed/entrepreneurial - 6/9
- Experience with large-scale financial tracking systems / financial products (preferred) - 4/9
- API design taste: "expressive yet simple", "simple abstractions that hide complexity", developer experience - 4/9
- Cloud/infra: AWS (S3/EC2/EBS), gRPC, GraphQL, Docker, Kubernetes (preferred) - 3/9
- Data stores: MongoDB, MySQL, Redshift/Presto/Trino (Internal Systems) - 1/9
- Real-time transaction processing: authorizations, clearing, settlement, ledgering (Issuing) - 1/9
- Card networks, BIN sponsorship, issuer integrations, KYC/KYB, audit trails (Issuing) - 1/9
- Pricing models, SaaS subscriptions, usage-based billing, recurring + one-time payments (Billing) - 2/9
- Hosted UIs / checkout flows / payment methods / merchants / experiment analysis (OCL) - 1/9
- New-grad specifics: degree by summer 2026, <=18 months experience, "some experience with programming", ability to "independently research unfamiliar systems", read large codebases, code review + safe production deploy familiarity (preferred)

Domain vocabulary that recurs across JDs and Stripe's own docs (use these words in the OA/interviews): payments, charges, PaymentIntent, refunds, disputes/chargebacks, payouts, balances (pending/available), balance transactions, ledger / double-entry, idempotency keys, webhooks/events, subscriptions, invoices, prices/products, metered/usage-based billing, tiers (graduated/volume), proration, billing cycle anchor, card networks, issuer/acquirer, BIN, Luhn, MCC (merchant category code), Radar rules / risk level / velocity, reconciliation, settlement (T+N), currency / ISO 4217 / minor units / zero-decimal, rate limits (429, token bucket), Connect (platform / connected accounts / transfers / application fees), Atlas (Delaware C-corp/LLC naming).

---

## (D) Stripe domain glossary relevant to OA problems (with doc links)

**Money representation.** All API `amount`s are integers in the currency's minor unit (`1000` = 10.00 USD; `10` = 10 JPY). Zero-decimal currencies (JPY, KRW, etc.) need no scaling. Special cases: ISK and UGX are zero-decimal but must be sent as two-decimal with `00`; HUF and TWD can be charged in two decimals but payouts must be divisible by 100; Stripe rounds fractional UGX invoice totals to nearest 100 and books the difference to customer balance. Currency codes are lowercase ISO 4217. Minimum charge 0.50 USD-equivalent; max 12 digits (9 for Amex). https://docs.stripe.com/currencies

**Tiered pricing.** `tiers_mode=volume`: whole quantity billed at the unit price of the tier the total falls in (5 -> 5x7=35; 6 -> 6x6.5=39). `tiers_mode=graduated`: each tier's slice priced separately and summed (6 -> 5x7 + 1x6.5 = 41.5; 20 -> 127.5). Tiers have `up_to` (last tier `inf`), optional `unit_amount` and/or `flat_amount`; flat amounts add per applicable tier (graduated, qty 12 with the doc's flat table -> 111 USD; volume -> 12x3+30 = 66). Quantity 0 still bills the first tier's flat amount. https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing and https://docs.stripe.com/products-prices/pricing-models

**Usage-based / metered billing.** Meter events `{event_name, payload{stripe_customer_id, value}, identifier, timestamp}`; `identifier` is an idempotency key unique for a rolling >=24 h; `timestamp` must be within past 35 days or <=5 min future; aggregation (sum / count / last) at period end; usage-based charges are NOT prorated. https://docs.stripe.com/api/billing/meter-event/create ; https://docs.stripe.com/billing/subscriptions/usage-based

**Proration.** Default `proration_behavior=create_prorations` (invoice items, billed on next invoice); `always_invoice` bills immediately; `none` disables. Computed to the second by default: credit = unused time on old price, debit = remaining time on new price (10 -> 20 USD halfway through month: -5 + 10 = +5). Uses discounted price; proration lines are `discountable=false`. Triggers: price/quantity/item changes, trial_end, billing_cycle_anchor, cancel_at; not triggered by metadata, payment method, coupons alone. `billing_mode=flexible` credits based on last price actually billed. https://docs.stripe.com/billing/subscriptions/prorations

**Billing cycle / dates.** `billing_cycle_anchor` = UNIX seconds (UTC). Monthly sub anchored Jan 31 bills Feb 28/29, Mar 31, Apr 30 (clamp to month end). `billing_cycle_anchor_config[day_of_month=31]` = always last day. Trials set the anchor to `trial_end`. https://docs.stripe.com/billing/subscriptions/billing-cycle

**Subscription lifecycle.** Statuses: `incomplete` (23 h to pay first invoice) -> `active` | `incomplete_expired`; `trialing` -> `active`; failed renewal -> `past_due` -> (after smart retries) `canceled` | `unpaid` | stay `past_due`; `paused` (trial ended w/o payment method); `canceled` is terminal. Invoice statuses: draft, open, paid, void, uncollectible. Payment outcome mapping: succeeded/paid/active; card error -> requires_payment_method/open/incomplete; auth needed -> requires_action/open/incomplete. https://docs.stripe.com/billing/subscriptions/overview

**Idempotency keys.** Header `Idempotency-Key` on POST only; <=255 chars; V4 UUID recommended; Stripe stores first response (status + body, even 500s) and replays it for the same key; reusing a key with different params -> error; keys pruned after >=24 h; results saved only once endpoint execution begins (validation failures / concurrent conflicts are not saved, so retry is safe). https://docs.stripe.com/api/idempotent_requests

**Rate limits.** Global 100 req/s live, 25 req/s sandbox; most endpoints 25 req/s; Payouts create 15/s, 30 concurrent; Search 20 reads/s; Files 20/20. 429 with `Stripe-Rate-Limited-Reason` (global-rate, endpoint-rate, global-concurrency, endpoint-concurrency, resource-specific); `lock_timeout` 429 for object lock contention. Recommended client handling: exponential backoff with jitter; client-side token bucket. Read allocation: 500 reads per transaction over rolling 30 days, min 10k/month. https://docs.stripe.com/rate-limits

**Webhooks / events.** At-least-once delivery; retries with exponential backoff up to 3 days in live mode (3 retries over a few hours in sandbox); ordering NOT guaranteed; dedupe by `event.id` (and by `data.object.id` + `event.type` when two distinct events are generated); verify `Stripe-Signature` (HMAC-SHA256 over `t.payload`, 5-minute tolerance); return 2xx fast and process async. https://docs.stripe.com/webhooks

**Disputes / chargebacks.** Flow: (optional) early fraud warning -> (optional, Amex/Discover) inquiry (`warning_needs_response` -> `warning_under_review` -> `warning_closed` after 120 days) -> chargeback (`needs_response` -> `under_review` -> `won` | `lost`; rare `lost`->`won` "late win"). On dispute Stripe debits disputed amount + dispute fee from balance; funds held for the whole lifecycle (2-3 months); you cannot refund while a dispute is open; respond within ~7-21 days; issuer decides in 60-75 days; cardholder window generally 120 days from charge (or from event date). Disputed amount can differ from charge (FX drift, partial disputes, bundled recurring charges). Won -> amount returned (countered fee returned; received fee not). https://docs.stripe.com/disputes/how-disputes-work

**Refunds.** Multiple partial refunds allowed but total <= original charge; refunds only to original payment method; processing fees not returned; refund statuses pending / succeeded / failed / canceled / requires_action; refunds draw on available (not pending) balance; failed refund returns funds to balance as `refund_failure`/`adjustment`. https://docs.stripe.com/refunds

**Balances / payouts / balance transactions.** Balance states pending -> available at `available_on` (settlement T+2 business days US, 7 cal days initial then 3 business days most of EU/UK, ACH 4 bd, SEPA 6 bd). Payout schedules manual/daily/weekly/monthly; negative balance -> debit payout / top-up. Every money movement is a BalanceTransaction with `type` (charge, payment, refund, refund_failure, adjustment [disputes], payout, payout_failure, stripe_fee, transfer, application_fee, topup, currency_conversion, reserve_hold/release, issuing_*), `amount`, `fee`, `net`, `source`, `status`. https://docs.stripe.com/payouts ; https://docs.stripe.com/payments/balances ; https://docs.stripe.com/reports/balance-transaction-types

**Radar rules.** Syntax `{action} if {condition}`, condition = `[attribute] [operator] [value]`, e.g. `Block if :amount_in_usd: > 1000.00`, `Block if :card_country: != :ip_country:`, metadata `::key::`, lists `@list`. Actions evaluated in priority order: Request 3DS, then Allow, then Block, then Review; first match wins, same-type rules unordered. Operators: `= != < > <= >= IN INCLUDES LIKE`, boolean `AND/OR/NOT` (`&& || !`) with C-like precedence and parentheses. Missing attributes: any comparison is false (even `!=` and `NOT`), use `is_missing()`. Velocity attributes (`..._hourly/daily/weekly/yearly/all_time`) exclude the current payment and use bucketed windows (hourly up to 3900 s). `amount_in_xyz` auto-converts. https://docs.stripe.com/radar/rules/reference

**Cards: BIN / Luhn / networks.** BIN = first 6 (now 8) digits identifying network + issuer; last digit = Luhn check digit. Network detection used in the OA problem: Visa 16 digits starting `4`; Mastercard 16 digits starting `51-55` (real world also `2221-2720`); Amex 15 digits starting `34`/`37`; Discover 16 starting `6011`/`65`; Diners 14; UnionPay 16-19. Luhn: from the right, double every second digit, subtract 9 if >9, sum divisible by 10. Stripe test cards (all Luhn-valid): 4242424242424242, 5555555555554444, 2223003122003222, 378282246310005, 6011111111111117; 4242424242424241 is the canonical invalid-Luhn example. https://docs.stripe.com/testing ; https://docs.stripe.com/issuing/customize-your-program

**Atlas company names.** Delaware C-corp must end in "Inc." (Atlas default), LLC in "LLC"; name must be "distinguishable upon the records" of Delaware (small punctuation/spelling/order differences may not count: "Acme Corp." vs "Acme Corporation"); restricted words (bank, attorney, university) need approval; availability checked against the Delaware name database without the suffix. The OA variant adds: case-insensitive, `&`/commas as spaces, strip suffixes, drop leading articles. https://support.stripe.com/questions/choosing-a-name-for-your-stripe-atlas-company ; https://stripe.com/resources/more/is-your-company-name-available-in-delaware-here-is-how-to-find-out

**MCC.** ISO 18245 4-digit merchant category code attached to a merchant; Radar/Issuing use it for category-level controls; OA fraud problem keys thresholds by MCC.

**Connect vocabulary (for API-design rounds).** Platform vs connected account; direct / destination / separate charges-and-transfers; application_fee; transfer reversals; connected-account negative balance reserves. https://docs.stripe.com/connect

---

## (E) Test targets: what a 60-minute multi-part Stripe OA actually tests

Each bullet = skill; rationale; source.

1. **Reading a long, dense spec completely before coding** - later parts change requirements; candidates who "panic-implemented Part 1" had to refactor and ran out of time. [Blind cracking-stripe-oa; Exponent "prompts hide tasks in dense descriptions"]
2. **Line-oriented input parsing with delimiters (`,` `|` spaces), typed fields, and malformed/edge input** - every reported OA starts with parsing (`CHARGE,charge_id,account_id,amount,code`, `account_id|name`, Y/N logs, BEGIN/END blocks). [extrabrain; oavoservice; programhelp]
3. **Modeling the domain as small classes/records + dictionaries keyed by ID** - Blind (Stripe employee-confirmed): "creating classes, using proper data structures, business logic"; fraud state is "two counters per merchant". [Blind what-does-stripe-hackerrank-test-have; interviewfox]
4. **Grouping / aggregation (group by merchant, by customer-merchant, by customer-merchant-hour) and applying a rule once per group, not per row** - the #1 reported failure in the merchant-scoring problem was double-counting additive rules. [oavoservice; programhelp]
5. **Threshold semantics: strict vs non-strict comparisons, count vs ratio thresholds, minimum-volume gates** - explicit `>` vs `>=` errors flip hidden tests; fraud problem moves from count to fraction thresholds. [programhelp; extrabrain fraud part 2]
6. **Money arithmetic in integer minor units; no floats for currency; explicit rounding rule (half-up vs banker's) and formatting to 2 decimals / zero-decimal** - Stripe API semantics; proration and UGX rounding show Stripe rounds and books the remainder; output "consistent numeric formatting to avoid precision errors". [docs.stripe.com/currencies; prorations; programhelp]
7. **Percent / tiered computations (graduated vs volume, flat + unit)** - Billing team problems ("Chat Billing", "Payment Invoices", "Transaction Fee") map directly to Stripe tier math. [docs tiered-pricing; interviewdb.io titles]
8. **Deterministic sorting with explicit tie-breaks (lexicographic IDs, chronological then message-type order, smallest closing time on tie)** - almost every OA output is "sorted by X, ties by Y"; ordering mistakes fail tests. [extrabrain closing-time and scheduler; oavoservice]
9. **Exact output formatting (separators, padding, zero-padded 16-digit numbers, tags like `[Changed]`)** - "Output formatting errors (spacing, commas) causing HackerRank rejection". [oavoservice; extrabrain BIN problem]
10. **State machines / event streams processed in order with reversals (CHARGE -> DISPUTE -> dispute reversal; plan change -> renewal)** - parts 3-5 of the fraud problem and parts 2-3 of the scheduler; reversal bookkeeping was the last failing group for a 22/25 candidate. [interviewfox; extrabrain]
11. **Idempotency / de-duplication of repeated events (double disputes, duplicate IDs, retried requests)** - explicit OA edge case ("double disputes"); mirrors Stripe idempotency keys, meter-event identifiers, webhook event IDs. [interviewfox part 5; docs idempotent_requests; docs webhooks]
12. **Time and date handling: parsing `YYYY-MM-DD HH`, hour-bucket grouping, day offsets (-15 days), durations, month-end clamping, chronological merge of generated events** - scheduler and same-hour-penalty problems; Stripe billing anchors clamp to month end. [programhelp; extrabrain scheduler; docs billing-cycle]
13. **Interval / range logic with inclusive endpoints and gap filling (BIN ranges), off-by-one discipline** - BIN obfuscation problem explicitly warns about inclusive endpoints. [extrabrain]
14. **String normalization and canonicalization (case folding, punctuation -> spaces, suffix/article stripping, email dot/plus rules, Luhn digit walking, wildcard `*`/`?` expansion)** - Atlas, card validation, email normalization problems. [extrabrain; programhelp]
15. **Simple combinatorics on masked input (count valid completions of `*` digits; enumerate single-digit edits and adjacent swaps for `?`)** - card validation parts 3-4. [extrabrain]
16. **Sliding-window / rate-limit counters (N requests per T seconds per key)** - recurring OA/phone topic and Stripe's own token-bucket guidance. [programhelp; interviewing.io "design a rate limiter"; docs rate-limits]
17. **Ledger-style balance tracking (credits/debits per account, available vs pending, never negative unless allowed)** - "parse transaction logs -> balances", "Optimizing Money Transfer", "Stripepay Backend". [programhelp; interviewdb.io]
18. **Validation and error paths (missing keys, invalid numbers, unknown codes, nested BEGIN/END invalid)** - phone-screen rubric explicitly listed "dictionary key presence validation, input number validity checks". [linkjob shipping-cost report; extrabrain closing-time]
19. **Incremental design: parse -> model -> compute -> render as separate functions so Part N+1 adds a rule without rewriting Parts 1..N** - "later parts build on earlier ones and bugs compound"; "write modular code from the start". [Blind; interviewfox; Exponent]
20. **Self-testing discipline: run sample I/O immediately, write 2-3 of your own edge cases per part (empty input, zero-volume merchant, single record, ties), bank passing tests before moving on** - "lock Part 1 completely before advancing"; testing instinct is a stated screen criterion. [interviewfox; Exponent; Blind phone-screen thread]
21. **Speed in a concise language with strong stdlib (Python/Go/JS over Java); fluency with dict/defaultdict/sorted(key=...)/dataclasses** - Stripe engineers on Blind: Java verbosity cost candidates; no extra time. [Blind stripe-phone-screen-march-2025; programhelp reference solution uses defaultdict]
22. **Time-boxing: ~10-12 min per part, leave 5 min for final formatting checks; know that partial credit (e.g. 18/20, 22/25) advances** - reported outcomes. [Blind; interviewfox]
23. **Print-debugging in a browser IDE (no breakpoints); keep the tab focused (tab-switch pattern is logged)** - environment constraints. [interviewfox; HackerRank plagiarism docs]
24. **Domain literacy to decode the prompt fast: merchant/MCC/dispute/chargeback/refund/payout/subscription/proration/tier/BIN/Luhn/idempotency** - Stripe says the challenge "reflects the real-world engineering work we do"; JDs and all reported problems use this vocabulary. [Section C, D]

---

## Sources

Official / docs
- https://docs.stripe.com/currencies
- https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing
- https://docs.stripe.com/products-prices/pricing-models
- https://docs.stripe.com/billing/subscriptions/prorations
- https://docs.stripe.com/billing/subscriptions/billing-cycle
- https://docs.stripe.com/billing/subscriptions/overview
- https://docs.stripe.com/billing/subscriptions/usage-based
- https://docs.stripe.com/api/billing/meter-event/create
- https://docs.stripe.com/api/idempotent_requests
- https://docs.stripe.com/rate-limits
- https://docs.stripe.com/webhooks
- https://docs.stripe.com/disputes/how-disputes-work
- https://docs.stripe.com/refunds
- https://docs.stripe.com/payouts
- https://docs.stripe.com/payments/balances
- https://docs.stripe.com/reports/balance-transaction-types
- https://docs.stripe.com/radar/rules/reference
- https://docs.stripe.com/testing
- https://support.stripe.com/questions/choosing-a-name-for-your-stripe-atlas-company
- https://stripe.com/resources/more/is-your-company-name-available-in-delaware-here-is-how-to-find-out
- JDs: https://stripe.com/jobs/listing/software-engineer-payments/7529787 ; https://stripe.com/careers/listing/backend-engineer-api-payments-and-risk/4921361 ; https://stripe.com/careers/listing/staff-software-engineer-issuing/7369269 ; https://stripe.com/careers/listing/software-engineer-internal-systems/7543868 ; https://jobs.glynncapital.com/companies/stripe/jobs/57800855-software-engineer-new-grad ; https://jobs.generalcatalyst.com/companies/stripe/jobs/73804609-software-engineer ; https://careers.base10.vc/companies/stripe/jobs/38300794-full-stack-engineer-optimized-checkout-link ; https://builtin.com/job/backend-engineer-billing/7224418 ; https://builtin.com/job/software-engineer-payments/4205822
- HackerRank: https://www.hackerrank.com/blog/how-plagiarism-detection-works-at-hackerrank/ ; https://support.hackerrank.com/articles/8000786908-ai-plagiarism-detection

Process guides / candidate reports
- https://interviewing.io/stripe-interview-questions
- https://www.tryexponent.com/guides/stripe-software-engineer-interview
- https://www.techinterview.org/post/3233476020/stripe-bug-bash-api-design-interview/
- https://www.techinterview.org/post/3233460268/stripe-interview-guide-2026-process-bug-bash-round-and-payment-systems/
- https://igotanoffer.com/en/advice/stripe-interview-process
- https://www.finalroundai.com/blog/stripe-interview-process
- https://interviewfox.ai/interview-questions/stripe-oa-hackerrank-guide/
- https://www.linkjob.ai/interview-questions/stripe-hackerrank-online-assessment/
- https://www.linkjob.ai/interview-questions/stripe-interview-questions/
- https://www.linkjob.ai/interview-questions/stripe-technical-interview/
- https://extrabrain.app/interview-questions/stripe-hackerrank-online-assessment-extrabrain/
- https://oavoservice.com/en/articles/stripe-2025-hackerrank-oa-merchant-fraud-scoring-system-oavoservice
- https://programhelp.net/en/oa/stripe-hackerrank-online-assessment-questions-guide/
- https://programhelp.net/en/oa/stripe-2026-new-grad-oa-overview/
- https://programhelp.net/en/how-to-pass-stripe-swe-oa-real-coding-challenges/
- https://www.interviewdb.io/question/stripe (pages 1-3, titles only)
- https://www.teamblind.com/post/how-are-you-guys-cracking-stripe-oa-wjh6exbn
- https://www.teamblind.com/post/what-does-stripe-hackerrank-test-have-ijfwtgl0
- https://www.teamblind.com/post/stripe-hackerrank-rrt4pa6q
- https://www.teamblind.com/post/stripe-new-grad-oa-what-to-expect-jhav82mt
- https://www.teamblind.com/post/stripe-phone-screen-march-2025-oqru2jvw
- https://www.teamblind.com/post/how-to-approach-the-stripe-on-site-coding-challenges-qb0yu0tx
- https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1
- https://www.codinginterview.com/guide/stripe-interview-questions/
- Blocked/paywalled (not used beyond snippets): leetcode.com/discuss Stripe OA posts, 1point3acres threads, Glassdoor, Medium OA posts.
