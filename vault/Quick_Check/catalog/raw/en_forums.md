# Stripe OA / HackerRank / Phone-Screen Problems — English-forum sweep

Compiled 2026-08-25. Sources: LeetCode Discuss (fetched via LeetCode GraphQL API — verbatim post text), Blind, Levels.fyi, Glassdoor (titles only; pages 403), GitHub, 1point3acres English problem pages, PracHub, InterviewDB, plus SEO/AI aggregators (linkjob.ai, interviewfox.ai, extrabrain.app, programhelp.net, oavoservice.com, lodely, vervecopilot).

Confidence key: **HIGH** = original candidate post with verbatim/near-verbatim statement; **MED** = candidate post with paraphrase, or multiple independent aggregators agreeing; **LOW** = single SEO/AI-farm rewrite.

Format facts (consistent across HIGH sources):
- OA = HackerRank, **60 min, ONE problem, 3–5 progressive parts** (parts unlock on pass). Reported test-case totals: 20 (Sr SWE, Mar 2026, Blind), 25 (intern 2025, LC), ~17 (NG 2025, programhelp), 20 (2020-era "18/20", Blind).
- Older (2019–2021) NG/intern OA was **90 min** ("Stripe in a box", "logging/transaction loan calculation").
- Phone/team screen = 45–60 min, one problem with 3–4 linked parts on HackerRank/CoderPad; OA problems recycle into phone screens (Blind Nov 2025: "the coding question would resemble the OA problem").
- Not LeetCode-style: parsing, hash maps, state machines, business rules. Code quality is graded (Blind: single-letter var names hurt; AI-code flags).

---

## 1. Merchant Fraud Detection — MCC thresholds, CHARGE/DISPUTE ("Catch Me If You Can")
**Confidence: HIGH** (LC intern post + interviewfox self-report + 4 aggregators agree)
Sources:
- https://leetcode.com/discuss/post/7344444/ — "Stripe OA | SWE Intern 2026", posted 2025-11-12, role: SWE Intern (2025–26 University Recruiting). Verbatim: "The OA had one coding question (60 minutes) — not a typical DSA-style problem, but more of a system design. The question was based on fraud detection for merchants: 1. Each merchant is linked to an MCC (Merchant Category Code) with its own fraud threshold. 2. We had to process a stream of transactions (CHARGE) and disputes (DISPUTE) in real time. 3. Fraudulent and non-fraudulent codes were given separately. 4. Merchants had to be marked as fraudulent based on thresholds — which could be integer (count-based) or float (ratio-based). 5. Disputed transactions could reverse previously marked fraud charges. Passed 22/25 test cases. The remaining few likely involved rare async edge cases like multiple disputes or out-of-order charge/dispute handling."
- https://interviewfox.ai/interview-questions/stripe-oa-hackerrank-guide/ — author claims 2026 new-grad SWE track, 22/25. Five parts with test counts: Part 1 Parse Setup (3 cases), Part 2 Process Event Stream (5 → 8 cum.), Part 3 Mark Fraudulent Merchants (5 → 13), Part 4 Handle Dispute Reversal (5 → 18), Part 5 Edge Cases (7 → 25). Rules: count threshold flags when `fraud_count >= value`; ratio threshold flags when `fraud_count/total_count >= value` (only if total_count > 0). Disputes reverse charges and subtract from counts; double disputes and disputes of non-fraud charges are no-ops. (MED — self-reported, SEO site.)
- https://www.linkjob.ai/interview-questions/stripe-hackerrank-online-assessment/ (Sep 16 2025) and https://extrabrain.app/interview-questions/stripe-hackerrank-online-assessment-extrabrain/ — title "Catch Me If You Can – Fraud Detection", 3 parts:
  - Input: list of non-fraudulent result codes, list of fraudulent result codes, MCC→threshold table, merchant→MCC table, a minimum transaction count, then charge events `CHARGE,charge_id,account_id,amount,code`.
  - Part 1 (count-based): merchant is fraudulent once its fraudulent-transaction count exceeds its MCC threshold (after the minimum transaction count is met). Output: lexicographically sorted, comma-separated fraudulent account_ids.
  - Part 2 (percentage-based): MCC thresholds become fractions in [0,1]; fraudulent if fraud_count/total >= threshold; **once fraudulent, stays fraudulent** even if percentage later drops; min transaction count still applies.
  - Part 3 (disputes): `DISPUTE,charge_id` — disputed charge is treated as non-fraudulent; a merchant flagged solely because of now-disputed charges may return to non-fraudulent until it crosses the threshold again with new charges.
- https://programhelp.net/en/stripe-oa-question-stripe-sde/ — "Fraudulent Merchant Detection": fraud rate = fraudulent/total, re-evaluate after each transaction, flag when min transactions reached AND rate exceeds threshold; flagged merchants remain flagged permanently (variant of Part 2).
- https://oavoservice.com/articles/stripe-0109.en (Jan 4 2026) — a DIFFERENT "fraud detection" 4-part problem (CSV transaction verification), see §21.
Variants: Part 2 "permanent" vs Part 3 "reversible via dispute" — both reported; Part 3 overrides Part 2's permanence only for disputed charges.

## 2. Chat Billing — token usage, payg vs fixed plan, plan switching
**Confidence: HIGH-MED** (1point3acres English problem page with exact numbers + examples; InterviewDB lists "Chat Billing — OA, last reported 1 week ago" (Aug 2026); 1p3a "last asked 2026-04-17")
Sources:
- https://www.1point3acres.com/interview/problems/f8e3ed43-0b33-4b13-a879-a559ccd803f2 and https://www.1point3acres.com/interview/problems/59a39c1c-3696-400e-81b6-c3fdd3b56895 and https://www.1point3acres.com/interview/problems/company/stripe/chat-billing-oa (OA, medium, 60 min, last asked 2026-04-17)
- https://www.interviewdb.io/question/stripe — "Chat Billing", Coding/OA, last reported ~Aug 2026.
Statement (1p3a):
- Input: array of strings `"user_id,input_tokens,output_tokens,plan"`; tokens non-negative ints; plan ∈ {`payg`, `fixed`}. Each line = one chat session in the month.
- Output: array of strings `"user_id: $x.xx"`, sorted alphabetically by user_id, 2 decimals; include users with charges < $1.00.
- Tokens billed in **blocks of 100; partial blocks not billed** (`blocks = floor(tokens/100)`).
- **payg**: input $0.03 per 100-token block, output $0.04 per 100-token block; per session `cost = floor(in/100)*0.03 + floor(out/100)*0.04`.
- **fixed**: flat **$15.00/month**, includes **40,000 tokens/month** allowance (one page says 40,000 input + 20,000 output; the other says 40,000 tokens counted in 100-token blocks) — overage charged at payg rates.
- **Plan switching (Part 3)**: if a user has N sessions in the month, F of which are `fixed`, prorate by `r = F/N`: fee = `15.00 * r`, allowance = `40000 * r` tokens. Token blocks computed separately per plan; fixed sessions consume the prorated allowance first; payg sessions always charged at payg. Total = `payg_cost + 15.00*r + fixed_overage_cost`.
- Parts: (1) payg only, (2) fixed only, (3) mixed/switching.
- Examples (1p3a): Ex1 payg-only → `["userA: $0.07", "userB: $0.14"]`; Ex2 fixed → `["userA: $0.07", "userB: $17.30"]`; Ex3 mixed → `["userA: $7.71", "userB: $0.07"]` (raw inputs not shown on public page).
- interviewfox describes the same as "Compute each user's monthly bill across two plans: pay-as-you-go (per-token) and subscription with a token threshold. If a user has both, split usage proportionally".

