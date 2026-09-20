# System design problem survey — Hello Interview & ByteByteGo

Covers: Hello Interview problem breakdowns, ByteByteGo book Vol 1, ByteByteGo book Vol 2,
ByteByteGo other-course design problems. See `SURVEY_AGENT.md` for method.

## Hello Interview

URL: https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview

Licence / access: Proprietary — no open licence. The index and some breakdowns are free to
read; most breakdowns require a paid "Hello Interview Premium" subscription (page shows a
"Purchase Premium to Keep Reading" wall and a lock icon on locked rows/sections).

Authority: Hello Interview is a system-design mock-interview and prep platform run by
ex-FAANG senior/staff engineers; its "System Design in a Hurry" problem breakdowns are
widely linked from system-design prep communities (Reddit r/ExperiencedDevs, Blind, prep
YouTube channels) as a go-to alongside Alex Xu's books.

Fetched: 2026-09-19, WebFetch of the overview index page (table rendered with title, slug,
access, difficulty for every row), cross-checked with a `site:hellointerview.com/learn/
system-design/problem-breakdowns` WebSearch (returned individual breakdown pages, confirming
the index and several slugs are real, live pages). Depth pattern spot-checked by fetching one
free page (`bitly`) and one premium page (`instagram`) directly: the free page showed full
sections (requirements, entities, API, high-level design, and three worked deep dives); the
premium page showed only section headers (requirements, entity/API headers, three deep-dive
titles) before the paywall message — so free rows are recorded as `deep` and premium rows as
`outline` (that is the depth actually visible without paying), not a claim about what premium
subscribers see.

The index groups problems by difficulty (Easy / Medium / Hard); that grouping is reproduced
below as three blocks in one table.

| Problem (site's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Bitly | URL shortener | https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly | free | deep |
| Dropbox | File sync (Dropbox/Drive) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox | free | deep |
| Yelp | Proximity / nearby search (Yelp) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp | paywalled | outline |
| Local Delivery Service (Gopuff) | Food delivery | https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff | free | deep |
| Ticketmaster | Ticket booking (Ticketmaster) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster | free | deep |
| Instagram | Instagram / photo sharing | https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram | paywalled | outline |
| FB News Feed | News feed / timeline | https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed | free | deep |
| Tinder | Tinder | https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder | free | deep |
| LeetCode | Online judge (LeetCode) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode | free | deep |
| WhatsApp | WhatsApp | https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp | free | deep |
| Strava | Fitness activity feed (Strava) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/strava | paywalled | outline |
| Distributed Cache | Distributed cache | https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-cache | paywalled | outline |
| Rate Limiter | Rate limiter | https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter | free | deep |
| Online Auction | Auction | https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction | paywalled | outline |
| YouTube | Video streaming (YouTube/Netflix) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube | free | deep |
| Job Scheduler | Distributed job scheduler | https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler | paywalled | outline |
| FB Live Comments | Live comments | https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments | free | deep |
| News Aggregator (Google News) | News aggregator | https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-news | paywalled | outline |
| Price Tracking Service (camelcamelcamel) | Price tracker | https://www.hellointerview.com/learn/system-design/problem-breakdowns/camelcamelcamel | paywalled | outline |
| Notification System | Notification system | https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system | paywalled | outline |
| YouTube Top K | Top-K / heavy hitters | https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k | free | deep |
| Uber | Ride hailing (Uber) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber | free | deep |
| Robinhood | Stock trading (Robinhood) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood | paywalled | outline |
| Google Docs | Google Docs / collaborative editing | https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs | paywalled | outline |
| Web Crawler | Web crawler | https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler | free | deep |
| Ad Click Aggregator | Ad click aggregation | https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator | free | deep |
| FB Post Search | Search engine (FB Post Search) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search | free | deep |
| Payment System | Payment system | https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system | paywalled | outline |
| Metrics Monitoring | Metrics / monitoring | https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring | paywalled | outline |
| Online Chess | Online multiplayer game (Chess) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-chess | paywalled | outline |
| ChatGPT | AI chat assistant (ChatGPT) | https://www.hellointerview.com/learn/system-design/problem-breakdowns/chatgpt | paywalled | outline |
| Flash Sale | Flash sale / high-contention inventory | https://www.hellointerview.com/learn/system-design/problem-breakdowns/flash-sale | paywalled | outline |

32 problems total on the index: 4 Easy, 16 Medium, 12 Hard. 15 free, 17 paywalled.

## System Design Interview – An Insider's Guide, Volume 1 (Alex Xu)

URL (TOC sources): https://bytebytego.com/courses/system-design-interview (ByteByteGo course
page mirrors the book, unlabelled by volume) and https://blog.bytebytego.com/p/system-design-interview-books-volume
(ByteByteGo's own blog post explicitly splitting Vol 1 vs Vol 2 chapter lists).

Licence / access: paid book (ISBN 9798664653403) / paid ByteByteGo course; no open licence.

Authority: Alex Xu, ex-Meta/Twitter/Google engineer; this is the best-known system design
interview book in the field — #1 in its Amazon category for years, the de facto baseline
every other source (including Hello Interview) is implicitly compared against.

Fetched: 2026-09-19, WebFetch of https://bytebytego.com/courses/system-design-interview
(returned a flat 1–31 chapter list covering both volumes) and WebFetch of
https://blog.bytebytego.com/p/system-design-interview-books-volume (returned the same
chapters explicitly split "Volume 1 (16 chapters)" / "Volume 2 (13 chapters)"), plus a
WebSearch confirming the Vol 1 chapter list against third-party listings (Medium chapter-1
recap, GitHub PDF mirror, bookseller pages). All three agree. Depth is recorded as the book's
known format (worked solution with requirements → API → high-level design → deep dives per
chapter, per every published description of the book) — not independently read chapter by
chapter here.

