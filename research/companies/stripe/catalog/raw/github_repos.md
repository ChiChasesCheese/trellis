# Stripe OA / Interview Problems — GitHub Repos & Gists Research

Research date: 2026-08-25. Focus: code repositories, gists, and repo-hosted problem statements.
Raw dumps of every fetched file are in `./raw/` and the aggregated per-repo dumps are
`joeytor.txt`, `femisowems.txt`, `sahaia1.txt`, `hazeera.txt`, `yingw787.txt`, `kushal.txt`,
`premjm.txt`, `kylelong.txt`, `suman.txt`, `twins.txt`, `sabiha.txt`, `am001.txt`, `trees.txt`.

## Key source repos (the gold mines)

| Repo | What it is | Value |
|---|---|---|
| https://github.com/joeytor/StripeInterview (mirror: https://github.com/arpit006/interview-stripe) | Java, 11 problems w/ **full prompts in file headers**; README lists phone/onsite/integration/bug-squash/system-design breakdown | **Highest** |
| https://github.com/femisowems/stripe-interview-questions | 6 HackerRank-style problems, each with `ProblemN.md` + `sample_input.txt` + `expected_output.txt` (verbatim I/O) | **Highest** |
| https://github.com/sahaia1/Stripe_Pyhton_libraries | Python versions of the same set (Radar rules, capital, currency graph, invoicer, money transfer, apibox tracker) | High |
| https://github.com/Hazeera65/stripe-interview | Phone-screen part1/2/3 statements (UTF-16 text files) + LC-mapped problems, round1 folder | High |
| https://github.com/yingw787/stripe-interview (2024-04-04) | closing-time problem w/ **pytest test vectors** | High |
| https://github.com/kylelong/stripe-interview | Radar Rules (ALLOW/BLOCK) HackerRank question w/ verbatim task comment | High |
| https://github.com/SabihaNazKhan/StripePhoneScreen24Nov25 (2025) | **Shipping cost** phone screen, full prompt in comments + tiered-pricing follow-up in code | High |
| https://github.com/TWINSRIRAM/Stripe_OA_Prep (2025-12/2026-01) | closing-time part1-3, shipping cost graph variant, brace expansion, LC set | Medium-High |
| https://github.com/freecodemessiah/stripe-interview | Two Jupyter notebooks with the **verbatim `min_by_key`/`first_by_key`/comparator** prompt | High |
| https://gist.github.com/stealthbomber10/d85d44776ad58ba66d84ff76fd5be736 (2018-10-10) | apibox/sitebox server allocator | High |
| https://gist.github.com/aranibatta/ffa87e94d117a86fc05b6940e626ee56 (2016-09-01) | same allocator, w/ unittest vectors | High |
| https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1 (2023-10-15) | Kotlin solution to closing-time parts 1-3 | Medium |
| https://github.com/prashantrai/Algo_DS_InterviewPrep `src/Stripe/` | StoreHours.java, AnalyzeServerProcessUptimeLog.java | Medium (not yet fetched) |
| https://github.com/SogAniMic/Stripe_coding_challenge (2023-01-27) | MultiTimeMap + first missing positive w/ prompts | Medium |
| https://github.com/Murillo2380/interview-coding-solutions | `medium-stripe-timestamp-cache` | Medium |
| https://github.com/Shivam5022/Interview-Experiences (181★) | Stripe round-by-round format writeup (2025) | Medium |
| https://github.com/ombharatiya/FAANG-Coding-Interview-Questions | Stripe section: 19 LC-mapped + custom problem list + 2026 format notes | Medium |
| https://github.com/Molakim/stripeCoding | **DMCA-taken-down by Stripe 2022-05-17** (https://github.com/github/dmca/blob/master/2022/05/2022-05-17-stripe.md) — was ALLOW/BLOCK charge rules | n/a |
| https://github.com/stripe-interview/* (official org) | Stripe's own per-language interview *setup* repos (python/java/js/cpp/kotlin/react-native) — environment only, no problems | Low |

---

# PROBLEMS

## 1. Store Closing Time Penalty (a.k.a. Minimum Penalty for a Shop)
**Confidence: HIGH** — the single most-attested Stripe problem. Also LeetCode 2483 (Stripe tag freq 100%).

**Sources / stages**
- https://github.com/Hazeera65/stripe-interview/tree/main/round1/PhoneScreen (parts 1/2/3) — **Phone screen**, repo created 2025-12-31
- https://leetcode.com/discuss/post/2585038/ — "Stripe | Phone Screen | Senior SE | Reject" (2022)
- https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1 — 2023-10-15, Kotlin
- https://github.com/yingw787/stripe-interview — "Interview w/ Stripe 04/04/2024"
- https://github.com/femisowems/stripe-interview-questions/tree/main/question4 — OA framing
- https://github.com/TWINSRIRAM/Stripe_OA_Prep/tree/main/part1-3 — OA, 2025-12
- https://github.com/premjm-67/stripe-interview-questions `MP.java`

**Statement (verbatim from femisowems/question4/Problem4.md)**
> We own a store that records, hour by hour, whether there were customers shopping. Each hour is marked with a single letter: `'Y'` if there were customers during that hour, `'N'` if the store was empty during that hour.
> ```
> hour:         | 1 | 2 | 3 | 4 |
> log:          | Y | Y | N | Y |
> ```
> We want to analyze when we should have closed the store to minimize wasted hours. The closing time is expressed as an integer from 0 to n: `0` → never open at all; `n` → open the entire day.
> ```
> hour:         | 1 | 2 | 3 | 4 |
> closing_time: 0  1  2  3  4
> ```
> **Penalty**: `+1` for every hour we were open with no customers (unnecessary open time); `+1` for every hour we were closed with customers present (lost opportunity).
> - **Part 1: Compute Penalty** — For a given log and closing time, compute the total penalty.
> - **Part 2: Find Best Closing Time** — Return the closing time that yields the minimum penalty. If multiple closing times yield the same minimum penalty, return the smallest closing time.
> - **Part 3: Aggregate Logs** — Sometimes, employees record multiple days' logs in one file. Valid logs are sequences that: Start with `BEGIN`; Followed by zero or more `'Y'`/`'N'` characters (with optional whitespace); End with `END`. Rules: Valid logs cannot be nested (no `BEGIN ... BEGIN ... END` inside). Valid logs can span multiple lines. There may be multiple valid logs per line. Extra garbage text or unfinished logs must be ignored.
> Output: For each valid log found (in order), output the best closing time on a separate line.

**Sample I/O (femisowems, verbatim)**
```
sample_input.txt:
BEGIN
Y Y N Y N N N Y Y N
END
GARBAGE
BEGIN
N N Y Y Y N Y Y
END

expected_output.txt:
2
8
```
(NB: the `Problem4.md` prose example claims `4` / `7`; the repo's actual expected_output is `2` / `8`. The Problem4.md walkthrough is inconsistent with its own harness — treat `2`/`8` as the code's output.)

**Verbatim test vectors from yingw787/stripe-interview (pytest, 2024)**
```python
compute_penalty("Y Y N Y", 0) == 3
compute_penalty("N Y N Y", 2) == 2
compute_penalty("Y Y N Y", 4) == 1
compute_penalty("", 0) == 0
compute_penalty("Y Y N", 0) == 2
compute_penalty("Y Y N Y", 1) == 2
compute_penalty("Y Y Y N N N N", 0) == 3
compute_penalty("Y Y Y N N N N", 7) == 4
compute_penalty("Y Y Y N N N N", 3) == 0
compute_penalty("Y N Y N N N N", 3) == 1

find_best_closing_time("Y Y N N") == 2
find_best_closing_time("Y Y Y N N N N") == 3
find_best_closing_time("") == 0
find_best_closing_time("Y") == 1
find_best_closing_time("N N N N") == 0
find_best_closing_time("Y Y Y Y") == 4
find_best_closing_time("N Y Y Y Y N N N Y N N Y Y N N N N Y Y N N Y N N N") == 5
find_best_closing_time("N N N N N Y Y Y N N N N Y Y Y N N N Y N Y Y N Y N") == 0
find_best_closing_time("Y Y N N N Y Y N Y Y N N N Y Y N N Y Y Y N Y N Y Y") == 25

find_best_closing_times("BEGIN Y Y END \nBEGIN N N END") == [2, 0]
find_best_closing_times("BEGIN BEGIN \nBEGIN N N BEGIN Y Y\n END N N END") == [2]
```

**Hazeera65 part-2 worked example (verbatim, decoded from UTF-16)**
> Input: "YYNY" — Closing at hour 0: Penalty = 3; hour 1: Penalty = 2; hour 2: Penalty = 1; hour 3: Penalty = 2; hour 4: Penalty = 1. Earliest minimum penalty is at hour 2.

**Hazeera65 part-3 notes**: input may contain nested/multiple BEGIN…END; solution uses a **stack** of BEGIN indices, pops on END, concatenates tokens between them, and computes the penalty per block. Example given: innermost block `Y Y N Y` → penalty 2; next block `BEGIN Y Y N Y END Y Y N N` → penalty 0.

**Approach**: prefix/suffix counts or one-pass running penalty (start = count of all 'Y', then per hour: 'Y' → −1, 'N' → +1; track min with earliest index). Part 3 = stack-based tokenizer.

---

