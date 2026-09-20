# System design problem survey — Grokking, Exponent, and others

Companion to the other survey files in this folder. Covers the sources assigned to this
agent: the DesignGurus/Educative "Grokking" course family, Exponent, interviewing.io,
systemdesign.one / systemdesignschool.io, Codemia / LeetCode Discuss, Tech Interview
Handbook / course-author blog posts, and company-reported lists.

## Grokking the System Design Interview (DesignGurus / originally Educative)

URL: https://www.designgurus.io/course/grokking-the-system-design-interview
Licence / access: paid book/course (no open licence; DesignGurus.io is the current home of
the original Educative course, since rewritten with video).
Authority: written by Design Gurus (ex-FAANG authors incl. Arslan Ahmad); the original
Educative "Grokking the System Design Interview" is the best-known system design prep
course in the industry (175,000+ learners per the vendor, widely referenced across
interview-prep blogs and reviews).
Fetched: 2026-09-19, WebFetch of the DesignGurus course page, cross-checked against an
independent third-party review (dev.to "Grokking the System Design Interview: A Detailed
Review") which lists the identical 15 problems — both agree, so this list is high
confidence. Note: WebFetch of the parallel Educative URL
(https://www.educative.io/courses/grokking-the-system-design-interview) returned a list
that in fact matches "Grokking Modern System Design Interview" (source 3 below), not this
course — Educative's rendered page appears to surface related/upsell content rather than
this course's own TOC, so that fetch was discarded in favour of the DesignGurus page + the
dev.to review.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Designing a URL Shortening Service like TinyURL | URL shortener | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Pastebin | Pastebin | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Instagram | Instagram / photo sharing | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Dropbox | File sync (Dropbox/Drive) | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Facebook Messenger | Chat / messaging | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Twitter | News feed / timeline | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Youtube or Netflix | Video streaming (YouTube/Netflix) | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Typeahead Suggestion | Typeahead / autocomplete | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing an API Rate Limiter | Rate limiter | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Twitter Search | Search engine | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing a Web Crawler | Web crawler | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Facebook's Newsfeed | News feed / timeline | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Yelp or Nearby Friends | Proximity / nearby search (Yelp) | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Uber backend | Ride hailing (Uber) | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |
| Designing Ticketmaster | Ticket booking (Ticketmaster) | https://www.designgurus.io/course/grokking-the-system-design-interview | book | walkthrough |

## Grokking the Advanced System Design Interview (DesignGurus, Volume II)

URL: https://www.designgurus.io/course/grokking-the-advanced-system-design-interview
Licence / access: paid book/course.
Authority: DesignGurus.io, same authors as the original Grokking course; explicitly
targeted at L5/L6-level candidates; 142 lessons / ~36 hours per the vendor's own curriculum
page.
Fetched: 2026-09-19, WebFetch of the course curriculum page (rendered successfully, listing
both "Application-Level Design Problems" and "Real Distributed Systems Deep-Dives"
sections with per-topic lesson counts).

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| YouTube Likes Counter | Web analytics | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Unique ID Generator | Unique ID generator | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Notification Service | Notification system | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Reddit | Reddit / forum feed | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Google Calendar | Google Calendar | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Gmail | Email service | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Google News | News aggregator | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Netflix Recommendation System | Recommendation system | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Code Judging System | Online judge (LeetCode) | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Payment System | Payment system | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Flash Sale System | Flash sale system | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Reminder Alert System | Notification system | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Dynamo: Key-Value Store | Case study: Dynamo | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Cassandra: Wide-Column NoSQL Database | Case study: Cassandra | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Kafka: Distributed Messaging System | Case study: Kafka | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| Chubby: Distributed Locking Service | Case study: Chubby | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| HDFS: File Storage System | Case study: HDFS | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| GFS: Distributed File System Storage | Case study: GFS | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |
| BigTable: Wide Column Storage System | Case study: BigTable | https://www.designgurus.io/course/grokking-the-advanced-system-design-interview | book | deep |

## Grokking Modern System Design Interview (Educative)

URL: https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers
Licence / access: paid book/course.
Authority: Educative's own current flagship system-design course (successor positioning to
the original Grokking course, aimed at both engineers and managers); listed and promoted
directly on educative.io.
Fetched: 2026-09-19, WebFetch of the course page rendered a full "Design Problems &
Case Studies" TOC directly.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design YouTube | Video streaming (YouTube/Netflix) | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design TikTok | Video streaming (YouTube/Netflix) | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Quora | Reddit / forum feed | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Google Maps | Google Maps | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a Proximity Service/Yelp | Proximity / nearby search (Yelp) | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Uber | Ride hailing (Uber) | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Uber Eats | Food delivery | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Twitter | News feed / timeline | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Newsfeed System | News feed / timeline | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Instagram | Instagram / photo sharing | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a URL Shortening Service/TinyURL | URL shortener | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a Web Crawler | Web crawler | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design WhatsApp | WhatsApp | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Facebook Messenger | Chat / messaging | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design Typeahead Suggestion | Typeahead / autocomplete | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a Collaborative Document Editing Service/Google Docs | Google Docs / collaborative editing | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a Deployment System | Distributed job scheduler | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a Payment System | Payment system | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a LeetCode System | Online judge (LeetCode) | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a ChatGPT System | ChatGPT-style LLM service | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| Design a Data Infrastructure System | Data infrastructure system | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| LLM-Powered Customer Support Bot System Design | LLM customer support bot | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |
| AI-Powered Code Assistant System Design | AI code assistant | https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers | book | walkthrough |

## Exponent

URL: https://www.tryexponent.com/courses/system-design-interviews (course) and
https://www.tryexponent.com/questions?type=system-design (question bank)
Licence / access: course is paid/subscription; the question bank browsing pages are free
to read (individual answers may be gated).
Authority: Exponent (formerly "Exponent", now also branded "Aced") is a well-known
interview-prep platform built from real candidate-submitted questions and mock interviews
with ex-FAANG interviewers; the question bank entries carry explicit company tags and
submission dates, which is unusually well-sourced compared to most listicles.
Fetched: 2026-09-19. The paid course's own lesson-by-lesson curriculum page
(`/courses/system-design-interviews/...`) returned no body content via WebFetch (JS-gated,
likely requires login) — this path failed. Fell back to the public, crawlable question bank
at `/questions?type=system-design`, pages 1–2, which rendered fully via WebFetch and
includes real company attributions and submission recency, arguably more useful for this
survey's purpose than a generic course TOC.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design webhook delivery | Distributed message queue | https://www.tryexponent.com/questions?type=system-design | free | outline; reported 5 days ago (no company given) |
| Design an LLM-based Q&A System | ChatGPT-style LLM service | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Google |
| Design a system to track reviews abuse on Amazon.com | Top-K / heavy hitters | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at DoorDash, Amazon |
| Design a priority heap | Distributed job scheduler | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Google |
| Design S3 | Object storage (S3) | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at JP Morgan Chase, Amazon |
| How would you design a system like Google Street View? | Google Street View | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Meta |
| Design a system to help internal company teams arrange events/meetups | Event/meetup scheduler | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Palantir |
| You have one huge file coming in over a constrained link. How do you distribute it to thousands of machines? | Large file distribution | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Anthropic |
| Design an inference batching system for a single GPU | LLM inference service | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Anthropic |
| Design LFU cache | Distributed cache | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Microsoft |
| Design an API that lets a customer sample from large generative models | LLM inference service | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Anthropic |
| Design a system to log messages in order | Distributed message queue | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Microsoft, Google |
| Design a link sharing application | URL shortener | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at MongoDB |
| Design Google Docs | Google Docs / collaborative editing | https://www.tryexponent.com/questions?type=system-design | free | outline (no company given) |
| Design a document processing pipeline | Data infrastructure system | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Databricks |
| Design a retrieval-augmented generation system over a customer's private data | RAG system | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at OpenAI, Google |
| Design Cookie Clicker | Cookie Clicker game backend | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Nvidia, Netflix |
| Design Instagram | Instagram / photo sharing | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Amazon, DoorDash, Meta |
| Design a multi-region architecture | Multi-region architecture | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Amazon |
| Design a distributed logging system | Metrics / monitoring | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Goldman Sachs, Amazon |
| Design a next word prediction system | Typeahead / autocomplete | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Meta |
| Design a Distributed LRU Cache | Distributed cache | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Google, Walmart, Stripe |
| Design a system that delivers firmware updates to devices | Large file distribution | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Microsoft, Amazon |
| Design TurboTax | Tax-filing platform | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Stripe |
| Design TikTok | Video streaming (YouTube/Netflix) | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at TikTok, Nordstrom, Reddit |
| How would you build TinyURL? | URL shortener | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Amazon, Meta, Confluent |
| Design Amazon Prime video | Video streaming (YouTube/Netflix) | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Amazon |

## interviewing.io — "A Senior Engineer's Guide to the System Design Interview"

URL: https://interviewing.io/guides/system-design-interview
Licence / access: free to read.
Authority: interviewing.io runs anonymous mock interviews with engineers from top
companies and publishes guides distilled from those sessions; this guide is widely
recommended in engineering interview-prep circles for being written from actual interviewer
feedback rather than as a listicle.
Fetched: 2026-09-19, WebFetch rendered the guide's worked examples directly.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design TikTok (simplified version) | Video streaming (YouTube/Netflix) | https://interviewing.io/guides/system-design-interview | free | walkthrough |
| Design Pastebin | Pastebin | https://interviewing.io/guides/system-design-interview | free | walkthrough |
| Unique ID Generation (the Key Generation Service / KGS) | Unique ID generator | https://interviewing.io/guides/system-design-interview | free | walkthrough |
| Design AOL Instant Messenger | Chat / messaging | https://interviewing.io/guides/system-design-interview | free | walkthrough |
| Design Ticketmaster | Ticket booking (Ticketmaster) | https://interviewing.io/guides/system-design-interview | free | walkthrough |
| Design Google Docs (30-minute mock, two experts) | Google Docs / collaborative editing | https://interviewing.io/guides/system-design-interview | free | walkthrough |
| Design a remote compiler (30-minute mock, two experts) | Remote code execution service | https://interviewing.io/guides/system-design-interview | free | walkthrough |
| Design a recording service (30-minute mock, two experts) | Recording service | https://interviewing.io/guides/system-design-interview | free | walkthrough |

## systemdesign.one and System Design School (systemdesignschool.io)

URL: https://systemdesign.one/sitemap.xml (systemdesign.one; `/posts/` index is paginated
and only partially rendered via WebFetch) and https://systemdesignschool.io/problems
(System Design School).
Licence / access: free to read (both sites; systemdesign.one is ad/newsletter-supported,
systemdesignschool.io shows a paid "solution" behind some problems but the list itself is
free).
Authority: systemdesign.one is run by Neo Kim (also behind The System Design newsletter,
widely followed on Substack/LinkedIn); System Design School is a dedicated prep site with a
large, actively maintained catalogue of problem write-ups, frequently cited alongside
Grokking/ByteByteGo in "best system design resources" round-ups.
Fetched: 2026-09-19. systemdesign.one's `/posts/` index rendered only its latest-post
snippet via WebFetch (JS pagination) — that path returned an incomplete list, so the
`sitemap.xml` was used instead, which listed the individual case-study article URLs
directly. systemdesignschool.io/problems rendered its full list directly via WebFetch.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Slack Architecture That Powers Billions of Messages a Day | Chat / messaging | https://systemdesign.one/slack-architecture/ | free | deep |
| Distributed Counter System Design | Distributed counter | https://systemdesign.one/distributed-counter-system-design/ | free | deep |
| Real-Time Presence Platform System Design | Online presence indicator | https://systemdesign.one/real-time-presence-platform-system-design/ | free | deep |
| Live Comment System Design | Live comments | https://systemdesign.one/live-comment-system-design/ | free | deep |
| Leaderboard System Design | Leaderboard | https://systemdesign.one/leaderboard-system-design/ | free | deep |
| System Design Pastebin | Pastebin | https://systemdesign.one/system-design-pastebin/ | free | deep |
| URL Shortening System Design | URL shortener | https://systemdesign.one/url-shortening-system-design/ | free | deep |
| Design URL Shortener | URL shortener | https://systemdesignschool.io/problems | free | outline |
| Design Pastebin | Pastebin | https://systemdesignschool.io/problems | free | outline |
| Design Webhook | Distributed message queue | https://systemdesignschool.io/problems | free | outline |
| Design Typeahead / Autocomplete | Typeahead / autocomplete | https://systemdesignschool.io/problems | free | outline |
| Design Tinder | Tinder | https://systemdesignschool.io/problems | free | outline |
| Design LeetCode (Online Judge) | Online judge (LeetCode) | https://systemdesignschool.io/problems | free | outline |
| Design a Distributed Rate Limiter | Rate limiter | https://systemdesignschool.io/problems | free | outline |
| Design Google Calendar | Google Calendar | https://systemdesignschool.io/problems | free | outline |
| Design Twitter | News feed / timeline | https://systemdesignschool.io/problems | free | outline |
| Design Yelp | Proximity / nearby search (Yelp) | https://systemdesignschool.io/problems | free | outline |
| Design Netflix | Video streaming (YouTube/Netflix) | https://systemdesignschool.io/problems | free | outline |
| Design Robinhood (Stock Trading) | Stock exchange | https://systemdesignschool.io/problems | free | outline |
| Design Dropbox | File sync (Dropbox/Drive) | https://systemdesignschool.io/problems | free | outline |
| Design Google Docs | Google Docs / collaborative editing | https://systemdesignschool.io/problems | free | outline |
| Design Ticketmaster | Ticket booking (Ticketmaster) | https://systemdesignschool.io/problems | free | outline |
| Design Live Comments (Real-Time Fan-Out) | Live comments | https://systemdesignschool.io/problems | free | outline |
| Design a News Aggregator | News aggregator | https://systemdesignschool.io/problems | free | outline |
| Design Post Search (Full-Text Search) | Search engine | https://systemdesignschool.io/problems | free | outline |
| Design Local Delivery (Gopuff) | Food delivery | https://systemdesignschool.io/problems | free | outline |
| Design an Online Auction | Auction | https://systemdesignschool.io/problems | free | outline |
| Design a Metrics Monitoring System | Metrics / monitoring | https://systemdesignschool.io/problems | free | outline |
| Design a Distributed Job Scheduler | Distributed job scheduler | https://systemdesignschool.io/problems | free | outline |
| Design a Payment System | Payment system | https://systemdesignschool.io/problems | free | outline |
| Design a Web Crawler | Web crawler | https://systemdesignschool.io/problems | free | outline |
| Design an Ad Click Aggregator | Ad click aggregation | https://systemdesignschool.io/problems | free | outline |
| Design Top K (Trending) | Top-K / heavy hitters | https://systemdesignschool.io/problems | free | outline |
| Design Uber / Nearby Drivers | Ride hailing (Uber) | https://systemdesignschool.io/problems | free | outline |
| Design a Pub-Sub / Message Queue | Distributed message queue | https://systemdesignschool.io/problems | free | outline |
| Design a Chat App (WhatsApp / Messenger) | WhatsApp | https://systemdesignschool.io/problems | free | outline |
| Design YouTube | Video streaming (YouTube/Netflix) | https://systemdesignschool.io/problems | free | outline |
| Design a News Feed | News feed / timeline | https://systemdesignschool.io/problems | free | outline |
| Design Instagram | Instagram / photo sharing | https://systemdesignschool.io/problems | free | outline |
| Design a Distributed Cache | Distributed cache | https://systemdesignschool.io/problems | free | outline |
| Design a Distributed Key-Value Store | Key-value store | https://systemdesignschool.io/problems | free | outline |
| Design Google Maps | Google Maps | https://systemdesignschool.io/problems | free | outline |

