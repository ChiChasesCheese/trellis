# Sources — TikTok / ByteDance senior backend research (English half)

Fetched 2026-10-24 (Sat; collection ran 2026-10-23 to 2026-10-24). Ids are used as `[id]` in `loop.md`, `coding.md`, `system_design.md`, `behavioral.md`, `company.md`. Raw notes: `raw/github_repos.md`, `raw/forums_en.md`, `raw/official.md`.
Types: official / paper / candidate report / aggregator / blog (SEO) / forum.  Never cited: lodely.com, vervecopilot.com.

## Official and peer-reviewed

| id | URL | date | type | what it gave |
|---|---|---|---|---|
| O1 | https://lifeattiktok.com/search/7629632161631308037 (and /7660767102572398901, /7689368204483758341, /teams/technology, /teams/usds-jv) | live 2026-10-24 | official | the target posting "Senior Backend Software Engineer - Innovative Growth" (San Jose, base $218,400-$387,600, 3+ yrs, Go/Python/Java/C++, AIGC/search/growth), sibling senior postings (7+ yrs; 5+ yrs with AI-assisted dev), TikTok tech-team descriptions ("over a billion people") |
| O2 | https://lifeattiktok.com/apply , /interview , /faq | live 2026-10-24 | official | process wording: several interviews, assessment by role/region, "usually one month", 3-5 office days, visa sponsorship, English CV |
| O3 | https://joinbytedance.com/culture , https://joinbytedance.com/philosophy | page footer 2012-2025, undated | official | the six ByteStyle values (exact text), mission |
| O4 | https://www.bytedance.com/en/ | live 2026-10-24 | official | values summary, products, 150,000+ employees in ~120 cities |
| O5 | https://www.theregister.com/2026/01/23/jv_announces_tiktok_us_acquisition/ ; https://en.wikipedia.org/wiki/TikTok_USDS ; https://usdsjv.tiktok.com/ ; announcement PDF copy https://static.poder360.com.br/2026/01/anuncio-oficial-tik-tok-jointventure-eua-23jan2026.pdf (undecodable) ; search summaries of the TikTok newsroom text | 2026-01-23 | news/secondary + official site shell | USDS JV: formation 2026-01-22, Oracle/Silver Lake/MGX 15% each, ByteDance 19.9%, board, CEO, Oracle role, algorithm retraining, commercial activities left to TikTok global US entities, "200 million Americans / 7.5 million businesses" |
| O6 | https://www.cloudwego.io/blog/2022/06/21/hertz-an-ultra-large-scale-enterprise-level-microservice-http-framework-is-now-officially-open-source ; https://www.cloudwego.io/blog/2022/09/30/kitex-unifying-open-source-practice-for-a-high-performance-rpc-framework/ ; https://www.cloudwego.io/blog/2023/06/15/cloudwego-a-leading-practice-for-building-enterprise-cloud-native-middleware/ | 2022-2023 | official blog (seen via search snippets) | Hertz >10,000 services / >40M QPS; Kitex >60,000 services; Go as main language |
| O7 | ByteGraph https://vldb.org/pvldb/vol15/p3306-li.pdf ; ByteHTAP https://www.vldb.org/pvldb/vol15/p3411-chen.pdf ; ByteHouse https://arxiv.org/abs/2602.08226 ; ByteMQ SoCC 2024 DOI 10.1145/3698038.3698536 ; StreamShield arXiv 2602.03189 ; Monolith arXiv 2209.07663 ; plus secondary https://factorhouse.io/articles/bytedance-kafka-architecture/ | 2022-2026 | papers (ByteGraph/ByteHTAP fetched; others via secondary summaries) | storage/streaming/recommendation stack and scale numbers; no confirmation of TiDB at ByteDance |
| O-jobs | https://www.themuse.com/jobs/tiktok/backend-software-engineer-tiktok-live-revenue-f242b2 ; https://nodeflair.com/jobs/tiktok-backend-software-engineer-tiktok-shop-trading-515412 ; https://lifeattiktok.com/search/7394711631551465738 | 2024-2026 | job posts via search snippets | LIVE revenue / Global LIVE Wallet / Shop transaction teams, Redis/MySQL/Java/Go hints (low) |

## GitHub (details in `raw/github_repos.md`)