Non-design chapters skipped per instructions: "Scale From Zero To Millions Of Users",
"Back-of-the-envelope Estimation", "A Framework For System Design Interviews" (all concept
chapters, not *design X*), and "Design Consistent Hashing" (a concept/algorithm chapter,
same exclusion the instructions give for consistent hashing by name), and the closing
"The Learning Continues".

| Problem (book's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design A Rate Limiter | Rate limiter | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A Key-value Store | Key-value store | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A Unique Id Generator In Distributed Systems | Unique ID generator | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A Url Shortener | URL shortener | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A Web Crawler | Web crawler | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A Notification System | Notification system | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A News Feed System | News feed / timeline | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A Chat System | Chat / messaging | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design A Search Autocomplete System | Typeahead / autocomplete | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design Youtube | Video streaming (YouTube/Netflix) | https://bytebytego.com/courses/system-design-interview | book | deep |
| Design Google Drive | File sync (Dropbox/Drive) | https://bytebytego.com/courses/system-design-interview | book | deep |

11 design-problem chapters in Volume 1.

## System Design Interview – An Insider's Guide, Volume 2 (Alex Xu & Sahn Lam)

URL (TOC sources): same two as Volume 1 —
https://bytebytego.com/courses/system-design-interview and
https://blog.bytebytego.com/p/system-design-interview-books-volume.

Licence / access: paid book (ISBN 9781736049112); no open licence.

Authority: same author (Alex Xu) plus Sahn Lam (ex-Amazon); the standard sequel to Volume 1,
covering the harder/more specialized problems Volume 1 didn't reach (payments, messaging
infra, gaming, proximity).

Fetched: 2026-09-19, same two WebFetch calls as Volume 1 (both list Volume 2 as the same 13
chapters, in the same order), plus a WebSearch cross-check against Amazon/AbeBooks/Google
Books listings which confirm the title and author pair. All 13 chapters are *design X*
problems (no fundamentals/concept chapters in this volume, so none were skipped).

