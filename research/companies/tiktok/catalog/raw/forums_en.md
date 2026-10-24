# English forums and aggregators — TikTok / ByteDance interviews

Collected 2026-10-24. Window: 2025-10 to 2026-10-24 (older items are marked "background"). Every item: date, platform + URL, level/team/location, round, content, confidence.
Confidence: high = first-hand post with the problem text; medium = summary that names the problem; low = fragment, ask-for-advice post, or SEO.
Reach notes: LeetCode Discuss via `POST /graphql` (works with `ugcArticleDiscussionArticles` + `ugcArticleDiscussionArticle(topicId: ID!)`); Reddit via Arctic Shift (posts) and `.rss` (comments; throttled, retry with 30 s gaps); Blind with a browser User-Agent (post pages render the body; comment lists are mostly collapsed); HN Algolia; Hello Interview and 1point3acres through the Playwright browser; Glassdoor 403 (WebSearch snippets only); trueinterview.io question pages are Insider-gated (only the first ~100 words show) but its GitHub mirror holds the free questions.

---

## A. LeetCode Discuss  (https://leetcode.com/discuss/)

Keyword searches "tiktok", "bytedance", "byte dance", "tiktok senior/backend/onsite/phone screen/system design/2-2/usds/offer", filtered to posts from 2025-09-01. Result: only 6 real interview posts, no senior-backend ones. The site is dominated by Indian-company experiences.

| Date | topicId / URL | What | Level / team / place | Round | Confidence |
|---|---|---|---|---|---|
| 2025-09-03 | 7150750 · https://leetcode.com/discuss/post/7150750/tiktokbytedance-interview-experience-by-8vcmw/ | "Tiktok bytedance Mid level (2-1) Interview": **2 LC problems** — LC 1293 (shortest path in grid with obstacle elimination) and "a weirdly worded graph problem about friends being split into groups ... boiled down to BFS while keeping track of even and odd levels" (= bipartite check); **1 system design — "design monitoring system that can send alerts that users can configure"**, "just followed HelloInterview format structure"; **1 behavioral** (favorite project, biggest challenge/conflict, anything you'd do differently). Comp: "211k base, 25% bonus, 36k RSU each yr = 300k TC". 2,419 views. | 2-1 (mid), US (TC in USD), team unstated | 2 coding + 1 SD + 1 BQ | high (first-hand, short) — just before the window, kept because it is the only US mid/senior loop on LC |
| 2025-12-19 | 7423011 | "TikTok OA Report | Research Assistant Internship": CodeSignal, proctored, **4 problems / 70 min**; Q1 easy combinatorics/counting; Q2 easy simulation with a tricky edge case; Q3 medium-hard "complex simulation and state management"; Q4 medium string counting/permutations; score 460/600 (Q4 240/300 on hidden tests). | intern / research | OA | high for format; role not ours |
| 2026-04-11 | 7875289 | "Tiktok 26ng sde VO": **in-memory file system** (LC 588: `ls`, `mkdir`, then addContentToFile / readContentFromFile). Posted by a prep-service account. | new grad 2026 | VO | medium (service-posted) |
| 2026-04-11 | 7875303 | "Most Frequent Subtree Sum in a Binary Tree" (LC 508, return all values with the highest frequency on ties). Same service poster. | n/a | n/a | low |
| 2026-10-14 | 8572114 | Question only: "Anyone attended interview with titok for SRE role, what level of DSA questions ..." | SRE | coding | low |
| 2026-10-09 | 8563517 | Question only: TikTok MLE intern, data search/visual search team. | intern | technical | low |

Background (found via source lists of derivative repos, not re-fetched): 2025-03 TikTok Singapore Android SWE-2 (leetcode.com/discuss/post/6802671/), 2024-05 Singapore iOS (…/5550559/), 2021-02 ByteDance Singapore rejected (…/1100219/).

## B. Reddit

Arctic Shift post search (`title=` and `selftext=` for tiktok/bytedance, after 2025-09-01) over r/leetcode, r/csMajors, r/cscareerquestions, r/ExperiencedDevs, r/developersIndia, r/cscareerquestionsEU, r/SoftwareEngineering, r/recruitinghell → 96 posts; ~15 are interview or offer posts that matter. Comments from `.rss`.
r/ExperiencedDevs, r/developersIndia: no TikTok/ByteDance interview posts in the window.

