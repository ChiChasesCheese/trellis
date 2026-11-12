# Timeline (per minute)

| min | phase | candidate words | interviewer msgs | first question |
|---|---|---|---|---|
| 00 |  | 31 | 2 |  |
| 01 |  | 56 | 2 | When you say streaming, what do you mean exactly? |
| 02 |  | 54 | 1 | Does that change how you'd shape the system? |
| 03 |  | 87 | 1 | Can you turn that into notifications per second, both the daily average and the spike, and tell me what that implies for your design? |
| 04 |  | 31 | 1 | So what's the average per second from five hundred million a day, and how does that compare with the spike? |
| 05 |  | 44 | 2 | Now what's the peak per second, and what does that tell you about where the bottleneck will be? |
| 06 |  | 38 | 1 |  |
| 07 |  | 35 | 2 | Let's move on: what would the API look like for a product team sending a single payment receipt? |
| 08 |  | 62 | 1 | What is that ID for, and what happens if the product team retries the same request twice? |
| 09 |  | 18 | 1 | At the moment of that response, has the notification actually been delivered to the phone, or something else? |
| 10 |  | 61 | 1 | What exactly happens between the two hundred and the actual send, and what if the notification server crashes right after it acknowledged? |
| 11 |  | 95 | 1 | I pinned a question on the database: can it handle your hundred thousand writes per second at peak? |
| 12 |  | 68 | 0 |  |
| 13 |  | 154 | 1 | Now walk me through one message end to end: who calls Apple or Google push, the email provider and the SMS gateway, and what happens when one of those providers is slow or down? |
| 14 |  | 55 | 0 |  |
| 15 |  | 115 | 1 | What does the worker do with the messages that fail, and how do you avoid blocking the ones behind them? |
| 16 |  | 1 | 0 |  |
| 17 |  | 117 | 1 | But if Apple is down, how do your email and SMS messages in the same Kafka topic keep flowing, and how do you space out the retries? |
| 18 |  | 141 | 1 | How does the receipt avoid waiting behind the campaign? |
| 19 |  | 105 | 1 | When the campaign is running flat out, how do you make sure receipts still get through? |
| 20 |  | 78 | 0 |  |
| 21 |  | 58 | 1 | How do you make sure the user doesn't get two payment receipts? |
| 22 |  | 91 | 0 |  |
| 23 |  | 86 | 1 | But where does that check happen? |
| 24 |  | 67 | 0 |  |
| 25 |  | 94 | 1 | Now a different angle, how does a campaign to ten million users actually fan out into individual notifications? |
| 26 |  | 81 | 1 | Where does that expansion happen in your design, and who stores the audience list? |
| 27 |  | 119 | 1 | If that fan-out job dies after four million of ten million, how do you resume without messaging those first four million again? |
| 28 |  | 75 | 0 |  |
| 29 |  | 7 | 1 | After the crash, what state tells the job it already handled the first four million, and where is it stored? |
| 30 |  | 94 | 0 |  |
| 31 |  | 120 | 0 |  |
| 32 |  | 91 | 1 | What does that table look like after a year, and what do you do about it? |
| 33 |  | 86 | 0 |  |
| 34 |  | 75 | 1 | What optimizations would you apply to that table now? |
| 35 |  | 77 | 1 | What would you shard on, and do you really need to keep every row for three years? |
| 36 |  | 0 | 0 |  |
| 37 |  | 115 | 1 |  |
