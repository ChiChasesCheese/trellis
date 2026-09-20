# System design interview problems — GitHub repository survey

Scope: curated GitHub repositories that teach system design interview problems. Companion
to the web/book survey; this file only covers what is visible in the repository itself
(README + linked in-repo folders). Concept-only pages (CAP theorem, consistent hashing as
a topic, OOD toy classes like parking lot/vending machine/deck of cards) are excluded per
`SURVEY_AGENT.md`; building-block "design X" problems (rate limiter, distributed cache,
consistent hashing *service*) are kept.

## donnemartin/system-design-primer

URL: https://github.com/donnemartin/system-design-primer#system-design-topics-table-of-contents (problem tables); solutions under `solutions/system_design/`
Licence / access: **CC BY 4.0** (`LICENSE.txt`: "Creative Commons Attribution 4.0 International License", Copyright 2017 Donne Martin)
Authority: the best-known system-design-interview repo on GitHub (370,793 stars as of 2026-09-19); written/maintained by Donne Martin (ex-Amazon, ex-Capital One), cited constantly across the rest of this survey's sources and in nearly every other list of "how to prep for system design interviews."
Fetched: 2026-09-19 via `gh api repos/donnemartin/system-design-primer/readme` and `gh api repos/donnemartin/system-design-primer/contents/solutions/system_design`.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design Pastebin.com (or Bit.ly) | Pastebin | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md | free | deep |
| Design the Twitter timeline and search (or Facebook feed and search) | News feed / timeline | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md | free | deep |
| Design a web crawler | Web crawler | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md | free | deep |
| Design Mint.com | Personal finance aggregator (Mint) | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/mint/README.md | free | deep |
| Design the data structures for a social network | Social graph (data structures) | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md | free | deep |
| Design a key-value store for a search engine | Key-value store | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md | free | deep |
| Design Amazon's sales ranking by category feature | Product sales ranking (Amazon) | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md | free | deep |
| Design a system that scales to millions of users on AWS | Cloud scaling case study (AWS) | https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md | free | deep |
| Design a file sync service like Dropbox | File sync (Dropbox/Drive) | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a search engine like Google | Search engine | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a scalable web crawler like Google | Web crawler | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design Google docs | Google Docs / collaborative editing | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a key-value store like Redis | Key-value store | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a cache system like Memcached | Distributed cache | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a recommendation system like Amazon's | Recommendation system | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a tinyurl system like Bitly | URL shortener | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a chat app like WhatsApp | WhatsApp | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a picture sharing system like Instagram | Instagram / photo sharing | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design the Facebook news feed function | News feed / timeline | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design the Facebook timeline function | News feed / timeline | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design the Facebook chat function | Chat / messaging | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a graph search function like Facebook's | Social graph search | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a content delivery network like CloudFlare | CDN | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a trending topic system like Twitter's | Trending topics | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a random ID generation system | Unique ID generator | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Return the top k requests during a time interval | Top-K / heavy hitters | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a system that serves data from multiple data centers | Multi-datacenter serving | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design an online multiplayer card game | Online multiplayer game | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a garbage collection system | Garbage collector | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design an API rate limiter | Rate limiter | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |
| Design a Stock Exchange (like NASDAQ or Binance) | Stock exchange | https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions | free | outline |

Note: the primer's `solutions/object_oriented_design/` table (hash map, LRU cache, call
center, deck of cards, parking lot, chat server) was read but excluded — those are
low-level/OOD class-design problems, not system-scale "design X" problems, and belong to
the vault's `low-level-design` domain instead.

## karanpratapsingh/system-design