## 2. Server Process Uptime Log / Best Removal Time (0/1 twin of #1)
**Confidence: HIGH**

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/ServerPenalty.java` (README lists it under **Phone Interview**); mirrored in https://github.com/prashantrai/Algo_DS_InterviewPrep `src/Stripe/AnalyzeServerProcessUptimeLog.java`.

**Statement (verbatim from ServerPenalty.java header)**
> Throughout this interview, we'll write code to analyze a simple server process uptime log. These logs are much simplified, and are just strings of space separated 0's and 1's. The log is a string of binary digits (e.g. "0 0 1 0"). Each digit corresponds to 1 hour of the server running:
> `"1" = <crashed>, "down"` — server process crashed during the hour; `"0" = <didn't crash>, "up"`.
> EXAMPLE: A server with log "0 0 1 0" ran for 4 hours and its process crashed during hour #3.
> ```
> hour: |1|2|3|4|
> log : |0|0|1|0|
> ```
> We can *permanently remove* a server at the beginning of any hour during its operation. A server is on the network until it is removed. Note that a server stays POWERED ON after removal, it's just not on the network. We'd like to understand the best times to remove a server. So let's introduce an aggregate metric called a "penalty" for removing a server at a bad time.
> ```
> hour : | 1 | 2 | 3 | 4 |
> log  : | 0 | 0 | 1 | 0 |
> remove_at: 0 1 2 3 4   // remove_at being `x` means "server removed before hour `x+1`"
> ```
> We define our penalty like this: `+1` penalty for each DOWN hour when a server is on the network; `+1` penalty for each UP hour after a server has been removed.
> Note that for a server log of length `n` hours, the remove_at variable can range from 0, meaning "before the first hour" to n, meaning "after the final hour".
> **1a)** Write a function `compute_penalty`, that computes the total penalty, given a server log (as a string) AND a time at which we removed the server from the network (call that variable `remove_at`). In addition to writing this function, you should use tests to demonstrate that it's correct.
> Examples: `compute_penalty("0 0 1 0", 0)` should return `3`; `compute_penalty("0 0 1 0", 4)` should return `1`
> **1b)** Use your answer for compute_penalty to write another function `find_best_removal_time`, that returns the best remove_at hour, given a server log.
> Example: `find_best_removal_time("0 0 1 1")` should return `2`
> **2a)** Now that we're able to analyze single server logs, let's analyze some aggregate logs. Aggregate logs are text files that contain lots of logs. The files contain only BEGIN, END, 1, 0, spaces and newlines. Aggregate logs include some servers that aren't actually finished, so we might have some BEGINs scattered throughout. We'll only consider inner BEGINs and ENDs to be valid log sequences. Put another way, any sequence of 0s and 1s surrounded by BEGIN and END forms a valid sequence. For example, the sequence `"BEGIN BEGIN BEGIN 1 1 BEGIN 0 0 END 1 1 BEGIN"` has only one valid sequence `"BEGIN 0 0 END"`. Write a function `get_best_removal_times`, that takes the file's contents as a parameter, and returns an array of best removal hours for every valid server log in that file. Note: that logs can span 1 or many lines.
> Example: `get_best_removal_times("BEGIN BEGIN \nBEGIN 1 1 BEGIN 0 0\n END 1 1 BEGIN")` should return an array: `[2]`

---

## 3. HTTP Accept-Language Header Parser
**Confidence: HIGH** — long-standing Stripe phone screen.

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/HttpHeaderParser.java` (README → **Phone Interview**); https://adonais0.github.io/20210603/interview-stripe/ (phone, 2021-06); Glassdoor QTN_4469893.

**Statement (verbatim from HttpHeaderParser.java header)**
> **Part 1** — In an HTTP request, the Accept-Language header describes the list of languages that the requester would like content to be returned in. The header takes the form of a comma-separated list of language tags. For example: `"Accept-Language: en-US, fr-CA, fr-FR"` means that the reader would accept: 1. English as spoken in the United States (most preferred) 2. French as spoken in Canada 3. French as spoken in France (least preferred).
> We're writing a server that needs to return content in an acceptable language for the requester, and we want to make use of this header. Our server doesn't support every possible language that might be requested (yet!), but there is a set of languages that we do support. Write a function that receives two arguments: an Accept-Language header value as a string and a set of supported languages, and returns the list of language tags that will work for the request. The language tags should be returned in descending order of preference (the same order as they appeared in the header). In addition to writing this function, you should use tests to demonstrate that it's correct, either via an existing testing system or one you create.
> ```
> parse_accept_language("en-US, fr-CA, fr-FR", ["fr-FR", "en-US"])  -> ["en-US", "fr-FR"]
> parse_accept_language("fr-CA, fr-FR", ["en-US", "fr-FR"])         -> ["fr-FR"]
> parse_accept_language("en-US", ["en-US", "fr-CA"])                -> ["en-US"]
> ```
> **Part 2** — Accept-Language headers will often also include a language tag that is not region-specific — for example, a tag of "en" means "any variant of English". Extend your function to support these language tags by letting them match all specific variants of the language.
> ```
> parse_accept_language("en", ["en-US", "fr-CA", "fr-FR"])        -> ["en-US"]
> parse_accept_language("fr", ["en-US", "fr-CA", "fr-FR"])        -> ["fr-CA", "fr-FR"]
> parse_accept_language("fr-FR, fr", ["en-US", "fr-CA", "fr-FR"]) -> ["fr-FR", "fr-CA"]
> ```
> **Part 3** — Accept-Language headers will sometimes include a "wildcard" entry, represented by an asterisk, which means "all other languages". Extend your function to support the wildcard entry.
> ```
> parse_accept_language("en-US, *", ["en-US", "fr-CA", "fr-FR"])     -> ["en-US", "fr-CA", "fr-FR"]
> parse_accept_language("fr-FR, fr, *", ["en-US", "fr-CA", "fr-FR"]) -> ["fr-FR", "fr-CA", "en-US"]
> ```

**Variant (2026 OA reports, medium confidence)**: some write-ups add **q-values**: input `"en-US,en;q=0.8,fr;q=0.9,de;q=0.7"` → sort by q desc (default 1.0), ties by appearance → `["en-US","fr","en","de"]`. (programhelp.net, Sept 2025.)

**Edge cases**: dedupe already-emitted variants (see solution: remove matched region from the map so `"fr-FR, fr"` doesn't repeat fr-FR); wildcard must exclude already-listed languages and preserve supported-list order.

---

## 4. Stripe Capital — Loan Bookkeeping
**Confidence: HIGH**

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/StripeCapital.java` (README → **Phone Interview**); Python variant https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/capital.py. Also matches Shivam5022's described OA ("parse a command string and execute commands simulating transactions between users' bank accounts", 60-min HackerRank, 2025).

**Statement (verbatim from StripeCapital.java header)**
> Stripe Capital lends our merchants funds in order to grow their businesses. In exchange for these funds, instead of a traditional interest over time model, Stripe charges a fixed loan fee on top of the original loan amount. To get back the investment, some percentage of the merchant's future sales goes towards repayment, until the total owed amount is repaid.
> In this problem, you'll be building a bookkeeping system for a modified version of Stripe Capital. This bookkeeping system will have 4 API methods: 1. A merchant can create a loan. 2. A merchant can pay down a loan manually. 3. A merchant can process transactions, from which some percentage of the processed amount goes towards repayment towards a loan. 4. A merchant can increase an existing loan's amount.
> **Your Task**: 1. Evaluate each line of stdin, performing the actions as described by documentation below. Each line will always begin with an API method, followed by a colon and a space, then followed by comma separated parameters for the API method, in order of the documentation. 2. After evaluating all actions, print out a list of `$merchant_id, $outstanding_debt` pairs, skipping over merchants who do not have an outstanding balance. This list should be lexicographically sorted by the merchant ID.
> Keep in mind: We will not test you against unparsable input formats. Handle them as you see fit. We will evaluate both code correctness and code quality. You are allowed to refer the web to make sure of various resources, tools, and documentation. However, do not copy code verbatim.
> **API Documentation**
> `CREATE_LOAN`: Merchant initiates a loan. Fields: merchant_id (String; non-empty), loan_id (String; non-empty), amount (Integer; x >= 0). Ex: `CREATE_LOAN: merchant1, loan1, 1000`
> `PAY_LOAN`: Merchants pays off their loans on a one-time basis. Fields: merchant_id, loan_id, amount (the amount given back to Stripe). Ex: `PAY_LOAN: merchant1, loan1, 1000`
> `INCREASE_LOAN`: Merchant increases an existing loan. Fields: merchant_id, loan_id, amount (the amount to increase the loan by).
> `TRANSACTION_PROCESSED`: A single transaction. A portion of the transaction amount is withheld to pay down the merchant's outstanding loans. Fields: merchant_id, loan_id, amount, repayment_percentage (Integer; 1 <= x <= 100). Ex: `TRANSACTION_PROCESSED: merchant1, loan1, 500, 10`
> **System Behavior**: This version of Capital will represent all monetary amounts as U.S. cents in integers (e.g. amount = 1000 => $10.00 USD). A merchant may have multiple outstanding loans. Loan IDs are unique to a given merchant only. A loan's outstanding balance should never go negative. Ignore the remaining amount in the case of overpayment. Truncate repayments when applicable (e.g. if withholding from a transaction is 433.64 cents, truncate to 433 cents). Your system should handle invalid API actions appropriately (ex: attempting to pay-off a nonexistent loan).

**Verbatim examples**
```
Example 0 (manual repayment):
  CREATE_LOAN: acct_foobar,loan1,5000
  PAY_LOAN: acct_foobar,loan,1000
Expected Output:
  acct_foobar,4000

Example 1 (transaction repayment):
  CREATE_LOAN: acct_foobar,loan1,5000
  CREATE_LOAN: acct_foobar,loan2,5000
  TRANSACTION_PROCESSED: acct_foobar,loan1,500,10
  TRANSACTION_PROCESSED: acct_foobar,loan2,500,1
Expected Output:
  acct_foobar,9945

Example 2 (multiple actions):
  CREATE_LOAN: acct_foobar,loan1,1000
  CREATE_LOAN: acct_foobar,loan2,2000
  CREATE_LOAN: acct_barfoo,loan1,3000
  TRANSACTION_PROCESSED: acct_foobar,loan1,100,1
  PAY_LOAN: acct_barfoo,loan1,1000
  INCREASE_LOAN: acct_foobar,loan2,1000
Expected Output:
  acct_barfoo,2000
  acct_foobar,3999
```

---