| Date | URL | Content | Level / team / place | Confidence |
|---|---|---|---|---|
| 2026-04-12 | https://reddit.com/r/leetcode/comments/1sjfel3/ | "Aced interviews, how to avoid downleveling": ~3 YOE, Singapore, **3 interviews all with managers**, passed all; worried about 2-1 vs 2-2. Comments (same day): interviews were "Technical discussions (deep) + leetcode + system design ... They want you to solve leetcode medium to hard in 20 mins"; "last interview is usually with hiring manager doing behavioral. Offer negotiation is done with recruiter"; "first time was them moving me to a new team because i was strong candidate but not exactly what the hiring manager was looking for"; OP later: "They offered me 3-1"; another commenter: "3 interviews sounds like a 2-1 loop ... If you didn't have a 2-2 loop then you won't be considered for it unless you ask specifically. Bytedance used to aggressively uplevel folks ... there's less competition in hiring so it doesn't happen as aggressively"; "There is a huge gap between 2-1 and 2-2 on levels website". | SG, SWE, ~3 YOE | medium (several consistent comments, SG) |
| 2026-04-09 | https://reddit.com/r/leetcode/comments/1sgn71t/ | Same author, SG loop in detail: (1) coding + technical discussion, "a hard LC question. I solved it, then we had a technical discussion"; (2) coding + technical discussion (research papers, easy question because time ran out); (3) **system design + technical discussion: scheduled 1 hour, ran 3 hours; ~1 h on experience then ~2 h on "a very famous system design question and he dug very deep"**; all 3 with managers; final HR call; "Both the first and second interviewers submitted feedback on the same day". | SG, SWE | high (first-hand) |
| 2026-01-29 | https://reddit.com/r/leetcode/comments/1qqb5n6/ | "Backend Software Engineer – Singapore – loop done": 3 technical rounds. R1: "answered every theoretical system design question and solved a hard problem in 20 minutes". R2: "theoretical system design questions" + 2 mediums in 20 min. R3: **hiring manager asked about experience and projects, then system design: listed requirements, entities, flow, drew the diagram; then the HM asked 4 questions about the one specific flow that was the whole point of the design and the candidate hesitated and contradicted himself**; HM took a screenshot of the final design. | SG, backend, ~2 YOE | high (first-hand) |
| 2026-01-18 | https://reddit.com/r/leetcode/comments/1qg6vxf/ | Pre-interview question: backend SG, "All interviewers will be Chinese"; hard DP? backtracking / "generate all"? (20 comments, not fetched) | SG, backend | low |
| 2026-09-03 | https://reddit.com/r/leetcode/comments/1w6uktk/ | "Tiktok / Bytedance Singapore": three tech rounds; claim "coding rounds are not pure coding: 40 mins behaviour + open question and 20 mins coding". Comments (2026-09-04): "ByteDance interviewers are curt and efficient"; "mostly graphs and strings, small variations ... upper middle/lower hard LC tier"; "they have high churn like Meta ... a lot of recycling"; "LC-Medium to Hard. One guy asked me to implement Regex, ... another a queue with 2 stacks"; **"two coding rounds all start with 30 mins resume digging first"**; "First round is an easy BFS array flatten + AI coding assessment" (frontend); a commenter who "worked at TikTok SG for 3 years and don't speak a word of Mandarin" disputes the claim that Mandarin is required; the original commenter says it applied to the ML e-commerce recommendation team since mid-2025 for a senior role. | SG, mixed roles | medium (several concordant comments; the Mandarin claim disputed) |
| 2026-04-21 | https://reddit.com/r/leetcode/comments/1ss8ba6/ | "TikTok Interview Timeline" — **San Jose** SDE mid-level: round 1 LeetCode (feedback next day), then system design round ("3 business days" waiting). Comments: "Hiring manager round decides everything (behavioral). I failed and was moved to a different team's interview loop"; "I've been on pause on their pipeline for ever since the Oracle situation ... since nov 2025"; "choose the teams that work on core AIML infra for search/recommendation". | San Jose, SDE mid | medium |
| 2026-05-06 | https://reddit.com/r/leetcode/comments/1t5pu24/ | San Jose, 3rd round "mostly behavioral": "One of the first questions they asked was whether I spoke Chinese"; HM asked about background; candidate had to repeat answers. | San Jose | low-medium |
| 2026-05-11/12 | https://reddit.com/r/leetcode/comments/1taje6a/ , …/1tbi9rq/ | San Jose: "passed all 3 rounds, the first 2 were technical and the 3rd was a mix of behavioral/technical with a hiring manager", then a **department-manager round**; HR slow/unresponsive except for scheduling. | San Jose | medium |
| 2026-05-01 | https://reddit.com/r/leetcode/comments/1t18egt/ | Round 2 on a Tuesday, feedback for round 1 came 2 days later; HR unresponsive on next steps. | US | low |
| 2026-01-23 | https://reddit.com/r/leetcode/comments/1ql95y7/ | "ByteDance / TikTok Hiring Pause / Freeze?": recruiter emailed that interviews were being paused (poster blames "the whole Oracle thing"). 2026-04-22 commenter: "on pause in their pipeline since Nov 2025". | US | medium (two reports) |
| 2025-11-02 | https://reddit.com/r/cscareerquestions/comments/1omb5ze/ | SDE req closed mid-loop; recruiter moved the candidate to SRE; final round pending. Shows the cross-req rematch. | US | medium |
| 2026-08-09 | https://reddit.com/r/leetcode/comments/1vk9kg8/ | "Tiktok USDS SRE coding round in 5 days": recruiter said "prepare medium to hard leetcode". | USDS SRE | low |
| 2026-06-13 | https://reddit.com/r/leetcode/comments/1u4zr8g/ | Offer: **TikTok Seattle SRE 2-1: base $185k, annual bonus $50k, cash incentive $25k/yr, relocation $5k, TC $250k** vs Bloomberg. | SRE 2-1 | medium (first-hand numbers) |
| 2025-11-26 | https://reddit.com/r/leetcode/comments/1p74jfg/ | Offer: SRE 2-1 (Palo Alto area): base $210k, RSU 600 units at $240 over 4 years, sign-on $35k, bonus 25%. | SRE 2-1 | medium |
| 2025-10-15 | https://reddit.com/r/leetcode/comments/1o7mxj9/ | "ByteDance OA ... I scored 600/600 and still got rejected": OA is not a reliable gate. | new grad/intern | low |
| 2026-06-11 | https://reddit.com/r/leetcode/comments/1u3fpb4/ | Dataset of 300 OA/interview questions: TikTok is 26 of 300 (3rd after Amazon 38, Uber 29); questions are "practical data manipulation dressed up as business problems". | mixed | low |
| 2026-09-08 | https://reddit.com/r/leetcode/comments/1waqrk0/ , 1wao995 | London Solutions Engineer asking whether tagged questions are accurate; "Mind blown by the talent at TikTok" (295 comments, culture talk). | n/a | low |

OA reports (new-grad/intern, background for what "OA" means here): CodeSignal, 4 problems / 70 min (r/leetcode 1nadwk4 "416/600", 1rd4s9s, 1s4mgf2, 1wu6ww4 "1200/1200").
Comments for 1qg6vxf, 1ql95y7, 1u4zr8g, 1omb5ze, 1t5pu24 could not be fetched (Reddit `.rss` throttling); only the posts themselves are recorded.

## C. Blind  (https://www.teamblind.com/post/...)

Search pages `teamblind.com/search/<query>` (queries: tiktok interview/usds/system design/2-2/onsite/hiring manager/coding/phone screen, bytedance system design/2-2/offer/senior interview) returned 152 distinct posts; 140 fetched. Bodies render, comments are mostly collapsed (only what shows below). 2020-2024 posts are only background.

In-window and near-window posts that matter:

