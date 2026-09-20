# LLD / OOD / machine-coding survey — companies (Part A) and Python material (Part B)

Scope and method: see `LLD_SURVEY_AGENT.md` in this folder. Every row below is something an
agent actually saw on a page or in a repository on 2026-09-20, via WebFetch, WebSearch (before
the session's search budget was exhausted — see Notes) or `gh` (GitHub CLI). No AI-generated
listicle is cited.

---

# Part A — what companies really ask

## 1. Exponent (tryexponent.com) question bank

URL: https://www.tryexponent.com/questions?type=coding (the `type=coding` filter; a
`type=low-level-design` or `type=object-oriented-design` filter returns "Sorry, no results
found" — Exponent does not tag questions with those two type strings)

Licence / access: proprietary, free to browse the list; full answers/practice are behind a paid
plan.

Authority: Exponent (formerly "Aced") is a commercial interview-prep company; questions are
user- and coach-submitted and dated, with company tags shown per question — closer to a live
company-tagged bank than a curated syllabus.

Languages: no solution code is shown in the fetched list view; per-question pages may have
written/video answers (not verified language).

Fetched: 2026-09-20 via WebFetch. `?type=low-level-design` and `?type=object-oriented-design`
both 404'd to empty result sets — Exponent's own taxonomy has no such filter value. Fell back to
`?type=coding`, which does surface LLD-shaped design/implementation questions alongside plain
DSA coding questions (no separate LLD facet exists on this site).

Table 1 — problems (rows found under `type=coding` that are LLD-shaped, i.e. "design and
implement a stateful component", not plain algorithm questions):

| Problem (source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Implement mutex | Thread pool / synchronization primitive | https://www.tryexponent.com/questions | paywalled | outline | — |
| Design LFU cache | LFU cache | https://www.tryexponent.com/questions | paywalled | outline; reported at Microsoft, 5 months before fetch (~2026) | — |
| Implement an LRU cache with serialization and evolving constraints | LRU cache | https://www.tryexponent.com/questions | paywalled | outline; reported at Anthropic, Nvidia, ~9 months before fetch | — |
| Implement LRU Cache | LRU cache | https://www.tryexponent.com/questions | paywalled | outline; reported at LinkedIn, Amazon, Google + 26 more companies | — |
| Design and implement a ranked cache system | Cache with TTL | https://www.tryexponent.com/questions | paywalled | outline; reported at LinkedIn, ~2 years before fetch | — |

Notes on this source: Exponent's "Company" facet (Meta, Google, Amazon, Microsoft, DoorDash,
Anthropic, Apple, OpenAI, Uber, Stripe, Nvidia, TikTok, JP Morgan Chase, Sierra AI …) is much
richer than its "type" facet — most of the site's design-flavoured content is system-design
(`Design S3`, `Design webhook delivery`) rather than class-level LLD, so this source is thinner
for LLD specifically than for HLD. Table 2 not applicable — Exponent is a flat question bank, not
a syllabus with its own headings.

---

## 2. GitHub — kumaransg/LLD

URL: https://github.com/kumaransg/LLD

Licence / access: no LICENSE file in the repo (GitHub reports none) — default all-rights-reserved,
free to read on GitHub.

Authority: individual curator (kumaransg); 2,061 stars, the highest-starred repo found under a
"low level design interview questions" GitHub search — a widely-bookmarked community list rather
than an authored course.

Languages: not verified per-problem (index page links out to sub-folders and to a third-party
site, lldcoding.com, for solutions); no explicit Python confirmation.

Fetched: 2026-09-20 via `gh api repos/kumaransg/LLD/readme`.

Table 1 — problems (from the repo's own two tables, "Company Asked" is the source's own column):

| Problem (source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Cricket Match Dashboard | Cricinfo / sports scoreboard | https://github.com/kumaransg/LLD/tree/main/Cricket%20Match%20Dashboard | free | outline; reported as "Udaan Assignment" | — |
| Event Calendar | Meeting scheduler / calendar | https://github.com/kumaransg/LLD/tree/main/Event_calendar_flipkart | free | outline; reported at Flipkart | — |
| FoodKart or food ordering System | Food delivery | https://github.com/kumaransg/LLD/tree/main/FoodKart | free | outline; reported at Flipkart | — |
| Stock Exchange | Stock brokerage | https://github.com/kumaransg/LLD/tree/main/StockExchange | free | outline; reported at Navi | — |
| PropertyHunt or property Listing site | Online shopping (Amazon)-like listing site (new: Property listing site) | https://github.com/kumaransg/LLD/tree/main/PropertyHunt | free | outline; reported at ClearTrip | — |
| ledger company | Bank account system | https://www.geektrust.in/coding-problem/backend/ledger-co | free | outline; reported at Navi (Geektrust OA) | — |
| Leetcode Like platform LLD | Online shopping-like judge platform (new: Coding-judge platform) | https://github.com/kumaransg/LLD/tree/main/leetcode-lld-flipkart-coding-blox | free | outline; reported at Flipkart | — |
| Ride Sharing like App | Ride sharing (Uber) | https://github.com/kumaransg/LLD/tree/main/Ride%20Sharing%20 | free | outline; "frequently asked in all companies" (source's own label) | — |
| Design Lift/Elevator | Elevator system | https://lldcoding.com/design-lld-lift-machine-coding | free (external) | outline; "frequently asked in all companies" | — |
| Design Splitwise | Splitwise / expense sharing | https://lldcoding.com/design-lld-splitwise-application-machine-coding | free (external) | outline; "frequently asked in all companies" | — |
| Design AWS Lambda | Event bus (new: FaaS scheduler) | https://lldcoding.com/design-lld-aws-lambda-machine-coding | free (external) | outline | — |
| Design Newsletter Service | Notification service | https://lldcoding.com/design-lld-newsletter-service-machine-coding | free (external) | outline | — |
| Design Whatsapp | Social network-like chat (new: Chat system) | https://lldcoding.com/design-lld-whatsapp-messenger-machine-coding | free (external) | outline | — |
| Design Event Calender | Meeting scheduler / calendar | https://lldcoding.com/design-lld-event-calendar-machine-coding | free (external) | outline | — |
| Design Zoom | Video conferencing (new canonical name) | https://lldcoding.com/design-lld-a-video-conferencing-application-like-zoom-machine-coding | free (external) | outline | — |
| Design Google Doc | Text editor / undo-redo (collaborative variant) | https://lldcoding.com/design-lld-a-real-time-collaborative-document-editing-platform-like-google-docs-machine-coding | free (external) | outline | — |
| Design Food Delivery App | Food delivery | https://lldcoding.com/design-lld-a-system-for-online-food-ordering-and-delivery-like-zomato-machine-coding | free (external) | outline | — |
| Design Dropbox | In-memory file system (cloud variant) | https://lldcoding.com/design-lld-a-file-sharing-system-like-dropbox-machine-coding | free (external) | outline | — |
| Design Bittorrent | Pub-sub / message broker (P2P variant, new canonical) | https://lldcoding.com/design-lld-a-peer-to-peer-file-sharing-system-like-bittorrent-machine-coding | free (external) | outline | — |
| Design Twitter/X | Social network | https://lldcoding.com/design-lld-twitter-machine-coding | free (external) | outline | — |

Half of this repo's "Frequently asked Problems" table only points to a third-party site
(lldcoding.com) rather than hosting its own solution — recorded as `outline` since the repo page
itself gives no code, and the target site was not independently fetched.

---

## 3. GitHub — jkaus324/machine-coding-interview-questions

URL: https://github.com/jkaus324/machine-coding-interview-questions

Licence / access: repo licence not checked for a LICENSE file (page shows no licence badge); the
repo itself is a free 20-problem pilot of a paid product ("Crack LLD Interviews", ₹1,199,
topmate.io) — the free tier is what is tabulated below.

Authority: Jatin Kaushal, self-described "SDE at Amazon India" per the README byline; explicitly
built to bridge "DSA-only" prep to LLD, with company tags and design-pattern tags per problem —
this repo is also the clearest **frequency/tiering** artefact found for source 5 below (98 stars).

Languages: solutions exist in **C++, Go, Java, Python, and JavaScript**, one `spec.yaml`-driven
test harness per problem, run through `harness/python/runner.py` — confirmed Python.

Fetched: 2026-09-20 via `gh api repos/jkaus324/machine-coding-interview-questions/readme`.

Table 1 — problems (source's own "Companies" column; tier is the source's own Tier 1/Tier 2
label, folded into Depth):

| Problem (source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Payment Method Ranker | (new) Payment method ranker | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/001-payment-ranker | free | code (C++, Go, Java, Python, JS); Tier 1 | — |
| Notification System | Notification service | .../tier1-foundation/003-notification-system | free | code (5 langs incl. Python); Tier 1 | — |
| Vending Machine | (new) Vending machine | .../tier1-foundation/004-vending-machine | free | code (5 langs incl. Python); Tier 1 | — |
| Customer Issue Resolution | (new) Ticketing / issue queue | .../tier1-foundation/005-customer-issue-resolution | free | code (5 langs incl. Python); Tier 1 | — |
| Billing & Discount Engine | Digital wallet (billing variant) | .../tier1-foundation/006-billing-discount-engine | free | code (5 langs incl. Python); Tier 1 | — |
| Order Management System | (new) Order management system | .../tier1-foundation/007-order-management | free | code (5 langs incl. Python); Tier 1 | — |
| File Search System | In-memory file system | .../tier1-foundation/008-file-search-system | free | code (5 langs incl. Python); Tier 1 | — |
| API Rate Limiter | Rate limiter | .../tier1-foundation/011-api-rate-limiter | free | code (5 langs incl. Python); Tier 1 | — |
| Meeting Room Scheduler | Meeting scheduler / calendar | .../tier2-intermediate/009-meeting-room-scheduler | free | code (5 langs incl. Python); Tier 2 | — |
| Ride Surge Pricing Engine | Ride sharing (Uber) | .../tier2-intermediate/010-ride-surge-pricing | free | code (5 langs incl. Python); Tier 2 | — |
| Elevator System | Elevator | .../tier2-intermediate/012-elevator-system | free | code (5 langs incl. Python); Tier 2 | — |
| Parking Lot System | Parking lot | .../tier2-intermediate/013-parking-lot-system | free | code (5 langs incl. Python); Tier 2 | — |
| Splitwise Expense-Sharing | Splitwise / expense sharing | .../tier2-intermediate/014-splitwise | free | code (5 langs incl. Python); Tier 2 | — |
| BookMyShow Ticket Booking | Movie ticket booking (BookMyShow) | .../tier2-intermediate/015-bookmyshow | free | code (5 langs incl. Python); Tier 2 | — |
| Amazon Locker System | Amazon locker | .../tier2-intermediate/016-amazon-locker | free | code (5 langs incl. Python); Tier 2 | — |
| LRU Cache | LRU cache | .../tier2-intermediate/017-lru-cache | free | code (5 langs incl. Python); Tier 2 | — |
| Simplified Twitter | Social network | .../tier2-intermediate/018-simplified-twitter | free | code (5 langs incl. Python); Tier 2 | — |
| Online Auction System | (new) Online auction system | .../tier2-intermediate/019-online-auction | free | code (5 langs incl. Python); Tier 2 | — |
| Logger System | Logger / logging framework | .../tier2-intermediate/020-logger-system | free | code (5 langs incl. Python); Tier 2 | — |
| Ride-Sharing Application | Ride sharing (Uber) | .../tier2-intermediate/021-ride-sharing | free | code (5 langs incl. Python); Tier 2 | — |

Company tags recorded by the source, per problem (its "Companies" column, reproduced verbatim
for the frequency analysis in Part A §5 / Notes): Payment Method Ranker — Amazon, Flipkart;
Notification System — Flipkart, Swiggy; Vending Machine — Amazon, Flipkart; Customer Issue
Resolution — PhonePe, Flipkart; Billing & Discount Engine — Flipkart, Amazon, Meesho; Order
Management System — Meesho, PhonePe, Amazon; File Search System — Amazon, Microsoft; API Rate
Limiter — Amazon, Razorpay, Uber; Meeting Room Scheduler — Flipkart, Razorpay, Groww; Ride Surge
Pricing Engine — Uber, Ola; Elevator System — Adobe; Parking Lot System — Salesforce; Splitwise —
ShareChat, Razorpay, Flipkart, Paytm; BookMyShow — DoorDash, BookMyShow, Swiggy, Paytm; Amazon
Locker System — Amazon; LRU Cache — Kutumb; Simplified Twitter — AngelOne; Online Auction System —
Flipkart; Logger System — Amazon; Ride-Sharing Application — Flipkart.

---

## 4. GitHub — prsnt558908/CodeZymSolutions (mirrors codezym.com)

URL: https://github.com/prsnt558908/CodeZymSolutions ; problem statements themselves live at
https://codezym.com/ (a JS-rendered app — WebFetch could not read it directly, see Notes; the
GitHub repo mirrors the same author's dated per-company blog posts as plain Markdown, which is
what was actually read).

Licence / access: no LICENSE file (GitHub reports none) — free to read on GitHub; codezym.com
itself sells structured practice.

Authority: Prashant Priyadarshi (byline in the company files: "book LLD Mock Interview with me:
https://topmate.io/prashant_priyadarshi"), running codezym.com; the repo's
`0-company-wise-interview-questions/2026/` folder is explicitly **dated per company per year**
(e.g. `11-amazon-lld-sep-2026.md`) and states its questions are "built ... from recent interview
experiences of candidates" — this is the strongest genuinely-dated, company-attributed source
found.

Languages: repo has `q-java-tutorial.md` and `q-python-tutorial.md`, and individual problem
folders contain both, e.g. `1-100/q01_parking_lot/` has
`1_python_simple_solution/`, `q01_default_code_1_python`, and Java files alongside — confirmed
Python.

Fetched: 2026-09-20 via `gh api` (repo contents + file contents, base64-decoded). codezym.com
itself returned only its static shell via WebFetch (client-rendered; the problem list did not
appear) — noted as a failed fetch, worked around via the GitHub mirror.

Table 1 — problems (company-wise files, "2026" folder; each file is the source's own
company/year write-up):

| Problem (source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design Unix "find" command for file search | In-memory file system | https://codezym.com/question/14-design-unix-find-command-file-search | free | outline; reported at Amazon, Sep 2026 | — |
| Design Unix "find" command — boolean predicates | In-memory file system | https://codezym.com/question/15-design-unix-find-command-boolean-predicates | free | outline; reported at Amazon, Sep 2026 | — |
| Design a Parking Lot | Parking lot | https://codezym.com/question/7-design-a-parking-lot | free | code (Java, Python; see repo `q01_parking_lot`) | — |
| Design Ride-Hailing System Like Uber, Ola | Ride sharing (Uber) | https://codezym.com/question/458-ride-hailing-system-like-uber | free | outline; reported at Amazon, Sep 2026 | — |
| Design LRU Cache With Time Constraint | Cache with TTL | https://codezym.com/question/165-design-lru-cache-time-constraint | free | outline; reported at Amazon, Sep 2026 | — |
| Design Cron Job Scheduler | Job scheduler | https://codezym.com/question/456-cron-job-scheduler | free | outline; reported at Amazon, Sep 2026 | — |
| LRU Cache (leetcode-style, but treated as LLD/DSA crossover) | LRU cache | https://leetcode.com/problems/lru-cache/description/ | free | outline; reported at Microsoft and Salesforce and Walmart, 2026 | — |
| LFU Cache | LFU cache | https://leetcode.com/problems/lfu-cache/description/ | free | outline; reported at Salesforce and Walmart, 2026 | — |
| Design Splitwise | Splitwise / expense sharing | https://github.com/prsnt558908/CodeZymSolutions/tree/main/1-100/q12_expense_sharing_splitwise | free | code (per repo folder) | — |
| Design Trello | (new) Kanban board (Trello-like) | https://codezym.com/lld/microsoft | free | outline; reported at Amazon, Sep 2026 | — |
| Design an In-Memory Key-Value Store | In-memory key-value store | https://codezym.com/lld/amazon | free | outline; reported at Amazon (SDE II/III), Sep 2026 | — |
| Design a Distributed Queue (Kafka) | Pub-sub / message broker | https://codezym.com/lld/amazon | free | outline; reported at Amazon (SDE II/III), Sep 2026 | — |
| Chess Game / Chess Validator | Chess | https://github.com/prsnt558908/CodeZymSolutions/tree/main/1-100/q08_chess_game | free | code (per repo folder) | — |
| Text Editor LLD | Text editor / undo-redo | https://github.com/prsnt558908/CodeZymSolutions/tree/main/1-100/q09_text_editor_lld | free | code (per repo folder) | — |
| Movie Booking App | Movie ticket booking (BookMyShow) | https://github.com/prsnt558908/CodeZymSolutions/tree/main/1-100/q10_movie_booking_app | free | code (per repo folder) | — |
| Elevator System (simple) | Elevator system | https://github.com/prsnt558908/CodeZymSolutions/tree/main/1-100/q11_elevator_system_simple | free | code (per repo folder) | — |

Company-round notes recorded verbatim (useful for the concept side, not just problem titles):

- **Microsoft, 2026**: "Microsoft has introduced an AI-assisted Low Level Design round" — a
  three-phase pair-programming round: architect the system, prompt an AI model (ChatGPT/Gemini)
  to generate the implementation, then critically audit the AI-generated output; run for SDE-2+;
  DSA-flavoured LLD favourites are LRU cache, Tic-Tac-Toe, Google-Search-autocomplete; expect
  concurrency questions (`synchronized` in Java) on caches and config-management services.
- **Salesforce, 2026**: pub-sub/Kafka/Observer-pattern LLD is frequent; LRU/LFU cache common;
  interviewers deliberately under-specify requirements to test clarifying questions; the same
  "bounded resource" pattern (connection pool / job scheduler) recurs; may escalate into HLD
  (concurrency across a central DB); separate round of C++/OOP short-answer questions (private
  constructors, abstraction vs encapsulation, destructor/memory-leak questions).
- **Walmart, 2026**: ticket-booking apps with DB schema discussion (e.g. BookMyShow), cache
  implementation, and payment systems dominate; expects discussion of optimistic vs pessimistic
  locking and SQL isolation levels; Strategy and Observer are the two patterns interviewers probe
  deepest; LLD round may segue into a basic HLD discussion for Software Engineer III; Java
  preferred but not mandated; Spring Boot questions can appear alongside LLD.

---

## 5. GitHub — abhaypaswan/lld-python (Python-only)

URL: https://github.com/abhaypaswan/lld-python

Licence / access: **MIT** (confirmed via `gh api repos/.../license`); free to read.

Authority: individual author (abhaypaswan); backs the LLD track of a companion site,
goatengineer.com; 40 stars — smaller than the Java-first repos above but the only repo found in
this survey whose solutions are **Python-only, standard-library-only, and pytest-verified** for
every problem (`python3 -m pytest problems/<slug>`), each with a runnable `src/main.py`, a
mermaid class diagram, and a rationale write-up.

Languages: **Python only**, explicitly "only the standard library" by design rule ("If a problem
looks like it needs a dependency, that is usually a sign the design is doing something the
problem did not ask for").

Fetched: 2026-09-20 via `gh api repos/abhaypaswan/lld-python/readme`.

Table 1 — problems (source's own table: `#`, difficulty emoji, design patterns, time budget):

| Problem (source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design Tic Tac Toe | Tic-tac-toe | https://github.com/abhaypaswan/lld-python/tree/main/problems/tic-tac-toe | free | code (Python) | easy (40 min) |
| Snake and Ladder | Snake and ladder | .../problems/snake-and-ladder | free | code (Python) | easy (45 min) |
| Design Splitwise | Splitwise / expense sharing | .../problems/splitwise | free | code (Python) | medium (60 min) |
| Design a Chat Room | (new) Chat room | .../problems/chat-room | free | code (Python) | medium (50 min) |
| Design a Logging Framework | Logger / logging framework | .../problems/logging-framework | free | code (Python) | medium (45 min) |
| Design a Notification Service | Notification service | .../problems/notification-service | free | code (Python) | medium (55 min) |
| Design a Parking Lot | Parking lot | .../problems/parking-lot | free | code (Python) | medium (60 min) |
| Design a Rate Limiter | Rate limiter | .../problems/rate-limiter | free | code (Python) | medium (50 min) |
| Design a Text Editor with Undo | Text editor / undo-redo | .../problems/text-editor | free | code (Python) | medium (55 min) |
| Design a Vending Machine | (new) Vending machine | .../problems/vending-machine | free | code (Python) | medium (50 min) |
| Design an ATM | ATM | .../problems/atm | free | code (Python) | medium (60 min) |
| Design an In-Memory File System | In-memory file system | .../problems/file-system | free | code (Python) | medium (55 min) |
| Design an LRU Cache | LRU cache | .../problems/lru-cache | free | code (Python) | medium (45 min) |
| Design Chess | Chess | .../problems/chess | free | code (Python) | hard (90 min) |
| Design a Movie Ticket Booking System | Movie ticket booking (BookMyShow) | .../problems/movie-ticket-booking | free | code (Python) | hard (80 min) |
| Design a Payment Gateway | Digital wallet (payment variant) | .../problems/payment-gateway | free | code (Python) | hard (70 min) |
| Design an Elevator System | Elevator system | .../problems/elevator-system | free | code (Python) | hard (75 min) |

Design-pattern tags recorded by the source per problem: Tic-Tac-Toe (Strategy, Observer); Snake
and Ladder (Strategy); Splitwise (Strategy, Observer); Chat Room (Mediator, Observer, Facade);
Logging Framework (Chain of Responsibility, Strategy, Singleton); Notification Service (Decorator,
Observer, Factory Method, Strategy); Parking Lot (Strategy, Factory Method, Command, Facade); Rate
Limiter (Strategy); Text Editor (Command, Memento, Composite, Facade); Vending Machine (State);
ATM (State, Chain of Responsibility); File System (Composite, Visitor, Iterator, Facade); LRU
Cache (Strategy, Template Method); Chess (Strategy, Command, Template Method, Observer); Movie
Ticket Booking (Builder, Repository, Proxy, Strategy, Facade); Payment Gateway (Adapter, Abstract
Factory, Strategy, Facade); Elevator System (Strategy, State, Observer).

---

## 6. workat.tech — Machine Coding Round practice platform

URL: https://workat.tech/machine-coding (landing/hub page); individual problems at
`https://workat.tech/machine-coding/practice/<slug>`, e.g.
https://workat.tech/machine-coding/practice/splitwise-problem-0kp2yneec2q2 and
https://workat.tech/machine-coding/practice/design-parking-lot-qm6hwq4wkhp8.

Licence / access: proprietary; problem statements are free to read, worked solutions are behind
a paid plan (neither fetched page showed code).

Authority: workat.tech is an India-focused interview-prep platform; its machine-coding hub
explicitly frames the round by company — "Flipkart, Uber, Swiggy, Udaan, Gojek, Amazon,
Microsoft, Google, Adobe, Facebook" are the companies named on the hub page as running this round
— and its own `SDE I` / `SDE I/II` / `SDE II` labels are used as the source's difficulty scale by
other repos that link to it (e.g. lavakumarThatisetti/Machine-Coding-Round, §2 above, links
directly to workat.tech problem-statement URLs for its own solutions).

Languages: no code shown on the two problem pages fetched (statement + I/O examples only).

Fetched: 2026-09-20 via WebFetch, two levels: the hub page (`/machine-coding`) and two individual
practice pages reached via slugs discovered from an external GitHub repo's links (direct guesses
at `/machine-coding/practice`, `/machine-coding/tutorial/...` and a `codesignal.com` counterpart
URL both 404'd — workat.tech's real URLs carry an opaque slug suffix, e.g. `-0kp2yneec2q2`, not
guessable from the title alone).

Table 1 — problems:

| Problem (source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| How to design Splitwise? | Splitwise / expense sharing | https://workat.tech/machine-coding/practice/splitwise-problem-0kp2yneec2q2 | paywalled (statement free) | outline (three split types: EQUAL, EXACT, PERCENT; 1.5 h budget stated on page) | SDE I/II |
| Design a Parking Lot | Parking lot | https://workat.tech/machine-coding/practice/design-parking-lot-qm6hwq4wkhp8 | paywalled (statement free) | outline (multi-floor, multiple vehicle types, CLI I/O format) | SDE I/II |
| How to design Snake and Ladder? | Snake and ladder | https://workat.tech/machine-coding/practice/snake-and-ladder-problem-zgtac9lxwntg | paywalled (statement free) | outline | — |
| Trello problem | (new) Kanban board (Trello-like) | https://workat.tech/machine-coding/practice/trello-problem-t0nwwqt61buz | paywalled (statement free) | outline | — |
| Design Tic-Tac-Toe | Tic-tac-toe | https://workat.tech/machine-coding/practice/design-tic-tac-toe-smyfi9x064ry | paywalled (statement free) | outline | — |

(The last three rows above were located only as URLs — linked from the
lavakumarThatisetti/Machine-Coding-Round README, §2 — not independently WebFetched for content;
recorded at `outline` on the strength of the two pages that were actually fetched, which share the
identical format.)

---

## 7. CodeSignal "Industry Coding Assessment" / "Industry Coding Framework" (ICF)

URL: no live page on codesignal.com describes this by name any more as of 2026-09-20 (see Notes —
several direct and guessed URLs 404'd, and the current site groups it under "Technical
Assessments" as one of several "Assessment" products, with only the name "Industry Coding
Assessment" surfacing, via `codesignal.com/technical-assessments/`, linking to an
authenticated-only instance at `app.codesignal.com/explore-assessments/BCeD5qaPgZDudLhXQ` that
WebFetch could not read). What was actually read: a public GitHub mock/practice repo and a named
author's blog post about the format, both independent of CodeSignal's own marketing copy.

- Mock/practice repo: https://github.com/PaulLockett/CodeSignal_Practice_Industry_Coding_Framework
- Named write-up: https://yanirseroussi.com/2023/05/26/how-hackable-are-automated-coding-assessments/

Licence / access: the PaulLockett repo has no LICENSE file (GitHub reports none), free to read;
Yanir Seroussi's blog post is free to read.

Authority: PaulLockett's repo (421 stars) explicitly reproduces the structure of CodeSignal's
real assessment (its own README says: "It's important to highlight the rarity of comprehensive
guides or examples on navigating these types of assessments") and includes a PDF titled "CodeSignal
Skills Evaluation Framework.pdf" plus a worked `file_storage` practice level. Yanir Seroussi
(self-described AI/ML "Success Architect", cited by the PaulLockett repo as the source of the
level-timing table) actually sat the real CodeSignal assessment and wrote a critique — he notes he
"agreed not to share the content of the assessment", so his post has no problem text, only the
structure and a critique.

Languages: the PaulLockett repo's harness is Python (`simulation.py` / `test_simulation.py`,
targets **Python 3.10.6**, "the version CodeSignal utilizes for its assessments" per the README);
its one public practice level is `practice_assessments/file_storage/`.

Fetched: 2026-09-20. Failed fetches, in order tried: `codesignal.com/industry-coding-framework/`
(404), `codesignal.com/blog/industry-coding-framework/` (404), `codesignal.com/blog/…/` variants
(404), `support.codesignal.com` article guess (403) and search (403), `codesignal.com/general-coding-assessment/`
(404), `codesignal.com/products/industry-coding-assessment/` (404),
`app.codesignal.com/explore-assessments/...` (returned only a bare "CodeSignal" header, no body —
likely requires login). Fell back to a Bing HTML search (`bing.com/search?q=...`), which for the
CodeSignal query returned real, on-topic results (a Reddit thread, an `interviewfox.ai` and a
`lodely.com` page — both excluded per this survey's "no AI content farm" rule) that led to the
correct term "Industry Coding Assessment"; a second Bing query (for workat.tech) returned garbage
(a page of unrelated Chinese chemical-reagent sites) and was discarded — recorded here so the
failure mode is visible, not silently dropped.

Table 1 — problem *types* (the framework's own scenario families, from the PaulLockett repo's
directory structure and README; this is a framework of levelled scenarios, not fixed single
problems, so canonical names are approximate):

| Problem (source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| File Storage (practice level, 4 sub-levels) | In-memory file system | https://github.com/PaulLockett/CodeSignal_Practice_Industry_Coding_Framework/tree/main/practice_assessments/file_storage | free | code (Python); 4 levels, each adding requirements to `simulation.py` | Level 1: 10-15 min, Level 2: 20-30 min, Level 3 & 4: 30-60 min each |

The task's own stated (but not-independently-verified, per Seroussi's NDA note) other scenario
families — **in-memory database, banking system, task management, cloud storage** — were named in
this survey's own task instructions and by community discussion, but were not directly observed
in either fetched source; only `file_storage` was confirmed as a real, public practice scenario.
Recorded as a gap rather than invented.

Level-timing table (source: PaulLockett's README, itself citing Yanir Seroussi):

| Level | Expected time | Cumulative |
|---|---|---|
| 1 | 10–15 min | |
| 2 | 20–30 min | |
| 3 | 30–60 min | |
| 4 | 30–60 min | 90–165 min total, but the candidate is given only 90 minutes — Seroussi calls this gap intentional: CodeSignal accepts partial completion because "candidate willingness to engage with the assessment drops significantly for tests exceeding 2 hours." |

Seroussi's critique (for the concept-skeleton / methodology side, not a problem row): the format
is "hackable" because "making speed a key factor in test success" rewards test-specific practice
over engineering judgement; no partial credit for good design that doesn't pass the automated
tests in time; doesn't simulate real refactoring (days/weeks vs minutes).

---

## 8. Tiering evidence (Part A §5) — no single named-author sighting-count source found

No source was found that publishes an explicit *count* of how many times each LLD problem was
reported (the equivalent of a LeetCode-company-tag frequency table, but for LLD). The closest
credible, named-author signals, all already tabulated above, are:

- **jkaus324/machine-coding-interview-questions** (§3): explicit Tier 1 ("Foundation") / Tier 2
  ("Intermediate") labelling by a named author with a stated company source per problem, and a
  claim of "105 machine coding + LLD problems ... pulled from real interviews" in the paid
  product this repo previews (unverified — the free tier only exposes 20).
- **prsnt558908 / codezym.com** (§4): per-company, per-year write-ups (dated 2026) that
  explicitly say problems are drawn from "recent interview experiences of candidates" — the
  repeat appearance of LRU cache, LFU cache, and Observer-pattern pub/sub across the Salesforce,
  Walmart, and Microsoft 2026 files is the closest thing to a cross-company frequency signal
  actually observed.
- **abhaypaswan/lld-python** (§5) tags each problem with a fixed time budget and an
  easy/medium/hard label but not a frequency count.
- **Exponent** (§1) sorts by recency ("N months/years ago") and shows how many companies a
  question is tagged with (e.g. "+26 more", "+63 more") — the closest thing to a numeric signal
  on that site, though it mixes plain DSA and LLD-shaped questions in one list.

Consistent with the sightings above, the problems that recur across the *most* independent
sources in this survey are, in descending order of how many of sections 1–7 mention them: **LRU
cache** (5 of 7 sources), **Splitwise / expense sharing** (5 of 7), **Parking lot** (4 of 7),
**Elevator system** (4 of 7), **Rate limiter / API rate limiter** (3 of 7), **In-memory file
system** (3 of 7), **Movie ticket booking (BookMyShow)** (3 of 7), **LFU cache** (2 of 7).

---

# Part B — Python-specific design material

## 9. python-patterns.guide (Brandon Rhodes)

URL: https://python-patterns.guide/

Licence / access: © 2018–2020 Brandon Rhodes; no explicit open licence statement seen on the
fetched page; free to read.

Authority: Brandon Rhodes — long-time CPython core developer and PyCon speaker; this is a
personal reference site, not a company product.

Languages: Python (the entire site is about idiomatic Python pattern implementations).

Fetched: 2026-09-20 via WebFetch of the site root.

Table 2 — outline:

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Gang of Four: Principles | The Composition Over Inheritance Principle | https://python-patterns.guide/ |
| Python-Specific Patterns | The Global Object Pattern; The Prebound Method Pattern; The Sentinel Object Pattern | https://python-patterns.guide/ |
| Gang of Four: Creational Patterns | The Abstract Factory Pattern; The Builder Pattern; The Factory Method Pattern; The Prototype Pattern; The Singleton Pattern | https://python-patterns.guide/ |
| Gang of Four: Structural Patterns | The Composite Pattern; The Decorator Pattern; The Flyweight Pattern | https://python-patterns.guide/ |
| Gang of Four: Behavioral Patterns | The Iterator Pattern | https://python-patterns.guide/ |
| Bibliography | Gang of Four book; *Refactoring* by Martin Fowler | https://python-patterns.guide/ |

Note: the site's own "Python-Specific Patterns" section (3 patterns: Global Object, Prebound
Method, Sentinel Object) is the material an LLD-in-Python answer should reach for that a
Java/C++-oriented LLD guide would never mention.

---

## 10. Architecture Patterns with Python / "Cosmic Python" (Percival & Gregory)

URL: https://www.cosmicpython.com/book/preface.html

Licence / access: Creative Commons **CC BY-NC-ND** (attribution, non-commercial, no derivatives);
free to read online; also sold as a print/ebook by O'Reilly.

Authority: Harry Percival and Bob Gregory, written out of MADE.com's engineering practice;
widely cited as the practitioner-facing companion to Fowler's *Patterns of Enterprise Application
Architecture*, scoped to Python.

Languages: Python throughout (Flask, SQLAlchemy, Django examples in the appendices).

Fetched: 2026-09-20 via WebFetch of the preface page (table of contents).

Table 2 — outline:

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Front Matter | Preface; Introduction | https://www.cosmicpython.com/book/preface.html |
| Part 1 — Building an Architecture to Support Domain Modeling | 1. Domain Modeling; 2. Repository Pattern; 3. A Brief Interlude: On Coupling and Abstractions; 4. Our First Use Case: Flask API and Service Layer; 5. TDD in High Gear and Low Gear; 6. Unit of Work Pattern; 7. Aggregates and Consistency Boundaries | https://www.cosmicpython.com/book/preface.html |
| Part 2 — Event-Driven Architecture | 8. Events and the Message Bus; 9. Going to Town on the Message Bus; 10. Commands and Command Handler; 11. Event-Driven Architecture: Using Events to Integrate Microservices; 12. Command-Query Responsibility Segregation (CQRS); 13. Dependency Injection (and Bootstrapping) | https://www.cosmicpython.com/book/preface.html |
| Back Matter | Epilogue: How to Get There from Here; Appendix A: Summary Diagram and Table; Appendix B: A Template Project Structure; Appendix C: Swapping Out the Infrastructure: Do Everything with CSVs; Appendix D: Repository and Unit of Work Patterns with Django; Appendix E: Validation | https://www.cosmicpython.com/book/preface.html |

Note: this book's centre of gravity is application/service architecture (repository, unit-of-work,
message bus), one level above class-design LLD — most directly relevant to the *Dependency
injection container* and *Event bus / Pub-sub* canonical leaves, and to "why the design looks
this way" narrative for any LLD answer that separates domain objects from persistence.

---

## 11. Fluent Python, 2nd edition (Luciano Ramalho)

URL: https://github.com/fluentpython/example-code-2e (author's own example-code repo; book itself
is the O'Reilly 2022 print/ebook, paywalled)

Licence / access: the example-code repo is **MIT**; the book text itself is a paid O'Reilly title
(not open-access) — the table of contents below was read from the free repo, not the paywalled
book text.

Authority: Luciano Ramalho, the book's sole author, a well-known figure in the Python community
(co-founded Garoa Hacker Clube, PSF fellow); Fluent Python is one of the most-cited intermediate/
advanced Python references.

Languages: Python (the whole book).

Fetched: 2026-09-20 via `gh api repos/fluentpython/example-code-2e/readme`.

Table 2 — outline (source's own part/chapter numbering; "1st ed. ch #" column omitted here, 🆕
marks chapters new to the 2nd edition):

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Part I — Data Structures | 1 The Python Data Model; 2 An Array of Sequences; 3 Dictionaries and Sets; 4 Unicode Text versus Bytes; 5 Data Class Builders 🆕; 6 Object References, Mutability, and Recycling | https://github.com/fluentpython/example-code-2e |
| Part II — Functions as Objects | 7 Functions as First-Class Objects; 8 Type Hints in Functions 🆕; 9 Decorators and Closures; 10 Design Patterns with First-Class Functions | https://github.com/fluentpython/example-code-2e |
| Part III — Object-Oriented Idioms | 11 A Pythonic Object; 12 Special Methods for Sequences; 13 Interfaces, Protocols, and ABCs; 14 Inheritance: For Better or For Worse; 15 More About Type Hints 🆕; 16 Operator Overloading | https://github.com/fluentpython/example-code-2e |
| Part IV — Control Flow | 17 Iterators, Generators, and Classic Coroutines; 18 with, match, and else Blocks; 19 Concurrency Models in Python 🆕; 20 Concurrent Executors; 21 Asynchronous Programming | https://github.com/fluentpython/example-code-2e |
| Part V — Metaprogramming | 22 Dynamic Attributes and Properties; 23 Attribute Descriptors; 24 Class Metaprogramming | https://github.com/fluentpython/example-code-2e |

Note: Part III (chapters 11–16, especially "13 Interfaces, Protocols, and ABCs" and "14
Inheritance: For Better or For Worse") is the direct match to the LLD round's core
question — "how do I express an interface / a class hierarchy in Python" — and is a stronger,
more opinionated source on that specific question than either python-patterns.guide or Cosmic
Python.

---

## 12. Official Python documentation

URL prefix: https://docs.python.org/3/library/

Licence / access: PSF licence for the documentation; free to read.

Authority: the canonical reference; every fact below is the page's own text.

Languages: Python (the standard library itself).

Fetched: 2026-09-20, one WebFetch per page below.

| Page | 2–3 facilities an LLD answer actually reaches for |
|---|---|
| [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) | `@dataclass` (auto `__init__`/`__repr__`/`__eq__`; `frozen=True` for immutable value objects; `slots=True`); `field(default_factory=...)` for mutable defaults (e.g. a list-valued attribute); `__post_init__` for derived/validated fields. |
| [`abc`](https://docs.python.org/3/library/abc.html) | `ABC` / `ABCMeta` + `@abstractmethod` to define an interface that cannot be instantiated until implemented (the direct Python analogue of a Java `interface`); `register()` for declaring a virtual subclass without inheritance; `__subclasshook__` for structural/duck-typed `isinstance` checks. |
| [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) | `Protocol` itself for structural (static duck-typing) interfaces that need no explicit inheritance; `@runtime_checkable` to allow `isinstance()`/`issubclass()` against a Protocol (structural only — it does not check signatures); generic protocols (`class GenProto[T](Protocol)`). |
| [`enum`](https://docs.python.org/3/library/enum.html) | `Enum` for closed sets of named constants (state-machine states, order/ticket status); `Flag`/`IntFlag` with bitwise `|`/`&` for combinable capability/permission sets; `auto()` to avoid hand-assigning values. |
| [`functools`](https://docs.python.org/3/library/functools.html) | `@lru_cache` (memoisation — the standard-library answer to "design an LRU cache" as a decorator, and a natural citation inside a hand-rolled LRU-cache answer); `@cached_property` (compute-once instance attribute); `@singledispatch` (type-based dispatch as an alternative to a class hierarchy). |
| [`contextlib`](https://docs.python.org/3/library/contextlib.html) | `@contextmanager` (turn a generator into a resource-acquire/release pair without writing `__enter__`/`__exit__`); `ExitStack` (dynamic/variable-count resource management, e.g. "open N files, close all on any failure"); `ContextDecorator` (one implementation usable both as `with` and as a decorator). |
| [`threading`](https://docs.python.org/3/library/threading.html) | `Lock` (`acquire`/`release`, mutual exclusion on shared state — e.g. a parking-lot spot map); `Condition` (`wait_for`, `notify_all` — producer/consumer, bounded-blocking-queue designs); `Semaphore`/`BoundedSemaphore` (fixed-size resource pool, e.g. a connection pool). |
| [`queue`](https://docs.python.org/3/library/queue.html) | `Queue` / `LifoQueue` / `PriorityQueue` (FIFO, stack, and priority orderings, thread-safe by construction); `maxsize` (bounded-blocking-queue behaviour "insertion blocks once full"); `task_done()`/`join()` (tracking in-flight work for a worker-pool shutdown). |
| [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) | `ThreadPoolExecutor`/`ProcessPoolExecutor` with `submit()`/`map()` (the standard-library answer to "design a thread pool"); `Future.result()`/`.cancel()`; `as_completed()`/`wait(..., return_when=...)` for collecting results as they finish. |
| [`asyncio`](https://docs.python.org/3/library/asyncio.html) | via its own sub-pages: [asyncio-task](https://docs.python.org/3/library/asyncio-task.html) (`Task`, `create_task()`, `gather()`); [asyncio-sync](https://docs.python.org/3/library/asyncio-sync.html) (`Lock`, `Event`, `Condition`, `Semaphore` — async equivalents of `threading`'s primitives); [asyncio-queue](https://docs.python.org/3/library/asyncio-queue.html) (`Queue`/`LifoQueue`/`PriorityQueue` for async producer/consumer). |

---

## 13. Raymond Hettinger and Hynek Schlawack on Pythonic class design

### Hynek Schlawack — "Subclassing in Python Redux"

URL: https://hynek.me/articles/python-subclassing-redux/

Licence / access: personal blog post, free to read.

Authority: Hynek Schlawack — creator of `attrs` and `structlog`, CPython/PyPA-adjacent, a
frequently-cited voice on Python class design.

Languages: Python.

Fetched: 2026-09-20 via WebFetch, dated 22 June 2021 on the page.

Key content (for the concept skeleton, not a Table 2 subject-outline — this is a single
argumentative post): identifies three kinds of inheritance in Python and argues they should never
be mixed — **avoid subclassing for code reuse** ("subclass explosion", muddied namespaces,
confusing indirection: "don't make it a central part of your design"); **prefer structural typing**
(`typing.Protocol`) **over nominal typing** (ABCs) for interface-shaped problems; **reserve
subclassing for genuine is-a specialisation** where a subtype is strictly "the base class plus
more" with no behavioural mixing-in. Direct quotes captured: "Python is designed in a way that you
can't write idiomatic code without subclassing sometimes"; "code is much more often read than
written, avoid subclassing in general."

### Hynek Schlawack — "Why not…" (attrs documentation, `why.html`)

URL: https://www.attrs.org/en/stable/why.html

Licence / access: MIT-licensed project documentation, free to read.

Authority: same author, as the `attrs` project's own maintainer-written rationale page.

Languages: Python.

Fetched: 2026-09-20 via WebFetch.

Key content: argues `attrs` removes the boilerplate of hand-written `__init__`/`__repr__`/
`__eq__`/`__hash__` ("quite a mouthful" and typo-prone by hand); positions itself as a superset of
`dataclasses` — dataclasses "solved the namedtuple problem" but deliberately omit validators,
converters and fine-grained equality/ordering control "for the sake of simplicity", which `attrs`
provides; supports slotted classes with working `super()`. Relevant to LLD answers that need
value objects with validation (e.g. a `Money` type, an `Address`) beyond what `@dataclass` alone
gives.

### Raymond Hettinger — "Beyond PEP 8: Best practices for beautiful, intelligible code" (PyCon 2015)

URL: video exists on YouTube (title confirmed: "Raymond Hettinger - Beyond PEP 8 -- Best practices
for beautiful intelligible code - PyCon 2015"); no transcript or independent write-up was
reachable.

Fetched: 2026-09-20 — **failed fetch, recorded honestly rather than invented**. WebFetch on the
YouTube watch page returned only the page footer/copyright boilerplate (YouTube pages are
JS-rendered and blocked WebFetch from seeing the description or a transcript); a `noembed.com`
oEmbed proxy returned 401; a guessed pyvideo.org URL for the same talk 404'd; a GitHub code search
for a hosted transcript returned zero results. This is the one source-10 item recorded as
unreached rather than summarised — do not treat any secondhand paraphrase of "Beyond PEP 8" that
might appear elsewhere as sourced from this survey.

---

# Notes

**Companies genuinely tied to problems in this survey** (i.e. actually seen attached to a named
LLD problem, not inferred): Amazon (locker system, file search, logger, in-memory KV store,
distributed queue/Kafka, ride-hailing, LRU-with-TTL, cron scheduler, payment-ranker, vending
machine, billing engine — CodeZym Sep-2026 and jkaus324), Flipkart (event calendar, food ordering,
leetcode-like judge platform, notification system, billing engine, order management, meeting
scheduler, Splitwise, auction system, ride-sharing — kumaransg and jkaus324), Microsoft (AI-assisted
LLD round with an audit phase, LRU cache, Tic-Tac-Toe, search-autocomplete, file search — CodeZym
2026), Salesforce (parking lot, LRU/LFU cache, pub-sub/Kafka/Observer — CodeZym 2026 and jkaus324),
Walmart (BookMyShow-style ticket booking, LRU/LFU cache — CodeZym 2026), Uber/Ola (ride surge
pricing, ride-hailing — jkaus324, CodeZym, kumaransg), Navi (stock exchange, ledger/Geektrust OA —
kumaransg), ClearTrip (property listing — kumaransg), Udaan (cricket match dashboard — kumaransg),
Swiggy/PhonePe/Razorpay/Meesho/Paytm/ShareChat/Adobe/Groww/DoorDash/BookMyShow/Kutumb/AngelOne
(various, all from jkaus324's per-problem company tags).

**Newly popular-looking**: Microsoft's *AI-assisted* LLD round (architect → prompt an LLM →
critically audit its output) is a 2026-dated format change, not present in any older source found
here — worth a leaf of its own if the domain wants to cover "auditing AI-generated code" as an
LLD-adjacent skill. CodeZym's dated 2026 files across four companies (Amazon, Microsoft,
Salesforce, Walmart) are the only sources in this survey with an explicit year, so "newly popular"
claims above rest entirely on them, not on a longitudinal comparison.

**Python-specific, gathered across Part B**: `typing.Protocol` + `@runtime_checkable` as the
idiomatic alternative to Java-style `interface` + `implements` (Schlawack's explicit argument,
also documented on its own docs.python.org page); `@dataclass`/`attrs` as the alternative to
hand-written value-object boilerplate; `functools.lru_cache`/`cached_property` as a decorator-first
alternative to hand-rolling caching logic; `queue.Queue`/`threading.Condition`/`Semaphore` as the
standard-library building blocks for the concurrency-flavoured LLD problems (bounded blocking
queue, connection pool, thread pool) that recur in the company sources (Salesforce, Walmart,
Microsoft all named concurrency as a discussion topic); `abc.ABC` as the nominal-interface
fallback when Protocol's structural typing isn't wanted. Only two of the Part A GitHub repos are
Python-only end to end: abhaypaswan/lld-python (§5) and jkaus324's five-language repo (§3) which
includes Python as one of five; the rest are Java-first with Python as a secondary or absent
language.

**How sources rank/tier problems**: no source publishes hard sighting counts (see §8/Part A §5
above for the full discussion); the best available signals are jkaus324's Tier 1/Tier 2 labels,
codezym.com's per-company-per-year write-ups, and Exponent's "+N more companies" tag count.

**Sources this survey could not reach, and what was tried instead** (see also the inline "Fetched"
notes above for exact failed URLs): this session's WebSearch budget was already exhausted (200/200
calls used before this task started, apparently shared session-wide), so after the first two
WebSearch calls at the very start (both returned early results before the cutoff) all further
lookups had to go through WebFetch of guessed/known URLs, `gh` CLI (GitHub search + content APIs),
and two ad-hoc HTML search-engine fetches (DuckDuckGo — blocked by a CAPTCHA both times; Bing —
worked once, for "codesignal industry coding framework", and returned garbage once, for "workat.tech
splitwise"). This means: (a) Atlassian's "code design round" and Amazon's OOD round were not
independently verified from a first-person write-up or the company's own careers page — an
Atlassian careers-culture URL 404'd, a Medium post 403'd (bot-blocked, consistent with the task's
own warning); (b) GeeksForGeeks interview-experience pages for Flipkart's and Uber's machine-coding
format were guessed at two URLs, both 404 — GfG's real URLs were not discovered; (c) CodeSignal's
own marketing page for the "Industry Coding Framework"/"Industry Coding Assessment" could not be
found live on codesignal.com as of 2026-09-20 (nine distinct URL guesses across two batches, all
404/403) — the framework is now findable only through third parties (PaulLockett's mock repo,
Yanir Seroussi's blog post) and a login-gated `app.codesignal.com` link, suggesting CodeSignal has
either renamed, de-emphasised, or paywalled its own explainer since the framework's older
public documentation (which the community sources still cite) was written; (d) codezym.com itself
is JS-rendered and unreadable by WebFetch — worked around via its GitHub markdown mirror, which is
maintained by the same author and appears to be the source of truth for the blog anyway; (e) the
Raymond Hettinger "Beyond PEP 8" talk (§13) has no transcript reachable by this survey — recorded
as an explicit gap rather than paraphrased from memory.