| id | URL | date | type | what it gave |
|---|---|---|---|---|
| G1 | https://github.com/kevin-2023-code/Tech-Interview-Questions (companies/bytedance*.md, data/questions.jsonl, questions/system-design/job-scheduler-design) | commit 2026-10-24 | aggregator mirror (TrueInterview, CC BY 4.0) | 345 questions, 200 dated sightings since 2025-10, process guides (SWE/infra/overview, 92-111 reports), job-scheduler design text with follow-ups, level ladder |
| G2 | https://github.com/kevin-2023-code/Tech-OA-Questions (companies/bytedance.md) | 2026-10-24 | aggregator | per-question level tags and rounds |
| G3 | https://github.com/ombharatiya/FAANG-Coding-Interview-Questions (README, FAANG-Recent-Questions.md) | 2026-10-09 | derived list | LC list, custom problems, SD list, claims on OA (CodeSignal, 4 problems, 70-90 min), AI ban |
| G4 | https://github.com/liquidslr/leetcode-company-wise-problems (TikTok/, ByteDance/) | 2026-10-20 | crowd tags | frequency scores by window |
| G5 | https://github.com/atomeocean/job-compass (docs/assets/json/interview-experience) | 2026-10 | metadata mirror of 1point3acres | one 2026-05 senior SRE row; others new grad |
| G6 | lmiztbrv/tiktok-interview-patterns ; AlexiosNine/tiktok-algorithm-prep | 2026-10 | SEO / derivative | corroboration only (low) |

## LeetCode Discuss

| id | URL | date | type | what it gave |
|---|---|---|---|---|
| L1 | https://leetcode.com/discuss/post/7150750/tiktokbytedance-interview-experience-by-8vcmw/ (topicId 7150750) | 2025-09-03 | candidate report | Mid (2-1) loop: 2 LC (1293; bipartite BFS) + 1 SD (alert/monitoring system) + 1 BQ; $300k TC |
| L2 | topicId 7423011 | 2025-12-19 | candidate report | OA format: CodeSignal, 4 problems / 70 min (research intern) |
| L3 | topicId 7875289 , 7875303 | 2026-04-11 | prep-service posts | in-memory file system, subtree sum (new grad) |

## Reddit  (https://reddit.com/r/leetcode/comments/<id>/ unless noted)

| id | thread | date | type | what it gave |
|---|---|---|---|---|
| R1 | 1sjfel3 | 2026-04-12 | candidate report + comments | SG, downlevel worry; 3 manager interviews; "2-1 loop"; 3-1 offer claim; negotiation advice |
| R2 | 1sgn71t | 2026-04-09 | candidate report | SG, 3 interviews w/ managers; 3-hour system design |
| R3 | 1qqb5n6 | 2026-01-29 | candidate report | SG backend loop in detail; HM round design drill |
| R3b | 1qqb5n6 comment | 2026-01-29 | candidate report | 2-1 HM round: LC then payment system HLD |
| R3c | 1qqb5n6 comment | 2026-01-30 | candidate comment | final round cancelled the day before after 3-4 rounds |
| R4 | 1w6uktk (+comments) | 2026-09-03/04 | forum | SG: 30-min resume dig, curt interviewers, Mandarin dispute |
| R5 | 1ss8ba6 (+comments) | 2026-04-21 | candidate + comments | San Jose mid SDE: LC, SD; HM decides; paused since Nov 2025 |
| R6 | 1t5pu24 , 1taje6a , 1tbi9rq | 2026-05 | candidate posts | San Jose 3rd round, "Chinese?" question, department manager round, slow HR |
| R7 | 1ql95y7 (+comments) | 2026-01-23 | forum | hiring pause; offer withdrawn Dec 2025; reorg comment |
| R-1omb | https://reddit.com/r/cscareerquestions/comments/1omb5ze/ | 2025-11-02 | forum | req closed mid-loop; SDE→SRE rematch |
| R-offer | 1u4zr8g | 2026-06-13 | candidate | 2-1 SRE Seattle offer numbers |
| R-offer2 | 1p74jfg | 2025-11-26 | candidate | 2-1 SRE offer numbers |
| R-oa | 1o7mxj9 | 2025-10-15 | candidate | 600/600 OA rejected |
| (index) | Arctic Shift post search over 8 subreddits; 96 posts listed in scratch | 2026-10-24 | — | discovery |

## Blind  (https://www.teamblind.com/post/<slug>; browser User-Agent works; comments mostly collapsed)

