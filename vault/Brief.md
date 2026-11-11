# Design Airbnb Wallet

Your interview feedback

Tutor

# This was a Lean No Hire interview

Design Airbnb Wallet at **Senior** · medium confidence

Strong on wallet data model, fund holds, atomic withdrawal admission, write-before-vendor idempotency, and transactional status/balance updates, but below Senior because lost vendor outcomes were only handled by vague polling/scanning with no cadence or freshness/call-rate bound, and revised sizing/idempotent callback details remained incomplete.

## Main takeaways

1. 1
    
    ### Put a limit on any external call users can trigger.
    
    For pending transfers, you read wallet and transactions first, then said that if the transaction was still pending you might do a real-time query to the payment service platform. That keeps the local completed and failed states clean, but it leaves the pending branch open-ended. If many users refresh pending transfers, your servers can pile up calls to the payment platform. Then a slow vendor makes user reads slow, and a burst of status checks becomes a burst of vendor traffic.
    
    Use a freshness window on the transaction row. Add last_vendor_check_at. If a user asks for a pending transfer and it was checked less than 30 seconds ago, using an assumed 30 second window, return pending from your table. If it is older, put one refresh job in a queue and still return pending. A worker calls the payment platform, then updates the transaction status and wallet balance in one database transaction. That way user reads never wait for the vendor, and the vendor sees at most one refresh per transaction per window.
    
    Next interview, when a user read can call another company, set a freshness window and say who refreshes it.
    
2. 2
    
    ### For every added piece, say its job, cost, and trigger.
    
    You gave a useful reason for Postgres, saying wallet and transaction updates need atomic changes and ordered reads. But some later choices did not get the same treatment. The real-time pending-status query to the payment platform was described without a call-rate limit. Kafka was added late for status updates, but the design did not say what problem it solved at this scale, what delay it adds, or what duplicate-message handling it requires.
    
    Use a three-part sentence before you keep any component. For Kafka in your wallet design, the sentence would be this. Kafka buffers payment-platform updates when they arrive faster than the database writer can safely process them. Its cost is extra delay, duplicate delivery, and another place to operate and monitor. I would add it only when direct webhook writes to Postgres cannot keep up, or when we need to survive the wallet updater being down without losing vendor updates. If you cannot fill in those three parts, leave the component out for now.
    
    Next interview, when you name a database, queue, cache, or shard, immediately give its job, cost, and trigger.
    
3. 3
    
    ### Answer the case you were asked, then name nearby cases separately.
    
    When the question was two distinct 500 dollar withdrawals arriving against a 500 dollar wallet, you first talked about transaction IDs and attempt IDs. That answer fits duplicate retries, where the same user action should return the same transaction. It did not answer the asked case, where two separate withdrawals must not both spend the same 500 dollars. The difference matters because duplicate retries need idempotency, while distinct withdrawals need one database update that only one request can win.
    
    Start with the exact case in one sentence. For two distinct withdrawals, I let the database admit only one of them. Then show the one operation. For your wallet table it could be this.
    
    ```
    UPDATE wallets
    SET ready_to_use = ready_to_use - 500,
        on_hold = on_hold + 500
    WHERE wallet_id = $1
      AND ready_to_use >= 500;
    ```
    
    If one row is updated, create the pending withdrawal. If zero rows are updated, reject it for insufficient funds. After that, separately say that duplicate retries use attempt_id to return the first transaction.
    
    Next interview, when a question gives a concrete race, answer that race first before discussing retries.
    

## What to do differently