| Date | URL slug | Content | Confidence |
|---|---|---|---|
| 2026-10-13 | tiktok-usds-jv-senior-software-interview-process-pws7m0wc | "Tiktok USDS JV Senior software interview process" (poster at Microsoft): "I interviewed with bytedance last year and those were **pass/fail interviews**. I failed the third one where he asked lc medium hard but I couldn't finish typing fully in 20 mins and then we deep dived into a **consistency system design problem** which I eventually came to a solution which tiktok actually uses in the field. Should I expect the process to be similar?" One reply (Oct 14, Meta): "Pretty much the same process". | medium (one report + one confirmation) |
| 2026-10-22 | snap-l5-vs-tiktok-2-2-senior-h0kmt2vh | Offer eval: **Snap L5 $550k WA vs TikTok 2-2 senior $470k CA, both infra teams**; comment: "Tik tok makes you work with Chinese teams at midnight". | medium (offer numbers) |
| 2026-10-21 | tiktok-bytedance-employees-compensation-leveling-guidance-needed-urgent-rwuks4o3 | Candidate seeking comp/level info; replies: "The stock is worth pennies. You will never own 90% of your offer. If you don't speak Mandarin, you will not survive."; "do you speak mandarin? natively? if not, whatever money doesn't matter, run". | low (opinions) |
| 2026-09-24 | is-it-true-that-in-bytedance-they-switched-their-levels-from-1-1-and-2-1-to-l1-and-l2-to8hs3d8 | Recruiter told the poster levels were relabeled **1-2 = L1, 2-1 = L2, 2-2 = L3**; replies: "Yeah. Basically the new levels are 2 lower than the equivalent Meta/Google ... 2-2 equals new TikTok L3 which equals roughly Meta IC5"; "Yes it's true." | medium-low (3 concordant replies, no official confirmation found) |
| 2026-08-18 | bytedance-interview-timeline-ptpnexbp | Infra team candidate: "last time they scheduled all three interviews at once, back-to-back, and told me they would cancel the later rounds if I didn't make it through. This time the process seems a little different"; contact is a recruiter in Asia, "why don't they have US recruiters?" | low-medium |
| 2026-07-08 | tiktok-ai-assisted-coding-interview-mrho747e | Tech screen where "Recruiter said to have my own ide with ai assistance installed". (matches TrueInterview's AI-assisted Order Validator.) | medium |
| 2026-06-24 | tiktok-interviewer-spoke-mandarin-for-5-minutes-… | Interviewer spoke Mandarin for 5 min despite repeated "I don't understand"; "he then asked me a system design question in a coding platform, despite recruiter saying this is a coding round. The tool does not have any way to draw and only code. I got rejected a week later". | medium |
| 2026-08-05 / 2026-07-27 / 2026-08-04 / 2026-07-02 | google-l4-vs-tiktok-2-2-ua4u1qxw, pinterest-ic14-versus-tiktok-usds-2-1-znmgypbt, pinterest-ic13-vs-tiktok-usds-2-1-dsjrglzd, tiktok-offer-xo57lzto | Offer evaluations (comp numbers in `loop.md`/`company.md`). | low-medium |
| 2026-01-10 | bytedance-senior-engineering-manager-interview-process-0w1moyxy | EM asking for process; no replies. | low |
| 2025-11-28 | tiktok-coding-interview-what-do-they-ask-1gudrufj | Asks whether TikTok questions come from "last 30 days / 3 months / further"; no answers. | low |
| 2025-09-17 | tiktok-interviewer-asked-inappropriate-questions-1unjb725 | Last round with the hiring manager asked "Are you married? Do you have kids?"; then ghosted (37 comments). Relevant to what an HM round can feel like; not a content source. | low |
| 2025-09-02 | tiktok-interview-process-for-senior-swe-01772lfc | Senior SWE (Google): round 1 = 1 h via **HackerRank & Zoom, 2 LC easy-medium**; round 2 = "another 1-hour interview via **Lark + HackerRank**", interviewer with 20+ YOE, unsure if SD or coding. | medium |
| 2025-05-30 | interview-journey-meta-airbnb-tiktok-snap-bj01gcot | Amazon L6, 9 YOE: "**TikTok pass/fail rounds (pass but downlevel to 2-2): TikTok has an unusual process of four pass/fail rounds on different days. 1x coding (screen), 1x system design, 1x project walkthrough/experience, 1x HR/experience. System design was a standard prompt. Overall nothing challenging. I didn't get feedback on the downlevel reasoning**" (staff/3-1 target, got 2-2). Also: "TikTok 3-1 (pass): practical (non-LC) coding" in the screening step. | medium (first-hand, senior; just outside the window) |
| 2025-04-21, 2025-04-05 | tiktok-hiring-manager-insight-1pdpseue, tiktok-hiring-manager-round-ohywmwrg | Recruiter screen follows resume pass; resume reviewers "not always HM"; 2-1 SDE candidate asks if HM round is a formality; replies "very loose hiring criteria ... average tenure is 7 months" (opinion). | low |
| 2025-03-30 | tiktok-level-2-2-lowball-offer-bp1xzovd | MLE 2-2 USDS Seattle: base $215k + 25% bonus, RSU $330k/4y, no sign-on, 7 YOE + PhD; replies call it a 2-1-level offer; "The least offer I've seen for level 2-2 is 270 base". | medium |
| 2025-02-05 | tiktok-rejected-after-passing-interviews-s7wdgi3w | "They said I did well on interviews but hiring priorities have changed, and they could share my profile with other teams." | medium (pattern repeated elsewhere) |
| 2024-10-18/25, 2024-06-11 | tiktok-2-12-no-system-design-interview-dv0i0tj5, tiktok-system-design-interview-zdxwrk5j, tiktok-system-design-interview-6laxh7na | background: loops "1 coding + 1 system + 1 behavioral + 1 HR"; "TikTok tends to schedule both rounds (1 coding and 1 SD) within 2 days"; some e-commerce 2-1/2-2 loops told "2 rounds of DSA and one behavioral with TA partner" (no SD). | low-medium (2024) |
| 2024-07-17 | will-i-pass-tiktok-coding-round-cwshnxpu | background: two coding rounds, each began with domain-specific questions, then **3 LC mediums (round 1)** and 2 LC mediums (round 2) "not including follow ups". | low (2024) |
| 2024-01-22 | tiktok-bytedance-huge-compensation-update-bmduw72l | RSU schedule changed from 15/25/25/35 to **20/25/25/30**, 12-month cliff then quarterly vesting; 287 comments; commenter notes "buyback program ... limited selling of vested stock" (no IPO). | medium (matches levels.fyi vesting table) |
| 2023-2020 | many (tiktok-hiring-manager-round-*, bytedance-system-design-*) | Asks without content; HM round repeatedly described as behavioral + project ("mostly behavioral, with maybe a coding question at the end", 2020). | low |

Blind-wide patterns across the 140 posts (all low confidence, opinions): interviewers' accent/Mandarin switching; rounds booked back-to-back then cancelled on failure; pass/fail per round; ghosting after HM; re-matching across teams; long hours ("I worked 100", 2025) and Chinese-team overlap at night.

## D. Hacker News

Algolia queries "tiktok interview", "bytedance interview", "tiktok engineer interview process" with `created_at_i > 2025-09-01`: no interview-process content (only politics/Show HN noise). Dropped.

## E. Glassdoor (WebSearch snippets only; fetch is 403)  — all low confidence

- Sep 2026, San Jose, recruiter-sourced: live coding "the original question in leetcode, lc445" (Add Two Numbers II) right after a brief introduction, then deep dive into the resume and "how the candidate would scale their choices".
- Sep 2026, Singapore, backend: discussion of prior work, then system design and engineering topics — "high traffic, idempotency, distributed consistency, database indexing, data archiving, asynchronous processing, reconciliation, and downstream protection" — and a medium coding problem at the end.
- May 2025, San Jose: "design a system for ingesting large amounts of data and flagging when certain rules are met"; three rounds, last = behavioral + system design.
- 2025 San Jose loop: HR call, virtual onsite LeetCode, virtual onsite "Domain Knowledge", virtual onsite hiring-manager call.
- 2026 reviews: "3x leetcode medium with some behavioral mixed in"; an "AI-assisted coding task".
- Glassdoor aggregate quoted by a search result: 38.8% positive experience, difficulty 3.12/5 (TikTok overall); Senior SWE: difficulty 3.4/5, 17% positive (older interviews).
URLs: https://www.glassdoor.com/Interview/TikTok-Senior-Software-Engineer-Interview-Questions-EI_IE2230881.0,6_KO7,31.htm , https://www.glassdoor.com/Interview/TikTok-San-Jose-Interview-Questions-EI_IE2230881.0,6_IL.7,15_IM761.htm

## F. PracHub  (https://prachub.com)

- Guide https://prachub.com/interview-guide/bytedance-software-engineer-interview-questions-guide-2026 (updated 2026-09-24; 21 candidate experiences, 5 shown; bank of 138 questions by its own count, 214 on the company page): loop = recruiter screen, OA (reported by some, skipped by others), technical phone (HackerRank or Lark code pad; coding + CS theory, 1 h), virtual onsite of **three technical rounds** (coding, system design, fundamentals, past projects), final HM or HR round; 3-6 weeks; "some rounds were in Chinese". Candidate rows: TikTok LIVE SWE rejected at phone screen (Possible Bipartition, HackerRank); TT USDS SWE: three rounds with LeetCode 3 and 210 and a 207 variant, then design, "ghosted after HR call"; E-commerce backend intern rejected after Spiral Matrix follow-ups; new-grad tic-tac-toe `GameOver` O(1) (modified LC 348) in Chinese. System design prompts listed: ticket booking at release time; **payment system (TT USDS round 3)**; online auction with MQ and caching to prevent bid races; distributed KV cache with timestamped keys and strictly increasing versions; global API rate limiter; real-time top-k trending posts with global and regional rankings; RBAC schema. Fundamentals: URL-entered flow (DNS/TCP/TLS/HTTP), TCP vs UDP, MySQL clustered vs secondary, B+tree vs hash, Redis sorted sets and persistence, deadlock, **monitoring/tracing/telemetry (TT USDS round 2)**. HM/project questions: most complex architecture and its bottlenecks; production outage triage; stability and latency SLA metrics; slow query/service optimization; architectural disagreement settled with metrics; monolith-to-microservices migration with zero downtime. Medium (aggregator; individual rows not independently verifiable).
- Question page https://prachub.com/interview-questions/design-a-payment-system-time-boxed-high-level-design (2026-09-10, ByteDance SWE onsite, medium; source: "three rounds and an HR call, then silence"): "Design a system that lets a product accept payments ... purchase confirmed only after payment succeeds ... integrates with an external PSP ... correctness before latency: a user must never be charged twice; an order must never be marked paid without collected money; keep it high level". Follow-ups: (1) seller payouts and how the ledger changes; (2) routing between two PSPs and failover when one degrades; (3) a payment pending for an hour — how resolved, what the user sees; (4) full and partial refunds without breaking reconciliation. Strong answer = flow + idempotency at each retryable step + payment state machine + append-only ledger in integer minor units + reconciliation with PSP + lost/duplicate notifications. Medium.
- Company page https://prachub.com/companies/bytedance (214 questions; first two pages = 40, newest 2026-10-10): items relevant to a backend loop: "Implement an Idempotent Versioned Database Update" (2026-08-09, SWE, locked); "Simulate a fixed-capacity LRU cache" (2026-10-04, Hard); "Implement a binary min-heap and use it to order courses with prerequisites" (2026-10-04, coding round ~30 min); "Implement Expiring LRU Cache" (2026-04-14, Hard); "Build a Removable Timestamp-Ordered Task Scheduler" (2026-08-20, locked); "Split n people into two groups so no disliked pair shares a group" (2026-09-23, Hard); "C++ vs Go for backend services: memory, concurrency" (2026-09-25, intern); "Elasticsearch: index mapping and inverted index" (2026-09-25); "TCP vs UDP" (2026-09-25); "Tell me about a challenge you faced at work" (2026-09-23, technical phone screen 1 h, Hard); "How You Build Service Stability and Troubleshoot Production Incidents" (2026-09-05, SRE Senior+); "Design a Data Service for Downstream Consumers" (2026-08-28, Data Engineer); "Evaluate a Migration from MySQL to MongoDB" (2026-08-13).

## G. Hello Interview community questions  (https://www.hellointerview.com/community/questions?company=TikTok, Playwright)

13 TikTok questions total; 5 visible without Premium (ByteDance filter: none). Page-level counter "13,941 total reports" is the site-wide total.

| Title | Type | Level | Last asked | Reports | Description |
|---|---|---|---|---|---|
| Design a TikTok Live Coin Tracking System | System design | Senior | Early Sept 2026 | 1 | "Design a globally distributed, highly accurate coin tracking and settlement system for a live-streaming platform. The system must process real-time virtual gifting from users worldwide with **guaranteed idempotency**, ensuring **precise per-session earnings for creators and reliable weekly financial settlements**." |
| Design a Metrics Aggregator | System design | Senior | Late Sept 2026 | 1 | count-based metrics from services via a client library, histogram dashboard, time-bucket queries (StatsD/Datadog-style); common deep dives: hot keys, correctness under retries/duplicates, rollups, cardinality control. Page lists DoorDash, OpenAI, Rippling, LinkedIn +10 as other askers. |
| Design a Video Moderation System | System design | Senior, Manager | Mid April 2026 | 4 | "ingest millions of daily video uploads, apply ML-based risk scoring and rule-based moderation logic in near real-time, and automatically handle policy violations while maintaining audit trails"; deep dives: near-real-time SLA with heavy ML, rule engine updated without redeploy, idempotent enforcement and auditability, global scale/data residency. |
| LeetCode 721 Accounts Merge | Coding | Senior | Late July 2026 | 1 | union-find / graph over shared emails. |
| LeetCode 101 Symmetric Tree | Coding | Senior | Mid Aug 2026 | 1 | |
| (3 hidden) | SD "Mid-Senior" 34 reports; Coding "Senior-Staff" 19 reports; Behavioral "Mid-level" 11 reports | | | | placeholders, text not shown |

Confidence: medium-high (first-hand submissions, de-identified), small n.

## H. 1point3acres (https://www.1point3acres.com/interview/…, Playwright; body text behind login)

- `…/interview/company/tiktok` lists 5 recent items: "TikTok CodeSignal OA March High-Frequency Questions Summary" (2026-03-20, new grad), "TikTok Research Assistant Internship OA (Dec 2025)", "TikTok Machine Learning Engineer Interview Experience: Recommendation Systems Focus" (2025-12-08, job-hopper), "TikTok New Grad SDE Round 2 Onsite" (2025-12-04), "TikTok SRE-SWE Technical Phone Interview" (2025-10-17). Bodies hidden.
- `…/interview/problems/company/bytedance` ("ByteDance / TikTok Hot Questions", 79 questions, updated ~3 days before 2026-10-24): Coding 58 / System Design 11 / Behavioral 4 / Other 6; frequency buckets: Very high 1, High 6, Medium 7, Low 16, Single report 49; recency: 15 asked in the past 30 days, 29 in 90 days, 14 in 180 days; roles SWE 65, MLE 12, RS 8, Infra 8; "Coding problems 381". Visible free-preview item: "Basic Calculator (with and without parentheses)" (60 min, medium, 5 related discussions). Other rows are member-only; the tags reveal: a TTL hash-map/LRU (High, 9 discussions), graph BFS/DFS/topological sort (High, 8), grid BFS/DFS/union-find (High, 10), multi-head attention (MLE), intervals, tree DP, k-group linked-list reversal (7), heap scheduler, flash-sale, payment/idempotency, Kafka, Redis, transactions, websocket/SSE, rate limiting, leaderboard, top-k, schema design/versioning, ingestion, job system, moderation, feed.
- Guide `…/interview/guides/tiktok-interview-trend-2026q2` (2026-05-08, 10,372 views, partly hidden): "TikTok hiring (across USDS, E-commerce, Ads, Monetization, SRE, and MLE orgs) ramped up noticeably from late 2025 into 2026 Q2 ... the OA → phone screen → VO cadence is tight (**one round per week, only schedule the next if the previous one passes — otherwise early break**), and reschedules, ghosting, and cross-team rematches are common. The bar is medium-high: coding is mostly LC medium originals or light variants, but deep dive on resume and ML/system fundamentals carries growing weight — especially for MLE / SRE / Backend roles." Question distribution (105 threads): general coding 70 (67%), system design 11 (10%), ML coding/debugging 14 (13%), behavioral/other 10 (10%). Top hot topics visible: #1 Number of Islands and variants (same-shape, flow direction, BFS-only) 11; #2 LRU/LFU (with TTL) 5; #3 Content moderation system design (with ML infra) 4. "Notable Changes" headings (text hidden): HR-initiated reach-outs surge; **cross-team rematch is now the norm**; **system design is mandatory for NG**; MLE fundamentals strict; **HM round occasionally requires live pseudo-code**; USDS/SRE recruiting is a separate track. Also: "many failures are not from missing the algorithm but from shallow BQ answers, weak fundamentals, or IDE pitfalls (HackerRank/Lark have no default input, so candidates must construct test cases)".
- `…/interview/thread/1040939` "ByteDance SDE General Onsite Interview: TikTok System Design (Round 3)": "TikTok **video view history system design** questions and scale discussion" (date not visible; body hidden).
- Confidence: medium for the aggregate numbers (self-reported by the site), low for individual items.

## I. Prep-site guides (SEO-grade; used only for corroboration)

- Codemia guide https://codemia.io/guides/tiktok-software-engineer (updated 2026-02): recruiter 20-30 min; phone screen 60 min with 2-3 medium-hard coding problems; optional second screen; onsite coding 60 min each (1-2); onsite system design 45-60 min "often related to video, content delivery, or recommendations"; HM 30-45 min; 3-6 weeks. SD prompts: short-video recommendation, real-time video upload and processing pipeline (transcoding to multiple formats and resolutions), CDN for short videos. Low.
- Fahim ul Haq, Educative/"Engineering Enablement" Substack, 2026-09-29 https://engineeringenablement.substack.com/p/tiktok-software-engineering-interview : "no single universal loop"; 2025 Android SG: recruiter + 2 technical + 2 system design + behavioral, each ~1 h; 2026 backend SG: 3 technical mixing coding, SD, project discussion and HM; "a complete high-level design in a hiring-manager round, followed by detailed questioning on one flow"; seniors "practice ambiguous decisions, trade-offs, failure behavior". Low-medium.
- TrueInterview/GitHub mirror (see `github_repos.md` §1) is the richest guide; Interview Query and Dataford returned 429.

## J. Never cited
lodely.com, vervecopilot.com (AI question farms) — not used.

## K. TrueInterview filtered list: every ByteDance/TikTok question with a sighting date from 2025-10 on
Source: `data/questions.jsonl` of https://github.com/kevin-2023-code/Tech-Interview-Questions (2026-10-24). Format: reported date | format | difficulty | round | title | topics. "reported" is the month/day of the sighting; ranking within the same date is arbitrary. 345 questions in total; 204 carry a date (the other 141 are undated). Level tags per question are in `Tech-OA-Questions/companies/bytedance.md`.

```
2026-10-05 | system-design | medium | onsite | Ticket Booking System Under Flash-Sale Traffic |  
2026-10-01 | ai-coding | medium | phone-screen | LRU Cache |  
2026-09-28 | algorithm | medium | phone-screen | Spiral Matrix (LC 54) with Follow-Up Constraints | arrays,matrix 
2026-09-25 | algorithm | medium | phone-screen | Tic-Tac-Toe Game-State Check | matrix 
2026-09-15 | system-design | medium | phone-screen | Design a Monitoring Dashboard with Explicit Latency Goals |  
2026-09-10 | algorithm | medium | oa | Convert Identifier Naming in Docstrings | strings 
2026-09-10 | algorithm | medium | oa | Count Cyclic Rotation Pairs | arrays,strings,math 
2026-09-09 | blog | None | phone-screen | AI Agent Intern Technical Questions |  
2026-09-06 | blog | None | phone-screen,onsite | CAP, DB Indexing, Concurrency and Logging: Backend Fundamentals Oral Round |  
2026-09-06 | object-oriented-programming | medium | phone-screen,onsite | LRU Cache (with TTL and LFU Follow-ups) | hashing,linked-list 
2026-09-05 | blog | None | phone-screen | Explain TLS Handshakes and HTTPS Traffic Inspection |  
2026-09-05 | blog | None | phone-screen | Give a Technical Research-Project Deep Dive |  
2026-09-05 | blog | None | phone-screen | How You Build Service Stability and Troubleshoot Production Incidents |  
2026-09-05 | blog | None | phone-screen | Investigate an iOS Memory Failure |  
2026-09-05 | blog | None | phone-screen | SRE Background: Development vs. Stability Focus and Your Most Memorable Project |  
2026-09-05 | blog | None | phone-screen | Trace Source Code to an Executable |  
2026-09-04 | algorithm | medium | phone-screen | Restore IP Addresses | strings,backtracking,graphs 
2026-09-02 | object-oriented-programming | medium | phone-screen | Seller Task Scheduler | stack,heap,greedy 
2026-08-31 | blog | None | phone-screen | Data Engineering Experience Screen |  
2026-08-31 | object-oriented-programming | medium | phone-screen,onsite | Design In-Memory File System |  
2026-08-30 | system-design | hard | onsite | Top Songs by Country Leaderboard |  
2026-08-28 | system-design | medium | phone-screen | Choose Components for a Data Warehouse |  
2026-08-28 | system-design | medium | phone-screen | Design a Data Service for Downstream Consumers |  
2026-08-28 | system-design | medium | phone-screen | Model Data for Analytics, Reporting, and Applications |  
2026-08-25 | system-design | medium | phone-screen | AI-Driven QA Pipeline Workflow |  
2026-08-25 | blog | None | phone-screen | Motivation, Ambiguity, and Collaboration Screen |  
2026-08-23 | algorithm | hard | phone-screen | Enumerate All Simple Directed Cycles | graphs,backtracking 
2026-08-23 | algorithm | medium | phone-screen | Enumerate All Simple Directed Paths | graphs,backtracking 
2026-08-23 | blog | None | phone-screen | Explain the TCP Three-Way Handshake and Its Guarantees |  
2026-08-23 | blog | None | phone-screen | Explain Virtual Memory Beyond Physical RAM |  
2026-08-23 | algorithm | hard | phone-screen | Trace and Debug Agent Tool-Call Failures |  
2026-08-21 | algorithm | medium | phone-screen,onsite | Search in Rotated Sorted Array | arrays,binary-search 
2026-08-20 | algorithm | medium | phone-screen | Timestamped Task Scheduler | heap,greedy 
2026-08-17 | algorithm | medium | onsite | Create Binary Tree from Descriptions (LC 2196) | hashing,trees 
2026-08-17 | algorithm | medium | onsite | Pythagorean Triple in an Integer Array | arrays,hashing,two-pointers,math 
2026-08-17 | system-design | hard | onsite | Short-Video Recommendation System |  
2026-08-17 | algorithm | hard | onsite | Stickers to Spell Word (LeetCode 691) | strings,dynamic-programming,bit-manipulation 
2026-08-15 | algorithm | hard | phone-screen | Infer an Alien Alphabet from Sorted Words | topological-sort 
2026-08-13 | algorithm | medium | phone-screen | Build a Nested Comment Tree from Flat Records | hashing,trees 
2026-08-13 | system-design | hard | phone-screen | Evaluate a Migration from MySQL to MongoDB |  
2026-08-12 | algorithm | medium | oa | Distinct Cyclic Number Pairs | arrays,strings,hashing 
2026-08-06 | object-oriented-programming | medium | phone-screen | AI-Assisted Order Validator |  
2026-07-29 | algorithm | hard | phone-screen | Bounded Number Construction from Allowed Digits | arrays,backtracking,greedy 
2026-07-29 | algorithm | medium | phone-screen | Top K Largest Elements | heap 
2026-07-22 | sql | easy | phone-screen | Signup Activation Rate |  
2026-06-29 | algorithm | medium | phone-screen | Minimum Window Substring | strings,hashing,sliding-window 
2026-06-29 | blog | None | phone-screen,onsite | Project Deep Dive (Resume Drill) |  
2026-06-28 | algorithm | hard | onsite | Maximum Unique Character Subset | backtracking,bit-manipulation 
2026-06-28 | system-design | medium | phone-screen,onsite | Design Google News |  
2026-06-26 | algorithm | medium | phone-screen | Elements Appearing More Than n/3 in a Sorted Array | binary-search 
2026-06-25 | algorithm | medium | phone-screen,onsite | Reverse Nodes in K-Group (incomplete tail variant) | two-pointers,linked-list 
2026-06-24 | algorithm | medium | phone-screen,onsite | Basic Calculator I / II | strings,stack 
2026-06-24 | algorithm | medium | phone-screen | Remove Duplicate Letters for Lexicographically Smallest Result | stack 
2026-06-19 | blog | None | phone-screen,onsite | Dropout, Overfitting, Normalization, Loss Functions |  
2026-06-17 | algorithm | medium | phone-screen | Longest Zigzag Path in a Grid | graphs,dynamic-programming 
2026-06-16 | algorithm | medium | phone-screen | Longest Palindromic Substring | strings 
2026-06-16 | algorithm | hard | onsite | Median of Two Sorted Arrays | arrays,binary-search 
2026-06-16 | algorithm | hard | phone-screen,onsite | Number of Islands and Grid BFS Variants | graphs,matrix 
2026-06-16 | algorithm | medium | onsite | Sliding Window Maximum | arrays,sliding-window,stack 
2026-06-16 | algorithm | medium | phone-screen | Validate Binary Search Tree | trees 
2026-06-16 | algorithm | medium | onsite | Word Break | strings,dynamic-programming 
2026-06-15 | object-oriented-programming | medium | phone-screen,onsite | Parallel Courses III |  
2026-06-11 | object-oriented-programming | medium | phone-screen | Contiguous Memory Allocator II |  
2026-06-11 | system-design | medium | onsite | Recent Like Count and Top Posts in a Sliding Window |  
2026-06-08 | algorithm | easy | phone-screen | Top K Frequent Elements | hashing,heap 
2026-06-06 | algorithm | medium | phone-screen,onsite | Print Execution Order in a DAG and Detect Cycles | graphs,topological-sort 
2026-06-06 | algorithm | medium | phone-screen,onsite | Course Schedule and Topological Sort on a Directed Graph | graphs,topological-sort 
2026-06-04 | algorithm | medium | phone-screen,onsite | Topological Sort / Course Schedule for Ads | topological-sort 
2026-06-03 | blog | None | phone-screen | RAG / Agent / Kafka Oral Drill |  
2026-06-01 | system-design | medium | onsite | Video-Keyword Association Review System |  
2026-05-31 | algorithm | medium | oa | House Segments After Deletions | arrays,hashing 
2026-05-27 | object-oriented-programming | easy | phone-screen,onsite | Design a HashMap |  
2026-05-27 | algorithm | medium | onsite | Shortest Path in a Grid with Obstacle Removal | graphs,matrix 
2026-05-25 | blog | None | phone-screen,onsite | SRE Linux / Networking Troubleshooting Round |  
2026-05-20 | blog | None | onsite | Hiring Manager / Final Behavioral Round |  
2026-05-20 | system-design | medium | onsite | Realtime Auction Bidding System |  
2026-05-13 | algorithm | medium | phone-screen | Course Schedule Cycle Detection | graphs,topological-sort 
2026-05-06 | algorithm | medium | phone-screen,onsite | Kth Largest Element / Quick Select | sorting 
2026-05-01 | algorithm | medium | phone-screen,onsite | Hand-Code Self-Attention and Cross-Entropy |  
2026-04-28 | system-design | hard | phone-screen | Design a Synchronized Live Comment Overlay |  
2026-04-28 | algorithm | medium | phone-screen | Implement Sorted Search and Array Updates | binary-search,arrays 
2026-04-26 | blog | None | phone-screen | Defend a Project's Schema, Indexes, and Concurrency Model |  
2026-04-23 | system-design | hard | onsite | Model Campaigns, Targeting, and Edit History for a Demand-Side Ad Platform |  
2026-04-20 | object-oriented-programming | medium | onsite | Implement Sliding Windows and LRU Cache |  
2026-04-20 | algorithm | medium | onsite | Longest Subarray of Ones | sliding-window 
2026-04-20 | algorithm | hard | oa | Sort Every Concentric Matrix Border Clockwise | matrix,sorting 
2026-04-19 | algorithm | medium | phone-screen | Compute Minimum Parentheses Additions | strings,greedy 
2026-04-17 | system-design | hard | onsite | Design Content Moderation System |  
2026-04-17 | blog | None | phone-screen | Describe a Favorite Project and Its Hardest Technical Challenge |  
2026-04-15 | algorithm | hard | phone-screen | Search Words in a Character Grid | tries,backtracking 
2026-04-12 | blog | None | onsite | Explain a Difficult Project and Its Scaling Decisions |  
2026-04-12 | blog | None | onsite | Explain Database Index Benefits and Write Costs |  
2026-04-09 | algorithm | medium | phone-screen,onsite | Number of Islands (Plain and Streaming) | graphs 
2026-04-05 | algorithm | medium | phone-screen | Longest Substring with At Most K Distinct Characters | strings,hashing,sliding-window 
2026-04-05 | algorithm | hard | phone-screen,onsite | Minimum-Cost Path on a Grid with Fuel and Recharge Cells | graphs,dynamic-programming 
2026-04-04 | sql | medium | phone-screen | Campaign Efficiency Metrics and Below-Average CTR |  
2026-04-04 | blog | None | phone-screen | Diagnose Low CTR in an Advertising Campaign Funnel |  
2026-04-04 | algorithm | medium | phone-screen | Find Maximum Chain Activations | graphs 
2026-04-04 | algorithm | medium | phone-screen | Probability That One Fair Die Beats Another | sorting,two-pointers 
2026-04-02 | algorithm | medium | phone-screen,onsite | Tree Diameter / Longest Path | trees,graphs 
2026-04-01 | algorithm | medium | phone-screen | Merge K Sorted Lists | linked-list,heap 
2026-04-01 | algorithm | hard | phone-screen | Trapping Rain Water | arrays,two-pointers,stack,dynamic-programming 
2026-03-30 | system-design | medium | phone-screen,onsite | Design Job Scheduler |  
2026-03-27 | system-design | hard | phone-screen | Design Self-Dealing Detection for Marketplaces |  
2026-03-27 | blog | None | phone-screen | Explain XGBoost's Overfitting Resistance |  
2026-03-20 | system-design | hard | onsite | Agent Tool-Use System Design (AML Volcano Engine) |  
2026-03-20 | algorithm | medium | onsite | Time Based Key-Value Store | hashing,binary-search 
2026-03-17 | algorithm | hard | oa | Aligned Memory Allocator and Related Tasks | strings,sliding-window,greedy 
2026-03-17 | algorithm | easy | oa | Drone Relay to Target | greedy,sorting 
2026-03-17 | algorithm | medium | oa | Two-Direction Justified Newspaper Layout | arrays,strings 
2026-03-17 | algorithm | medium | oa | Zigzag (Alternating-Parity) Subarrays | arrays 
2026-03-17 | algorithm | easy | onsite | In-Flight Movie Pair (Two Sum Variant) | arrays,hashing 
2026-03-14 | blog | None | phone-screen | Analyze Product Launch and Creator Engagement |  
2026-03-14 | sql | medium | phone-screen | Count Same-Day Registered Posters |  
2026-03-10 | algorithm | medium | onsite | Compute square root with precision | binary-search 
2026-03-10 | algorithm | medium | onsite | Reverse Words in a String (Preserve Spaces, In-Place) | two-pointers 
2026-03-09 | algorithm | easy | phone-screen | Best Time to Buy and Sell Stock II | arrays,greedy 
2026-03-06 | algorithm | easy | phone-screen | Longest Substring Without Repeating Characters II | strings,hashing,sliding-window 
2026-03-05 | algorithm | medium | phone-screen | Photo Groups via Transitive Similarity | graphs 
2026-03-05 | algorithm | easy | oa | Case-insensitive adjacent differences | strings 
2026-03-04 | algorithm | hard | phone-screen,onsite | Alien Dictionary | strings,graphs,topological-sort 
2026-03-01 | blog | None | phone-screen | Explain project choices, metrics, and AI usage |  
2026-02-28 | system-design | easy | phone-screen | Design a TinyURL-like short link service |  
2026-02-28 | blog | None | phone-screen | Explain a promotion and key project impact |  
2026-02-28 | system-design | hard | phone-screen | How do you assess database system stability? |  
2026-02-26 | algorithm | easy | phone-screen | Lowest Common Ancestor of a Binary Tree | trees,backtracking,graphs 
2026-02-26 | algorithm | medium | oa | Maximum Concurrent Processes / Meeting Rooms | intervals,sorting 
2026-02-25 | blog | None | phone-screen | Design a C++ Shared-Ownership Pointer Library |  
2026-02-21 | algorithm | medium | phone-screen,onsite | Find All Anagrams in a String | strings,hashing,sliding-window 
2026-02-19 | algorithm | hard | phone-screen | Word Search II | backtracking,graphs,tries 
2026-02-18 | algorithm | medium | phone-screen | Solve interval merging and histogram area | intervals,stack 
2026-02-17 | algorithm | medium | onsite | Minimum Coin Combination Counts | dynamic-programming 
2026-02-16 | algorithm | medium | phone-screen,onsite | N-Queens | arrays,backtracking 
2026-02-12 | blog | None | phone-screen | Answer common behavioral questions using STAR |  
2026-02-12 | system-design | hard | phone-screen | Design video captioning under compute limits |  
2026-02-12 | blog | None | phone-screen | Explain motivation for QA and career goals |  
2026-02-12 | blog | None | phone-screen | Explain overfitting, dropout, normalization, RL post-training |  
2026-02-12 | object-oriented-programming | medium | phone-screen | Implement stack variants and path-sum check |  
2026-02-11 | algorithm | medium | phone-screen | Delete nodes in linked list and binary tree | linked-list,trees 
2026-02-11 | algorithm | medium | oa | Solve string grouping and tree right-view problems | hashing,strings 
2026-02-11 | algorithm | medium | oa | Group words that are anagrams | hashing,strings 
2026-02-07 | algorithm | easy | phone-screen | Valid Parentheses | strings,stack 
2026-02-04 | algorithm | medium | phone-screen | Merge Intervals | arrays,intervals,sorting 
2026-02-04 | algorithm | medium | phone-screen | Serialize and Deserialize Binary Tree | trees,graphs 
2026-02-01 | algorithm | easy | phone-screen,onsite | Binary Tree Right Side View | trees,graphs 
2026-02-01 | blog | None | phone-screen | Describe Over-Engineering and UX Wins |  
2026-02-01 | object-oriented-programming | medium | phone-screen | Weighted LRU Cache |  
2026-01-31 | algorithm | medium | onsite | Gas Tank Grid Reachability | graphs,matrix 
2026-01-30 | algorithm | medium | phone-screen,onsite | Basic Calculator | strings,stack 
2026-01-30 | algorithm | hard | phone-screen,onsite | MinStack, MaxStack and Streaming Median | stack,heap 
2026-01-30 | algorithm | medium | phone-screen,onsite | Valid Parentheses with Wildcard '*' and DFS All Strings | strings,stack,backtracking,graphs,greedy 
2026-01-29 | algorithm | hard | phone-screen,onsite | Largest Rectangle in Histogram | arrays,stack 
2026-01-29 | algorithm | medium | phone-screen | Subarray Sum Equals K | arrays,hashing 
2026-01-28 | system-design | medium | onsite | Dynamic K in Retrieval Stage |  
2026-01-27 | blog | None | phone-screen | How to triage slow service alerts |  
2026-01-26 | algorithm | hard | phone-screen,onsite | Binary Tree Maximum Path Sum (with path reconstruction) | trees 
2026-01-26 | algorithm | medium | onsite | Find the Minimum Constant Processing Speed | binary-search 
2026-01-25 | algorithm | medium | phone-screen | Merge Overlapping Time Windows | intervals 
2026-01-23 | blog | None | phone-screen | Describe your most challenging project and leadership |  
2026-01-23 | algorithm | medium | phone-screen | Solve these string, subset, and date problems | math 
2026-01-22 | object-oriented-programming | medium | phone-screen,onsite | Design Circular Queue | arrays,stack 
2026-01-17 | blog | None | onsite | Explain deployment, retrieval, and regularization |  
2026-01-16 | object-oriented-programming | medium | phone-screen | Merge K Sorted Price Streams |  
2026-01-10 | blog | None | onsite | How to deploy and tune multimodal models? |  
2026-01-10 | algorithm | hard | onsite | Binary tree upward path sum | trees,hashing 
2026-01-10 | object-oriented-programming | medium | onsite | MaxStack |  
2026-01-10 | object-oriented-programming | medium | onsite | MinStack |  
2026-01-10 | algorithm | medium | phone-screen | Top K Frequent Elements | hashing,heap,sorting 
2026-01-04 | algorithm | hard | oa | ML Concepts and Coding Assessment | math 
2026-01-04 | algorithm | easy | oa | Bagging from scratch | math 
2026-01-04 | algorithm | medium | oa | k-Means from scratch |  
2026-01-04 | algorithm | medium | oa | Local maximum on a 1-D stream | arrays 
2026-01-04 | algorithm | hard | phone-screen,onsite | Find Median from Data Stream | heap 
2026-01-02 | blog | None | phone-screen | Describe a challenging project and your role |  
2026-01-01 | blog | None | phone-screen | Handle Communication Difficulty and Ambiguity on a Project |  
2025-12-16 | algorithm | medium | phone-screen,onsite | Wildcard / Regex String Matching (`*` operator) | dynamic-programming 
2025-12-15 | blog | None | phone-screen | Explain Transformer, GPT vs BERT, and PR metrics |  
2025-12-15 | blog | None | phone-screen | Explain your VLM project end-to-end |  
2025-12-11 | algorithm | medium | phone-screen | Reverse nodes in even-length linked-list groups | two-pointers 
2025-12-10 | system-design | hard | onsite | Design Payment System |  
2025-12-08 | blog | None | phone-screen | Describe career plan and teamwork approach |  
2025-12-08 | system-design | hard | phone-screen | Design system to detect privacy-leak records |  
2025-12-08 | blog | None | phone-screen | Explain DPO and construct its training data |  
2025-12-08 | algorithm | hard | phone-screen | Find kth smallest in sorted 2D matrix | binary-search,matrix 
2025-12-08 | algorithm | hard | phone-screen | Solve pair-counting and account-merging problems | binary-search,sorting 
2025-11-27 | system-design | medium | phone-screen | Plan DS approach for biker delivery project |  
2025-11-27 | sql | medium | phone-screen | Write monthly customer and sales SQL queries |  
2025-11-26 | algorithm | easy | phone-screen | Contiguous Subarray with Largest Min + Max | arrays,two-pointers 
2025-11-16 | blog | None | phone-screen | Explain Java ConcurrentHashMap and queues |  
2025-11-15 | blog | None | phone-screen | When prioritize precision vs recall |  
2025-11-12 | blog | None | phone-screen | Build and iteratively improve sentiment classifier |  
2025-11-12 | system-design | hard | phone-screen | Design low-latency large-scale hotel booking system |  
2025-11-12 | blog | None | phone-screen | Explain Type I/II errors vs precision/recall |  
2025-11-12 | sql | medium | phone-screen | Find top-paid employee per department |  
2025-11-12 | blog | None | phone-screen | How would you choose a classification threshold? |  
2025-11-12 | blog | None | phone-screen | Walk through a data pipeline project |  
2025-11-08 | blog | None | phone-screen | How do you choose a classification threshold? |  
2025-10-19 | algorithm | medium | phone-screen | Find first and last index of target | binary-search 
2025-10-09 | sql | medium | phone-screen | Write SQL for TikTok Live creator metrics |  
2025-10-09 | sql | medium | phone-screen | (Hard) |  
```