## 3. Merchant Fraud Scoring (rules: amount multiplier, repeat-customer ≥3, hourly penalty)
**Confidence: MED** (3 aggregators with consistent detailed rules; programhelp claims Fall 2025 NG cycle, ~17 test cases)
Sources:
- https://programhelp.net/en/oa/stripe-2026-new-grad-oa-overview/ — Fall 2025 (2026 NG), 60 min, ~17 test cases incl. hidden, Python/Java/C++. Input: `merch` (name, initial score), `trans` (merchant m, customer c, amount h), `rules`. Rule A: group by (m,c): if pair has ≥3 transactions, add the pair's total amount to merchant score. Rule B: group by (m,c,h): if the triple appears ≥3 times, add their total amount again. Output each merchant `name, score` sorted alphabetically; strict `>` on thresholds. Edge cases: zero/negative amounts, merchants with no trades, duplicate transactions.
- https://oavoservice.com/en/articles/stripe-2025-hackerrank-oa-merchant-fraud-scoring-system-oavoservice (Jan 3 2026) — fuller variant: inputs `transactions_list`, `rules_list` (one rule per transaction: `min_transaction_amount, multiplicative_factor, additive_factor, penalty`), `merchants_list` (merchant_id, base_score). Steps: (1) init score=base_score; (2) merge each transaction with its rule (merchant_id, customer_id, amount, hour); (3) **Multiplication rule**: if amount > min_transaction_amount → score *= multiplicative_factor (strict >, per transaction); (4) **Repeat-customer rule**: if same customer_id has ≥3 transactions (incl. current) with same merchant → add each of those transactions' additive_factor (process as a group, do not double-count); (5) **Hourly penalty**: for same (customer, merchant, hour) with ≥3 transactions: hours 12–17 inclusive → add penalty; hours 9–11 or 18–21 → subtract penalty; other hours → nothing; (6) output `name, score` sorted lexicographically.
- https://programhelp.net/en/oa/stripe-oa-questions-software-engineer/ — same 3-rule system; hourly rule "for transactions beyond the second from a customer to a merchant within an hour".
- https://medium.com/@program.net/in-depth-breakdown-of-stripe-software-engineer-oa-333c7db9e033 — simpler variant: each transaction adds `amount × factor`; +customer_bonus per transaction; if merchant has > hour_threshold transactions in same hour subtract hour_penalty; example params factor=2, customer_bonus=1, hour_threshold=3, hour_penalty=5, merchants M1/M2, 6 transactions $50–$300.

## 4. Card Range Obfuscation (BIN interval gap filling)
**Confidence: HIGH-MED** (csoahelp verbatim 2024-25 University Recruiting challenge text; scribd doc; 2 aggregators)
Sources: https://csoahelp.com/2024/11/04/... (Nov 4 2024, "Welcome to 2024-25 Stripe University Recruiting HackerRank Challenge"), https://www.scribd.com/document/945047774/Stripe-2 ("Card Range Obfuscation Methodology", 3 pages), linkjob, extrabrain, programhelp stripe-oa-question-stripe-sde.
Statement: "Payment card numbers are composed of eight to nineteen digits, the leading six referred to as the bank identification number (BIN). Stripe's card metadata API exposes information about different card brands within each BIN range by returning a mapping of card intervals to brands. A given BIN range may have gaps at the beginning, middle, or end where no valid cards are present; fraudsters can use this to test for valid cards. Fill the gaps."
- Input: line 1 = 6-digit BIN; line 2 = integer n; next n lines `start,end,brand` where start/end are the **10 digits following the BIN** (offsets 0000000000–9999999999), brand alphanumeric. Intervals initially non-overlapping.
- Output: sorted (by start) intervals covering the entire range `BIN0000000000`–`BIN9999999999`, each printed as full 16-digit numbers `BIN+start,BIN+end,brand`.
- Part 1 (test cases 1–4): extend the lowest interval down to the BIN range lower boundary and the highest up to the upper boundary. Example: BIN 424242, `1500000000,6555555555,VISA` → `4242420000000000,4242429999999999,VISA`.
- Part 2: interior gaps — "the interval on the lower end of the gap will be extended to fill the gap".
- Part 3: nested intervals — only extend the covering (outer) interval.
- Part 4: after extending, **merge adjacent intervals with the same brand**.
- linkjob example: BIN 777777 with VISA 1000000000–3999999999 and MASTERCARD 4000000000–5999999999.
- LOW-confidence variant (programhelp 6-high-frequency page): "replace digits with X except first 2 and last 2; merge overlapping ranges" — likely AI hallucination.

## 5. Atlas Company Name Check / normalization
**Confidence: MED** (Blind commenter names it; 2 aggregators with identical detailed rules)
Sources: Blind https://www.teamblind.com/post/what-does-stripe-hackerrank-test-have-ijfwtgl0 area (search snippet: "One problem was called Atlas Company Name Check and was divided into three parts, only 60 minutes"), linkjob, extrabrain, programhelp.
- Part 1 normalization rules: ignore case; treat `&` and `,` as spaces; collapse consecutive spaces; ignore company suffixes `Inc.`, `Corp.`, `LLC`, `L.L.C.`, `LLC.`; ignore leading `The`/`An`/`A`; ignore `And` unless it's the first word; empty normalized name = unavailable. Input: normalization rules, table of registered names, requests `account_id|proposed_name`. Output `account_id|Name Available` or `account_id|Name Not Available`.
- Part 2: persistent registry — an accepted name becomes permanently unavailable for later requests.
- Part 3: `RECLAIM,account_id,original_proposed_name` — only the original registering account may reclaim; removes the normalized name from the unavailable set.
- LOW variant (programhelp): "only letters/numbers/spaces, length 2–50, not on blacklist → valid/invalid".