## Codemia and LeetCode Discuss

URL: https://codemia.io/system-design (Codemia); LeetCode Discuss threads (see below).
Licence / access: Codemia's problem list is free to browse (solving/grading is
subscription-gated). LeetCode Discuss is free to read when reachable.
Authority: Codemia is a system-design-interview practice platform with an
automatically-graded write-up format; its catalogue (127 problems at fetch time, split
Easy/Medium/Hard/Advanced) is one of the largest curated problem sets found in this survey.
LeetCode Discuss is the community forum attached to LeetCode, widely used to crowdsource
"most asked" question lists, but individual threads carry no formal editorial review.
Fetched: 2026-09-19. codemia.io/system-design rendered its full catalogue via WebFetch.
LeetCode Discuss threads (`/discuss/interview-question/5806013/Most-asked-System-Design-questions/`
and `/discuss/interview-question/system-design/5324660/top-25-hld-questions-list/`) both
returned HTTP 403 to WebFetch, and a web.archive.org fallback for the same URL was also
unreachable from this environment — both LeetCode Discuss paths failed and no rows from it
are included below (see Notes).

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Designing a Simple URL Shortening Service: A TinyURL Approach | URL shortener | https://codemia.io/system-design | free | outline |
| Design an Efficient Parking Lot System | Parking lot system | https://codemia.io/system-design | free | outline |
| Design a Fitness Tracking App | Fitness tracking app | https://codemia.io/system-design | free | outline |
| Design a Weather Reporting System | Weather reporting system | https://codemia.io/system-design | free | outline |
| Design Pastebin | Pastebin | https://codemia.io/system-design | free | outline |
| Design a Nested Comments System | Nested comments system | https://codemia.io/system-design | free | outline |
| Design an Online Presence Indicator Service | Online presence indicator | https://codemia.io/system-design | free | outline |
| Design a Vending Machine System | Vending machine system | https://codemia.io/system-design | free | outline |
| Design a Tagging Service | Tagging service | https://codemia.io/system-design | free | outline |
| Design Craigslist | Craigslist / classifieds | https://codemia.io/system-design | free | outline |
| Design a Multi-Device Screenshot Capture System | Screenshot capture system | https://codemia.io/system-design | free | outline |
| Design a Network Connection Path Analyzer | Network path analyzer | https://codemia.io/system-design | free | outline |
| Design an Employee Swap System | Employee swap system | https://codemia.io/system-design | free | outline |
| Design a Conference Room Booking System | Conference room booking | https://codemia.io/system-design | free | outline |
| Design a Video View Count System | Web analytics | https://codemia.io/system-design | free | outline |
| Design Twitter | News feed / timeline | https://codemia.io/system-design | free | outline |
| Design Facebook Messenger | Chat / messaging | https://codemia.io/system-design | free | outline |
| Design an API Rate Limiter | Rate limiter | https://codemia.io/system-design | free | outline |
| Design Youtube or Netflix | Video streaming (YouTube/Netflix) | https://codemia.io/system-design | free | outline |
| Design Typeahead Suggestion | Typeahead / autocomplete | https://codemia.io/system-design | free | outline |
| Design Twitter Search | Search engine | https://codemia.io/system-design | free | outline |
| Design Instagram | Instagram / photo sharing | https://codemia.io/system-design | free | outline |
| Design an Online Chess Service | Online chess service | https://codemia.io/system-design | free | outline |
| Design a Web Cache | Distributed cache | https://codemia.io/system-design | free | outline |
| Design a Task Scheduler | Distributed job scheduler | https://codemia.io/system-design | free | outline |
| Design an E-commerce Service | E-commerce platform | https://codemia.io/system-design | free | outline |
| Design an Inventory Management System | Inventory management system | https://codemia.io/system-design | free | outline |
| Design an Online Payment Service | Payment system | https://codemia.io/system-design | free | outline |
| Design Spotify | Music streaming (Spotify) | https://codemia.io/system-design | free | outline |
| Design a Live Video Streaming Platform | Video streaming (YouTube/Netflix) | https://codemia.io/system-design | free | outline |
| Design a Video Conferencing system | Video conferencing | https://codemia.io/system-design | free | outline |
| Design an Ebook Distribution Platform | Ebook distribution platform | https://codemia.io/system-design | free | outline |
| Design a Blockchain Based System | Blockchain-based system | https://codemia.io/system-design | free | outline |
| Design a Web Analytics Tool | Web analytics | https://codemia.io/system-design | free | outline |
| Design a Public Transportation System | Public transportation system | https://codemia.io/system-design | free | outline |
| Design a Language Translation Service | Language translation service | https://codemia.io/system-design | free | outline |
| Design a Task Management Application | Task management application | https://codemia.io/system-design | free | outline |
| Design a Voting System | Voting system | https://codemia.io/system-design | free | outline |
| Design a Real Time Sports Scoring System | Real-time sports scoring | https://codemia.io/system-design | free | outline |
| Design a Podcast Hosting Platform | Podcast hosting platform | https://codemia.io/system-design | free | outline |
| Design Shopify | E-commerce platform | https://codemia.io/system-design | free | outline |
| Design a Digital Wallet | Digital wallet | https://codemia.io/system-design | free | outline |
| Design a Code Deployment System | Distributed job scheduler | https://codemia.io/system-design | free | outline |
| Design a Live Comment System | Live comments | https://codemia.io/system-design | free | outline |
| Design a Distributed Counter | Distributed counter | https://codemia.io/system-design | free | outline |
| Design a Distributed Locking System | Distributed locking service | https://codemia.io/system-design | free | outline |
| Design a Platform Like Reddit | Reddit / forum feed | https://codemia.io/system-design | free | outline |
| Design a CAPTCHA System | CAPTCHA system | https://codemia.io/system-design | free | outline |
| Design a Database Batch Auditing Service | Database batch auditing service | https://codemia.io/system-design | free | outline |
| Design a Distributed Unique Id Generator | Unique ID generator | https://codemia.io/system-design | free | outline |
| Design an Online Coupon Service | Online coupon service | https://codemia.io/system-design | free | outline |
| Design a Flash Sale System | Flash sale system | https://codemia.io/system-design | free | outline |
| Design an ATM Machine System | ATM machine system | https://codemia.io/system-design | free | outline |
| Design a Meeting Calendar System | Google Calendar | https://codemia.io/system-design | free | outline |
| Design a Collaboration Tool for Team Communication | Chat / messaging | https://codemia.io/system-design | free | outline |
| Design a Webhook Notification Service | Distributed message queue | https://codemia.io/system-design | free | outline |
| Design a Frequently Viewed Products Feature for an E-commerce Platform | Top-K / heavy hitters | https://codemia.io/system-design | free | outline |
| Design an E-commerce Recommendation System | Recommendation system | https://codemia.io/system-design | free | outline |
| Design an Air Traffic Control System | Air traffic control system | https://codemia.io/system-design | free | outline |
| Design a Digital Distribution Platform for Applications | App store / digital distribution | https://codemia.io/system-design | free | outline |
| Design a Competitive Programming Platform | Online judge (LeetCode) | https://codemia.io/system-design | free | outline |
| Design a Fresh Grocery Delivery System | Food delivery | https://codemia.io/system-design | free | outline |
| Design a Movie Reviews Aggregator System | Movie reviews aggregator | https://codemia.io/system-design | free | outline |
| Design a Collaborative Meeting Scheduler | Event/meetup scheduler | https://codemia.io/system-design | free | outline |
| Design a Server Architecture for Serving Geospatial Images | Geospatial image serving | https://codemia.io/system-design | free | outline |
| Design a QR Code System for a Grocery Shop | QR code system | https://codemia.io/system-design | free | outline |
| Design a Top-K Request Analysis System | Top-K / heavy hitters | https://codemia.io/system-design | free | outline |
| Design an Order Tracking System | Order tracking system | https://codemia.io/system-design | free | outline |
| Design a Collaborative Online Spreadsheet System | Google Docs / collaborative editing | https://codemia.io/system-design | free | outline |
| Design an Airport Baggage Handling System | Airport baggage handling system | https://codemia.io/system-design | free | outline |
| Design Ticketmaster | Ticket booking (Ticketmaster) | https://codemia.io/system-design | free | outline |
| Design Dropbox | File sync (Dropbox/Drive) | https://codemia.io/system-design | free | outline |
| Design Uber Backend | Ride hailing (Uber) | https://codemia.io/system-design | free | outline |
| Design Yelp or Nearby Friends | Proximity / nearby search (Yelp) | https://codemia.io/system-design | free | outline |
| Design Facebook's Newsfeed | News feed / timeline | https://codemia.io/system-design | free | outline |
| Design a Web Crawler | Web crawler | https://codemia.io/system-design | free | outline |
| Design Google Map | Google Maps | https://codemia.io/system-design | free | outline |
| Design Google Doc | Google Docs / collaborative editing | https://codemia.io/system-design | free | outline |
| Design an Automated Trading Platform | Stock exchange | https://codemia.io/system-design | free | outline |
| Design a Key Value Store | Key-value store | https://codemia.io/system-design | free | outline |
| Design a Global Content Distribution Network | CDN | https://codemia.io/system-design | free | outline |
| Design a Peer-to-Peer Network | Peer-to-peer network | https://codemia.io/system-design | free | outline |
| Design a Distributed Messaging System | Distributed message queue | https://codemia.io/system-design | free | outline |
| Design a Distributed File System | File sync (Dropbox/Drive) | https://codemia.io/system-design | free | outline |
| Design a Log Collection and Analysis System | Metrics / monitoring | https://codemia.io/system-design | free | outline |
| Design a Load Balancer | Load balancer | https://codemia.io/system-design | free | outline |
| Design a Scalable Email Service | Email service | https://codemia.io/system-design | free | outline |
| Design a Food Delivery Service | Food delivery | https://codemia.io/system-design | free | outline |
| Design a Hotel Booking Service | Hotel reservation | https://codemia.io/system-design | free | outline |
| Design an Auction system | Auction | https://codemia.io/system-design | free | outline |
| Design a Chatbot Framework | Chatbot framework | https://codemia.io/system-design | free | outline |
| Design a Push Notification Service | Notification system | https://codemia.io/system-design | free | outline |
| Design a Smart Home System | Smart home system | https://codemia.io/system-design | free | outline |
| Design a Secure Identity Management System | Identity/auth service | https://codemia.io/system-design | free | outline |
| Design a Real Time Stock Trading Platform | Stock exchange | https://codemia.io/system-design | free | outline |
| Design Google Search | Search engine | https://codemia.io/system-design | free | outline |
| Design a Scheduled Digital Transaction System | Payment system | https://codemia.io/system-design | free | outline |
| Design a Distributed Linked List | Distributed linked list | https://codemia.io/system-design | free | outline |
| Design a Distributed Tracing System | Metrics / monitoring | https://codemia.io/system-design | free | outline |
| Design a Wide Column Database | Case study: BigTable | https://codemia.io/system-design | free | outline |
| Design a Metrics Monitoring and Alerting System | Metrics / monitoring | https://codemia.io/system-design | free | outline |
| Design a Graph Search Function for a Social Network | Graph search (social network) | https://codemia.io/system-design | free | outline |
| Design a Resource Allocation Service | Resource allocation service | https://codemia.io/system-design | free | outline |
| Design an Event Lifecycle Management System | Event/meetup scheduler | https://codemia.io/system-design | free | outline |
| Design a Web Crawler That Will Crawl Wikipedia | Web crawler | https://codemia.io/system-design | free | outline |
| Design an Ad Click Aggregation System | Ad click aggregation | https://codemia.io/system-design | free | outline |
| Design a Service to Allocate Pool of Resources Optimally | Resource allocation service | https://codemia.io/system-design | free | outline |
| Design Sora | Video-generation LLM service | https://codemia.io/system-design | free | outline |
| Design ChatGPT | ChatGPT-style LLM service | https://codemia.io/system-design | free | outline |
| Design an LLM Inference Service | LLM inference service | https://codemia.io/system-design | free | outline |
| Design GitHub Actions | CI/CD pipeline service | https://codemia.io/system-design | free | outline |
| Design TikTok | Video streaming (YouTube/Netflix) | https://codemia.io/system-design | free | outline |
| Design a Container Orchestration System | Container orchestration system | https://codemia.io/system-design | free | outline |
| Design a High-Performance Computing Cluster | HPC cluster | https://codemia.io/system-design | free | outline |
| Design a Cloud Based Data Backup Solution | Cloud data backup solution | https://codemia.io/system-design | free | outline |
| Design a Cloud Storage Gateway | Cloud storage gateway | https://codemia.io/system-design | free | outline |
| Design a Virtualization System | Virtualization system | https://codemia.io/system-design | free | outline |
| Design a Disaster Recovery System | Disaster recovery system | https://codemia.io/system-design | free | outline |
| Design a Hybrid Cloud Workload Orchestrator | Hybrid cloud workload orchestrator | https://codemia.io/system-design | free | outline |
| Design a Multi-Cloud API Gateway | Multi-cloud API gateway | https://codemia.io/system-design | free | outline |
| Design a Serverless Architecture Framework | Serverless architecture framework | https://codemia.io/system-design | free | outline |
| Design a Large-Scale Graph Processing System | Large-scale graph processing | https://codemia.io/system-design | free | outline |
| Design a Big Data Processing Pipeline | Data infrastructure system | https://codemia.io/system-design | free | outline |
| Design a Virtual Reality Streaming Service | VR streaming service | https://codemia.io/system-design | free | outline |
| Design a Network Security Monitoring Tool | Network security monitoring tool | https://codemia.io/system-design | free | outline |
| Design a Distributed OLTP Database | Distributed OLTP database | https://codemia.io/system-design | free | outline |
| Design a Domain Name System | DNS | https://codemia.io/system-design | free | outline |

