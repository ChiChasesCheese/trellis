| dir | title | tests | p1/p2/p3/p4/p5 | edge | fmt | perf | io | measured | status |
|---|---|---:|---|---:|---:|---:|---:|---|---|
| q01_fraud_mcc_disputes | Fraud Detection by MCC — CHARGE/DISPUTE event stream ("Catch | 21 | 4/3/6/4/4 | 12 | 2 | 1 | 2 | 0.16s, 47 MB (budget 2 s / 256 MB). | 21 passed in 0.34s |
| q02_merchant_fraud_score | Merchant Fraud Score — base score × amount factor, repeat-cu | 20 | 6/5/9/0/0 | 12 | 1 | 1 | 1 | 0.19s, 97 MB | 29 passed in 0.41s |
| q03_chat_billing | Chat Billing — monthly billing by token usage and plan switc | 20 | 6/5/9/0/0 | 9 | 2 | 1 | 2 | — | 20 passed in 0.26s |
| q04_card_range_obfuscation | Card Range Obfuscation — fill the gaps in a BIN's brand inte | 24 | 8/4/4/8/0 | 13 | 1 | 1 | 2 | 0.295s, 69 MB | 24 passed in 0.54s |
| q05_card_validation_luhn | Payment Card Validation — Luhn, network detection, redacted  | 21 | 4/4/5/8/0 | 11 | 2 | 1 | 3 | 0.46s, 18 MB | 21 passed in 1.48s |
| q06_atlas_company_name | Atlas Company Name Availability — normalize, register, recla | 18 | 6/5/7/0/0 | 10 | 1 | 1 | 1 | 0.16s, 49 MB | 34 passed in 0.38s |
| q07_subscription_notifications | Subscription Notification Scheduler — welcome / expiry-warni | 23 | 7/5/7/4/0 | 10 | 2 | 2 | 2 | 0.95s, 197 MB (Part 3 perf) · 0.24s, 132 MB (Part 4 perf) | 23 passed in 1.42s |
| q08_store_closing_penalty | Store Closing-Time Penalty — Y/N hourly log, best closing ho | 16 | 4/5/7/0/0 | 6 | 0 | 2 | 1 | 0.23s, 36 MB | 33 passed in 0.69s |
| q09_jupyter_load_balancer | Jupyter Load Balancer — route WebSocket connections across n | 24 | 5/3/3/3/10 | 11 | 2 | 1 | 2 | 0.359s, 131 MB | 24 passed in 0.61s |
| q10_payment_intent_commands | Payment Intent Commands — INIT / CREATE / ATTEMPT / SUCCEED  | 25 | 9/4/5/7/0 | 15 | 1 | 1 | 1 | 0.170s, 53 MB | 25 passed in 0.33s |
| q11_subscription_database | Subscription Database — start / end / check with durations t | 24 | 9/7/8/0/0 | 14 | 1 | 1 | 2 | 0.16s, 44 MB (200k events, 20k users; budget 2 s / 256 MB). | 24 passed in 0.35s |
| q12_platform_balance_radar_rules | Platform Balance API strings + Radar rule engine | 24 | 8/6/10/0/0 | 15 | 1 | 1 | 2 | 0.28s, 33 MB (100k lines: 40k API, | 24 passed in 0.44s |
| q13_account_balance_ledger | Account Balance Ledger — balances, rejected debits, platform | 22 | 7/5/10/0/0 | 11 | 3 | 1 | 2 | 0.30s, 48 MB (200k lines, 5k users, 20% transfers; in-pytest | 22 passed in 0.57s |
| q14_join_dataset | Join Dataset — merge a legacy processor's export into Stripe | 18 | 9/4/5/0/0 | 8 | 3 | 1 | 1 | 0.325s, 121 MB | 18 passed in 0.44s |
| q15_kyc_verification | KYC Business Verification — progressive CSV validation of me | 17 | 4/3/3/2/5 | 10 | 1 | 1 | 2 | 0.27s, 103 MB (100k rows with reasons; budget 2 s / 256 MB). | 17 passed in 0.41s |
| q16_chargeback_parsing | Chargeback Parsing — parse network chargeback records, drop  | 18 | 6/5/7/0/0 | 10 | 2 | 1 | 2 | 0.75s, 148 MB (200k rows, 15% withdrawn, 5% corrupted, 128k  | 18 passed in 1.12s |
| q17_datacenter_router_haversine | Datacenter Request Router — registry, health, Haversine dist | 24 | 5/4/12/3/0 | 12 | 1 | 1 | 2 | 1.28s, 65 MB (100k commands, 50 regions; budget 2 s / 256 MB | 24 passed in 0.84s |
| q18_collusion_ring | Six Degrees of Collusion — fraud rings from shared identifie | 22 | 6/8/5/3/0 | 10 | 2 | 1 | 3 | 0.59s, 128 MB (100k records, | 22 passed in 0.87s |
| q19_accept_language | Accept-Language — resolve a request's language preferences a | 20 | 6/3/4/7/0 | 10 | 1 | 1 | 2 | 0.23s, 19 MB (10k entries × 1k supported; budget 2 s / 256 M | 20 passed in 0.35s |
| q20_transaction_fees_reconciliation | Transaction Fees, Receivables and Reconciliation — fees per  | 15 | 4/3/5/3/0 | 6 | 2 | 1 | 1 | 0.37 s, 159 MB for 10^5 receivables rows (8 columns) and 0.3 | 15 passed in 0.98s |
| q21_currency_conversion | Currency Conversion — direct, inverse and multi-hop best rat | 19 | 6/2/7/4/0 | 7 | 3 | 1 | 2 | 0.136s, 39 MB | 19 passed in 0.31s |
| q22_shipping_cost | Shipping Cost — carrier routes (direct / one transfer / chea | 22 | 3/5/3/4/7 | 12 | 1 | 1 | 2 | 0.10 s / 54 MB (1 000 orders × 100 items, graduated) and 0.9 | 22 passed in 1.18s |
| q23_rate_limiter | Rate Limiter — sliding window (global → per client → weighte | 18 | 5/4/4/5/0 | 12 | 0 | 1 | 1 | 0.61 s, 139 MB for 10^6 weighted requests over 2 000 clients | 18 passed in 1.20s |
| q24_server_allocator | Server Allocator — smallest free server number and hostname  | 15 | 4/7/2/2/0 | 7 | 0 | 1 | 2 | 0.50 s, 97 MB for 10^6 mixed commands (60 % allocate / 40 %  | 15 passed in 1.10s |
| q25_invoice_reconciliation | Invoice / Payment Reconciliation — match incoming payments t | 19 | 6/5/5/3/0 | 9 | 2 | 1 | 2 | 0.386s, 132 MB | 19 passed in 0.57s |
| q26_account_scheduler_lru | AccountScheduler — availability, timed locks, LRU auto-selec | 17 | 4/7/3/3/0 | 9 | 1 | 1 | 1 | 0.165s, 38.6 MB | 17 passed in 0.27s |
| q27_payment_ledger | PaymentLedger — idempotent payments, partial refunds, revenu | 17 | 3/4/5/5/0 | 7 | 2 | 1 | 1 | 0.694s, 102.8 MB | 17 passed in 0.85s |
| q28_worker_task_assignment | Worker Task Assignment — least-busy worker, required skills, | 16 | 4/3/3/6/0 | 8 | 1 | 1 | 1 | 0.154s, 50.4 MB | 16 passed in 0.27s |
| q29_deployment_windows | Weekly Deployment Window Scheduler — first K valid UTC deplo | 21 | 5/6/7/3/0 | 10 | 2 | 1 | 2 | 0.045s, 18.3 MB | 21 passed in 0.24s |
| q30_stripe_capital_loans | Stripe Capital — loan bookkeeping (CREATE / PAY / INCREASE / | 23 | 5/3/5/10/0 | 12 | 1 | 1 | 2 | 0.12s, 34 MB (perf test: 6k creates + 100k actions). | 23 passed in 0.28s |
| q31_wishlist_mutual_rank | Wishlist / Mutual Rank — apartment-swap pairings | 20 | 6/5/4/5/0 | 7 | 1 | 1 | 1 | 0.23s, 71 MB (10k users × 10 entries, 100k queries + PAIRS + | 20 passed in 0.43s |
| q32_money_transfer_rebalancing | Money Transfer — bank-account rebalancing (every account ≥ m | 19 | 6/5/4/4/0 | 8 | 0 | 1 | 1 | 0.17s, 55 MB (500 accounts + 100k audited transfers). | 19 passed in 0.29s |
| q33_analytical_db_min_by_key | Analytical Database — `min_by_key` / `first_by_key` / compar | 18 | 5/4/4/5/0 | 6 | 1 | 1 | 1 | 0.45s, 60 MB | 18 passed in 0.72s |
| q34_compress_url | Compress URL — numeronyms per path segment, tail folding, am | 17 | 5/5/3/4/0 | 6 | 1 | 1 | 1 | 0.34s, 83 MB (100k URLs, Part 4; budget 2 s / 256 MB). | 17 passed in 2.03s |
| q35_user_points_fifo | User Points — payer point spending, FIFO by timestamp | 16 | 3/5/4/4/0 | 7 | 2 | 1 | 1 | 0.27s, 64 MB | 16 passed in 0.47s |
| q36_time_kv_map | Time-based Key-Value Map (MultiTimeMap) — versioned get, his | 15 | 7/2/4/2/0 | 7 | 1 | 1 | 1 | 0.15s, 54 MB | 15 passed in 0.37s |
| q37_fraud_rule_timestamps | Fraud Rule Timestamps — authorization requests vs rule effec | 15 | 4/4/3/4/0 | 7 | 1 | 1 | 1 | 0.52s, 72 MB | 15 passed in 0.65s |
| q38_feature_flags | Feature Flags — allowlists, percentage rollout, attribute ru | 16 | 3/6/4/3/0 | 8 | 0 | 1 | 1 | 0.41s, 38 MB (10k users, 10-deep chain, | 16 passed in 0.51s |
| q39_server_uptime_log | Server Process Uptime Log — removal penalty, best removal ti | 14 | 3/4/4/3/0 | 4 | 0 | 1 | 1 | 0.08s, 36 MB (10^6-hour log, Part 2; the perf test | 14 passed in 0.47s |
| q40_query_words_within_k | Query Words Within k — proximity search, minimal window, nor | 13 | 5/4/2/2/0 | 5 | 0 | 1 | 1 | 0.33s, 44 MB (200k-word text, 20 three-word queries, Part 2; | 13 passed in 0.48s |
| qA01_lc2303_taxes | LC 2303 Calculate Amount Paid in Taxes — graduated brackets, | 15 | 6/4/3/2/0 | 6 | 1 | 1 | 2 | 0.08s (10^4 in-process calls at LC max + one script run), | 15 passed in 0.19s |
| qA02_lc787_cheapest_flights_k_stops | LC 787 Cheapest Flights Within K Stops — Bellman-Ford by rou | 17 | 7/4/4/2/0 | 8 | 1 | 1 | 1 | 0.15s | 17 passed in 0.28s |
| qA03_lc1087_brace_expansion | LC 1087 Brace Expansion — stack, backtracking, nested braces | 16 | 8/2/3/3/0 | 6 | 1 | 1 | 1 | 0.10s (60 expansions at LC max | 16 passed in 0.27s |
| qA04_lc1169_invalid_transactions | LC 1169 Invalid Transactions — amount cap, same-name/other-c | 15 | 9/3/3/0/0 | 7 | 0 | 1 | 1 | 0.29s | 15 passed in 0.47s |
| qA05_lc1604_keycard_alerts | LC 1604 Alert Using Same Key-Card ≥3 Times in 1 Hour — HH:MM | 15 | 8/3/4/0/0 | 5 | 2 | 1 | 1 | 0.20s (10^5 swipes in-process + | 15 passed in 0.33s |
| qA06_lc2043_simple_bank_system | LC 2043 Simple Bank System — validated transfer/deposit/with | 16 | 8/4/4/0/0 | 8 | 0 | 1 | 1 | 0.10s (10^4 random ops on 10^5 accounts in-process + | 16 passed in 0.20s |
| qA07_intervals_merge_covered | LC 56 Merge Intervals + LC 1288 Remove Covered Intervals — m | 16 | 6/4/4/2/0 | 7 | 0 | 1 | 1 | 0.34s (10 × LC max for LC 56 (10^4) and LC 1288 (10^3), thre | 16 passed in 0.49s |
| qA08_lc465_optimal_account_balancing | LC 465 Optimal Account Balancing — net balances, fewest tran | 16 | 8/5/3/0/0 | 7 | 1 | 1 | 1 | 0.17 s for the perf test (12-net worst shape + slowest-of-30 | 16 passed in 0.49s |
| qA09_lc2050_parallel_courses_iii | LC 2050 Parallel Courses III — weighted DAG longest path, th | 15 | 8/3/4/0/0 | 6 | 1 | 1 | 1 | 0.31 s for the perf test | 15 passed in 0.47s |
| qA10_lc161_one_edit_distance | LC 161 One Edit Distance — single pass, adjacent swap, name  | 15 | 6/3/3/3/0 | 5 | 0 | 1 | 1 | 0.34 s for the perf test (50 × Parts 1–3 on 10^4 chars + ban | 15 passed in 0.62s |
| qA11_lc2768_number_of_black_blocks | LC 2768 Number of Black Blocks — hash-count touched 2×2 bloc | 15 | 9/3/3/0/0 | 6 | 1 | 1 | 1 | 0.12 s for | 15 passed in 0.32s |
| qA12_lc399_evaluate_division | LC 399 Evaluate Division — BFS and weighted union-find, best | 15 | 5/4/3/3/0 | 5 | 1 | 1 | 1 | 0.20 s for the perf test (20 equations × 10^4 BFS and UF que | 15 passed in 0.37s |
| qA13_lc2483_minimum_penalty_for_a_shop | LC 2483 Minimum Penalty for a Shop — O(n) running penalty, o | 15 | 7/3/3/2/0 | 5 | 0 | 1 | 1 | 0.16 s for the | 15 passed in 0.33s |

**53 problems · 967 tests** (edge 454 · fmt 60 · perf 55 · io 76)