## 6. Payment Card Validation — Luhn, network detection, redacted `*`, corrupted `?`
**Confidence: MED** (linkjob + extrabrain identical 4-part spec with test-case ranges; phone-screen "redact card numbers" variant on codinginterview.com; InterviewDB lists "Credit Card Number — Phone" and "Card Parsing — Phone")
- Networks: VISA 16 digits starts with 4; MASTERCARD 16 digits starts 51–55; AMEX 15 digits starts 34 or 37.
- Luhn: from rightmost digit (excluding check digit) double every second digit, subtract 9 if >9, sum; valid if sum % 10 == 0.
- Part 1 (tests 1–5): 16-digit number starting with 4 → `VISA` or `INVALID_CHECKSUM`. Ex: `4532015112830366 → VISA`.
- Part 2 (tests 6–10): 15/16-digit → network name, `INVALID_CHECKSUM`, or `UNKNOWN_NETWORK`. Ex: `4425233430109994 → VISA`.
- Part 3 (tests 11–15): input contains `*` (1–5 redacted digits) → output count of valid completions per network, sorted alphabetically by network. Ex: `4242424242424*42 → VISA,1`.
- Part 4 (tests 16–20): input ends with `?` meaning exactly one error occurred (one digit changed OR two adjacent digits swapped) → output all possible valid originals in ascending numeric order, format `card_number,NETWORK`.
- Phone-screen variant (https://www.codinginterview.com/guide/stripe-interview-questions/): Part 1 `redact_card_numbers(str)`: tokens of 13–16 consecutive digits → replace all but last 4 with `x` (`"1234567890123456 is a number"` → `"xxxxxxxxxxxx3456 is a number"`); Part 2 brand rules (Visa starts 4, 13 or 16 digits; Amex 34/37, 15; Mastercard 16 digits, 51–55 or 2221–2720); Part 3 Luhn. interviewing.io lists "How would you blur credit card numbers from logs?"

## 7. Subscription Notification / Email Scheduler
**Confidence: HIGH-MED** (linkjob intern VO Oct 2025 report; 1p3a "Email Subscription"; oavoservice 2026; PracHub tech-screen variant; darkinterview/showoffer paywalled)
- Part 1: `send_schedule` maps offsets to email types: `"start"` (welcome on subscription start day), negative ints e.g. `-15` (days before end: "Upcoming expiry"), `"end"` ("Subscription expired"). Users: name, plan, account/start date, duration (days). Print chronologically: `<day>: [<Email Type>] Subscription for <name> (<plan>)`; tie-breaker rules for same day. Interviewer emphasised keys other than start/end must be treated as generic numbers (dynamic).
- Part 2: plan changes `(name, new_plan, change_date)` → print `[Changed]` on change date; future emails reference new plan; recalculate remaining duration.
- Part 3: renewals `(name, extension, change_date)` → print `[Renewed]`; extend end date and reschedule expiry/expired emails.
- oavoservice example: Alice start=0 dur=30, Bob start=10 dur=30; PlanChanges `[{user:"Alice", time:5, new_plan:"Gold"}]` → Alice's day-15 and day-30 emails must say Gold.
- Reported as intern Virtual Onsite programming round (Oct 2025) by linkjob; as OA by extrabrain/linkjob.
- PracHub variant "Generate Account Email Notifications" (Technical Screen, May 2026): input current_day, accounts {account_id, created_day, expires_day}, rules {name, trigger ∈ on_create | days_before_expiration(offset_days) | after_expiration, template}; output `<account_id> <rule_name> <template>` in account order then rule order; up to 200k accounts/rules; example current_day=10 → `["A1 welcome Welcome!", "A2 three_day_reminder Your account expires in 3 days.", "A3 expired Your account has expired."]`.
- 1p3a "Email Subscription": `subscribe(user_id, topic_id, expiry_date, schedule)` and `send_schedule()`; ≤100 subscriptions per user; O(n).

## 8. Store Closing Time Penalty (shop log Y/N, BEGIN/END)
**Confidence: HIGH** (verbatim LC phone-screen post; InterviewDB "Closing Time — Phone, 1 month ago" (Jul 2026))
Source: https://leetcode.com/discuss/interview-question/2585038/ — "Stripe | Phone Screen | Senior SE | Reject", 2022-09-16. Verbatim:
- Part 1: Customer log `"Y Y N Y"` (per hour, Y = customers came). Closing time = hour store closes. Penalty: +1 for each open hour with N; +1 for each closed hour with Y. `int compute_penalty(String log, int closing_time)`.
- Part 2: `int getClosingWithMinPenalty(String log)` — closing time (0..n) with minimum penalty (smallest on tie).
- Part 3: multiple stores: `"BEGIN BEGIN BEGIN Y Y N Y END Y Y N N END Y N Y N END"` → `List<Integer> getAllClosing(String log)` (stack + part 2).
- Aggregator Part 3 wording: valid log = `BEGIN` … Y/N tokens … `END`; cannot be nested; may span lines / several per line; ignore garbage and unfinished logs; return best times in order. Solution gist: https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1. Equivalent LC 2483 "Minimum Penalty for a Shop".

## 9. Radar Rules (charge string + ALLOW/BLOCK rules)
**Confidence: HIGH** (GitHub repo with task text; DMCA'd second repo confirms it's a real Stripe HackerRank question)
Source: https://github.com/kylelong/stripe-interview/blob/master/RadarRules.java (README: "Stripe HackerRank interview question"). Verbatim task header:
```
Basic Block:  In: ["CHARGE: card_country=US&currency=USD&amount=150&ip_country=CA","BLOCK:amount > 100"]  Out: 0
Compound Block: In: ["CHARGE: card_country=US&currency=USD&amount=150&ip_country=CA","ALLOW:amount<100","BLOCK:card_country != ip_country AND amount > 100"]  Out: 0
```
Charge properties: card_country, currency, amount, ip_country. Rules `ALLOW:`/`BLOCK:` with up to 2 conditions joined by `AND`/`OR`; operators `> < >= <= == !=`; return 1 if allowed, 0 if blocked. (github.com/Molakim/stripeCoding is DMCA-blocked by Stripe, 2022-05-17.)

## 10. Server Name Tracker — allocate/deallocate ("missing server")
**Confidence: HIGH** (Glassdoor question title verbatim; gist with full statement + examples)
Sources: https://gist.github.com/stealthbomber10/d85d44776ad58ba66d84ff76fd5be736 ; Glassdoor QTN_1221351 "Create a ServerManager class with allocate(string) and deallocate(string): allocate('apibox')='apibox1', allocate('apibox')='apibox2', allocate('sitebox')='sitebox1', allocate('apibox')='apibox3', deallocate('apibox2'), allocate('apibox')='apibox2'".
- Part 1: "servers numbered sequentially from 1; a server may explode and its number is reused; new server gets the lowest available number." `next_server_number([5,3,1])=2`, `([5,4,1,2])=3`, `([3,2,1])=4`, `([2,3])=1`, `([])=1`, `([1,1.5,2,2.5,3,3.5,4,5,5.5])=6`.
- Part 2: hostnames = host type + number (`apibox1`); class with `allocate(host_type)` → next available name, `deallocate(hostname)` → release. `allocate("apibox")="apibox1"`, `"apibox2"`, `deallocate("apibox1")`, `allocate("apibox")="apibox1"`, `allocate("sitebox")="sitebox1"`.

## 11. Currency Conversion / FX graph
**Confidence: HIGH** (two verbatim LC posts; Glassdoor variant with shipping method; 1p3a; bigtechexperts; InterviewDB "Currency Conversion — Phone")
- https://leetcode.com/discuss/interview-question/5740845/ (2024-09-05, reject): "Stripe operates in many countries… Depending on what bank we have a partnership with will determine what currency pairs can be swapped, and at what rate. Input: `AUD: USD: 0.75, USD: CAD: 1.26, USD: JPY: 109.28, GBP: JPY: 150.15`. Each element = currency pair + rate; conversion is symmetric (1 USD = 1/0.75 = 1.333 AUD). Write `f("AUD","USD")=0.75`, `f("USD","AUD")=1.333`. Follow-up: two-step conversion via one intermediate: `f("AUD","CAD")=0.945=0.75*1.26`."
- https://leetcode.com/discuss/interview-question/5150083/ (2024-05-13, Technical Screen Canada): input `USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110`. Part 1 direct rate; Part 2 one-hop (CAD:AUD); Part 3 "best conversion available" among paths; Part 4 return ALL pairs computable from the input.
- bigtechexperts (3 parts): Part 1 direct only, return -1 if none, round to 2 dp (`"USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.15"`, USD→CAD 100 → 130.0); Part 2 any path, return `{'route': 'USD -> CAD -> AUD', 'rate': 1.76, 'converted_value': 175.68}`; Part 3 shortest path (BFS, fewest hops).
- Glassdoor QTN_7989241 (SWE Intern): parse `"USD:CAD:DHL:5,USD:GBP:FEDX:10"` — source, target, shipping method, rate; write convert(amount, from, to). InterviewDB also lists "Shipping Route — Phone".

## 12. HTTP Accept-Language header parsing
**Confidence: HIGH** (verbatim LC phone screen post; Glassdoor QTN_4469893 "Parsing the HTTP Accept-Language header" (Infra Eng); Blind Apr 2022 "parsing some list of http headers"; InterviewDB "Header Parsing — Phone")
Source: https://leetcode.com/discuss/interview-experience/4742657/ (2024-02-17). Verbatim Part 1: "In an HTTP request, the Accept-Language header describes the list of languages the requester would like content returned in… comma-separated list of language tags, e.g. `Accept-Language: en-US, fr-CA, fr-FR` … Write a function that receives an Accept-Language header value (string) and a set of supported languages, and returns the list of language tags that will work, in descending order of preference (same order as header). Use tests to demonstrate correctness. `parse_accept_language("en-US, fr-CA, fr-FR", ["fr-FR","en-US"])` → `["en-US","fr-FR"]`; `("fr-CA, fr-FR", ["en-US","fr-FR"])` → `["fr-FR"]`; `("en-US", ["en-US","fr-CA"])` → `["en-US"]`." Known later parts (from public solutions of this classic Stripe question): Part 2 language-only tags (`en` matches all `en-*`), Part 3 wildcard `*`, Part 4 `;q=` quality weights. programhelp variant: `"en-US,en;q=0.8,fr;q=0.9,de;q=0.7"` → rank by q (default 1.0), tie by order → `["en-US","fr","en","de"]`.

## 13. Chargeback / Dispute file parsing (2024 NG OA)
**Confidence: HIGH** (verbatim LC post)
Source: https://leetcode.com/discuss/interview-question/5832245/ "Stripe University New Grad OA 2024", 2024-09-25. Verbatim: "Stripe processes billions of dollars… the end user can file a chargeback… the bank sends this chargeback information to Stripe. The chargeback is the first stage in the lifecycle of a dispute; your job is to extract relevant information about a dispute by parsing this chargeback information so the dispute can be surfaced to the merchant.
- Part 1: Parsing valid network chargeback information — construct a simple parser; read the contents of one or more files and output the aggregated dispute information. All input valid.
- Part 2: Filter out invalid data — corrupted rows; any one of the listed conditions makes a row invalid: ignore that row only and continue.
- Part 3: Filter out withdrawn disputes — if the same transaction ID appears in two valid rows in files for the same network, where the appearance in the later-dated file is listed with reason `withdrawn`, do not process either row."
(Exact field list not given in post.)

## 14. Bracket / Brace Expansion (screening round)
**Confidence: HIGH** (verbatim LC post; hackerprep "Bracket Expansion (Stack), last seen within 4 months, high confidence"; InterviewDB "Expansion — Phone, 5 days ago" (Aug 2026))
Source: https://leetcode.com/discuss/interview-experience/5341224/ "Stripe | Backend Engineer | Bangalore | Jun 2024 | Reject" (3.5 YOE, screening 1 hr on HackerRank). Verbatim: "string expression with several comma-separated tokens inside `{` `}`; optional prefix/suffix. Return list of strings. Ex1 `"/2022/{jan,feb,march}/report"` → `/2022/jan/report`, `/2022/feb/report`, `/2022/march/report`. Ex2 `"over{crowd,eager,bold,fond}ness"` → overcrowdness, overeagerness, overboldness, overfondness. Ex3 `"read.txt{,.bak}"` → `read.txt`, `read.txt.bak`. Follow-up: if fewer than 2 tokens inside braces or malformed (no braces / only opening / closing before opening) return input unchanged: `sun{mars}rotation`, `minimum{}change`, `hello-world`, `hello-{-world`, `hello-}-weird-{-world` → same. Usually 2–3 follow-ups (nested braces / multiple groups)." codinginterview.com variant: `"{a,b}c{d,e}f"` → `['acdf','acef','bcdf','bcef']` lexicographic.

## 15. Invoice Reconciliation (payment memo → invoice)
**Confidence: HIGH** (verbatim LC post; 1p3a onsite thread; InterviewDB "Payment Invoices — Phone")
Source: https://leetcode.com/discuss/post/7379560/ "Stripe Interview | Round 1", 2025-11-28. Verbatim: "Stripe's Invoicing product… standalone payments need to be reconciled with open invoices. Match incoming payments to invoices based on the memo line. `payment="paymentABC,500,Paying off: invoiceC"`, `invoices=["invoiceA,2024-01-01,100","invoiceB,2024-02-01,200","invoiceC,2023-01-30,1000"]`. Payment fields: id, amount in USD minor units ($1.00=100), memo always `Paying off: {INVOICE}`. Invoice fields: id, due date, amount due (minor units). `f("payment5,1000,Paying off: invoiceC", [...])` → `payment5 pays off 1000 for invoiceC due on 2023-01-30`." (Later parts — partial payments / multiple invoices / oldest-due-first — not in post.)

## 16. Load Balancer for WebSocket/Jupyter connections (OA, intern 2025-26)
**Confidence: HIGH-MED** (1p3a thread 1147495 "2025-2026 University Recruiting HackerRank Internship Online Test — multi-stage load balancing"; 1p3a thread 1147122 "Server Load Balancer Design, 60-min OA"; PracHub full spec (Intern, OA, Feb–May 2026); dev.to programhelp Mar 2026; csoasupport Sep 2025)
- Params: `numTargets` (m servers), `maxConnectionsPerTarget` / `capacity[m]`, `requests[n]` strings. Return log lines for CONNECT only: `connectionId,userId,targetIndex` (1-based per csoasupport; PracHub: `"connectionId serverIndex"` 0-based).
- Part 1: `CONNECT connectionId objectId/userId` → server with fewest active connections, tie → smallest index.
- Part 2: `DISCONNECT connectionId` → remove; invalid ids ignored; no log.
- Part 3: sticky routing — same objectId must go to the same server as its existing active connection even if that server has more load; if no active connection for the objectId, normal balancing.
- Part 4: capacity — server at capacity ineligible; if stickiness requires a full server, CONNECT rejected (no log, no state change).
- Part 5: `SHUTDOWN s` — server temporarily out of service; evict all its connections and re-route them one by one **in original arrival order** using the same rules.
- Constraints: 1 ≤ m ≤ 1e5, ≤ 2e5 requests, capacity ≤ 1e9.
- Example: `capacity=[2,2,2]`, `CONNECT c1 o1, CONNECT c2 o2, CONNECT c3 o3, CONNECT c4 o4, SHUTDOWN 0` → `['c1 0','c2 1','c3 2','c4 0','c1 1','c4 2']`.
- InterviewDB OA titles "Request Router" and "Proximity Request Routing" are likely this family / §17.

## 17. Data-center registry & nearest-healthy-region routing (OA, Aug 2026)
**Confidence: MED** (PracHub full spec dated Aug 22 2026, OA; 1p3a lists "Stripe L3 SWE OA on Datacenter Request Routing" 2026-08-11; InterviewDB "Proximity Request Routing — OA")
`processDataCenterCommands(commands)`: `["REGISTER", region, lat, lon, capacity]` → OK if new, lat∈[-90,90], lon∈[-180,180], capacity>0 else ERROR; `["SET_HEALTHZ", region, bool]`; `["DISTANCE", lat1, lon1, lat2, lon2]` → Haversine (R=6371 km) rounded `floor(d+0.5)`; `["ROUTE", lat, lon]` → `"region roundedDistance candidates"` ranking healthy regions by unrounded distance then name, `"NONE 0"` if none. Strict arity/type checks; invalid commands mutate nothing. Example: REGISTER east 40 -74 10; REGISTER west 34 -118 20; SET_HEALTHZ east false; ROUTE 41 -73 → `["OK","OK","OK","west 4000 west"]`.

## 18. Weekly Deployment Window Scheduler (OA, 2026)
**Confidence: MED** (PracHub spec Jul 2026 tech screen; InterviewDB "Deployment — OA, 1 month ago"; 1p3a OJ "Find the First K Valid UTC Deployment Windows"; 1p3a 2026-08-24 "OA UTC Timezone Mapping and Sliding Window")
- Part 1: rows `start,end,type` (type allowed|freeze), minutes in week `[0, 10080)`, half-open; return maximal allowed-minus-freeze intervals sorted, touching merged; freeze wins. `['540,600,allowed','570,585,freeze']` → `[[540,570],[585,600]]`; `['0,20,allowed','10,30,allowed','5,8,freeze','20,25,freeze']` → `[[0,5],[8,20],[25,30]]`.
- Part 2: first row `utc_now,lead_time_minutes,min_continuous_minutes,k`; rows `start,end,type,timezone_offset_minutes`; horizon `[utc_now+lead, utc_now+lead+W)`; `start==end` = full week; `UTC = local - offset`; return up to k windows of length ≥ min_continuous. No minute-by-minute iteration; handle week wrap.

## 19. Transaction fee computation (CSV) — phone screen / tech screen
**Confidence: HIGH-MED** (Glassdoor QTN "parse the input API and get account balance information for a user"; PracHub two specs; InterviewDB "Transaction Fee — Phone")
- Glassdoor/linkjob report: CSV columns `id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status`, e.g. `py_1,1,1000,eur,2025-01-01,acct_1,ie,payment,card,payment_completed`; compute fee; follow-up adds if/else: if payment_completed and country 'ie' and provider Klarna or 'card' then fee X; interviewer insisted on splitting into methods.
- PracHub "Compute transaction fees from a CSV string" (Data Eng, Hard): `compute_fees_per_merchant(csv_str, base_rate_by_provider, completed_rate_by_provider_and_country, fx_to_usd)`; statuses payment_completed/pending/failed, refund_completed, dispute_won/lost; refund → $0; completed → `amount×fx×completed_rate[(provider,country)] + $0.30` (fallback base_rate); others → `amount×fx×base_rate + $0.30`; unknown provider rate 0 (still +0.30), unknown currency fx 1.0; output `merchant_id,total_fee_usd` 2 dp sorted.
- PracHub "Calculate Transaction Fees" (Tech Screen, May 2026): fee rules `(payment_type, payment_status) → rate_bps`; transactions `(id, type, status, amount_cents)`; `fee = floor(amount_cents*rate_bps/10000)`; unmatched → 0; example card/paid 290 bps etc. on $100,$100,$250,$50 → `[290,100,200,0]`, total 590.
- Glassdoor also: account data lines `acct_123, 1, usd, 1000` (account_name, timestamp, currency, amount) — compute balances.

## 20. Account Transfer Ledger / bank-account command simulation (OA + intern VO)
**Confidence: MED** (GitHub Shivam5022 experience: OA "parse a command string and execute commands simulating transactions between users' bank accounts"; linkjob 2026 intern VO 3-part spec; PracHub "Build an Account Transfer Ledger" onsite May 2026; InterviewDB "Optimizing Money Transfer — Phone", "Merging Transactions — Phone")
- Part 1: process transfers; output accounts with non-zero balances.
- Part 2: reject transactions where `current_balance + amount < 0`; output rejected list and remaining balances.
- Part 3(a): a special `platform_id` account; any other account going below 0 may "borrow" from the platform to cover the deficit; output `max_reserve` (total borrowed), rejected transactions, non-zero-balance users.
- programhelp 2026 intern VO: `PaymentLedger` class `add_payment(id, amount, ts)`, `add_refund(id, amount, ts)`, `get_total_revenue()`, `get_payments_by_date(date)`; follow-ups partial refunds, time-range queries, bad timestamps.

## 21. Fraud-detection CSV verification (4-part, "Smart Report")
**Confidence: LOW-MED** (oavoservice Jan 2026; codingkaro lists "Verify Transaction Data Integrity / High-Risk Rule Validation / User Behavior Matching" phone screen Nov 30 2025)
Part 1 parse CSV (amount, currency, card_type, location…) rejecting empty/whitespace/null; Part 2 amount within min/max, payment method not on blocklist (e.g., prepaid) → SUSPICIOUS; Part 3 compare to user behavioural baseline, flag if <50% of features match; Part 4 replace SUSPICIOUS with specific codes (e.g., `AMOUNT_TOO_HIGH`), max two codes, `OK` for clean rows, aligned columns.

## 22. KYC verification (CSV validation, progressive)
**Confidence: MED** (Glassdoor QTN_8763050 "6 step KYC Verification coding Q"; 1p3a "KYC Conundrum"; Exponent "CSV parsing & validation… circular dependencies"; InterviewDB "Data Validation — Phone, 1 week ago"; 1p3a "KYC Data Validation")
Fields: business_name, business_profile_name, full_statement_descriptor, short_statement_descriptor, url, product_description. Part 1 VERIFIED only if all present & non-empty; Part 2 full_statement_descriptor length 5–31 inclusive; Part 3 blocklist descriptors `ONLINE STORE, ECOMMERCE, RETAIL, SHOP, GENERAL MERCHANDISE`. Output `VERIFIED: <name>` / `NOT VERIFIED: <name>`. Exponent: later parts cross-column rules and circular-dependency detection.

## 23. Shipping cost / tiered pricing (intern tech screen, Nov 2025 – 2026)
**Confidence: HIGH-MED** (Glassdoor QTN_8206177 "calculate the total shipping cost of an order where the shipping costs are tier based"; 1p3a threads 1131552 & 7331443; linkjob intern Sept 2025; codingkaro Nov 6/14 2025 intern; PracHub; InterviewDB "Shipping Cost — Phone")
- Part 1: order (JSON items with quantity) + shipping matrix keyed by country → product → per-unit price; compute total.
- Part 2: tiered/"incremental" pricing — unit price decreases as quantity increases; apply each tier only to units within its range (upTo inclusive; last tier unbounded / `maxQuantity: null`).
- Part 3: two methods per tier: `incremental` (quantity × cost) vs `fixed` (flat amount for the whole tier/range); order data unchanged.
- PracHub JS variant: `calculateShipping(destination, quantity, config)` with `{unitPrice}`, `{tiers:[{upTo,unitPrice}]}`, `{baseFlat:{upTo:n, amount:F}, tiers:[...]}`; unknown destination → null; qty ≤ 0 → 0. Tip: use cents.

## 24. Record linking / linked users (phone screen 2026)
**Confidence: MED** (linkjob 2026 phone screen; InterviewDB "Linked User — Phone", "Matching Contacts — Phone")
Rows of users {id, name, email, company}; field weights name 0.2, email 0.5, company 0.3; threshold 0.5; two records linked if sum of weights of matching fields ≥ threshold. Part 1 direct matches for target_user_id; Part 2 indirect (1-hop); Part 3 all connected components (unlimited hops). InterviewDB OA "Join Dataset" and "Collusion" (1p3a "Six Degrees of Collusion — Direct Links / Risk Scoring / Fraud Ring Size") appear to be the OA cousin: graph of linked accounts, ring size via BFS, risk score by degree.

## 25. Rate limiter
**Confidence: MED** (interviewing.io "Design a rate limiter in any programming language"; darkinterview "Rate Limiter" coding: "tracks API access patterns and enforces request limits; multiple clients identified by keys"; dev.to programhelp "3 requests per 10 seconds sliding window"; Exponent "stateful structure like a cache or rate limiter")
Sliding window / token bucket per client key; edge cases at window boundaries.

## 26. Transaction reconciliation (system vs gateway lists)
**Confidence: MED** (1p3a curated problem 41eadf8b…; 1p3a OJ "Payment Reconciliation (Transactions Matching & Discrepancy Report)")
Input: system records (txn id, amount) and gateway records (txn id, amount). Output three lists: matching ids, mismatched ids (present in both, amounts differ), ids only in gateway.

## 27. Other reported items (titles / fragments only)
- **"Stripe in a box"** (intern OA ~2019–2020, 90 min): "write a mini functioning Stripe API with transactions, charges, interest, different charges depending on which company's card is used" (Blind, naukri). InterviewDB "Stripepay Backend — OA".
- **Logging / transaction loan calculation** (NG OA Aug 2020, ~1.5 h, Blind mvtuacrh): "design Q, fairly easy but tricky edge cases; read their sample cases".
- **URL compression / string manipulation** phone screen May 2023 (Blind wgvdy4o7): "question was really long, solved 3 parts"; PracHub "Implement Validation and String Compression" (Senior onsite, Hard, Apr 2026): tokenization, hierarchical string manipulation. InterviewDB "Pattern Validator — Frontend Phone".
- **Numeronym validation** (Exponent/finalround): `i18n` valid; first/last letters, digits between; min length 3.
- **Parse & format hierarchical task CSV** (1p3a OJ title only).
- **Calculate Service Fees** (1p3a OJ title only).
- **Observability** (InterviewDB OA, reported Aug 2026 — no content).
- **Factory Cost**, **Fraud Reports**, **User Roles**, **User Feature System**, **Wishlist**, **Card Parsing** (InterviewDB phone titles, no content).
- **Assign reviewers from changed files** (PracHub, SWE-AI, Apr 2026).
- **Account scheduler / locked_until** (linkjob 2026 onsite): `is_available(account, ts)`, `acquire(account, duration)`, LRU selection.
- **State-machine command simulation** (LC 7428741, NG India OA Dec 10 2025, "Hard"): multiple entities, chronologically ordered commands, valid state transitions only, invalid ops are no-ops, final aggregated sorted output — description kept abstract by OP (matches §1 or §20).
- **3-part string-parsing OA** (LC 7285521, NG 2026 on-campus, Oct 2025): "3 parts building sequentially, single submission must pass all; getline + maps + sets; no complexity constraints".
- Tech screen after OA (LC 6896919, Jun 2025): 4-part linked question in 60 min; VO coding "repeat of phone screen but must use built-in libraries"; bug squash; integration = writing POST requests against provided API.
- Bug bash example (techinterview.org): ~200-line `PaymentProcessor` with 5–7 bugs (race, missing idempotency, non-atomic balance check, dedup, refund validation, max refund).

## Aggregator "problem lists" (LOW confidence unless corroborated above)
- linkjob.ai / extrabrain.app (identical 6-problem set): Atlas Company Name Check; Card Range Obfuscation; Catch Me If You Can – Fraud Detection; Store Closing Time Penalty; Subscription Notification Scheduler; Payment Card Validation System.
- programhelp.net "6 High-Frequency": same six but with an Accept-Language parser instead of card validation; its per-problem rules are partly hallucinated (see notes in §4, §5). Also claims "2 questions/90 min" — contradicts HIGH sources.
- lodely.com: generic LeetCode mapping (interval scheduling, merge-k streams, bracket validation) — not real Stripe statements.
- vervecopilot: 30 generic system/behavioral questions — not OA.
- dev.to programhelp: "Parse transaction logs `user event amount` → final balances"; "Email normalization (dots, plus)"; "Rate limiter 3 req/10 s".

## Sources checked with no problem content
Blind: rrt4pa6q (Apr, Sr, 18/20), wjh6exbn (Mar 19 2026, Sr, 14/20, "read whole problem first"), ijfwtgl0 (Mar 22), jhav82mt (Sep 2024), r2mcra36 (May, passed all → rejected, AI-code suspicion), svj60pbg (Apr 2022 phone: HTTP headers / two-pointer string), rptglpyd (May 2021: "practical 3-part"), h4oxxgnd (Jun 2023: "LC-medium split in 2–3 parts"), n4mqgn4g (Apr 2024 onsite), ha4pxp3h (Dec 2021: string/array multi-level, regex), wgvdy4o7, jcnxxpsh ("read JSON, transform it"), 5d7673dy (Nov 2025: pre-onsite Q resembles OA; min parts 3 Python / 2 C++/Java), ac6qeabo (May 2022: 3-part, parts 1–2 in 10 min), xt7z5dhx, 6ab5ozmg, r4qsumoi, tsgpu2rw. Levels.fyi yUBZ26. LC 1520689, 2716060, 793978 (2020: "code and written section"), 840872, 4198075, 5712510 — all questions with no answers. Glassdoor listing pages: 403. Reddit: no indexed threads surfaced via search (results were all Blind/LC).

---
# ADDENDUM A — LeetCode Discuss deep sweep (GraphQL, ~100 Stripe threads) + Blind curl sweep

## A1. Invoice Reconciliation — full 3-part spec (NG SDE Virtual Onsite, Mar 2026) — **HIGH**
Source: https://leetcode.com/discuss/post/7691354/ "Stripe NG SDE VO", 2026-03-25 (verbatim structure). Also https://leetcode.com/discuss/post/6696304/ (L2 Bangalore phone screen 2025-04-28, verbatim statement identical to §15, adds: "Be ready to generate the input on your own and write your own test cases (more than 2)"), and comment on 7379560 (2026-02-27).
- Input: payment string `"payment_name, amount, memo"`; invoices `["invoice_id, due_date, amount", ...]`.
- **Part 1 — match by invoice_id from memo**: memo may contain `"XXXX:invoice_id"` (e.g. `Paying off: invoiceC`). Extract id, match, output `payment_name, amount, due_date, invoice_id` (format from §15: `payment5 pays off 1000 for invoiceC due on 2023-01-30`).
- **Part 2 — fallback to amount**: memo may have no invoice id (e.g. `"pid123,500,Bank Transaction"`). Match invoices whose amount == payment amount; if several, choose the **earliest due_date**. Example: `f("pid123,500,Bank Transaction", ["invoiceA,2024-01-01,500","invoiceB,2024-02-01,500"])` → `pid123 pays off 500 for invoiceA due on 2024-01-01`.
- **Part 3 — tolerance ("forgiveness")**: integer `forgiveness`; match if `invoice_amount - forgiveness <= payment_amount <= invoice_amount + forgiveness`; if amounts differ, include the difference (`diff = payment_amount - invoice_amount`) in the output.

## A2. FX + shipping-method conversion (phone screen, 4 parts) — **HIGH**
Sources: https://leetcode.com/discuss/post/6006563/ "Stripe screening US 2024 [Rejected]" (2024-11-04); https://leetcode.com/discuss/post/5883672/ "Stripe Phone Screen" (2024-10-07); https://leetcode.com/discuss/post/5647506/ "Stripe Technical Interview" (2024-08-16); Glassdoor QTN_7989241; Blind d4f50dzn (Jul 2026: "prep phone-screen questions like Shipping Cost and Currency Conversion").
- Input variants: `"USD:CAD:DHL:5,USD:GBP:FEDX:10"` (source, target, shipping method, rate/cost); `"US,UK,UPS,5:US,CA,FedEx,3:CA,UK,DHL,7"`; `"US:UK:Fedex:5, CA:FR:DHL:10, FR:UK:UPS:6"`.
- Part 1: parse; direct conversion/cost only. `costOfPackages(input,"US","UK") -> 5`, `("FR","UK") -> 6`.
- Part 2: allow **at most one hop** (one intermediate); return cost **and the shipping methods involved**. `"US:UK:Fedex:5, CA:FR:DHL:10, FR:UK:UPS:6, UK:US:DHL:2, UK:FR:DHL:10"`, US→FR = US→UK→FR = 15.
- Part 3: **minimum** cost with at most one hop, plus methods.
- Part 4 (not reached by OP): presumably unlimited hops / best path.
- Poster advice: use Python for parsing; C++ cost them time.

## A3. Bank-account rebalancing (move money so every account ≥ 100) — **HIGH**
Source: https://leetcode.com/discuss/post/5647506/ (2024-08-16), quoted as the base problem the shipping question was "a variation of". Verbatim: "At Stripe we keep track of where the money is and move money between bank accounts to make sure their balances are not below some threshold… Let's say there are at most 500 bank accounts, some above 100 and some below. How do you move money between them so that they all have at least 100? Not looking for the optimal solution, but a working one." Example input `AU: 80, US: 140, MX: 110, SG: 120, FR: 70` → output `from: US, to: AU, amount: 20 / from: US, to: FR, amount: 20 / from: MX, to: FR, amount: 10`.
Related VO problem (https://leetcode.com/discuss/post/7521596/, 2026-01-24): "Minimum Transactions for Multi-Party Debt Settlement" — given borrowing/lending records, min number of transactions so all net balances are zero (LC 465 Optimal Account Balancing); follow-up: scale to hundreds of people. InterviewDB lists "Optimizing Money Transfer — Phone".

## A4. Closing-time problem — Dublin L2 screening variant with garbage logs — **HIGH**
Source: https://leetcode.com/discuss/post/3950781/ "Stripe | Dublin | Backend | Rejected | L2" (2023-08-23). Days instead of hours: `S = "Y N N Y N Y Y N"`, index `ind`; loss +1 for each closed day with a customer after, +1 for each open day without customer before. `S="Y N N Y N Y Y N", ind=2` → 1 + 3 = 4. Interviewer required full program (main, parse input incl. spaces, print). Follow-up 1: day with minimum loss. Follow-up 2: logs like `\t\t L R L R \nmtswioehdvdfoj R L R /t/n` "very random" — extract each valid pattern, print it and its minimum loss. (Note: this variant uses L/R tokens in the log example.) Comments on 2585038: "part 2 in O(n) with two prefix-sum arrays"; asked again Nov 2023 (3.5 YOE), Mar 2024 (senior SWE), Sep 2024.

## A5. Subscription email scheduler — concrete example I/O — **HIGH**
Source: https://leetcode.com/discuss/post/5918387/ "Stripe Interview Question Help" (2024-10-15):
```
users   = [{name: A, plan: X, begin_date: 0, duration: 30}, {name: B, plan: Y, begin_date: 1, duration: 15}]
changes = [{name: A, new_plan: Y, change_date: 5}, {name: B, extension: 15, change_date: 3}]
Output:
0: [Welcome] A, subscribe in plan X
1: [Welcome] B, subscribe in plan Y
1: [Upcoming expiration] B, subscribe in plan Y
3: [Renewed] B, subscribe in plan Y
5: [Changed] A, subscribe in plan Y
15: [Upcoming expiration] A, subscribe in plan Y
16: [Upcoming expiration] B, subscribe in plan Y
30: [Expired] A, subscribe in plan Y
30: [Expired] B, subscribe in plan Y
```
(Upcoming = 15 days before expiry; poster puzzled why B's new expiry is 30 rather than 31 — possible off-by-one in the source; expiry appears to be begin+duration-1 after renewal.) Same problem seen in an Aug 2024 SDE2 India LLD round as "subscription tracking service" (https://leetcode.com/discuss/post/5740522/).

## A6. Fraud-detection CSV 4-part — now confirmed as a real phone screen — **HIGH**
Source: https://leetcode.com/discuss/post/7497123/ "Stripe Interview Experience & Timeline" (2026-01-15, phone screen 60 min / 45 coding, parts unlock sequentially): Part 1 read six CSV fields per transaction, verify all non-empty; Part 2 amount within valid business range, payment method not in blocked list → `SUSPICIOUS`; Part 3 ≥50% of behavioural features (common countries, typical time ranges, average amount ranges) must match user's history else `SUSPICIOUS`; Part 4 replace `SUSPICIOUS` with up to two prioritized error codes, `OK` if none, column-aligned report. (Upgrades §21 from LOW-MED to HIGH.)

## A7. Card validation OA confirmed on Blind — **MED→HIGH-MED**
Blind https://www.teamblind.com/post/my-stripe-interview-gdmiywlu (Aug 27 2025): "I actually got their OA which had some insane 4 levels of credit card validation BS." Corroborates §6's 4-part structure as a real OA.

## A8. Other verbatim/near-verbatim phone-screen items from LeetCode
- https://leetcode.com/discuss/post/3102019/ (UAE, Jan 2023, offer): onsite coding round = Accept-Language problem verbatim (§12); system design = "design an architecture for delivering webhooks to customers"; debugging = clone repo, fix bugs. Comment on 4742657 (Dec 2025) says remaining parts are described at programhelp "stripe-interview-process-explained-2025-edition".
- https://leetcode.com/discuss/post/5883632/ (SE2, Oct 2024, 45-min phone screen): "object manipulation — traversing a JSON object and manipulating the data, increasing parts"; Blind j2emp8mu (Feb 2025): "JSON manipulation/parsing question"; Blind jcnxxpsh: "Read in this JSON, transform it".
- https://leetcode.com/discuss/post/5740522/ (SDE2 India, Aug 2024, HackerRank): Part 1 build a map-like wrapper class with modifications; Part 2 use it to solve a simple problem/extend; Part 3 parse input in a specified string format (regex expected).
- https://leetcode.com/discuss/post/7307271/ (Oct 2025, 2.8 YOE): phone screen 45 min 2 parts; programming exercise 35 min "part 1 based on heaps"; integration 3 parts (3rd has 2 sub-parts). Blind sa3i71d8 (Oct 2025): same — "part 1 easy-medium heaps, 35-min limit, no minimum parts".
- https://leetcode.com/discuss/post/7566910/ (NG 2026, Feb 2026): OA one question; phone screen "solved 4 parts within 45 minutes"; VO round 1 multi-part programming (2 parts + edge-case follow-ups), bug squash, HM.
- https://leetcode.com/discuss/post/5150083/ comments: 2 parts of the currency problem were enough to pass (May 2024); similar to LC 399 Evaluate Division.
- https://leetcode.com/discuss/post/5740845/ comments: "one more part where multiple paths exist and you must choose the best exchange rate"; related LC discuss 1335225 "Find best exchange rate from currency1 to currency2".
- https://leetcode.com/discuss/post/5341224/ comment: follow-up with multiple brace groups, e.g. `"abc{xyzzy,zyx}d{aa, bb}a"` / `"over{crowd,eager,bold,fond}ness{test,yest}it"` → cartesian product.
- https://leetcode.com/discuss/post/1340172/ (2021 onsite): phone screen = coderpad, requirements added step by step; onsite = manager, design, coding (same as phone), debugging (45 min clone & fix; Scala graph lib vs Python), "build a feature from scratch in 45 min".
- https://leetcode.com/discuss/post/8315891/ (Jun 2026): new **"AI Programming Exercise"** round for L2 — HackerRank AI assistant + internet allowed; graded on architecture, design, testing, optimization. Blind te2f32ik (Jun 2026): "real-world problem, you direct the AI, validate output, catch edge cases".
- https://leetcode.com/discuss/post/7323123/ (2025-11-03): "got the Fraud Detection System problem, passed 17/25" (matches §1, 25 test cases).
- https://leetcode.com/discuss/post/2172363/ (2022): system design "Design Stripe subscriptions" (10M DAU, prorated partial billing, retries, trials, coupons, sales tax).
- Blind bowkiqj3 (Feb 2021, SWE): "searching string patterns in a list of strings" (Trie discussion), easy + slight modification.
- Blind 5o8fbzmm (Apr 2021): phone screen has 4 parts, need to reach part 3 (Python speeds this up); L4 got a single no-parts LC-hard-rated 45-min question.
- Blind 1dbqalav (Jun 2024): "medium graph traversal question broken into 3 parts"; "minimum completion cutoff → auto reject".
- Blind dlhvzujm (May 2026): "always very csv/dict oriented — use Python"; "start part 3 and verbally solve it to pass".
- Blind bj5ehdwf (Mar 2022, mid-level phone screen): parts 1a/1b/2a = closing-time problem (confirmed by commenter).

## A9. Threads checked with no problem content (LeetCode)
7693860, 7742111, 7310505, 5766378, 5918395, 7232803, 3986919, 4183369, 803981, 5817417, 5812646, 7395064, 7307417, 7274168, 7267196 (round outcomes only), 7295884, 7352963, 7469752, 7347231, 6135840, 5899185, 5809763, 6893501, 5742110, 4618551/4706280/5034301 (comp only), 3605450, 4057853, 3893189, 1167072, 900990, 1967328, 1778766, 6455374, 7022942, 5466148, 6640996, 5800181, 7626973, 7513430, 7925076, 6544422, 6616202, 4786019, 6398821.

## A10. Reddit
Reddit search (reddit.com/search.json, old.reddit, pullpush mirror) all blocked from this environment; web-search results for r/csMajors, r/cscareerquestions, r/leetcode returned no indexed Stripe-OA threads. Blind XgnQ0GjX (Sep 2019) references "reddit: a lot of people were having trouble with test case 9" on the 2019 HackerRank.

## A11. Accept-Language — Part 2 (language-only tags, `q` weights, `*` wildcard) — **MED** (programhelp reproduction of the well-known Stripe 4-part question; consistent with LC 4742657 Part 1)
Source: https://programhelp.net/en/vo/stripe-interview-process-explained-2025-edition/ (Aug 7 2025), linked from a Dec 2025 comment on LC 4742657.
- Part 2: header may contain non-region tags, e.g. `en` = any variant of English → expand to all supported specific variants. Examples (with q-values already mixed in):
  - `parse_accept_language("fr-FR;q=1, fr-CA;q=0, fr;q=0.5", ["fr-FR","fr-CA","fr-BG"])` → `["fr-FR","fr-BG","fr-CA"]` (q=0 tags sink to the end / are least preferred)
  - `parse_accept_language("fr-FR;q=1, fr-CA;q=0, *;q=0.5", ["fr-FR","fr-CA","fr-BG","en-US"])` → `["fr-FR","fr-BG","en-US","fr-CA"]`
  - `parse_accept_language("fr-FR;q=1, fr-CA;q=0.8, *;q=0.5", [...])` → `["fr-FR","fr-CA","en-US","fr-BG"]` (ties within same q may be any order)
- Canonical 4-part breakdown seen in public solutions: (1) exact tags; (2) language-only prefix match; (3) `*` wildcard for all remaining supported; (4) `;q=` weights, sort by q desc, header order on ties, q=0 excluded/last.

## A12. Virtual-onsite round contents (programhelp VO write-up, Aug 6 2025; corroborated by linkjob Aug 2025 and LC 7521596 Jan 2026) — **MED**
- Coding: "balance account balances to a target value" (bank-account rebalancing, §A3) — working solution first; follow-ups: minimum number of transactions (LC 465-style greedy/backtracking), and an audit approach ("dry run then compare with DB").
- Integration: clone repo, call given API ("BikeMap"), store response, write POST requests.
- Bug squash: Mako templating library — bug 1: missing check whether a path is a directory; bug 2: missing visitor function for a specific AST node causing a runtime error. (1p3a also lists "Mako Debug (Bug Bash)": clone, run failing tests, fix 2–3 bugs.)
- System design: "Ledger service" / "Metric counter" — API-design heavy (service layer + DB schema), not macro-architecture. Another reported SD: "architecture for delivering webhooks to customers" (LC 3102019).

## A13. Merchant scoring OA (§3) confirmed by a candidate — **MED→HIGH-MED**
Comment (2025-11-03) on https://leetcode.com/discuss/post/7323123/: "I think I did the same interview question early last week, if it had to do with the merchants, customers and transaction times according to a set of rules. I ended up getting all the test cases working and got an invite ~2 days later." → the merchant/customer/transaction-hour rule-scoring problem was live in the Oct–Nov 2025 OA cycle alongside the MCC fraud-detection problem (OP of 7323123 got "Fraud Detection System", 17/25).

## A14. Medium — Diyaag (SWE Intern, Bengaluru, off-campus, Nov 22 2025) — **HIGH** for format, no statement
https://medium.com/@diyaag2020/my-stripe-interview-experience-2025-2026-a-journey-to-the-final-round-19990fa6876a — OA mid-Sept 2025: HackerRank, 60 min, 1 question in 3 parts, "implementation-heavy, solve Part 1 to unlock Part 2"; completed all 3. Tech screen early Oct 2025: 60 min (45 coding), "medium-level problems involving Arrays, Maps, Strings", solved 2 of 3 parts; interviewer: "focus on readable, clean, maintainable code, not just optimization". VO: programming exercise = "parse raw input, preprocess, return structured output"; integration = private GitHub repo + API docs, sub-task A file ops/data extraction, sub-task B external API interaction and continuous output updates.
Medium @azn7u1 (Nov 14 2025) and @caoxinyi945 (Sep 23 2025) are the same text as LC 6896919 (programhelp marketing reposts): OA 60 min one data-processing question, tech screen 4 linked parts, VO coding "repeat of phone screen but must use built-in libraries", bug finding, integration (POST requests, 4+ parts).

---
# ADDENDUM B — new verbatim OA statements (LeetCode, Jul–Aug 2026)

## B1. Data-center registry + Haversine + proximity routing (OA, SSE3, Aug 2026) — **HIGH** (verbatim; upgrades §17)
Source: https://leetcode.com/discuss/post/8470971/ "Stripe OA 2026 | SSE3", 2026-08-19. HackerRank, **1 hour, must process stdin/stdout from scratch**.
- **Part 1**: commands `REGISTER <region> <latitude> <longitude> <capacity>` and `SET_HEALTHZ <region> <state>`. Output `OK` / `ERROR` per command. Rules: lat ∈ [-90,90]; lon ∈ [-180,180]; capacity > 0; region must NOT already exist for REGISTER, MUST exist for SET_HEALTHZ; lat/lon/capacity are integers; healthz is boolean; new regions healthy by default.
  Sample: `REGISTER us-east-1 38 120 100` → OK; `REGISTER us-west-2 50 112 30` → OK; `SET_HEALTHZ us-west-2 false` → OK; `REGISTER eu-east-1 -10 15 0` → ERROR.
- **Part 2**: `DISTANCE <lat1> <long1> <lat2> <long2>` → Haversine distance (formula given in the prompt), integer inputs, output rounded to integer. Sample: `DISTANCE 0 0 100 100` → `10200`.
- **Part 3**: `ROUTE <latitude> <longitude>` → output `<chosen_region> <distance> <candidate1> <candidate2> ...`: choose the healthy region that can handle the load (load starts at 0 for every region), nearest by Haversine, ties broken alphabetically; candidates = all healthy regions; unhealthy regions are neither routable nor candidates; if none → `NONE 0` (distance 0). Sample: `REGISTER us-east-1 0 0 1`, `REGISTER ap-south-1 0 0 1`, `ROUTE 0 0`, `SET_HEALTHZ ap-south-1 false`, `ROUTE 0 0` → `OK`, `OK`, `us-east-1 0 us-east-1 ap-south-1`, `NONE 0 us-east-1` (note: last line shows the still-healthy-but-at-capacity region listed as candidate while chosen = NONE because capacity 1 was consumed — i.e. ROUTE consumes capacity).
- PracHub (§17) has a JSON-array variant of the same problem with R = 6371 km and `floor(d+0.5)` rounding; 1p3a lists "Stripe L3 SWE OA on Datacenter Request Routing" (2026-08-11); InterviewDB "Proximity Request Routing"/"Request Router" (OA).

## B2. Fraud ring / "Six Degrees of Collusion" (OA, Jul 2026) — **HIGH** (verbatim examples)
Source: https://leetcode.com/discuss/post/8385570/ "Stripe Hackerank OA", 2026-07-09. **3 questions building on each other, 60 min, 20 hidden test cases**, custom test runs allowed, any language.
- **Q1 — find groups**: `transactions = ["A:d1", "B:d2", "C:d3", "D:d2", "B:d3"]` (`customer:device_id`; a customer may appear multiple times). Customers sharing a device are in the same group, transitively (B–C via d3, B–D via d2 → {B,C,D}; A alone) → `[{B,C,D},{A}]` (union-find / BFS on shared device ids).
- **Q2 — largest ring size**: `transactions = ["A:d1:123", "B:d2:456", "C:d3:123", "D:d2:789", "E:d2:123"]` adds `credit_card_id`; link on shared device OR shared card. Poster's answer: groups {A,C} (card 123) and {B,D,E} (device d2) → largest = 3. (Commenter notes E also has card 123, which would merge everything — likely a typo in the post; treat linking as union over both fields.)
- **Q3 — group risk factor**: `transactions = ["A:d1:123:90", "B:d2:456:50", "C:d3:123:0", "D:d2:789:100", "E:d2:123:30"]` adds `risk_factor`. Group risk = average risk of members, **but members with risk_factor = 0 are removed from the group first**. {A,C} → 90 (C removed); {B,D,E} → (50+100+30)/3 = 60 → output `[90, 60]`.
- Matches 1p3a OJ titles "Six Degrees of Collusion — Direct Links / Fraud Ring Size / Risk Scoring" and InterviewDB "Collusion — OA".

## B3. Intern phone-screen: query words within k (Jan 2024) — **HIGH**
Source: https://leetcode.com/discuss/post/4595354/ "Stripe Intern Interview Question", 2024-01-20. Given a large text and a query string of words (e.g. `"quick fox"`) and k, return the starting indices of the query's first word such that all query words appear within at most k words after it. Text `"The quick brown fox is quick...quick fox"`, query `"quick fox"`, k=2 → `[1, 20]`. Follow-up: preprocess the text (word → sorted index set) so repeated queries don't rescan the text.

## B4. VO "Integration — request replaying" and coding "Email Subscriptions" (Feb 2026) — **HIGH**
Source: https://leetcode.com/discuss/post/7595344/ (Backend SWE VO, 2026-02-21). Integration: implement a system that detects duplicate requests and processes each only once — parse JSON objects from a string and from a file, compare for equality, consolidate duplicates. Debug: Mako templating library, several bugs, large codebase with many unit tests (use a real debugger). Coding: "build a system that sends subscription-related emails (subscribe/expired/reminders): given a send schedule, a list of user subscriptions, output the sending schedule" + 2 follow-ups (= §7); question bank copy at https://offerretriever.com/questions/58.

## B5. Misc
- https://leetcode.com/discuss/post/6483328/ (Mar 2025): "Previously it was 2 out of 3 parts" needed to pass the phone screen.
- https://leetcode.com/discuss/post/5984403/ (Sr MLE, Sep 2024): screen = 1-hr ML integration in Jupyter (build target, train a better-than-random model) + 1-hr multi-part LC-easy coding; onsite bug squash = HackerRank link with trained model + package, 2 bugs.
- https://leetcode.com/discuss/post/7391608/ (intern VO Dec 2025): programming 3/3 parts, integration 3/3.