URL: https://github.com/karanpratapsingh/system-design#table-of-contents (Chapter V, "System Design Interviews")
Licence / access: **CC BY-NC-ND 4.0** (Attribution-NonCommercial-NoDerivatives 4.0 International, per repo `LICENSE`)
Authority: 46,156 stars; a full self-published system-design course (also sold as a Leanpub ebook and hosted on the author's site karanpratapsingh.com/courses/system-design) — one of the most-forked "learn system design" repos after the primer.
Fetched: 2026-09-19 via `gh api repos/karanpratapsingh/system-design/readme`.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| URL Shortener | URL shortener | https://github.com/karanpratapsingh/system-design#url-shortener | free | deep |
| WhatsApp | WhatsApp | https://github.com/karanpratapsingh/system-design#whatsapp | free | deep |
| Twitter | News feed / timeline | https://github.com/karanpratapsingh/system-design#twitter | free | deep |
| Netflix | Video streaming (YouTube/Netflix) | https://github.com/karanpratapsingh/system-design#netflix | free | deep |
| Uber | Ride hailing (Uber) | https://github.com/karanpratapsingh/system-design#uber | free | deep |

Each chapter runs ~400-430 lines: requirements, capacity estimation, API design, data
model, high-level design, and a deep-dive/bottleneck section with diagrams — full book
chapters, not outlines. Access is free on GitHub even though the same content is also sold
as a Leanpub ebook.

## ashishps1/awesome-system-design-resources

URL: https://github.com/ashishps1/awesome-system-design-resources#-system-design-interview-problems
Licence / access: **GPL-3.0** (per repo metadata)
Authority: 41,529 stars; maintained by Ashish Pratap Singh (AlgoMaster newsletter/blog author); the list functions as a curated index pointing to the author's own algomaster.io articles (written walkthroughs) and to external YouTube system-design channels for problems without an article yet.
Fetched: 2026-09-19 via `gh api repos/ashishps1/awesome-system-design-resources/readme`.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design URL Shortener like TinyURL | URL shortener | https://algomaster.io/learn/system-design-interviews/design-url-shortener | free | walkthrough |
| Design Autocomplete for Search Engines | Typeahead / autocomplete | https://algomaster.io/learn/system-design-interviews/design-instagram | free | walkthrough |
| Design Load Balancer | Load balancer | https://www.youtube.com/watch?v=8zX0rue2Hic | free | outline |
| Design Content Delivery Network (CDN) | CDN | https://www.youtube.com/watch?v=8zX0rue2Hic | free | outline |
| Design Distributed Key-Value Store | Key-value store | https://www.youtube.com/watch?v=rnZmdmlR-2M | free | outline |
| Design Distributed Cache | Distributed cache | https://www.youtube.com/watch?v=iuqZvajTOyA | free | outline |
| Design Authentication System | Authentication system | https://www.youtube.com/watch?v=uj_4vxm9u90 | free | outline |
| Design Unified Payments Interface (UPI) | Payment system | https://www.youtube.com/watch?v=QpLy0_c_RXk | free | outline |
| Design WhatsApp | WhatsApp | https://algomaster.io/learn/system-design-interviews/design-whatsapp | free | walkthrough |
| Design Spotify | Music streaming (Spotify) | https://algomaster.io/learn/system-design-interviews/design-spotify | free | walkthrough |
| Design Instagram | Instagram / photo sharing | https://algomaster.io/learn/system-design-interviews/design-instagram | free | walkthrough |
| Design Notification Service | Notification system | https://algomaster.io/learn/system-design-interviews/design-notification-service | free | walkthrough |
| Design Distributed Job Scheduler | Distributed job scheduler | https://blog.algomaster.io/p/design-a-distributed-job-scheduler | free | walkthrough |
| Design Tinder | Tinder | https://www.youtube.com/watch?v=tndzLznxq40 | free | outline |
| Design Facebook | Social network (Facebook) | https://www.youtube.com/watch?v=9-hjBGxuiEs | free | outline |
| Design Twitter | News feed / timeline | https://www.youtube.com/watch?v=wYk0xPP_P_8 | free | outline |
| Design Reddit | Content aggregator (Reddit) | https://www.youtube.com/watch?v=KYExYE_9nIY | free | outline |
| Design Netflix | Video streaming (YouTube/Netflix) | https://www.youtube.com/watch?v=psQzyFfsUGU | free | outline |
| Design Youtube | Video streaming (YouTube/Netflix) | https://www.youtube.com/watch?v=jPKTo1iGQiE | free | outline |
| Design Google Search | Search engine | https://www.youtube.com/watch?v=CeGtqouT8eA | free | outline |
| Design E-commerce Store like Amazon | E-commerce platform (Amazon/Shopify) | https://www.youtube.com/watch?v=EpASu_1dUdE | free | outline |
| Design TikTok | Short-form video (TikTok) | https://www.youtube.com/watch?v=Z-0g_aJL5Fw | free | outline |
| Design Shopify | E-commerce platform (Amazon/Shopify) | https://www.youtube.com/watch?v=lEL4F_0J3l8 | free | outline |
| Design Airbnb | Booking marketplace (Airbnb) | https://www.youtube.com/watch?v=YyOXt2MEkv4 | free | outline |
| Design Rate Limiter | Rate limiter | https://www.youtube.com/watch?v=mhUQe4BKZXs | free | outline |
| Design Distributed Message Queue like Kafka | Distributed message queue | https://www.youtube.com/watch?v=iJLL-KPqBpM | free | outline |
| Design Flight Booking System | Flight booking system | https://www.youtube.com/watch?v=qsGcfVGvFSs | free | outline |
| Design Online Code Editor | Online code editor / collaborative IDE | https://www.youtube.com/watch?v=07jkn4jUtso | free | outline |
| Design an Analytics Platform (Metrics & Logging) | Metrics / monitoring | https://www.youtube.com/watch?v=kIcq1_pBQSY | free | outline |
| Design Payment System | Payment system | https://www.youtube.com/watch?v=olfaBgJrUBI | free | outline |
| Design a Digital Wallet | Digital wallet | https://www.youtube.com/watch?v=4ijjIUeq6hE | free | outline |
| Design Location Based Service like Yelp | Proximity / nearby search (Yelp) | https://www.youtube.com/watch?v=M4lR_Va97cQ | free | outline |
| Design Uber | Ride hailing (Uber) | https://www.youtube.com/watch?v=umWABit-wbk | free | outline |
| Design Food Delivery App like Doordash | Food delivery | https://www.youtube.com/watch?v=iRhSAR3ldTw | free | outline |
| Design Google Docs | Google Docs / collaborative editing | https://www.youtube.com/watch?v=2auwirNBvGg | free | outline |
| Design Google Maps | Maps / navigation (Google Maps) | https://www.youtube.com/watch?v=jk3yvVfNvds | free | outline |
| Design Zoom | Video conferencing (Zoom) | https://www.youtube.com/watch?v=G32ThJakeHk | free | outline |
| Design File Sharing System like Dropbox | File sync (Dropbox/Drive) | https://www.youtube.com/watch?v=U0xTu6E2CT8 | free | outline |
| Design Ticket Booking System like BookMyShow | Ticket booking (Ticketmaster) | https://www.youtube.com/watch?v=lBAwJgoO3Ek | free | outline |
| Design Distributed Web Crawler | Web crawler | https://www.youtube.com/watch?v=BKZxZwUgL3Y | free | outline |
| Design Code Deployment System | CI/CD deployment system | https://www.youtube.com/watch?v=q0KGYwNbf-0 | free | outline |
| Design Distributed Cloud Storage like S3 | Object storage (S3) | https://www.youtube.com/watch?v=UmWtcgC96X8 | free | outline |
| Design Distributed Locking Service | Distributed lock service | https://www.youtube.com/watch?v=v7x75aN9liM | free | outline |

Note: "Design Autocomplete for Search Engines" links to the author's Instagram article
(likely a stale link in the source repo) — recorded as seen; depth kept as "walkthrough"
on the assumption the algomaster.io article format matches its siblings.

## checkcheckzz/system-design-interview

URL: https://github.com/checkcheckzz/system-design-interview#qs
Licence / access: no LICENSE file in the repo (free to read on GitHub; no explicit reuse licence granted)
Authority: 23,707 stars; one of the earliest (pre-2016) "how to prep for system design interviews" GitHub lists, widely cited/forked in other awesome-lists; content is a curated bibliography rather than original worked solutions.
Fetched: 2026-09-19 via `gh api repos/checkcheckzz/system-design-interview/readme`.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design a CDN network | CDN | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a Google document system | Google Docs / collaborative editing | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a random ID generation system | Unique ID generator | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a key-value database | Key-value store | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design the Facebook news feed function | News feed / timeline | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design the Facebook timeline function | News feed / timeline | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a function to return the top k requests during past time interval | Top-K / heavy hitters | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design an online multiplayer card game | Online multiplayer game | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a graph search function | Social graph search | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a picture sharing system | Instagram / photo sharing | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a search engine | Search engine | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a recommendation system | Recommendation system | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a tinyurl system | URL shortener | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a garbage collection system | Garbage collector | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a scalable web crawling system | Web crawler | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design the Facebook chat function | Chat / messaging | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a trending topic system | Trending topics | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |
| Design a cache system | Distributed cache | https://github.com/checkcheckzz/system-design-interview#qs | free | outline |

## ByteByteGoHq/system-design-101

URL: https://github.com/ByteByteGoHq/system-design-101#readme
Licence / access: **CC BY-NC-ND 4.0** (per `LICENSE.md`: non-commercial, no-derivatives)
Authority: 89,437 stars; official repo of the ByteByteGo newsletter/YouTube channel (Alex Xu, author of the "System Design Interview" book series); content lives as visual one-pagers on bytebytego.com, this repo is the index + diagram assets.
Fetched: 2026-09-19 via `gh api repos/ByteByteGoHq/system-design-101/readme`.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design Gmail | Email service | https://bytebytego.com/guides/design-gmail | free | outline |
| How to Design Google Docs | Google Docs / collaborative editing | https://bytebytego.com/guides/how-to-design-google-docs | free | outline |
| Payment System | Payment system | https://bytebytego.com/guides/payment-system | free | outline |
| Design Google Maps | Maps / navigation (Google Maps) | https://bytebytego.com/guides/design-google-maps | free | outline |
| Designing a Chat Application (like WhatsApp/Messenger/Discord) | Chat / messaging | https://bytebytego.com/guides/how-do-we-design-a-chat-application-like-whatsapp-facebook-messenger-or-discord | free | outline |
| Design Stock Exchange | Stock exchange | https://bytebytego.com/guides/design-stock-exchange | free | outline |
| Proximity Service | Proximity / nearby search (Yelp) | https://bytebytego.com/guides/proximity-service | free | outline |
| Designing a Permission System | Authentication system | https://bytebytego.com/guides/how-do-we-design-a-permission-system | free | outline |

Most of this repo's 400+ linked items (API/networking guides, "how does X work" explainers,
company case studies like "Twitter Architecture 2022 vs. 2012") are concept or
architecture-teardown pages, not "design X" prompts, and were excluded per the skip rule —
only the "How it Works?" section's design-prompt items are listed above. Each linked item
is a single hosted page on bytebytego.com (not rendered in the repo itself), so depth is
recorded as "outline" based on what the repo's own README shows (a title + link only).