1. 1
    
    ### Recompute scale from the supplied units
    
    When the wallet-user numbers were supplied, your revised transfer and storage math dropped units and understated annual transfers, even though you used scale to justify storage and read choices. Carrying units separates representation from traffic and storage, so your design choices are anchored to the actual workload rather than a mistaken magnitude.
    
    Write rates, annual counts, and bytes as separate unit conversions before drawing conclusions.
    
    For example
    
    > “Given 10 million wallet users, 1 transfer per week is 10,000,000 / 604,800 ≈ 16.5 transfer creations per second, or 10,000,000 * 52 = 520 million transfers per year. Two balance or history checks per day is 20 million / 86,400 ≈ 231 reads per second. At 500 bytes per transfer, raw history is 520 million * 500 ≈ 260 GB/year; seven years is about 1.8 TB before indexes, replicas, and overhead.”
    
    #### Practice before your next interview
    
    Redo three capacity estimates using users, frequency, record size, and retention, keeping units on every line.
    
    [Learn more: Numbers to Know for System Design Interviews: Premature sharding](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know#premature-sharding)
    
2. 2
    
    ### Bound pending status refreshes
    
    For pending transfers, you read local tables first but then considered synchronously calling the payment platform on user reads, without a freshness window, throttle, or background policy. This keeps user-read latency tied to your database, while still making progress on stale pending transfers under controlled vendor load.
    
    Define when reads return local pending state and when refresh work is queued or rate-limited.
    
    For example
    
    > “For getTransactionStatus, read the local transaction row and return its status plus last_checked_at. If it is completed or failed, return immediately. If it is pending and last_checked_at is recent, return pending without a vendor call. If it is stale, enqueue an idempotent refresh job keyed by transaction_id, return pending, and let workers poll the vendor under a global QPS cap. The worker updates status and wallet balance in the same database transaction you already proposed.”
    
    [Learn more: Managing Long Running Tasks Pattern for System Design Interviews: Preventing Duplicate Work](https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks#preventing-duplicate-work)
    
3. 3
    
    ### Add a daily sweep for pending transfers that never get a callback
    
    You correctly modeled transfers as pending and accepted webhook or polling-based completion, but you never pinned down a concrete reconciliation cadence and stale-pending selection rule that would update missed callbacks within the expected recovery window. A callback handles the common case cheaply, and the sweep is the reconciliation path for dropped notifications. By reusing the same transactional status-change rule, duplicate or late updates stay safe, at the cost of a background job and bounded staleness for rare exceptions.
    
    Define webhook as the normal completion path and a daily reconciliation sweep over still-pending transfers.
    
    For example
    
    > “Store the transfer row first as pending, then save the vendor transfer id when createTransfer returns. When the vendor webhook arrives, look up by vendor transfer id and, in one database transaction, change transactions.status from pending to completed or failed and update the wallet’s ready_to_use and on_hold amounts. If the row is already terminal, do nothing. Separately, run a daily job that selects transfers still in pending, calls the vendor status API by vendor transfer id, and applies the same transaction. That job is what recovers when your webhook endpoint was down or the vendor never delivered the event.”
    
    [Learn more: Payment System: Transaction safety despite asynchronous payment networks](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system#3-the-system-should-guarantee-transaction-safety-and-financial-integrity-despite-the-inherently-asynchronous-nature-of-external-payment-networks)[Learn more: Dealing with Contention Pattern for System Design Interviews: Conditional Writes](https://www.hellointerview.com/learn/system-design/patterns/dealing-with-contention#conditional-writes)
    

## What to keep doing

1. 1
    
    ### Protected the same-wallet money invariant
    
    After an initial retry-idempotency detour, you recovered to the core concurrency issue and used row serialization plus a conditional balance update. That directly prevents double spending under horizontally scaled servers.
    
    Keep naming the exact shared state and the atomic write that protects it.
    
    For example
    
    > “Your final answer made the wallet row the serialization point and used a condition like update balance where balance >= requested_amount, so only one of two simultaneous withdrawals can consume the same available funds.”
    
2. 2
    
    ### Persisted transfer intent before the vendor call
    
    You gave a strong sequence for vendor uncertainty by storing the transaction as pending before contacting the payment platform. That turns timeout and crash recovery into reconciliation against a durable local record.
    
    Keep explaining the failure that the ordering prevents.
    
    For example
    
    > “You pointed out that if the vendor accepts a request but the local row was never written, later webhooks or retries cannot map the movement back to your system. Writing the pending row first preserves that mapping.”
    
3. 3
    
    ### Separated available and held funds
    
    You introduced a ready-to-use versus on-hold balance split and used it to reason about pending withdrawals before final completion. The model makes pending transfer state visible in both admission checks and user-facing balances.
    
    Reuse this pattern when a request reserves scarce user-owned value.
    
    For example
    
    > “In your example, a wallet with 1000 and a 600 pending withdrawal had only 400 ready to use, so another 500 withdrawal was rejected locally instead of waiting for the vendor.”
    

## Competency Breakdowns

## Rate this feedback

How helpful was this feedback?

1 Stars2 Stars3 Stars4 Stars5 Stars

What would make it more useful? (optional)

Get more credits to keep practicing

You're out of Live Practice credits.

1. Main takeaways
    1. 1.Put a limit on any external call users can trigger.
    2. 2.For every added piece, say its job, cost, and trigger.
    3. 3.Answer the case you were asked, then name nearby cases separately.
2. What to do differently
    1. 1.Recompute scale from the supplied units
    2. 2.Bound pending status refreshes
    3. 3.Add a daily sweep for pending transfers that never get a callback
3. What to keep doing
    1. 1.Protected the same-wallet money invariant
    2. 2.Persisted transfer intent before the vendor call
    3. 3.Separated available and held funds
4. Competency Breakdowns
    1. 1.Problem Navigation
    2. 2.Solution Design
    3. 3.Technical Excellence
    4. 4.Technical Communication