## 5. Radar Rules — ALLOW/BLOCK charge evaluation
**Confidence: HIGH** (repo explicitly says "Stripe HackerRank interview question"; a second repo with the same problem was **DMCA'd by Stripe**, strong evidence of authenticity)

**Sources**: https://github.com/kylelong/stripe-interview/blob/master/RadarRules.java; Python: https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/radarrules.py; https://github.com/Molakim/stripeCoding (**451 / DMCA takedown by Stripe, 2022-05-17**).

**Statement (verbatim task comment from RadarRules.java)**
```
Task:
	Basic Block:
		In:["CHARGE: card_country=US&currency=USD&amount=150&ip_country=CA","BLOCK:amount > 100",]
    	Out: 0
    Compound Block:
    	In: ["CHARGE: card_country=US&currency=USD&amount=150&ip_country=CA","ALLOW:amount<100","BLOCK:card_country != ip_country AND amount > 100",]
		Out: 0
```

**Expanded statement (from sahaia1/radarrules.py trailing notes, verbatim)**
> You are given a system that evaluates financial transactions based on a set of rules. Each transaction has details such as the card's country of origin, the currency used, the transaction amount, and the IP country from which the transaction is initiated. The system needs to determine whether to allow or block a transaction based on these details.
> You need to implement a method that processes a list of rules and decides the outcome of a transaction. The rules are provided as strings in the format:
> `"CHARGE: card_country=XX&currency=XXX&amount=NNN&ip_country=YY"`, `"ALLOW:condition"`, `"BLOCK:condition"`.
> The method should return `0` if the transaction is blocked, `1` if the transaction is allowed.
> Key Points to Discuss: String Parsing — how would you efficiently parse and extract relevant fields; Condition Evaluation — how do you evaluate conditions dynamically, especially when multiple conditions are combined (e.g. `card_country != ip_country AND amount > 100`); Edge Cases — invalid formats or unexpected conditions.
> Example: `["CHARGE: card_country=US&currency=USD&amount=150&ip_country=CA", "BLOCK:amount > 100"]` → Expected Output: `0` (amount exceeds 100 → blocked).
> Example: `["CHARGE: ...amount=150&ip_country=CA", "ALLOW:amount<100", "BLOCK:card_country != ip_country AND amount > 100"]` → `0`.
> Further discussion: Design decisions (classes/methods for scalability & maintainability), optimizations for large sets of rules and transactions.

**Rule grammar observed**: fields `card_country`, `currency`, `amount`, `ip_country`; operators `>`, `<`, `==`, `!=`; up to **2 rules combined with `AND` / `OR`**; both field-vs-literal and **field-vs-field** comparisons (`card_country != ip_country`).

---

## 6. Wishlist / Mutual-Rank Apartment Swaps
**Confidence: HIGH**

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/MutualRank.java` (README → **Phone Interview**); https://adonais0.github.io/20210603/interview-stripe/ ("Wishlist", **phone**, 2021).

**Statement (verbatim from MutualRank.java header)**
> **Part 1** — Imagine an Airbnb-like vacation rental service, where users in different cities can exchange their apartment with another user for a week. Each user compiles a wishlist of the apartments they like. These wishlists are ordered, so the top apartment on a wishlist is that user's first choice for where they would like to spend a vacation. You will be asked to write part of the code that will help an algorithm find pairs of users who would like to swap with each other.
> Given a set of users, each with an *ordered* wishlist of other users' apartments:
> ```
> a's wishlist: c d
> b's wishlist: d a c
> c's wishlist: a b
> d's wishlist: c a b
> ```
> The first user in each wishlist is the user's first-choice for whose apartment they would like to swap into. Write a function called `has_mutual_first_choice()` which takes a username and returns true if that user and another user are each other's first choice, and otherwise returns false.
> ```
> has_mutual_first_choice('a') // true (a and c)
> has_mutual_first_choice('b') // false (b's first choice does not *mutually* consider b as their first choice)
> ```
> Then expand the base case beyond just "first" choices, to include all "mutually ranked choices". Write another function which takes a username and an option called "rank" to indicate the wishlist rank to query on. If given a rank of 0, you should check for a first choice pair, as before. If given 1, you should check for a pair of users who are each others' second-choice. Call your new function `has_mutual_pair_for_rank()` and when done, refactor `has_mutual_first_choice()` to depend on your new function.
> ```
> has_mutual_pair_for_rank('a', 0) // true (a and c)
> has_mutual_pair_for_rank('a', 1) // true (a and d are mutually each others' second-choice)
> data = { 'a': ['c','d'], 'b': ['d','a','c'], 'c': ['a','b'], 'd': ['c','a','b'] }
> ```
> **Part 2** — Every wishlist entry in the network is either "mutually ranked" or "not mutually ranked" depending on the rank the other user gives that user's apartment in return. The most common operation in the network is incrementing the rank of a single wishlist entry on a single user. This swaps the entry with the entry above it in that user's list. Imagine that, when this occurs, the system must recompute the "mutually-ranked-ness" of any pairings that may have changed. Write a function that takes a username and a rank representing the entry whose rank is being bumped up. Return an array of the users whose pairings with the given user *would* gain or lose mutually-ranked status as a result of the change, if it were to take place. Call your function `changed_pairings()`
> ```
> // if d's second choice becomes their first choice, a and d will no longer be a mutually ranked pair
> changed_pairings('d', 1) // returns ['a']
> // if b's third choice becomes their second choice, c and b will become a mutually ranked pair (mutual second-choices)
> changed_pairings('b', 2) // returns ['c']
> // if b's second choice becomes their first choice, no mutually-ranked pairings are affected
> changed_pairings('b', 1) // returns []
> ```

(adonais0 names the third part `changed_antipairings(username, rank)` — same idea.)

---

## 7. Money Transfer / Bank Account Rebalancing
**Confidence: HIGH**

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/MoneyTransfer.java` (README → **Virtual Onsite / Coding**); https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/money_transfer.py; adonais0 "Account Balance" (onsite/phone).

**Statement (verbatim)**
> At Stripe we keep track of where the money is and move money between bank accounts to make sure their balances are not below some threshold. This is for operational and regulatory reasons, e.g. we should have enough funds to pay out to our users, and we are legally required to separate our users' funds from our own. This interview question is a simplified version of a real-world problem we have here. Let's say there are at most 500 bank accounts, some of their balances are above 100 and some are below. How do you move money between them so that they all have at least 100? Just to be clear we are not looking for the optimal solution, but a working one.
> ```
> Example input:            Output:
> - AU: 80                  - from: US, to: AU, amount: 20
> - US: 140                 - from: US, to: FR, amount: 20
> - MX: 110                 - from: MX, to: FR, amount: 10
> - SG: 120
> - FR: 70
> ```
> **Follow-up 1** (verbatim CN in repo): 反过来问，假设给你一系列 transfer，问最后 account balance 是否满足条件。假设所给 account balance 无论如何也无法做到每个 account >= 100，问所给的 transfer 是不是 best effort？ — i.e. given a list of transfers, verify final balances satisfy the constraint; if it's impossible for all accounts to reach 100, determine whether the given transfers are a best-effort solution.
> **Follow-up 2**: 如何得到最优解？…面试官说转账次数越少越好。这样和 LC0465 就很像了 — how to get the optimal solution? Interviewer defines optimal as fewest transfers → becomes LeetCode 465 Optimal Account Balancing.

**Approach**: sort balances, two-pointer from richest to poorest, `amount = min(from-100, 100-to)`. Optimal variant = DFS/bitmask DP over non-zero balances (LC465). Hazeera65 has a whole `round1/465optimalaccountBalancing/` folder with an LC465 writeup, confirming the follow-up is asked.

---

## 8. Invoicer / Invoice Reminder Email Schedule
**Confidence: HIGH**

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/Invoicer.java` (README → **Virtual Onsite / Coding**); Python https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/invoicer.py; Glassdoor QTN_8287053 (verbatim OA text).

**Statement (Glassdoor, verbatim excerpt)**
> For this question, you will be outputting the subject line of each email we send for customers' invoices in sorted order. (Use any library/tool for sorting). Your invoicing system will need to be able to configure a reminder schedule. For example, you might want to send one email 10 days before the invoice comes out, one email when the invoice comes out, one email 20 days after the invoice comes out, and one email when the invoice is due, which is 30 days from when the invoice first…

**Schedule used in the reference solution (Invoicer.java)**
```java
sendSchedule.put(-10, "Upcoming");
sendSchedule.put(0,   "New");
sendSchedule.put(20,  "Reminder");
sendSchedule.put(30,  "Due");
```
**Output format (verbatim from code)**: `timestamp + ": [" + schedule + "] Invoice for " + name + " for " + amount + " dollars"`
**Driver / sample**
```java
sol.addInvoice(0, "Alice", 200);
sol.addInvoice(1, "Bob", 100);
// messages sorted ascending by scheduled timestamp
```
Invoice JSON shape in the repo: `{"invoice_time": <int>, "name": "<string>", "amount": <int>}`.

---

## 9. Subscription Notification Scheduler (evolution of #8 — the 2025/2026 OA version)
**Confidence: HIGH** (statement + verbatim sample I/O in repo)

**Sources**: https://github.com/femisowems/stripe-interview-questions/tree/main/question5 (created 2026-05-01, sourced from linkjob.ai's 2026 OA writeup); corroborated by linkjob.ai (reported 2025-09-16 HackerRank OA), 1point3acres "Email Subscription", showoffer "Subscription Email Scheduler", hackerprep "Dunning Email Reminder", oavoservice 2026.

**Statement (verbatim from Problem5.md)**
> You are asked to implement a notification system for subscription plans. Each user subscribes to a plan with a start date and a duration (in days). You must schedule and print emails at the correct dates based on the rules provided.
> **Part 1: Basic Email Scheduling.** Input: `send_schedule` – A mapping from relative day offsets to email message types: `"start"` → send on the subscription start day; Negative integers (e.g., `-15`) → send before subscription end date; `"end"` → send on the subscription end date. `user_accounts` – A list of user dictionaries with: `name`, `plan`, `account_date` (int; day subscription started), `duration` (int; days).
> Output: Print one line for each email event in ascending order of day. Each line format: `<day>: [<Email Type>] Subscription for <name> (<plan>)`
> **Part 2: Handling Plan Changes.** Now you are given an additional input: a list of plan change events. When a user changes plan, you must: Print a `[Changed]` message on the change date; Recalculate the remaining duration relative to the change date; Schedule future notifications (upcoming-expiry, expired) based on the new plan and updated timeline. Input `changes` – list of dicts: `{name, new_plan, change_date}`.
> **Part 3: Bonus - Renewals.** In addition to plan changes, you now have renewal events in the change list. Each renewal extends the subscription duration by the given number of days. You must: Print `[Renewed]` on the renewal date; Reschedule future emails based on the new end date. `changes` may now have two kinds of events: Plan change `{name, new_plan, change_date}`; Renewal `{name, extension, change_date}`.

**Verbatim sample I/O (repo files)**
```
sample_input.txt:
start,upcoming_expiry,-5,expired
2
alice,premium,0,30
bob,basic,5,20
2
CHANGE,alice,plus,15
RENEW,bob,10,20

expected_output.txt:
0: [start] Subscription for alice (premium)
5: [start] Subscription for bob (basic)
15: [Changed] Subscription for alice (plus)
19: [upcoming_expiry] Subscription for bob (basic)
20: [Renewed] Subscription for bob (basic)
24: [expired] Subscription for bob (basic)
24: [upcoming_expiry] Subscription for alice (plus)
29: [expired] Subscription for alice (plus)
29: [upcoming_expiry] Subscription for bob (basic)
34: [expired] Subscription for bob (basic)
```
**Worked reasoning given in Problem5.md**: Alice starts premium day 0, ends day 29 → start d0, upcoming_expiry d24 (29−5), expired d29. Bob starts basic d5, ends d24 → start d5, upcoming_expiry d19, expired d24. Alice changes to plus on d15: remaining = 29−15 = 14, new end = 15+14 = 29 (no reschedule as end stays same). Bob renews d20 extending 10 days → new end 34 → upcoming_expiry d29, expired d34.

**Edge cases**: events already emitted before the change/renewal must not be re-emitted; superseded future events (bob's original d24 expired) still appear in this expected output — i.e. the naive "emit then also emit new" behaviour is what the harness expects. In `send_schedule`, only `"start"` and `"end"` are fixed keys; **every other key is a number** (dynamic).

---

## 10. Atlas Company Name Availability Check
**Confidence: HIGH** (statement + verbatim I/O in repo; reported as HackerRank OA problem 1)

**Sources**: https://github.com/femisowems/stripe-interview-questions/tree/main/question1; linkjob.ai (2025-09-16 OA), extrabrain, programhelp.

**Statement (verbatim from Problem1.md)**
> **Background** — Stripe Atlas lets founders register a US company remotely. A core step is verifying whether a proposed company name is available. The check considers names unavailable not only for exact matches but also when names are considered equivalent under a set of normalization rules.
> **Part 1 — Basic Name Availability Check.** Task: Determine whether a proposed company name is available by normalizing it and comparing it against previously registered names (using the same normalization rules).
> Normalization rules (apply to both existing and proposed names):
> - Ignore case ("Llama, Inc." == "LLAMA, Inc.").
> - Treat `&` and `,` as spaces.
> - Collapse consecutive spaces into a single space.
> - Remove standard company suffixes (case-insensitive): `Inc.`, `Corp.`, `LLC`, `L.L.C.`, `LLC.`
> - Ignore a leading article: `The`, `An`, or `A` (e.g., "The Llama" == "Llama").
> - Ignore the word `And` unless it appears at the start of the name. (E.g., "Llama And Friend" == "Llama Friend"; but "And Llama Friend" is distinct.)
> - If the normalized name is empty or contains only spaces, treat it as unavailable.
> Input format (Part 1): Each request is a single line: `account_id|proposed_name`.
> Output format: For each request, output `account_id|Name Available` or `account_id|Name Not Available`. If a name is declared available, register it immediately so it becomes unavailable for subsequent requests.
> **Part 2 — Persistent Registration Tracking.** Extend Part 1 so that the system maintains a persistent record of all registered names. Any re-submission (by the same account or another) of a name that normalizes to an already-registered name should be marked unavailable.
> **Part 3 — Name Reclamation Requests.** Support reclamation (dissolution) requests that free previously registered names for reuse. Reclamation input format: `RECLAIM,account_id,original_proposed_name`. Behavior: When processing a reclamation, remove the normalized form of `original_proposed_name` from the registered (unavailable) set. Only the account that originally registered the name may reclaim it. If the requester is not the original registrant, ignore the reclaim request (or treat it as invalid).
> Example normalization: `The Llama, Inc.` -> `llama`.

**Verbatim sample I/O**
```
sample_input.txt:
1|Llama, Inc.
2|The Llama
3|Llama And Friend, Inc.
4|And Llama Friend, Inc.
5|Llama,  Inc.
6| &Co, LLC.
RECLAIM,1,Llama, Inc.
7|Llama
8|Co
9|and co
RECLAIM,6, &Co, LLC.
10|Co

expected_output.txt:
1|Name Available
2|Name Not Available
3|Name Available
4|Name Available
5|Name Not Available
6|Name Available
7|Name Available
8|Name Not Available
9|Name Available
10|Name Available
```
**Note the traps**: `2` normalizes to the same as `1`; `4` ("And Llama Friend") is distinct from `3` because leading `And` is kept; `5` differs from `1` only by double space → not available; after `RECLAIM,1` the name frees up so `7|Llama` is available; `8|Co` collides with the earlier `&Co, LLC.`; `9|and co` → leading "and" kept → distinct; after reclaim of `6`, `10|Co` is available again.

---

## 11. Card Range Obfuscation (BIN gap filling)
**Confidence: HIGH**

**Sources**: https://github.com/femisowems/stripe-interview-questions/tree/main/question2; linkjob.ai / extrabrain OA writeups.

**Statement (verbatim from Problem2.md)**
> Payment card numbers consist of 8-19 digits, with the first 6 digits referred to as the Bank Identification Number (BIN). For a given BIN, all 16-digit card numbers starting with that BIN are considered to be in the BIN range. For example, the BIN 424242 corresponds to card numbers from 4242420000000000 (inclusive) through 4242429999999999 (inclusive).
> Stripe's card metadata API may return partial coverage of this BIN range, by providing a list of intervals mapping to card brands (e.g., VISA, MASTERCARD). However, these intervals may have gaps (at the beginning, middle, or end of the BIN range), which can be exploited by fraudsters to probe for valid cards.
> The task is to fill in missing intervals so that the returned intervals fully cover the entire BIN range, with no gaps, and return them in sorted order.
> **Input Format**: Line 1: A 6-digit BIN. Line 2: A positive integer n, the number of intervals. Next n lines: `start,end,brand` where start and end are 10-digit numbers representing the offset within the BIN range (inclusive), and brand is an alphanumeric string.
> **Output Format**: A list of sorted, gap-free intervals formatted as `start,end,brand` where start and end are now full 16-digit card numbers (BIN + 10-digit offset), sorted by start.
> **Notes**: If the input intervals already cover the full BIN range, just return them sorted. If there are gaps, fill them so that no range is uncovered. Be careful with inclusive endpoints: ensure full coverage from BIN0000000000 to BIN9999999999.

**Verbatim sample I/O**
```
sample_input.txt:
777777
2
1000000000,3999999999,VISA
4000000000,5999999999,MASTERCARD

expected_output.txt:
7777770000000000,7777773999999999,VISA
7777774000000000,7777779999999999,MASTERCARD
```
Note the harness **extends the last brand to the end of the range** and **extends the first brand backwards to offset 0** (input started at 1000000000 but output starts at ...0000000000 as VISA) — i.e. gaps are absorbed by the adjacent interval rather than emitted as a separate "unknown" brand. The Problem2.md prose example shows a different (unextended) output — trust the expected_output.txt.

---

## 12. "Catch Me If You Can" — Merchant Fraud Detection (CHARGE / DISPUTE)
**Confidence: HIGH**

**Sources**: https://github.com/femisowems/stripe-interview-questions/tree/main/question3; interviewfox (new-grad HackerRank, July 2026, 5 parts); linkjob.ai; 1point3acres 2026 intern OA.

**Statement (verbatim from Problem3.md)**
> Stripe processes a large stream of merchant transactions and needs a simple fraud model that can mark merchants as fraudulent when their observed suspicious activity crosses a threshold. This version supports three ideas: Count-based thresholds for MCCs; Percentage-based thresholds for MCCs; Disputes that overturn the fraudulent classification of a specific charge.
> **Input Format**
> 1. Line 1: A comma-separated list of non-fraudulent codes.
> 2. Line 2: A comma-separated list of fraudulent codes.
> 3. Line 3: An integer `m`, the number of MCC threshold rows.
> 4. Next `m` lines: `MCC,threshold` — `threshold` may be either an integer greater than `1` for count-based fraud detection, or a decimal fraction between `0` and `1` for percentage-based fraud detection.
> 5. Next line: An integer `r`, the number of merchant rows.
> 6. Next `r` lines: `account_id,MCC`
> 7. Next line: The minimum number of total transactions that must be observed before evaluating a merchant.
> 8. Next line: An integer `e`, the number of event rows.
> 9. Next `e` lines: One of: `CHARGE,charge_id,account_id,amount,code` or `DISPUTE,charge_id`
> **Output Format**: Return a comma-separated list of fraudulent merchant `account_id`s, sorted lexicographically.
> **Behavior**: A charge is fraudulent when its `code` appears in the fraudulent code list. A dispute makes the referenced charge non-fraudulent for all future calculations. Merchants are re-evaluated after every event. Once a merchant no longer meets the threshold, it is removed from the fraudulent set. The minimum transaction requirement is checked against the total number of observed charges.

**Verbatim sample I/O**
```
sample_input.txt:
approved,invalid_pin,expired_card
do_not_honor,stolen_card,lost_card
2
RETAIL,2
AIRLINE,3
2
acct_a,RETAIL
acct_b,AIRLINE
2
9
CHARGE,c1,acct_a,100,do_not_honor
CHARGE,c2,acct_a,100,do_not_honor
CHARGE,c3,acct_a,100,approved
DISPUTE,c1
CHARGE,c4,acct_b,100,do_not_honor
CHARGE,c5,acct_b,100,stolen_card
CHARGE,c6,acct_b,100,do_not_honor
DISPUTE,c5
CHARGE,c7,acct_b,100,lost_card

expected_output.txt:
acct_b
```
(acct_a reaches 2 fraud charges but DISPUTE c1 drops it back to 1 < threshold 2 → not fraudulent. acct_b: c4,c5,c6,c7 fraud minus disputed c5 = 3 ≥ threshold 3 → fraudulent.)

**Part structure per interviewfox (new-grad, HackerRank, July 2026, 60 min)**
> Part 1: Parse the setup — read each merchant to its MCC, the per-MCC fraud threshold (either a hard integer count or a float ratio), and the separate list of fraud codes.
> Part 2: Process the event stream in order. Each `CHARGE` records a transaction for a merchant with a result code, each `DISPUTE` references a prior transaction by id.
> Part 3: After the stream, mark each merchant fraudulent. With a count threshold the merchant is flagged once its fraud charges reach the integer. With a ratio threshold it is flagged when fraud charges divided by total charges meets the float.
> Part 4: Handle dispute reversal. A successful dispute reverses the original charge, so a fraud charge that was already counted must be subtracted and the merchant re-evaluated.
> Part 5: Edge cases. Disputing a transaction twice, disputing a charge that was never fraud, and ratio merchants with zero volume should not flip to fraud.

**Related but distinct variant (medium confidence)** — "Merchant Fraud **Scoring** System" (oavoservice, 2025 HackerRank): inputs `transactions_list`, `rules_list` (1:1 with transactions), `merchants_list` with `base_score`. Rules: (1) *Amount multiplication* — if `transaction_amount > min_transaction_amount`, multiply merchant's `current_score` by `multiplicative_factor`; (2) *Customer+merchant additive* — if the same customer has 3+ transactions with the same merchant, sum `additive_factor` values; (3) *Same-hour penalty* — if 3+ transactions match customer_id, merchant_id and hour, apply a penalty by time range (hours 12–17: add; 9–11 or 18–21: subtract). Output sorted by merchant name lexicographically as `name, score`. Trap: double-counting when processing grouped transactions.

---

## 13. Payment Card Validation (Luhn + networks + redacted + corrupted)
**Confidence: HIGH** (repo statement + verbatim I/O; reported as OA problem 6)

**Sources**: https://github.com/femisowems/stripe-interview-questions/tree/main/question6; linkjob.ai OA writeup.

**Statement (verbatim from Problem6.md)**
> Stripe processes payment cards across multiple networks. For this exercise, a card is considered valid only if it matches a supported network and passes the Luhn checksum.
> Supported networks: VISA: 16 digits, starts with `4`; MASTERCARD: 16 digits, starts with `51` to `55`; AMEX: 15 digits, starts with `34` or `37`.
> **Luhn**: Starting from the rightmost digit and moving left: Double every second digit. If the doubled value is greater than 9, subtract 9. Sum all digits. A card is valid if the sum is divisible by 10.
> **Input Format**: The first line contains an integer `Q`, the number of queries. Each of the next `Q` lines has one of these forms: `P1 card_number` (basic Visa validation); `P2 card_number` (multi-network validation); `P3 redacted_card` (counting valid completions of a redacted card); `P4 corrupted_card?` (recovering all valid originals). For `P3`, the card contains one to five `*` characters, each representing exactly one unknown digit. For `P4`, the line ends with `?` and the observed card has exactly one error [one digit changed OR two adjacent digits swapped].
> **Output Format**: `P1`: output `VISA` or `INVALID_CHECKSUM`. `P2`: output `VISA`, `MASTERCARD`, `AMEX`, `INVALID_CHECKSUM`, or `UNKNOWN_NETWORK`. `P3`: output one line per network in alphabetical order, formatted as `NETWORK,count`. `P4`: output all valid original cards in ascending numeric order, formatted as `card_number,NETWORK`. If a `P3` or `P4` query has no results, it produces no output lines.
> **Notes**: Invalid prefixes or lengths should return `UNKNOWN_NETWORK` for `P2`. `P3` counts every valid completion, grouped by network. `P4` must deduplicate results before sorting.

**Verbatim sample I/O (expected_output.txt from repo)**
```
Input:
9
P1 4532015112830366
P1 4242424242424243
P2 5482334509943
P2 4425233430109994
P2 562523343010901
P3 4242424242424*42
P3 3*8282246310005
P3 **2424242424242
P4 4532015112830367?

Output:
VISA
INVALID_CHECKSUM
UNKNOWN_NETWORK
INVALID_CHECKSUM
UNKNOWN_NETWORK
VISA,1
AMEX,1
AMEX,1
4432015112830367,VISA
4523015112830367,VISA
4531015112830367,VISA
4532005112830367,VISA
4532010112830367,VISA
4532015012830367,VISA
4532015111830367,VISA
4532015112330367,VISA
4532015112820367,VISA
4532015112830267,VISA
4532015112830317,VISA
4532015112830366,VISA
4532015112839367,VISA
4532015152830367,VISA
4532915112830367,VISA
4572015112830367,VISA
```
(The Problem6.md prose lists `VISA` where expected_output has `VISA,1` for the first P3 — trust expected_output.txt.)

---

## 14. Currency Conversion (multi-part graph)
**Confidence: HIGH**

**Sources**: https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/graph_currency.py; adonais0 (phone, 2021); bigtechexperts (3 parts w/ examples); 1point3acres; also LC "Evaluate Division" is the Stripe-tagged analogue (83.5% freq).

**Statement (adonais0, phone screen, 4 parts)**
> Given input like `"USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110"`:
> Part 1: Return direct conversion rates between currency pairs.
> Part 2: Calculate rates requiring one intermediate conversion (e.g. CAD→AUD).
> Part 3: Use best available conversion calculation.
> Part 4: Return all computable conversion rate pairs (bidirectional).
> Note in the writeup: "Make sure to use BFS when they ask you to convert a currency."

**Alternate 3-part framing with verbatim examples (bigtechexperts)**
> **Part 1 (~10 min)**: You receive a string with exchange rates formatted as `Currency1:Currency2:Rate,...`. One unit of Currency1 equals Rate units of Currency2. Rates are bidirectional. Implement a function taking an input string, source currency, target currency, and amount, returning the converted amount rounded to two decimal places, or -1 if no direct conversion exists.
> - `input_str="USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.15"`, from `USD`, to `CAD`, amount `100.0` → `130.0`
> - `input_str="USD:CAD:1.3,EUR:USD:1.1"`, from `USD`, to `GBP`, amount `100.0` → `-1`
> **Part 2 (~20 min)**: Extend to support multi-hop conversions using intermediate currencies. Return a dictionary containing the conversion route, effective rate, and final converted amount.
> - `input_str="USD:CAD:1.3,AUD:CAD:0.74"`, USD→AUD, 100.0 → `{'route': 'USD -> CAD -> AUD', 'rate': 1.76, 'converted_value': 175.68}`
> **Part 3 (~25 min)**: Optimize to find the shortest conversion path using BFS, guaranteeing minimum currency hops.
> - `"USD:EUR:0.85,EUR:GBP:0.87,USD:CAD:1.3,CAD:GBP:0.58,USD:JPY:110,JPY:GBP:0.0065"`, USD→GBP, 100.0 → `{'route': 'USD -> EUR -> GBP', 'rate': 0.74, 'converted_value': 73.95}`
> - `"USD:EUR:0.85,EUR:GBP:0.87,USD:CAD:1.3,CAD:AUD:1.1,AUD:NZD:1.05,NZD:GBP:0.5"`, USD→GBP, 100.0 → `{'route': 'USD -> EUR -> GBP', 'rate': 0.74, 'converted_value': 73.95}`

**Repo test data (sahaia1)**
```python
rates = [['USD','JPY',100], ['JPY','CHN',20], ['CHN','THAI',200]]
queries = [['USD','CHN'], ['JPY','THAI'], ['USD','AUD']]   # last → -1.0
```
ombharatiya's list mentions a variant with a **carrier** field: `"USD:CAD:DHL:5,..."` → multi-hop → best rate over all paths (this overlaps with #20 shipping cost).

---

## 15. Hostname Allocator (apibox / sitebox) + next_server_number
**Confidence: HIGH** (two independent gists, 2016 and 2018)

**Sources**: https://gist.github.com/aranibatta/ffa87e94d117a86fc05b6940e626ee56 (2016-09-01, "Interview Code Written for Stripe"); https://gist.github.com/stealthbomber10/d85d44776ad58ba66d84ff76fd5be736 (2018-10-10); Python impl https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/code1.py

**Statement (reconstructed from both gists)**
> **Part 1**: Write a function `next_server_number(list_of_allocated_numbers)` that assigns the lowest available server number from a pool, where servers are numbered sequentially starting from 1. When servers are deallocated, their numbers become available for reuse.
> ```
> next_server_number([5, 3, 1]) == 2
> next_server_number([])        == 1
> next_server_number([3, 2, 1]) == 4
> ```
> **Part 2**: Build a `Tracker` class with two methods: `allocate(host_type)` — reserves and returns the next available hostname; `deallocate(hostname)` — releases a hostname back into the pool.

**Verbatim test vectors (aranibatta gist, 2016)**
```python
next_server_number([]) == 1
next_server_number([5, 4, 1, 2]) == 3
next_server_number([1, 2, 3, 4, 5]) == 6
next_server_number([5, 4, 3, 2]) == 1
next_server_number([1, 2, 3, 4, 6]) == 5
```
**Verbatim usage (sahaia1/code1.py)**
```python
tracker.allocate("apibox")    # "apibox1"
tracker.allocate("apibox")    # "apibox2"
tracker.deallocate("apibox1") # None, deallocates "apibox1"
tracker.allocate("apibox")    # "apibox1", reuses "apibox1"
tracker.allocate("sitebox")   # "sitebox1"
```
**Follow-up noted in a 2022 gist comment**: add validation for deallocating a hostname that doesn't exist in the tracking system.

---

## 16. Analytical Database: min_by_key / first_by_key / comparator
**Confidence: HIGH** (verbatim prompt captured in a repo notebook; also Glassdoor QTN_3113468 Senior SWE)

**Sources**: https://github.com/freecodemessiah/stripe-interview — `Stripe Technical Screen.ipynb` and `Stripe-Interview.ipynb` (repo desc: "This is what my stripe interview was like", 2019-01). **Stage: technical screen.**

**Statement (verbatim from notebook)**
> **Step 1: min_by_key** — Throughout this interview, we'll pretend we're building a new analytical database. Don't worry about actually building a database though – these will all be toy problems.
> Here's how the database works: all records are represented as maps, with string keys and integer values. The records are contained in an array, in no particular order.
> To begin with, the database will support just one function: `min_by_key`. This function scans the array of records and returns the record that has the minimum value for a specified key. Records that do not contain the specified key are considered to have value 0 for the key. Note that keys may map to negative values!
> Here's an example use case: each of your records contains data about a school student. You can use min_by_key to answer questions such as "who is the youngest student?" and "who is the student with the lowest grade-point average?"
> Implementation notes: You should handle an empty array of records in an idiomatic way in your language of choice. If several records share the same minimum value for the chosen key, you may return any of them.
> Java function signature: `public static Map<String, Integer> minByKey(String key, List<Map<String, Integer>> records);`
> ```python
> assert min_by_key("a", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 1, "b": 2}
> assert min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]) == {"a": 1, "b": 2}
> assert min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 2}
> assert min_by_key("a", [{}]) == {}
> assert min_by_key("b", [{"a": -1}, {"b": -1}]) == {"b": -1}
> ```
> **Step 2: first_by_key** — Our next step in database development is to add a new function. We'll call this function `first_by_key`. It has much in common with min_by_key. first_by_key takes three arguments: a string key; a string sort direction (which must be either "asc" or "desc"); an array of records, just as in min_by_key. If the sort direction is "asc", then we should return the minimum record, otherwise we should return the maximum record. As before, records without a value for the key should be treated as having value 0. Once you have a working solution, you should re-implement min_by_key in terms of first_by_key.
> Java signature: `public static Map<String, Integer> firstByKey(String key, String direction, List<Map<String, Integer>> records);`
> ```python
> assert first_by_key("a", "asc", [{"a": 1}]) == {"a": 1}
> assert first_by_key("a", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) in [{"b": 1}, {"b": -2}]
> assert first_by_key("a", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"a": 10}
> assert first_by_key("b", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": -2}
> assert first_by_key("b", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": 1}
> assert first_by_key("a", "desc", [{}, {"a": 10, "b": -10}, {}, {"a": 3, "c": 3}]) == {"a": 10, "b": -10}
> ```
> **Step 3: first_by_key comparator** — As we build increasingly rich orderings for our records, we'll find it useful to extract the comparison of records into a comparator. This is a function or object (depending on your language) which determines if a record is "less than", equal, or "greater than" another. In object-oriented languages, you should write a class whose constructor accepts two parameters: a string key and a string direction. The class should implement a method `compare` that takes as its parameters two records. This method should return -1 if the first record comes before the second record (according to key and direction), zero if neither record comes before the other, or 1 if the first record comes after the second. In functional languages, you should write a function which accepts two parameters: a string key and a string direction. The function should return a method that takes as its parameters two records… You should then use your comparator in your implementation of first_by_key.
> ```python
> cmp = Comparator("a", "asc")
> assert cmp.compare({"a": 1}, {"a": 2}) == -1
> assert cmp.compare({"a": 2}, {"a": 1}) == 1
> assert cmp.compare({"a": 1}, {"a": 1}) == 0
> ```
(Known later steps in this family, lower confidence: Step 4 multi-key/chained comparators, Step 5 sort_by with a list of (key, direction) pairs.)

---

## 17. Compress URL (numeronyms)
**Confidence: HIGH**

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/Compress.java` (README → **Phone Interview**).

**Statement (verbatim)**
> **Prompt** — Everyday we look at a lot of URLs, for example in our log files from client request. We want our data science team to perform analytics and machine learning, but: 1. we want to preserve the privacy of the user, but without completely obfuscating/hashing the URLs and making them useless, 2. we simply have a lot of data and we want to reduce our storage/processing costs. In real world, we may solve this with hashing; due to the time constraints of the interview, we use numeronyms instead of compress Strings.
> Example starter code:
> ```java
> String compress(String s) {
>    // requirement 1, 2, etc
>    String compressed_s = fx(s);
>    return compressed_s;
> }
> ```
> **Part 1** — Given a String, split it into "major parts" separated by special char `'/'`. For each major part that's split by `'/'`, we can further split it into "minor parts" separated by `'.'`. We assume the given Strings: Only have lower case letters and two separators (`'/'`, `'.'`). Have no empty minor parts (no leading / trailing separators or consecutive separators like `"/a"`, `"a/"`, `"./.."`). Have >= 3 letters in each minor part.
> Example:
> ```
> stripe.com/payments/checkout/customer.maria
> s4e.c1m/p6s/c6t/c6r.m3a
> ```
> **Part 2** — In some cases, major parts consists of dozens of minor parts, that can still make the output String large. For example, imagine compressing a URL such as `"section/how.to.write.a.java.program.in.one.day"`. After compressing it by following the rules in Part 1, the second major part still has 9 minor parts after compression.
> Task: Therefore, to further compress the String, we want to only keep m (m > 0) compressed minor parts from Part 1 within each major part. If a major part has more than m minor parts, we keep the first (m-1) minor parts as is, but concatenate the first letter of the m-th minor part and the last letter of the last minor part with the count [of characters in between].
> Driver calls in repo: `compress("stripe.com/payments/checkout/customer.maria")`, `compress(..., 1)`, `compress("section/how.to.write.a.java.program.in.one.day")`, `compress(..., 3)`.

---

## 18. User Points / Payer Point Spending (FIFO by timestamp)
**Confidence: MEDIUM-HIGH** (in the Stripe repo's phone-interview list, but this problem is also famously Fetch Rewards' take-home — likely reused)

**Sources**: https://github.com/joeytor/StripeInterview `src/main/java/UserPoints.java` (README → **Phone Interview**).

**Statement (verbatim)**
> **Background** — Our users have points in their accounts. Users only see a single balance in their accounts. But for reporting purposes we actually track their points per payer/partner. In our system, each transaction record contains: `payer (String), points (String), timestamp (date)`. For earning points it is easy to assign a payer, we know which actions earned the points, and thus which partner should be paying for the points.
> When a user spends points, they don't know or care which payer the points come from. But, our accounting team does care how the points are spent. There are two rules for determining what points to "spend" first: We want the oldest points to be spent first; We want no payer's points to go negative.
> You need to do: Add transaction for a specific payer and date. Spend points using the rules above and return a list of `{"payer": <string>, "points": <integer>}` for each call. Return all payer point balances.
> **Example** — add transactions:
> ```json
> { "payer": "DANNON",       "points": 1000,  "timestamp": "2020-11-02T14:00:00Z" }
> { "payer": "UNILEVER",     "points": 200,   "timestamp": "2020-10-31T11:00:00Z" }
> { "payer": "DANNON",       "points": -200,  "timestamp": "2020-10-31T15:00:00Z" }
> { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
> { "payer": "DANNON",       "points": 300,   "timestamp": "2020-10-31T10:00:00Z" }
> ```
> then spend `{ "points": 5000 }` → expected response:
> ```json
> [ { "payer": "DANNON", "points": -100 },
>   { "payer": "UNILEVER", "points": -200 },
>   { "payer": "MILLER COORS", "points": -4,700 } ]
> ```
> subsequent balance call → `{ "DANNON": 1000, "UNILEVER": 0, "MILLER COORS": 5300 }`
> FAQ: For any requirements not specified via an example, use your best judgement to determine the expected result.

**Repo assertions (verbatim)**
```java
assertEquals(p1.getBalance().toString(), "[UNILEVER: 200, MILLER COORS: 10000, DANNON: 1100]");
assertEquals(p1.spend(5000).toString(), "[UNILEVER: -200, MILLER COORS: -4700, DANNON: -100]");
assertEquals(p1.getBalance().toString(), "[UNILEVER: 0, MILLER COORS: 5300, DANNON: 1000]");
```

---

## 19. Load Balancer (onsite coding) and WebSocket Router (2025/26 OA)
**Confidence: MEDIUM-HIGH** — two distinct flavours.

### 19a. Onsite/coding "Load Balancer" (capacity + TTL)
**Source**: https://github.com/joeytor/StripeInterview `src/main/java/LoadBalancer.java` (README → **Virtual Onsite / Coding**). No prose prompt in repo; API inferred from code:
```java
LoadBalancer(int initialCapacity)
addServer(int id, int capacity)
routeRequest(int weight, int ttl) -> serverId or -1
```
Behavior: pick the server with the most remaining capacity (`capacity - load`), reject (-1) if the weight doesn't fit; the request frees its weight after `ttl` ms. Thread-safe with lock + notEmpty/notFull conditions. Driver: `addServer(1,10); routeRequest(4,1000); routeRequest(5,500); sleep(600); routeRequest(6,500);`

### 19b. 2025–2026 HackerRank OA "Server Load Balancing / WebSocket Router" (5 parts, 60 min)
**Sources**: Glassdoor QTN_8544368; jointaro SWE Canada 2025-09-27 (**HackerRank, 60 min, five parts**); voker.io; 1point3acres threads 1147122 / 1148545; programhelp/dev.to 2026.
**Statement (composite; no public repo with verbatim text found)**
> Design a server load-balancing system. You need to build the core data structures and logic that manage a pool of servers and distribute client connections across them. Simulate a load balancer routing three request types across `numTargets` servers, each supporting `maxConnectionsPerTarget` connections.
> - **CONNECT**: allocate the connection to the least-loaded non-full target; ties broken by **smallest index**. If an `objectId` is provided, enforce **sticky routing** — all active connections for that object must reside on the same server (even if it's not currently least-loaded). Log successful allocations as `(connectionId, userId, targetIndex)`.
> - **DISCONNECT**: release the connection slot; invalid connection IDs are ignored silently. If this was the final connection for an `objectId` on that server, remove the sticky binding.
> - **SHUTDOWN / `tdown`**: take a target offline by ID/sequence number, evict all its active connections, and reallocate the evictees with the normal CONNECT rules, processing them **sorted by ascending connectionId**. Return the target that has zero connections after reallocation completes.
> Output format for stage 1 reported as `connectionId,userId,targetIndex`.
> Edge cases: full clusters (all targets at max), repeated shutdowns, binding lifecycle.
> Suggested structures: hash maps `connectionId → (target, userId, objectId)` and `objectId → target`, plus a heap/ordered set keyed on (load, index).

---

## 20. Shipping Cost Calculator
**Confidence: HIGH** (verbatim prompt in a 2025 phone-screen repo)

**Sources**: https://github.com/SabihaNazKhan/StripePhoneScreen24Nov25/blob/master/src/Solution.java (repo name implies **phone screen, 2025-11-24**); graph variant https://github.com/TWINSRIRAM/Stripe_OA_Prep/blob/main/shipping_cost.cpp

**Statement (verbatim from Solution.java comments)**
> **Part 1** — Imagine an online hardware store that sells products of different sizes. The store could sell small items like a mouse or larger items like a laptop. These items cost a different amount to be shipped out. Shipping to different countries can also cost a different amount. Imagine you have an order object that looks like the below.
> ```json
> Order: { "country": "US",  // or "CA" for the CA order
>   "items": [ {"product": "mouse", "quantity": 20}, {"product": "laptop", "quantity": 5} ] }
> ```
> Note: In your solution you can pass in an in memory object that has the same shape as the json. You don't need to worry about parsing json for this problem. The US and CA orders have the same shape, they are just different countries.
> Each country/product has a corresponding shipping cost matrix. The cost is stored in the smallest currency unit.
> ```json
> Shipping Cost: { "US": [ {"product": "mouse", "cost": 550}, {"product": "laptop", "cost": 1000} ],
>                  "CA": [ {"product": "mouse", "cost": 750}, {"product": "laptop", "cost": 1100} ] }
> ```
> Write a function called `calculate_shipping_cost` that takes in an order and shipping cost matrix and returns the shipping cost.
> ```
> calculate_shipping_cost(order_us, shipping_cost) == 16000  // 20 * 550 + 5 * 1000 = 16000
> calculate_shipping_cost(order_ca, shipping_cost) == 20500  // 20 * 750 + 5 * 1100 = 20500
> ```

**Part 2 (inferred from the repo's own solution — tiered/volume pricing)**: each product's cost becomes a list of quantity intervals `Cost(cost, minQuantity, maxQuantity)`, and the per-unit price changes by band. Repo's driver data (verbatim):
```java
US: mouse  -> [ (550, 1..MAX) ]
    laptop -> [ (1000, 1..2), (950, 3..4), (900, 5..MAX) ]
CA: mouse  -> [ (750, 1..MAX) ]
    laptop -> [ (1100, 1..2), (1000, 3..MAX) ]
```

**Part 3 variant (TWINSRIRAM, routing/graph)**: input string of routes `"US,UK,UPS,5:US,CA,FedEx,3:CA,UK,DHL,7"` = `from,to,carrier,cost` separated by `:`; find the **minimum cost route** from src to dest via Dijkstra (multi-hop). Matches ombharatiya's note about `"USD:CAD:DHL:5,..."`.

---

## 21. Time-based Key-Value Map (MultiTimeMap)
**Confidence: MEDIUM-HIGH**

**Sources**: https://github.com/SogAniMic/Stripe_coding_challenge/blob/main/MultiTimeMap.ipynb (repo "Stripe_coding_challenge", 2023-01-27); https://github.com/Murillo2380/interview-coding-solutions `medium-stripe-timestamp-cache`; LC Stripe tag has "Time Based Key-Value Store".

**Statement (verbatim from the notebook)**
> It should contain the following methods: `set(key, value, time)`: sets key to value for t = time. `get(key, time)`: gets the key at t = time.
> The map should work like this. If we set a key at a particular time, it will maintain that value forever or until it gets set at a later time. In other words, when we get a key at a time, it should return the value that was set for that key set at the most recent time.
> ```
> d.set(1, 1, 0) # set key 1 to value 1 at time 0
> d.set(1, 2, 2) # set key 1 to value 2 at time 2
> d.get(1, 1) # get key 1 at time 1 should be 1
> d.get(1, 3) # get key 1 at time 3 should be 2
> d.set(1, 1, 5) # set key 1 to value 1 at time 5
> d.get(1, 0) # get key 1 at time 0 should be null
> d.get(1, 10) # get key 1 at time 10 should be 1
> d.set(1, 1, 0) # set key 1 to value 1 at time 0
> d.set(1, 2, 0) # set key 1 to value 2 at time 0
> d.get(1, 0) # get key 1 at time 0 should be 2
> ```
The same repo also has `first_missing_positive.ipynb`: "Given an array of integers, find the first missing positive integer in linear time and constant space… The array can contain duplicates and negative numbers as well. For example, the input `[3, 4, -1, 1]` should give `2`. The input `[1, 2, 0]` should give `3`. You can modify the input array in-place." (This pairs naturally with #15's `next_server_number`.)

---

## 22. Chat / Token Billing (payg vs fixed, plan switching) — 2026 OA
**Confidence: MEDIUM-HIGH** (no repo found; two 1point3acres problem pages give consistent rules and numbers)

**Sources**: https://www.1point3acres.com/interview/problems/59a39c1c-3696-400e-81b6-c3fdd3b56895 and .../f8e3ed43-0b33-4b13-a879-a559ccd803f2 ; "Chat Billing Calculation (OA)".

**Statement (composite, verbatim rules)**
> Implement a monthly billing calculator for a chat-based AI platform. **Input**: an array of strings representing chat sessions: `"user_id,input_tokens,output_tokens,plan"` where plan ∈ {`payg`, `fixed`}.
> **Block-based billing (per session)**: Tokens are billed in blocks of 100; **any partial block is free** — `blocks = floor(tokens / 100)`. Block rounding applies independently to **each session**; remainders from different sessions cannot be combined. Token blocks must be computed separately per plan.
> **Rates (payg)**: Input `$0.03` per 100-token block; Output `$0.04` per 100-token block.
> **Fixed plan**: `$15.00` monthly base fee; included allowance `40,000` tokens/month (one page splits this as 40,000 input + 20,000 output); overage charged at payg rates using per-session block rounding.
> **Requirement 1**: pay-as-you-go only — sum block-based costs across all payg sessions per user.
> **Requirement 2**: fixed plan only — base fee + overage above allowance.
> **Requirement 3 (plan switching / proration)**: With N total sessions and F fixed sessions for a user: prorated fee = `15.00 * (F / N)`; prorated allowance = `40,000 * (F / N)` tokens. Apply the prorated allowance to fixed sessions and charge overage at payg rates.
> **Output**: sorted array of strings `"user_id: $x.xx"`, alphabetical by user_id, 2-decimal precision; include all users even those charged < $1.00.
> Reported example results: Example 1 (payg only): userA `$0.07`, userB `$0.14`. Example 2 (fixed only): userA `$0.07`, userB `$17.30`. Example 3 (mixed): userA `$7.71`.

---

## 23. Feature Availability / A-B Test Flags
**Confidence: MEDIUM** (only one source: adonais0's phone-screen writeup, 2021-06)

**Source**: https://adonais0.github.io/20210603/interview-stripe/ (**phone**)
> Given users with locations and features with optional location restrictions and A/B test flags: implement `get_user_features(user, features)` returning applicable feature IDs where: features limited to the user's location apply (to users in that location); A/B test features (when the flag is true) apply only to users with **even IDs**.

---

## 24. Fraud Rule Timestamps (authorization requests vs rule effective time)
**Confidence: MEDIUM** (adonais0 only; distinct from #12)

**Source**: https://adonais0.github.io/20210603/interview-stripe/ (**phone**)
> Process authorization requests against fraud rules where e.g. "any Authorization Request with merchant of `bobs_burgers` is fraudulent." Rules become applicable from their timestamp forward and **cannot retroactively flag earlier requests**. Output format: timestamp, ID, amount, and `APPROVE`/`REJECT` decision.

---

## 25. Rate Limiter
**Confidence: MEDIUM** (listed as an onsite coding topic in the StripeInterview README but no statement or code in the repo; the canonical reference is Stripe's own blog)

**Sources**: joeytor/StripeInterview README (**Virtual Onsite / Coding → Rate Limiter**); https://gist.github.com/ptarjan/e38f45f2dfe601419ca3af937fff574d (Paul Tarjan, Stripe, 2017-03-29 — the four rate limiters from the Stripe engineering blog, with Redis+Lua pseudocode).
**The four limiter types to know (from the gist)**: (1) **Request Rate Limiter** — token bucket, 100 req/s with burst 500; two Redis keys per user (available tokens + last-refill timestamp); Lua for atomicity. (2) **Concurrent Requests Limiter** — max 100 in-flight per user, 60 s timeout, sorted set of active request IDs by timestamp with expiry pruning. (3) **Fleet Usage Load Shedder** — the concurrent logic applied globally, dropping non-critical traffic to protect e.g. charge creation. (4) **Worker Utilization Load Shedder** — above 80% utilization, ramp rejection probability over 120 s. Design principles: fail open on Redis outage; gradual (not sharp) shedding; monitor & alert.
Mock-interview variants seen: "Implement per-user 100 requests per 15 minutes" (store `(userId, windowStart, count)`, Redis TTL + atomic increment).

---

## 26. Integration Round — Request Replay & Bike Map
**Confidence: MEDIUM-HIGH** (README description + real helper code in the repo)

**Source**: https://github.com/joeytor/StripeInterview README + `src/main/java/BikeMap.java`
> **Request Replay** (verbatim README): read request and response from a JSON file; re-send the request to update the response or to check if response code is the same; may need to maintain a map of old response id to new response id.
> **Bike Map** (verbatim README): read from a JSON file, print something out; send request to a URL and save response to local file; Java file has some basic methods such as reading/writing JSON files; check GSON and OKHTTP library.

`BikeMap.java` is a prepared toolkit: `readFile`, `readObjectFromJsonString`, `readObjectFromJson`, `readArrayFromJson`, `readListFromJson`, `writeJson`, `download(url, filename)` using Gson + OkHttp; sample object shape `{"name": ..., "population": ..., "listOfStates": [...]}`. Python equivalent: https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/stripe_example_api.py (requests + json).

Corroborating reports: the Integration round = download a private GitHub repo, do JSON serialization/deserialization, call a public API and read the response; open-book (repo, API docs, internet allowed) but **AI coding assistants are not permitted** (2026 clarification, per ombharatiya's list). Recent variants: request deduplication (idempotency), JSON comparison.

---

## 27. Bug Squash round
**Confidence: MEDIUM-HIGH** (round format well attested; exact bugs vary)

**Sources**: joeytor README names the actual repos used: **jackson-core** (https://github.com/FasterXML/jackson-core) and **Moshi** (https://github.com/square/moshi). Shivam5022/Interview-Experiences (2025): "given access to an open-source **C++** repository and asked to fix **two bugs within an hour**; used a debugger and breakpoints". ombharatiya (2026): Bug Squash "focuses sharply on financial-logic bugs: race conditions, missing idempotency checks, non-atomic check-then-act, unvalidated refund logic (~5-7 bugs in ~200 lines)". Other reports: private repo with a pinned version of an OSS project for your language (Express/Day.js for JS, Sass for Ruby), several GitHub-style issues each backed by failing unit tests.

---

## 28. System Design prompts (onsite)
**Confidence: MEDIUM-HIGH**

**Source**: https://github.com/joeytor/StripeInterview README (verbatim list + the author's notes)
> - **Payment Webhook** — Background: https://stripe.com/docs/webhooks ; Reference design: https://tianpan.co/notes/166-designing-payment-webhook
> - **Counter Logging System** — Just take a look on how AWS or Azure or GCP handles metrics
> - **Identity and Access Management System** — Same as above, just refer to IAM systems in public clouds
> - **Ledger** — Nothing special, just use message queue to receive transactions, and consume by subscribing to different merchant accounts. You can use NoSQL such as Cassandra or others to store transaction data as there is no ACID requirement. For each merchant account, do an aggregation on all transactions to get balance. Periodically run aggregation to boost performance. For example, run it daily so you only need to run aggregation upon request for current day.

**adonais0 onsite prompts (verbatim)**
> - **Ledger**: Design a bookkeeping service tracking merchant financial activity supporting: record money sent/received on behalf of merchants; query account balance for a given merchant.
> - **Metrics Counter**: "Design everything that happens after `Track.increment('some-metric')` gets called on a service, from what happens inside the service to how the data is sent, collected, stored and accessed." Support querying metrics across variable time windows (minutes/hours/days/weeks) for trend analysis.

---

## 29. Telephone number input field (front-end / product engineer)
**Confidence: MEDIUM-HIGH**

**Source**: https://github.com/bradgarropy/stripe-telephone ("📞 stripe interview question - telephone input")
> During an interview with Stripe, a candidate was asked to code a telephone number input field which formats the phone number as you type. Requirements: the input should not allow invalid characters; formatting characters should only be inserted **preceding** digits; deleting a digit should also remove any formatting characters immediately preceding it; pasting a full or partial number into the input should work.

---

## 30. LeetCode problems tagged **Stripe**
**Confidence: HIGH** (source: https://github.com/liquidslr/leetcode-company-wise-problems `Stripe/5. All.csv`, updated 2025-06-20)

| Difficulty | Title | Freq % | Link |
|---|---|---|---|
| MEDIUM | Minimum Penalty for a Shop | 100.0 | https://leetcode.com/problems/minimum-penalty-for-a-shop |
| EASY | Calculate Amount Paid in Taxes | 92.7 | https://leetcode.com/problems/calculate-amount-paid-in-taxes |
| MEDIUM | Invalid Transactions | 89.7 | https://leetcode.com/problems/invalid-transactions |
| MEDIUM | Cheapest Flights Within K Stops | 82.0 | https://leetcode.com/problems/cheapest-flights-within-k-stops |
| MEDIUM | Brace Expansion | 82.0 | https://leetcode.com/problems/brace-expansion |
| MEDIUM | Evaluate Division | 76.9 | https://leetcode.com/problems/evaluate-division |
| HARD | Parallel Courses III | 61.2 | https://leetcode.com/problems/parallel-courses-iii |
| MEDIUM | One Edit Distance | 61.2 | https://leetcode.com/problems/one-edit-distance |
| MEDIUM | Number of Black Blocks | 61.2 | https://leetcode.com/problems/number-of-black-blocks |
| MEDIUM | Alert Using Same Key-Card Three or More Times in a One Hour Period | 61.2 | https://leetcode.com/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period |
| MEDIUM | Simple Bank System | 61.2 | https://leetcode.com/problems/simple-bank-system |
| MEDIUM | Merge Intervals | 61.2 | https://leetcode.com/problems/merge-intervals |
| MEDIUM | Remove Covered Intervals | 61.2 | https://leetcode.com/problems/remove-covered-intervals |

Corroborated by repos that collect the actual asked LC problems:
- https://github.com/Hazeera65/stripe-interview/tree/main/round1 → Evaluate Division (399), Optimal Account Balancing (465), Brace Expansion, Cheapest Flights Within K Stops (787) + the phone-screen penalty problem.
- https://github.com/premjm-67/stripe-interview-questions → `B.java` Brace Expansion, `CF.java` Cheapest Flights K Stops, `ED.java` Evaluate Division, `MP.java` Minimum Penalty for a Shop, `PL.java` Parallel Courses III.
- https://github.com/TWINSRIRAM/Stripe_OA_Prep → brace1/brace2/brace_followup, cheapest_flight, evaluatedivision, merge_intervals, top_k_elements, shipping_cost, part1-3 (penalty).
- ombharatiya's Stripe section adds: Two Sum, LRU Cache, Design Hit Counter, Top K Frequent, Subarray Sum Equals K, Time Based Key-Value Store, Course Schedule, Sliding Window Maximum, Serialize/Deserialize Binary Tree, Coin Change, Group Anagrams, Product of Array Except Self, Longest Substring Without Repeating Chars, Number of Islands, Single-Threaded CPU, LFU Cache.

**Brace expansion statement (verbatim, from Hazeera65 bracket.text)**
> You are given a string s representing a list of words. Each letter in the word has one or more options. If there is one option, the letter is represented as is. If there is more than one option, then curly braces delimit the options. For example, "{a,b,c}" represents options ["a", "b", "c"]. For example, if s = "a{b,c}", the first character is always 'a', but the second character can be 'b' or 'c'. The original list is ["ab", "ac"]. Return all words that can be formed in this manner, sorted in lexicographical order.
> Example 1: Input: s = "{a,b}c{d,e}f" → Output: ["acdf","acef","bcdf","bcef"]. Example 2: Input: s = "abcd" → Output: ["abcd"].
> **Follow-up seen in TWINSRIRAM/brace_followup.cpp**: handle a *single* brace group with validation — if there is no `{`/`}` or `}` precedes `{`, or fewer than 2 options, return the input unchanged; otherwise emit `prefix + option + suffix` for each option.

---

## 31. Interview format / round structure (repo-sourced)

**joeytor/StripeInterview README (verbatim structure)**
```
## Phone Interview      - Stripe Capital, Compress URL, HTTP Header Parser, Mutual Rank, Server Penalty, User Points
## Virtual Onsite
  ### Coding            - Money Transfer, Load Balancer, Invoicer, Rate Limiter
  ### Integration       - Request Replay, Bike Map
  ### Bug Swash         - Jackson-Core, Moshi
  ### System Design     - Payment Webhook, Counter Logging System, Identity and Access Management System, Ledger
```

**Shivam5022/Interview-Experiences (verbatim, 2025, IIT-D, systems role)**
> **Online Assessment**: It was a 60-minute test on HackerRank. The problem wasn't algorithmic, but rather implementation-heavy. I had to parse a command string and execute the commands, which simulated transactions between users' bank accounts. It wasn't very difficult, but the implementation was fairly long.
> **Phone Screening**: The next round was a 45-minute phone screening on Zoom with one of the engineers. This was a live coding round, which I could attempt either on my local IDE or in their HackerRank sandbox. Again, it involved an implementation-based problem with 2–3 subparts. Each subpart built upon the previous one.
> **Programming Round**: This round had one programming question (with multiple subparts), which I attempted in C++.
> **Bug-Squash Round**: I was given access to an open-source C++ repository and asked to fix two bugs within an hour. I used a debugger and breakpoints to trace and fix the issues.
> **Manager Chat Round**: final, non-technical, 30-minute round with an Engineering Manager. Questions: deep dive into internship experience; how I approached my project, its impact, follow-ups; goals as a software engineer for the next two years; a technically challenging past experience; why Stripe is the right career fit.

**2026 format notes (ombharatiya's curated list, verbatim)**
> Stripe does NOT use traditional LeetCode-style interviews. Problems model real engineering work — payment processing, debugging, API integration. Code quality valued over algorithmic cleverness. Unique rounds: Bug Squash (debug a GitHub repo), Integration (build with Stripe API), API Design (REST resource modeling).
> 2026 changes: The new-grad OA is now a single 60-minute multi-part question on HackerRank: "measuring true coding ability with one question." Integration round rules clarified: web/docs search is allowed, but AI coding assistants are NOT permitted.
> Custom problems list: Accept-Language header parser (parse q-values, sort by quality, the long-standing screen); currency conversion string parsing (`"USD:CAD:DHL:5,..."` → multi-hop → best rate over all paths); card range obfuscation; fraud detection stream (CHARGE/DISPUTE, per-MCC thresholds); subscription notification scheduler; CSV parse + validate with circular dependency detection; invoice reconciliation; request deduplication (idempotency); webhook handler debugging; payment retry with exponential backoff; shipping cost calculator.

---

## 32. Lower-confidence / mock-only problems (from prep repos, NOT verified as asked)

From https://github.com/sumansaurav91/stripe-interview-prep (AI-generated mock sets — treat as **LOW confidence**, listed for completeness):
- Transaction Reconciliation Tool (two ledgers, return unmatched; follow-up: same id different amount)
- Longest streak of consecutive successful payments per merchant (events `{id, merchantId, status, timestamp}`)
- Credit card masking (`"4242424242424242"` → `"************4242"`)
- Currency normalization to minor units (USD 2, JPY 0, KWD 3 decimals)
- Refund allocation proportionally across line items
- Rolling balance per account from an event stream
- Detect duplicate charges by idempotencyKey
- Rate limiting window (100 req / 15 min per user)
- Ledger event reconciliation / matching transfers with refunds
- System design: refund service, webhook management API, multi-currency ledger, idempotent payment API, webhook delivery, invoicing engine, real-time dashboard, dispute resolution
- Debugging scenarios: idempotency key reused → 409 duplicate refund; Node memory leak; all charges failing

From https://github.com/kushal107/stripe_interview_practice (2026-04/06, personal practice; the interesting one):
- `emailsubs.py` — "Design a subscription management system that tracks user subscriptions and sends automated emails at specific lifecycle events" — models `SubscriptionStatus{TRIALING, ACTIVE, CANCELED}`, `EventBus`, `NotificationService` with **idempotency via processed-event-ID set**, `check_trial_expiry()`. Suggests the emailed-subscription problem is sometimes asked as an **OOD/extensibility** exercise ("define your own structure; the code should be reusable and general to handle various future changes").
- `callapi.py` / `callapi2.py` — practising `requests.get` + `raise_for_status` + `.json()` (Integration round prep).

Repos checked and found **not** to contain interview problems (payment-integration demos only): PisoMojado/StripeInterview, braslavskyiandrii/stripe-interview, PatrikFomin/stripe-interview, vorpavnik/Stripe_interview, Vishesh20155/Stripe-Interview-Prep, krutin47/stripe-interview-new, Saikiran-1999/StripeTest, harsha-vardhan-2/stripe-interview-prep, ash-bd/s2-stripe-onsite, MyNameIsBond/StripeCodingChallenge, steph-viereckl/stripe-coding-challenge, jejrthompson/stripe-interview-demo, am-stripe-001/stripe-interview (technical brief for a payments design, not an interview problem).

---

## Search notes / gaps
- GitHub MCP tools failed with "Bad credentials"; used the authenticated `gh` CLI instead. `gh search code` is limited to 10 req/min and returned nothing for most Stripe-specific phrases — Stripe appears to actively DMCA repos hosting their verbatim problems (confirmed: Molakim/stripeCoding taken down 2022-05-17), so verbatim OA text mostly survives in *derivative* repos (femisowems) and prompts embedded in solution comments (joeytor, kylelong, SabihaNazKhan).
- Not fetched (rate/session limits): https://github.com/prashantrai/Algo_DS_InterviewPrep `src/Stripe/StoreHours.java` and `src/Stripe/AnalyzeServerProcessUptimeLog.java`; https://github.com/KuriyamaMiraiQcy/Leetcode `src/Stripe.java`. These matched a `find_best_closing_time` code search and are expected to duplicate #1/#2.
- Paywalled/blocked, so only summarized: 1point3acres problem pages, showoffer, darkinterview, hackerprep, LeetCode discuss posts 2585038 / 7566910 / 7595344, Glassdoor, Medium.