## binhnguyennus/awesome-scalability

URL: https://github.com/binhnguyennus/awesome-scalability#interview
Licence / access: **MIT**
Authority: 74,055 stars; a widely-cited curated bibliography of engineering-blog posts on scalability/availability/stability, organized as a "big archive" rather than an interview-prep course.
Fetched: 2026-09-19 via `gh api repos/binhnguyennus/awesome-scalability/readme`.

No rows. Read the full README (976 lines, sections Principle/Scalability/Availability/
Stability/Performance/Intelligence/Architecture/Interview/Organization/Talk). Its
`## Interview` section links only to generic interview-prep advice ("Anatomy of a System
Design Interview," "Top 10 System Design Interview Questions," "How NOT to design Netflix
in your 45-minute interview") and to "what happens when..." mechanism explainers — no
"design X" prompts naming a specific system to design. Everything else in the repo is
real-world architecture case studies (e.g. "Scaling Twitter," "Netflix: What Happens When
You Press Play?"), which `SURVEY_AGENT.md` scopes out as concept/case-study pages, not
design problems. Per the task instructions this repo is covered but contributes zero rows.

## Jeevan-kumar-Raj/Grokking-System-Design

URL: https://github.com/Jeevan-kumar-Raj/Grokking-System-Design#system-designs
Licence / access: **GPL-3.0** (per repo `LICENSE`)
Authority: 6,583 stars; the most-starred of several GitHub mirrors of Educative's paywalled
"Grokking the System Design Interview" course notes (confirmed against
`sharanyaa/grok_sdi_educative`, `imujjwalanand/Grokking-the-System-Design`, and other forks
found in the same search, all lower-starred copies of the same content).
Fetched: 2026-09-19 via `gh api repos/Jeevan-kumar-Raj/Grokking-System-Design/readme` and one `designs/*.md` file read directly.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Short URL Service | URL shortener | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/short-url.md | free | deep |
| Pastebin | Pastebin | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/pastebin.md | free | deep |
| Instagram | Instagram / photo sharing | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/instagram.md | free | deep |
| Dropbox | File sync (Dropbox/Drive) | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/dropbox.md | free | deep |
| Twitter | News feed / timeline | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/twitter.md | free | deep |
| Youtube | Video streaming (YouTube/Netflix) | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/youtube.md | free | deep |
| Twitter Search | Search engine | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/twitter-search.md | free | deep |
| Web Crawler | Web crawler | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/web-crawler.md | free | deep |
| Facebook Newsfeed | News feed / timeline | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/facebook-newsfeed.md | free | deep |
| Yelp | Proximity / nearby search (Yelp) | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/yelp.md | free | deep |
| Uber Backend | Ride hailing (Uber) | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/uber-backend.md | free | deep |
| Ticketmaster | Ticket booking (Ticketmaster) | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design/blob/master/designs/ticketmaster.md | free | deep |
| Design a product based on maps, eg hotel / ATM finder given a location | Proximity / nearby search (Yelp) | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design#designques | free | outline |
| A web application for instant messaging, eg WhatsApp, Facebook chat | WhatsApp | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design#designques | free | outline |
| Design a system for collaborating over a document simultaneously (eg Google Docs) | Google Docs / collaborative editing | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design#designques | free | outline |
| Top 'n' or most frequent items of a running stream of data | Top-K / heavy hitters | https://github.com/Jeevan-kumar-Raj/Grokking-System-Design#designques | free | outline |

`designs/short-url.md` runs 185 lines with requirements, capacity estimation, API,
high-level and detailed design — "deep" depth; the other `designs/*.md` files follow the
same template (verified via the README's per-page structure) so all twelve are recorded as
deep. The `#designques` list further down the README is a bare bullet list of additional
prompts with only external reference links (no in-repo write-up) — outline depth. Several
items there duplicate the `designs/` list (e.g. news feed, picture sharing, search engine,
random ID generation, GC, tinyurl) and were not re-recorded; only the four rows above are
new relative to the `designs/` table.

## liquidslr/system-design-notes

URL: https://github.com/liquidslr/system-design-notes#readme
Licence / access: no LICENSE file in the repo (free to read on GitHub; personal notes on a
paid book, no explicit reuse licence granted)
Authority: 20,304 stars; a chapter-by-chapter notes mirror of the book "System Design
Interview – An Insider's Guide" (Vol 1 & 2, Alex Xu / ByteByteGo) — one of the two most
recommended system-design books; the repo's own README links to bytebytego.com's official
course page for the same material and to a third-party notes site (pagefy.io).
Fetched: 2026-09-19 via `gh api repos/liquidslr/system-design-notes/readme` and one chapter
`Readme.md` (`04. Rate Limiter/Readme.md`) read directly to check depth.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Chapter 4 - Design A Rate Limiter | Rate limiter | https://github.com/liquidslr/system-design-notes/blob/main/04.%20Rate%20Limiter/Readme.md | free | deep |
| Chapter 5 - Design Consistent Hashing | Consistent hashing service | https://github.com/liquidslr/system-design-notes/tree/main/05.%20Consistent%20Hashing | free | deep |
| Chapter 6 - Design A Key-Value Store | Key-value store | https://github.com/liquidslr/system-design-notes/tree/main/06.%20Key-Value%20Store | free | deep |
| Chapter 7 - Design A Unique ID Generator In Distributed Systems | Unique ID generator | https://github.com/liquidslr/system-design-notes/tree/main/07.%20Unique-Id%20Generator | free | deep |
| Chapter 8 - Design A URL Shortener | URL shortener | https://github.com/liquidslr/system-design-notes/tree/main/08.%20URL%20Shortener | free | deep |
| Chapter 9 - Design A Web Crawler | Web crawler | https://github.com/liquidslr/system-design-notes/tree/main/09.%20Web%20Crawler | free | deep |
| Chapter 10 - Design A Notification System | Notification system | https://github.com/liquidslr/system-design-notes/tree/main/10.%20Notification%20System | free | deep |
| Chapter 11 - Design A News Feed System | News feed / timeline | https://github.com/liquidslr/system-design-notes/tree/main/11.%20News%20Feed%20System | free | deep |
| Chapter 12 - Design A Chat System | Chat / messaging | https://github.com/liquidslr/system-design-notes/tree/main/12.%20Chat%20System | free | deep |
| Chapter 13 - Design A Search Autocomplete System | Typeahead / autocomplete | https://github.com/liquidslr/system-design-notes/tree/main/13.%20Search%20Autocomplete | free | deep |
| Chapter 14 - Design YouTube | Video streaming (YouTube/Netflix) | https://github.com/liquidslr/system-design-notes/tree/main/14.%20Youtube | free | deep |
| Chapter 15 - Design Google Drive | File sync (Dropbox/Drive) | https://github.com/liquidslr/system-design-notes/tree/main/15.%20Google%20Drive | free | deep |
| Chapter 16 - Proximity Service | Proximity / nearby search (Yelp) | https://github.com/liquidslr/system-design-notes/tree/main/16.%20Proximity%20Service | free | deep |
| Chapter 17 - Nearby Friends | Nearby friends (real-time location) | https://github.com/liquidslr/system-design-notes/tree/main/17.%20Nearby%20Friends | free | deep |
| Chapter 18 - Design Google Maps | Maps / navigation (Google Maps) | https://github.com/liquidslr/system-design-notes/tree/main/18.%20Google%20Maps | free | deep |
| Chapter 19 - Distributed Message Queue | Distributed message queue | https://github.com/liquidslr/system-design-notes/tree/main/19.%20Distributed%20Message%20Queue | free | deep |
| Chapter 20 - Metrics Monitoring and Alerting System | Metrics / monitoring | https://github.com/liquidslr/system-design-notes/tree/main/20.%20Metrics%20Monitoring%20and%20Alerting%20System | free | deep |
| Chapter 21 - Ad Click Event Aggregation | Ad click aggregation | https://github.com/liquidslr/system-design-notes/tree/main/21.%20Ad%20Click%20Event%20Aggregation | free | deep |
| Chapter 22 - Hotel Reservation System | Hotel reservation | https://github.com/liquidslr/system-design-notes/tree/main/22.%20Hotel%20Reservation%20System | free | deep |
| Chapter 23 - Distributed Email Service | Email service | https://github.com/liquidslr/system-design-notes/tree/main/23.%20Distributed%20Email%20Service | free | deep |
| Chapter 24 - S3-like Object Storage | Object storage (S3) | https://github.com/liquidslr/system-design-notes/tree/main/24.%20S3-like%20Object%20Storage | free | deep |
| Chapter 25 - Real-time Gaming Leaderboard | Leaderboard | https://github.com/liquidslr/system-design-notes/tree/main/25.%20Real-time%20Gaming%20Leaderboard | free | deep |
| Chapter 26 - Payment System | Payment system | https://github.com/liquidslr/system-design-notes/tree/main/26.%20Payment%20System | free | deep |
| Chapter 27 - Digital Wallet | Digital wallet | https://github.com/liquidslr/system-design-notes/tree/main/27.%20%20Digital%20Wallet | free | deep |
| Chapter 28 - Stock Exchange | Stock exchange | https://github.com/liquidslr/system-design-notes/tree/main/28.%20Stock%20Exchange | free | deep |

Chapters 1-3 (Scale From Zero To Millions Of Users, Back-of-the-envelope Estimation, A
Framework For System Design Interviews) were read but excluded — they are methodology/
concept chapters, not "design X" problems. `04. Rate Limiter/Readme.md` runs 132 lines with
requirements, high-level design (with diagram), algorithm tradeoffs and a distributed-system
deep dive, matching the book's per-chapter structure — recorded as "deep" for all 25 design
chapters on the strength of that one verified sample plus the consistent per-chapter layout
implied by the README's own chapter titles ("Design A ...").

## Notes

- **Coverage**: 8 repositories read (donnemartin, karanpratapsingh, ashishps1, checkcheckzz,
  ByteByteGoHq, binhnguyennus, liquidslr, Jeevan-kumar-Raj) — the six required by the task
  plus two extra high-star repos (`liquidslr/system-design-notes`, 20,304 stars;
  `Jeevan-kumar-Raj/Grokking-System-Design`, 6,583 stars) surfaced by the same GitHub
  searches, chosen because both contain original worked walkthroughs rather than link
  lists.
- **liquidslr/system-design-notes** section is written separately below this list because
  it was the single richest source found — see its own `## liquidslr/system-design-notes`
  section for the full 25-row table.
- **Licence spread is wide and matters for reuse**: CC BY 4.0 (donnemartin, most permissive,
  genuinely reusable) vs. CC BY-NC-ND 4.0 (karanpratapsingh, ByteByteGoHq — no derivatives
  allowed, so their wording cannot be adapted into cards, only cited/linked) vs. GPL-3.0
  (ashishps1, Jeevan-kumar-Raj — a software licence applied to prose, ambiguous for text
  reuse) vs. no LICENSE at all (checkcheckzz, liquidslr — default copyright, read-only)
  vs. MIT (binhnguyennus). None of the sources here are safe to copy verbatim into the
  vault; all are safe to read, cite and re-derive from.
- **Consistent-hashing-as-a-service and rate limiters recur as "building block" design
  problems** across nearly every source (donnemartin's additional list, karanpratapsingh's
  Chapter IV as a concept but not a full chapter, ashishps1, liquidslr ch.4-5,
  checkcheckzz) — these are clearly core canon, not edge cases.
- **liquidslr/system-design-notes is structurally unique**: it is the only repo whose whole
  README *is* a 28-chapter table of contents mirroring a specific paid book ("System Design
  Interview – An Insider's Guide," Vol 1 & 2, Alex Xu), one folder per chapter, each with
  its own `Readme.md` and diagram images. No LICENSE file, so treat it as read-only
  reference, not a source to copy from.
- **Newly-popular problems** relative to the older sources (checkcheckzz, donnemartin, both
  written before ~2018): Digital Wallet, Stock Exchange, Distributed Job Scheduler, Online
  Code Editor / collaborative IDE, Distributed Locking Service, CI/CD deployment system,
  Short-form video (TikTok), UPI/payment-specific systems — these only show up in the two
  newest, most actively maintained sources (ashishps1's 2025-era list and liquidslr's
  Vol.-2-based chapters), not in the pre-2018 lists.
- **Problems only one source has**: "Design an online multiplayer card game" and "Design a
  garbage collection system" (donnemartin's additional list and checkcheckzz only — both
  copy the same original list, so this is really one source, not two independent
  sightings); "Design Zoom" / video conferencing (ashishps1 only); "Nearby Friends" as
  distinct from generic proximity search (liquidslr only, ch.17); "Designing a Permission
  System" (ByteByteGoHq only).
- **Could not fully use**: `binhnguyennus/awesome-scalability` — read in full, contributes
  no rows because it curates real-world architecture write-ups, not "design X" interview
  prompts (see its section above for the reasoning). This is a legitimate zero, not a
  fetch failure.
- **Seen but not covered** (ran out of scope at 8 sources, found via the same searches and
  plausibly worth a follow-up pass): `liquidslr/system-design-notes` is included above;
  additionally `madd86/awesome-system-design` (12,495 stars, general awesome-list, likely
  low "design X" density similar to awesome-scalability) and
  `DreamOfTheRedChamber/system-design-interviews` (2,137 stars, just under the ~3,000-star
  bar) were noted in the search results but not opened.