| id | slug | date | what it gave |
|---|---|---|---|
| B1 | tiktok-usds-jv-senior-software-interview-process-pws7m0wc | 2026-10-13 | USDS JV senior; pass/fail rounds; consistency SD in round 3 |
| B2 | interview-journey-meta-airbnb-tiktok-snap-bj01gcot | 2025-05-30 | L6 → TikTok 2-2 downlevel; 4 pass/fail rounds |
| B3 | is-it-true-that-in-bytedance-they-switched-their-levels-…-to8hs3d8 | 2026-09-24 | L1/L2/L3 relabel claim |
| B4 | snap-l5-vs-tiktok-2-2-senior-h0kmt2vh | 2026-10-22 | 2-2 senior infra offer $470k CA; night meetings |
| B5 | tiktok-ai-assisted-coding-interview-mrho747e | 2026-07-08 | own AI IDE in tech screen |
| B6 | tiktok-interviewer-spoke-mandarin-for-5-minutes-…-nxyk54kz | 2026-06-24 | SD asked on a code-only platform |
| B7 | tiktok-level-2-2-lowball-offer-bp1xzovd | 2025-03-30 | MLE 2-2 offer numbers |
| B8 | tiktok-interview-process-for-senior-swe-01772lfc | 2025-09-02 | senior SWE screen: HackerRank/Zoom + Lark |
| B9 | tiktok-bytedance-huge-compensation-update-bmduw72l | 2024-01-22 | RSU schedule 20/25/25/30 |
| B-tl | bytedance-interview-timeline-ptpnexbp | 2026-08-18 | back-to-back scheduling, Asia recruiter |
| B-comp | tiktok-bytedance-employees-compensation-leveling-guidance-needed-urgent-rwuks4o3 | 2026-10-21 | opinions on Mandarin and stock |
| B-hm | tiktok-hiring-manager-round-ohywmwrg | 2025-04-05 | 2-1 SDE HM round question; opinions |
| B-hm1 | tiktok-hiring-manager-insight-1pdpseue | 2025-04-21 | resume review / recruiter order |
| B-hm2 | tiktok-interviewer-asked-inappropriate-questions-1unjb725 | 2025-09-17 | HM conduct |
| B-reject | tiktok-rejected-after-passing-interviews-s7wdgi3w | 2025-02-05 | passed rounds, priorities changed |
| B-old | tiktok-2-12-no-system-design-interview-dv0i0tj5 ; tiktok-system-design-interview-zdxwrk5j ; tiktok-system-design-interview-6laxh7na | 2024-06/10 | loop shapes (background) |
| B-old2 | will-i-pass-tiktok-coding-round-cwshnxpu | 2024-07-17 | 3 LC mediums in a round (background) |
| B-old3 | got-destroyed-in-a-tiktok-interview-o6xqpdvk | 2020-07-29 | fundamentals questions (background) |
| B-2023 | tiktok-interviewer-asking-for-mandarin-bumfs8px | 2023-04-18 | Mandarin question in HM (London PM) |
| B-sd2 | bytedance-tiktok-system-design-interview-d8teeq8a | 2024-07-15 | whiteboard = HackerRank link |
| (index) | search pages `teamblind.com/search/<q>` (12 queries, 152 posts, 140 fetched) | 2026-10-24 | discovery |

## Aggregators and guides

| id | URL | date | type | what it gave |
|---|---|---|---|---|
| P1 | https://prachub.com/interview-guide/bytedance-software-engineer-interview-questions-guide-2026 | 2026-09-24 | aggregator guide | loop, TT USDS rounds, SD prompts, fundamentals, HM question list |
| P2 | https://prachub.com/interview-questions/design-a-payment-system-time-boxed-high-level-design | 2026-09-10 | aggregator | payment system HLD with follow-ups |
| P3 | https://prachub.com/companies/bytedance (pages 1-2) | 2026-10-24 | aggregator | 214-question bank, newest titles |
| H1 | https://www.hellointerview.com/community/questions?company=TikTok (+ detail pages) | 2026-10-24 | community (Playwright) | live coin tracking, video moderation, metrics aggregator, Accounts Merge, Symmetric Tree |
| A1 | https://www.1point3acres.com/interview/guides/tiktok-interview-trend-2026q2 | 2026-05-08 | aggregator guide (partly gated) | one-round-per-week cadence, rematch norm, distribution, hot topics |
| A2 | https://www.1point3acres.com/interview/problems/company/bytedance ; /interview/company/tiktok ; /interview/thread/1040939 | 2026-10-24 | aggregator (gated) | 79-question bank stats; video view history SD title |
| LV | https://www.levels.fyi/company/ByteDance/salaries/Software-Engineer | 2026-10-23 | aggregator | level ladder with US TC and vesting |
| CM | https://codemia.io/guides/tiktok-software-engineer | 2026-02 | SEO guide | generic loop, 3 SD prompts (low) |
| SU | https://engineeringenablement.substack.com/p/tiktok-software-engineering-interview | 2026-09-29 | blog | "no universal loop", prep framing |
| GD | Glassdoor search snippets (TikTok Senior SWE, San Jose pages; direct fetch 403) | 2025-2026 | candidate reports (snippets) | LC445 San Jose, SG idempotency/reconciliation, ingest-and-flag-rules SD |

## Failed or empty paths (so nobody retries blindly)

- reddit.com HTML/.json blocked; `.rss` works but throttles after ~5 fetches (retry 30 s apart); Arctic Shift post search OK, comment search rate-limited ("Too many requests").
- Hacker News Algolia: nothing relevant in the window.
- Glassdoor direct: 403. Interview Query, Dataford: 429. Medium-type sites not attempted.
- trueinterview.io question pages: Insider-gated after ~100 words (browser shows the same); the GitHub mirror has only the free ones (job scheduler, LRU, memory allocator, islands, Parallel Courses III, Time Based KV).
- 1point3acres: interview-bank pages render in Playwright, bodies behind login ("[hidden]"); tRPC list not needed.
- Hello Interview: only 5 of 13 TikTok questions visible without Premium; ByteDance filter empty.
- lifeattiktok.com/how-we-hire does not exist (the page is /apply).