## Tech Interview Handbook and course-author blog posts

URL: https://www.techinterviewhandbook.org/system-design/ (Tech Interview Handbook);
https://www.educative.io/blog/system-design-interview-questions (Educative's own blog);
https://www.designgurus.io/blog/system-design-interview-questions-to-crack-your-next-faang-interview
(DesignGurus's own blog, "Top 25").
Licence / access: Tech Interview Handbook is open-source (MIT licence, GitHub
`yangshun/tech-interview-handbook`), free to read. Both blog posts are free to read
(vendor-owned marketing content, but written by the same authors as the paid courses, per
the task's instructions).
Authority: Tech Interview Handbook is one of the most-starred (100k+) interview-prep
repositories on GitHub, maintained by Yangshun Tay (ex-Meta staff engineer); its system
design page is a curated primer rather than an exhaustive list. The Educative and
DesignGurus blog posts are first-party content from the same teams that write the Grokking
courses, useful as a distilled "top N" companion list.
Fetched: 2026-09-19, all three fetched via WebFetch and rendered content directly.

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design a URL shortener (e.g. Bitly) | URL shortener | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a social media website (e.g. Twitter) | News feed / timeline | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a video watching website (e.g. YouTube) | Video streaming (YouTube/Netflix) | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a chatting service (e.g. Telegram, Slack, Discord) | Chat / messaging | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a file sharing service (e.g. Google Drive, Dropbox) | File sync (Dropbox/Drive) | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a ride sharing service (e.g. Uber, Lyft) | Ride hailing (Uber) | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a photo sharing service (e.g. Flickr, Pinterest) | Instagram / photo sharing | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design an e-commerce website (e.g. Amazon, eBay) | E-commerce platform | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a jobs portal (e.g. LinkedIn, Indeed) | Jobs portal | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design a web crawler (e.g. Google) | Web crawler | https://www.techinterviewhandbook.org/system-design/ | free | outline |
| Design an API rate limiter for sites like Firebase or GitHub | Rate limiter | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a pub/sub system like Kafka | Case study: Kafka | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a scalable content delivery network (CDN) | CDN | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design an authentication and SSO platform like Auth0 | Identity/auth service | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design an AI-powered customer support platform | LLM customer support bot | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a social network service like Reddit or Quora | Reddit / forum feed | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a distributed locking service like Google Chubby locking | Case study: Chubby | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a coordination system like ZooKeeper | Coordination service (ZooKeeper) | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a scalable distributed storage system like Bigtable | Case study: BigTable | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design an online multiplayer game system | Online multiplayer game | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a Zoom-like video conferencing system | Video conferencing | https://www.educative.io/blog/system-design-interview-questions | free | outline |
| Design a unique ID generator (Snowflake) | Unique ID generator | https://www.designgurus.io/blog/system-design-interview-questions-to-crack-your-next-faang-interview | free | walkthrough |
| Design a parking lot system | Parking lot system | https://www.designgurus.io/blog/system-design-interview-questions-to-crack-your-next-faang-interview | free | walkthrough |
| Design Airbnb (a two-sided marketplace) | Airbnb / two-sided marketplace | https://www.designgurus.io/blog/system-design-interview-questions-to-crack-your-next-faang-interview | free | walkthrough |

## Company-reported lists

URL: https://raw.githubusercontent.com/checkcheckzz/system-design-interview/master/README.md
(GitHub repo); company tags captured for Exponent's question bank above also belong here.
Licence / access: free to read on GitHub (no LICENSE file found in the repo at fetch time,
so treat as "all rights reserved / read-only" per GitHub's default).
Authority: `checkcheckzz/system-design-interview` is a long-standing, heavily-starred
(16k+ stars) community-curated repo of "hot" system design interview questions,
predominantly reported from Facebook interview experiences; widely cited in other
interview-prep round-ups as an early, primary crowdsourced source (predates most of the
paid courses above). This section also captures other cross-tool company-reported rows
duplicated from the Exponent question bank (source 4) that are strongly company-specific.
Fetched: 2026-09-19, WebFetch of the raw README rendered directly (falling back to the raw
GitHub content URL rather than the rendered repo page, to get the actual markdown).

| Problem (the source's own title) | Canonical name | URL | Access | Depth |
|---|---|---|---|---|
| Design a CDN network | CDN | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook (per repo framing) |
| Design a Google document system | Google Docs / collaborative editing | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a random ID generation system | Unique ID generator | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a key-value database | Key-value store | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design the Facebook news feed function | News feed / timeline | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design the Facebook timeline function | News feed / timeline | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a function to return the top k requests during past time interval | Top-K / heavy hitters | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design an online multiplayer card game | Online multiplayer game | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a graph search function | Graph search (social network) | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a picture sharing system | Instagram / photo sharing | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a search engine | Search engine | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a recommendation system | Recommendation system | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a tinyurl system | URL shortener | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a garbage collection system | Garbage collection system | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a scalable web crawling system | Web crawler | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design the Facebook chat function | Chat / messaging | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a trending topic system | Top-K / heavy hitters | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| Design a cache system | Distributed cache | https://github.com/checkcheckzz/system-design-interview | free | outline; reported at Facebook |
| How would you design a system like Google Street View? | Google Street View | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Meta |
| Design a system to help internal company teams arrange events/meetups | Event/meetup scheduler | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Palantir |
| You have one huge file coming in over a constrained link. How do you distribute it to thousands of machines? | Large file distribution | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Anthropic |
| Design an inference batching system for a single GPU | LLM inference service | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Anthropic |
| Design a Distributed LRU Cache | Distributed cache | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Google, Walmart, Stripe |
| Design TurboTax | Tax-filing platform | https://www.tryexponent.com/questions?type=system-design | free | outline; reported at Stripe |

## Notes

- **Educative page ambiguity**: fetching `educative.io/courses/grokking-the-system-design-interview`
  directly returned a problem list identical to "Grokking Modern System Design Interview"
  (source 3), not the original 15-problem course. This looks like Educative's rendered page
  surfacing a related/upsell course's content rather than its own — possibly because the
  original course's marketing page now cross-promotes the newer one prominently. The
  15-problem list recorded above for source 1 instead comes from DesignGurus.io's own
  course page (the current canonical home of the original course) and is independently
  confirmed by a third-party review (dev.to). Treat this as the reason source 1 and source
  3 share a URL "personality" on Educative's own site but are recorded as distinct courses.
- **LLM/AI-system problems are newly popular**: "Design ChatGPT", "Design an LLM inference
  service", "Design a RAG system", "Design an AI-powered code assistant", and "Design an
  LLM-powered customer support bot" appear independently across Grokking Modern System
  Design Interview, DesignGurus's advanced blog content, Codemia's catalogue, and
  Exponent's real company-tagged question bank (Anthropic, Google, OpenAI). None of the
  older/original course lists (Grokking v1, checkcheckzz's 2017-era GitHub repo) have any
  of these — this looks like a genuinely new cluster of problems from the last 1–2 years,
  not something artifactual to one source.
- **Problems only one source has**: Codemia's catalogue contains many problems no other
  source lists at all — e.g. "Design an Airport Baggage Handling System", "Design a
  Conference Room Booking System", "Design a QR Code System for a Grocery Shop", "Design
  Sora", "Design GitHub Actions", "Design a Distributed Linked List". These read as
  Codemia's own long-tail expansion beyond the classic canon and are worth treating with
  lower prior for how commonly they're actually asked, despite being real catalogue
  entries.
- **Case-study systems** (Dynamo, Cassandra, Kafka, Chubby, HDFS, GFS, BigTable) appear
  only in the Advanced Grokking course among this agent's sources, plus ZooKeeper and
  BigTable again in the DesignGurus blog post — these are consistently "volume II / advanced"
  material, never in the entry-level course lists.
- **Sources not reachable or excluded**: LeetCode Discuss (`leetcode.com/discuss/...`)
  returned HTTP 403 on every attempt, including via a web.archive.org fallback which this
  environment could not reach at all — no rows from LeetCode Discuss are included, and this
  survey could not independently verify any LeetCode-crowdsourced "most asked" list.
  `systemdesign.one/posts/` (the full post index) only partially rendered via WebFetch
  (JS-driven pagination showing just the latest post) — the sitemap.xml fallback was used
  instead and may be missing a few older case-study posts not present in the sitemap.
  Exponent's actual paid-course curriculum (as opposed to its free question bank) could not
  be fetched — its lesson pages require login and returned empty content to WebFetch.
  Two generic "top N system design questions" listicles turned up in search
  (`growtechie.substack.com` and `jobaajlearnings.com`) but were excluded: both have the
  generic, uniform "How would you design a system like X?" phrasing pattern typical of
  AI-generated content-farm listicles, carry no company sourcing or evidence of firsthand
  reporting, and are not written by a named, identifiable practitioner — they were treated
  as disqualified under the "never cite AI content farms" rule rather than as confirmed
  human-authored sources.