| Problem (book's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Proximity Service | Proximity / nearby search (Yelp) | https://bytebytego.com/courses/system-design-interview | book | deep |
| Nearby Friends | Proximity / nearby search (Yelp) | https://bytebytego.com/courses/system-design-interview | book | deep |
| Google Maps | Google Maps / mapping | https://bytebytego.com/courses/system-design-interview | book | deep |
| Distributed Message Queue | Distributed message queue | https://bytebytego.com/courses/system-design-interview | book | deep |
| Metrics Monitoring and Alerting System | Metrics / monitoring | https://bytebytego.com/courses/system-design-interview | book | deep |
| Ad Click Event Aggregation | Ad click aggregation | https://bytebytego.com/courses/system-design-interview | book | deep |
| Hotel Reservation System | Hotel reservation | https://bytebytego.com/courses/system-design-interview | book | deep |
| Distributed Email Service | Email service | https://bytebytego.com/courses/system-design-interview | book | deep |
| S3-like Object Storage | Object storage (S3) | https://bytebytego.com/courses/system-design-interview | book | deep |
| Real-time Gaming Leaderboard | Leaderboard | https://bytebytego.com/courses/system-design-interview | book | deep |
| Payment System | Payment system | https://bytebytego.com/courses/system-design-interview | book | deep |
| Digital Wallet | Digital wallet | https://bytebytego.com/courses/system-design-interview | book | deep |
| Stock Exchange | Stock exchange | https://bytebytego.com/courses/system-design-interview | book | deep |

13 design-problem chapters in Volume 2 — "Nearby Friends" is recorded under the same
canonical name as "Proximity Service" (Yelp-style geo search) since both are proximity-search
variants; kept as two rows because the book teaches them as two distinct chapters.

## ByteByteGo other courses — design-X problems only

Per instructions, these are ByteByteGo courses beyond the two Volume 1/2 books, filtered to
only the chapters that are *design a specific X* problems (frameworks/intro/reference-sheet
modules are skipped).

Licence / access for all three below: paid ByteByteGo course subscription; no open licence.
Depth: `outline` for every row — what was actually seen is the course's own chapter/module
list (and, for ML and GenAI, the one-line chapter blurb from the companion GitHub README),
not the full chapter content.

### Machine Learning System Design Interview course

URL: https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview

Authority: companion book "Machine Learning System Design Interview" by Alex Xu and Ali
Aminian; same ByteByteGo/Alex Xu brand as the two flagship volumes.

Fetched: 2026-09-19 — direct WebFetch of the course's `introduction-and-overview` page
returned only the header/nav (JS-rendered body), so the chapter list was taken instead from
WebFetch of the companion open GitHub repo https://github.com/ByteByteGoHq/ml-bytebytego
(reference-materials README lists the same chapter structure the course follows), found via
WebSearch. That repo path is the one that worked.

| Problem (course's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Visual Search System | Visual search (reverse image search) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| Google Street View Blurring System | Image blurring / PII redaction (Street View) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| YouTube Video Search | Search engine (video search) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| Harmful Content Detection | Content moderation / harmful-content detection | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| Video Recommendation System | Recommendation system (video) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| Event Recommendation System | Recommendation system (events) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| Ad Click Prediction on Social Platforms | Ad click prediction | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| Similar Listings on Vacation Rental Platforms | Recommendation system (similar listings) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| Personalized News Feed | News feed / timeline (ML ranking) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |
| People You May Know | Social graph recommendation (People You May Know) | https://bytebytego.com/courses/machine-learning-system-design-interview/introduction-and-overview | paywalled | outline |

10 design-problem chapters (11th chapter, "Introduction and Overview", is the framework and
was skipped).

### Generative AI System Design Interview course

URL: https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview

Authority: same ByteByteGo/Alex Xu brand; companion book "Generative AI System Design
Interview".

Fetched: 2026-09-19, direct WebFetch of the course page — unlike the ML course page, this one
returned the full 11-module table of contents with per-module descriptions (path worked on
first try, no fallback needed).

| Problem (course's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Gmail Smart Compose | Text autocomplete (Smart Compose) | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| Google Translate | Machine translation | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| ChatGPT: Personal Assistant Chatbot | AI chat assistant (ChatGPT) | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| Image Captioning | Image captioning | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| Retrieval-Augmented Generation | RAG (retrieval-augmented generation) | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| Realistic Face Generation | Generative image synthesis (face generation) | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| High-Resolution Image Synthesis | Generative image synthesis (high-res) | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| Text-to-Image Generation | Text-to-image generation | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| Personalized Headshot Generation | Generative image synthesis (personalized headshots) | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |
| Text-to-Video Generation | Text-to-video generation | https://bytebytego.com/courses/genai-system-design-interview/introduction-and-overview | paywalled | outline |

10 design-problem chapters (11th chapter, "Introduction and Overview", is the framework and
was skipped).

### Mobile System Design Interview course

URL: https://bytebytego.com/courses/mobile-system-design-interview/introduction

Authority: same ByteByteGo brand; course/book written by Manuel Vicente Vivo (mobile
engineering background), ByteByteGo's newest system-design book line as of 2025–2026,
explicitly aimed at mobile-app-specific system design.

Fetched: 2026-09-19, direct WebFetch of the course's `introduction` page returned the full
11-module sidebar table of contents on first try.

| Problem (course's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| News feed app | News feed / timeline (mobile client) | https://bytebytego.com/courses/mobile-system-design-interview/introduction | paywalled | outline |
| Chat app | Chat / messaging (mobile client) | https://bytebytego.com/courses/mobile-system-design-interview/introduction | paywalled | outline |
| Stock trading app | Stock exchange (mobile client) | https://bytebytego.com/courses/mobile-system-design-interview/introduction | paywalled | outline |
| Pagination library | Pagination library (mobile client) | https://bytebytego.com/courses/mobile-system-design-interview/introduction | paywalled | outline |
| Hotel reservation app | Hotel reservation (mobile client) | https://bytebytego.com/courses/mobile-system-design-interview/introduction | paywalled | outline |
| Google Drive app | File sync (Dropbox/Drive) (mobile client) | https://bytebytego.com/courses/mobile-system-design-interview/introduction | paywalled | outline |
| YouTube app | Video streaming (YouTube/Netflix) (mobile client) | https://bytebytego.com/courses/mobile-system-design-interview/introduction | paywalled | outline |

7 design-problem chapters (the other 4 modules — "Introduction", "A framework for Mobile SD
interviews", "Mobile System Design Building Blocks", "Quick Reference Cheat Sheet" — are
framework/reference, not *design X*, and were skipped).

## Notes

- Hello Interview's own on-page link text for the "News Aggregator" problem uses the slug
  `google-news`, not `news-aggregator` as guessed in the task brief; `.../news-aggregator`
  404s. Recorded the real slug.
- Hello Interview has four problems no ByteByteGo source covers at all: **Online Chess**,
  **ChatGPT** (as a general-purpose chat product, distinct from ByteByteGo's GenAI-course
  ChatGPT chapter which is scoped to the model-serving/RAG side), **Flash Sale**, and
  **FB Post Search** — all Hard-difficulty and, except FB Post Search, paywalled. These read
  as the newest additions to the Hello Interview catalogue (chess and flash-sale in
  particular are not classic FAANG-blog problems).
  Only Hello Interview teaches **Strava**, **Price Tracker (camelcamelcamel)**, and
  **Online Auction** — none of these three appear in either ByteByteGo book or the three
  other ByteByteGo courses checked.
- Conversely, ByteByteGo Volume 1's **Consistent Hashing** chapter is a building block /
  concept chapter (an algorithm, not a full system), so per SURVEY_AGENT.md's own example it
  was excluded from the table — flagging this explicitly since the chapter title literally
  starts with "Design", which could look like a miss otherwise.
  **Key-Value Store**, **Search Autocomplete (Typeahead)**, and **Unique ID Generator** are
  Volume-1-only: Hello Interview's public index has no equivalent breakdown for any of them.
- Volume 2's **Proximity Service** / **Nearby Friends** pair and Hello Interview's **Yelp**
  breakdown are the same canonical problem (geo-proximity search) approached from slightly
  different angles (business search vs. friend search) — worth merging into one skeleton leaf
  with two worked variants rather than two leaves.
- ByteByteGo's Machine Learning and Generative AI courses are a different genre from the rest
  of this survey — every problem is an ML/AI *feature* (recommendation, ranking, generation,
  RAG) rather than a classic backend system, so most rows needed new canonical names not in
  SURVEY_AGENT.md's seed list. Flagging in case the domain skeleton wants these split into a
  separate "ML system design" branch rather than merged into the general system-design one.
  Mobile System Design's 7 problems are themselves client-side retellings of problems already
  in the book/Hello Interview list (news feed, chat, stock trading, hotel reservation, Drive,
  YouTube) plus one new one (pagination library) — kept as separate rows with an explicit
  "(mobile client)" qualifier on the canonical name since the actual design content (offline
  sync, optimistic writes, battery) differs from the backend-only chapters even though the
  product is the same.
- The ByteByteGo course page https://bytebytego.com/courses/system-design-interview renders
  Volume 1 and Volume 2 chapters as one continuous, unlabelled 1–31 list (no "Volume 1" /
  "Volume 2" heading in the fetched text); the volume split used in this file's two sections
  comes from https://blog.bytebytego.com/p/system-design-interview-books-volume, which states
  the split explicitly ("Volume 1 (16 chapters, 320 pages)" / "Volume 2 (13 chapters, 434
  pages)") and matches chapter-for-chapter.
- Not reached: could not load the general https://bytebytego.com/courses catalogue page
  (returned HTTP 404 for that exact path) to get an authoritative full list of *all*
  ByteByteGo courses; the three "other courses" covered here (ML, GenAI, Mobile) were found
  via WebSearch instead, each individually confirmed to exist by fetching its own course URL.
  There may be additional ByteByteGo courses (e.g. coding patterns, OOD) not checked because
  they were not named in the task and, per a quick WebSearch skim, don't appear to contain
  *design X* system chapters.
