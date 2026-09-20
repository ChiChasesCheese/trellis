# LLD survey — curated GitHub repositories

Source type: curated GitHub repositories on low-level design / OOD / machine coding interviews,
and on design patterns in Python. Found via `gh api search/repositories` (queries: "low level
design interview", "object oriented design interview", "python design patterns"; "machine coding"
and "LLD python" as literal-string GitHub searches returned mostly unrelated repos — machine-code
compilers and LLDB debugger scripts — so candidates from those two queries were cross-checked
individually instead of trusted as a ranked list). 10 repositories covered.

## ashishps1/awesome-low-level-design

URL: https://github.com/ashishps1/awesome-low-level-design
Licence / access: GPL-3.0 (repo's own LICENSE file, GNU GPL v3)
Authority: maintained by Ashish Pratap Singh (AlgoMaster.io); 26.9k stars, the highest-starred
repo in this survey; backs a paid "Master LLD Interviews" course but the repo content is free.
Languages: solutions exist in Python, Java, C++, C#, Go and TypeScript under `solutions/<lang>/`;
**Python solutions confirmed** at `solutions/python/<problem>/` for 35 problems (one folder per
problem, several files each, e.g. `solutions/python/parkinglot/parking_lot.py`).
Fetched: 2026-09-20, via `gh api repos/.../readme` and `git/trees/HEAD?recursive=1`. No fetch
failures.

**Table 1 — problems** (README's own Easy/Medium/Hard tiers; every row below also has a Python
folder under `solutions/python/`, confirmed against the repo tree)

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design Parking Lot | Parking lot | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/parking-lot.md | free | code (Python, Java, C++, C#, Go, TypeScript) | easy |
| Design Stack Overflow | Stack Overflow | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/stack-overflow.md | free | code | easy |
| Design a Vending Machine | Vending machine | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/vending-machine.md | free | code | easy |
| Design Logging Framework | Logger / logging framework | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/logging-framework.md | free | code | easy |
| Design Traffic Signal Control System | Traffic signal | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/traffic-signal.md | free | code | easy |
| Design Coffee Vending Machine | Coffee machine | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/coffee-vending-machine.md | free | code | easy |
| Design a Task Management System | Task scheduler | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/task-management-system.md | free | code | easy |
| Design ATM | ATM | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/atm.md | free | code | medium |
| Design LinkedIn | LinkedIn | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/linkedin.md | free | code | medium |
| Design LRU Cache | LRU cache | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/lru-cache.md | free | code | medium |
| Design Tic Tac Toe Game | Tic-tac-toe | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/tic-tac-toe.md | free | code | medium |
| Design Pub Sub System | Pub-sub / message broker | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/pub-sub-system.md | free | code | medium |
| Design an Elevator System | Elevator system | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/elevator-system.md | free | code | medium |
| Design Car Rental System | Car rental | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/car-rental-system.md | free | code | medium |
| Design an Online Auction System | Online auction | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-auction-system.md | free | code | medium |
| Design Hotel Management System | Hotel booking | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/hotel-management-system.md | free | code | medium |
| Design a Digital Wallet Service | Digital wallet | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/digital-wallet-service.md | free | code | medium |
| Design Airline Management System | Airline management | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/airline-management-system.md | free | code | medium |
| Design a Library Management System | Library management | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/library-management-system.md | free | code | medium |
| Design a Social Network like Facebook | Social network | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/social-networking-service.md | free | code | medium |
| Design Restaurant Management System | Restaurant management | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/restaurant-management-system.md | free | code | medium |
| Design a Concert Ticket Booking System | Movie ticket booking (BookMyShow) | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/concert-ticket-booking-system.md | free | code | medium |
| Design CricInfo | Cricinfo / sports scoreboard | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/cricinfo.md | free | code | hard |
| Design Splitwise | Splitwise / expense sharing | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/splitwise.md | free | code | hard |
| Design Chess Game | Chess | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/chess-game.md | free | code | hard |
| Design a Snake and Ladder game | Snake and ladder | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/snake-and-ladder.md | free | code | hard |
| Design Ride-Sharing Service like Uber | Ride sharing (Uber) | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/ride-sharing-service.md | free | code | hard |
| Design Course Registration System | Course registration | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/course-registration-system.md | free | code | hard |
| Design Movie Ticket Booking System | Movie ticket booking (BookMyShow) | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/movie-ticket-booking-system.md | free | code | hard |
| Design Online Shopping System like Amazon | Online shopping (Amazon) | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-shopping-service.md | free | code | hard |
| Design Online Stock Brokerage System | Stock brokerage | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-stock-brokerage-system.md | free | code | hard |
| Design Music Streaming Service like Spotify | Music streaming (Spotify) | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/music-streaming-service.md | free | code | hard |
| Design Online Food Delivery Service like Swiggy | Food delivery | https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/food-delivery-service.md | free | code | hard |

Also 35 Python solution folders exist under `solutions/python/`, including 3 not in the tiered
README problem list above: `hotelmanagement` (a second, older hotel-booking folder alongside
`hotelmanagementsystem`), `concertbookingsystem` (alongside `concertticketbookingsystem`), and
`votingsystem` (no matching `problems/*.md` page found — canonical name **Voting system**, new,
not yet documented with a write-up).

Concurrency/multithreading problems (separate list, no local file — each links straight to an
`algomaster.io` article, not tracked in Table 1 since they are not classic LLD "systems" but
threading primitives): Print FooBar Alternately, Print Zero Even Odd, Fizz Buzz Multithreaded,
Building H2O Molecule, Thread-Safe Cache with TTL (**Cache with TTL**), Concurrent HashMap,
Thread-Safe Blocking Queue (**Bounded blocking queue**), Concurrent Bloom Filter, Multi-threaded
Merge Sort.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| OOP Fundamentals | Classes and Objects, Enums, Interfaces, Encapsulation, Abstraction, Inheritance, Polymorphism | https://github.com/ashishps1/awesome-low-level-design#-oop-fundamentals |
| Class Relationships | Association, Aggregation, Composition, Dependency | https://github.com/ashishps1/awesome-low-level-design#-class-relationships |
| Design Principles | DRY, YAGNI, KISS, SOLID (pictures), SOLID (code) | https://github.com/ashishps1/awesome-low-level-design#-design-principles |
| Design Patterns | Creational: Singleton, Factory Method, Abstract Factory, Builder, Prototype. Structural: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy. Behavioral: Iterator, Observer, Strategy, Command, State, Template Method, Visitor, Mediator, Memento, Chain of Responsibility | https://github.com/ashishps1/awesome-low-level-design#-design-patterns |
| UML | Class Diagram, Use Case Diagram, Sequence Diagram, Activity Diagram, State Machine Diagram | https://github.com/ashishps1/awesome-low-level-design#-uml |
| Concurrency and Multi-threading Concepts | Concurrency 101 (Introduction, Concurrency vs Parallelism, Processes vs Threads, Thread Lifecycle, Race Conditions); Synchronization Primitives (Mutex, Semaphores, Condition Variables, Coarse vs Fine-grained Locking, Reentrant Locks, Try-Lock/Timed Locking, CAS); Concurrency Challenges (Deadlock, Livelock); Concurrency Patterns (Signaling, Thread Pool, Producer-Consumer, Reader-Writer) | https://github.com/ashishps1/awesome-low-level-design#%EF%B8%8F-concurrency-and-multi-threading-concepts |
| How to Answer a LLD Interview Problem | (single linked article + template image) | https://blog.algomaster.io/p/how-to-answer-a-lld-interview-problem |

---

## tssovi/grokking-the-object-oriented-design-interview

URL: https://github.com/tssovi/grokking-the-object-oriented-design-interview
Licence / access: **no LICENSE file in the repo** (root listing has no LICENSE/LICENSE.md;
`contents/LICENSE` 404s); GitHub reports no detected license, so default all-rights-reserved
applies to the author's own text, though the content itself is explicitly an extended/annotated
copy of the paid DesignGurus.io course "Grokking the Object Oriented Design Interview".
Authority: community extension (by GitHub user tssovi) of the well-known DesignGurus.io course;
6.4k stars; widely cited as the standard free OOD-case-study set.
Languages: Python only for `example-codes/`; the case-study `.md` write-ups themselves are
language-agnostic prose + class lists, not code.
Fetched: 2026-09-20, via `gh api repos/.../readme` and `git/trees/HEAD?recursive=1`. No fetch
failures.

**Table 1 — problems** (README's own case-study list; each has both a `.md` write-up and, for
most, an `example-codes/<slug>/` Python folder confirmed in the repo tree)

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design a Library Management System | Library management | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-a-library-management-system.md | free | walkthrough | — |
| Design a Parking Lot | Parking lot | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-a-parking-lot.md | free | code (Python, `example-codes/parking-lot/`) | — |
| Design Amazon - Online Shopping System | Online shopping (Amazon) | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-amazon-online-shopping-system.md | free | code (Python, `example-codes/online-shopping-system/`) | — |
| Design Stack Overflow | Stack Overflow | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-stack-overflow.md | free | code (Python, `example-codes/stack-overflow/`) | — |
| Design a Movie Ticket Booking System | Movie ticket booking (BookMyShow) | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-a-movie-ticket-booking-system.md | free | code (Python, `example-codes/movie-ticket-booking-system/`) | — |
| Design an ATM | ATM | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-an-atm.md | free | code (Python, `example-codes/atm/`) | — |
| Design an Airline Management System | Airline management | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-an-airline-management-system.md | free | code (Python, `example-codes/airline-management-system/`) | — |
| Design Blackjack and a Deck of Cards | Deck of cards / blackjack | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-blackjack-and-a-deck-of-cards.md | free | code (Python, `example-codes/blackjack-and-a-deck-of-cards/`) | — |
| Design a Hotel Management System | Hotel booking | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-a-hotel-management-system.md | free | code (Python, `example-codes/hotel-management-system/`) | — |
| Design a Restaurant Management system | Restaurant management | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-a-restaurant-management-system.md | free | code (Python, `example-codes/restaurant-management-system/`) | — |
| Design Chess | Chess | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-chess.md | free | code (Python, `example-codes/chess/`) | — |
| Design an Online Stock Brokerage System | Stock brokerage | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-an-online-stock-brokerage-system.md | free | code (Python, `example-codes/stock-brokerage-system/`) | — |
| Design a Car Rental System | Car rental | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-a-car-rental-system.md | free | code (Python, `example-codes/car-rental-system/`) | — |
| Design LinkedIn | LinkedIn | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-linkedin.md | free | code (Python, `example-codes/linkedin/`) | — |
| Design Cricinfo | Cricinfo / sports scoreboard | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-cricinfo.md | free | code (Python, `example-codes/cricinfo/`) | — |
| Design Facebook - a Social Network | Social network | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/object-oriented-design-case-studies/design-facebook.md | free | code (Python, `example-codes/facebook/`) | — |

The repo tree also has `example-codes/uber/` (Python + Java subfolders, `main.py`, `trip.py`,
`user.py`, `vehicle.py`) — canonical name **Ride sharing (Uber)** — with **no matching `.md`
case study** in `object-oriented-design-case-studies/`, i.e. code-only, undocumented in the
README's list.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Object-Oriented Design and UML | Object Oriented Basics, Object Oriented Analysis and Design, What is UML?, Use Case Diagrams, Class Diagram, Sequence Diagram, Activity Diagrams | https://github.com/tssovi/grokking-the-object-oriented-design-interview/tree/master/object-oriented-design-and-uml |
| Object Oriented Design Case Studies | (the 15 case studies listed in Table 1) | https://github.com/tssovi/grokking-the-object-oriented-design-interview#readme |
| Object Diagrams | Comprehensive Object Diagram (covers 8+ case studies), System Overview Diagram, Documentation | https://github.com/tssovi/grokking-the-object-oriented-design-interview/blob/master/OBJECT-DIAGRAM-DOCUMENTATION.md |

---

## prasadgujar/low-level-design-primer

URL: https://github.com/prasadgujar/low-level-design-primer
Licence / access: **no LICENSE file** (root has no LICENSE; `contents/LICENSE` 404s); README's own
"License" section literally says "- TODO".
Authority: personal curation repo by Prasad Gujar; 7.9k stars; explicitly credits Donne Martin's
`system-design-primer`, GeeksforGeeks and others as sources rather than original content — it is a
link-aggregator, not a from-scratch solution set.
Languages: none of its own; it links out to third-party solutions/videos of mixed and mostly
unspecified language (a few explicitly Java, several GeeksforGeeks articles use Java or C++; no
row in `solutions.md` is confirmed Python).
Fetched: 2026-09-20, via `gh api repos/.../contents/questions.md` and `.../contents/solutions.md`
(raw). No fetch failures.

**Table 1 — problems** (from `solutions.md`, the only file in this repo pairing a problem with a
concrete external solution URL; `questions.md` is a ~150-item flat prose list of problem prompts
with no per-item links or solutions, so it is not tabulated row-by-row — see Notes)

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design True caller | (no fit — invented: **Caller-ID / spam lookup**) | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| Design Snake and Ladder Game | Snake and ladder | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| Design Bill Sharing/Expense Sharing like Splitwise | Splitwise / expense sharing | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| Design Amazon Locker Service | Amazon locker | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| Design Vehicle / Car Rental Application like Zoomcar | Car rental | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| Cab Booking like Uber, Ola | Ride sharing (Uber) | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | code (external repo) | — |
| Design Parking lot system | Parking lot | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | code (external repo) | — |
| Design Chess Game | Chess | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | code (external repo) | — |
| Design Cache system | Cache with TTL | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | code (external repo) | — |
| Design an online hotel booking system | Hotel booking | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| Design Tic Tac Toe | Tic-tac-toe | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| Design a Vending Machine | Vending machine | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | outline (external LeetCode discuss) | — |
| Design Elevator | Elevator system | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | walkthrough (external links) | — |
| CricInfo/Cricbuzz | Cricinfo / sports scoreboard | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | code (external repo) | — |
| Movie Ticket Booking | Movie ticket booking (BookMyShow) | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | code (external repo) | — |
| Uber Eats/Door dash/Swiggy | Food delivery | https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md | free | code (external repo) | — |

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Resources | Questions, Solutions, Resources (marked #TODO, unwritten) | https://github.com/prasadgujar/low-level-design-primer#resources |

---

## kumaransg/LLD

URL: https://github.com/kumaransg/LLD
Licence / access: **no LICENSE file** (`contents/LICENSE` 404s); README does not mention a licence.
Authority: personal interview-prep collection by Kumaran S G; 2.1k stars; explicitly a mix of the
author's own machine-coding-round questions plus attributed external sources (lldcoding.com,
other GitHub repos); README states "page is under construction".
Languages: **Java only** — 2,505 `.java` files found in the repo tree, 0 `.py` files. No Python.
Fetched: 2026-09-20, via `gh api repos/.../readme` and `git/trees/HEAD?recursive=1`. No fetch
failures.

**Table 1 — problems** (README's own two tables: "asked during my machine coding rounds" and
"Frequently asked Problems"; the second table links to external articles on lldcoding.com rather
than in-repo code)

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Cricket Match Dashboard | Cricinfo / sports scoreboard | https://github.com/kumaransg/LLD/tree/main/Cricket%20Match%20Dashboard | free | code (Java) | — |
| Event Calendar | Meeting scheduler / calendar | https://github.com/kumaransg/LLD/tree/main/Event_calendar_flipkart | free | code (Java) | — |
| FoodKart or food ordering System | Food delivery | https://github.com/kumaransg/LLD/tree/main/FoodKart | free | code (Java) | — |
| Stock Exchange | Stock brokerage | https://github.com/kumaransg/LLD/tree/main/StockExchange | free | code (Java) | — |
| PropertyHunt or property Listing site | (invented: **Property listing site**) | https://github.com/kumaransg/LLD/tree/main/PropertyHunt | free | outline (question image only) | — |
| ledger company | (invented: **Ledger / accounting system**) | https://github.com/kumaransg/LLD/tree/main/ledger_company_navi | free | code (external repo credited) | — |
| Leetcode Like platform LLD | (invented: **Coding-judge platform**) | https://github.com/kumaransg/LLD/tree/main/leetcode-lld-flipkart-coding-blox | free | code (external repo credited) | — |
| Ride Sharing like App | Ride sharing (Uber) | https://github.com/kumaransg/LLD/tree/main/Ride%20Sharing%20 | free | code (Java) | — |
| Design Lift/Elevator | Elevator system | https://lldcoding.com/design-lld-lift-machine-coding | paywalled | walkthrough (external) | — |
| Design Splitwise | Splitwise / expense sharing | https://lldcoding.com/design-lld-splitwise-application-machine-coding | paywalled | walkthrough (external) | — |
| Design Event Calender | Meeting scheduler / calendar | https://lldcoding.com/design-lld-event-calendar-machine-coding | paywalled | walkthrough (external) | — |

Notes: the "Frequently asked Problems" table also lists 2048 Game, AWS Lambda, Game Engine,
Newsletter Service, Gmail, WhatsApp, Tinder, Zoom, Google Docs, Mentorship Platform, Crypto
Exchange, Codepair Platform, Chat System, Dropbox, Music Recognition, Spotify, BitTorrent,
Distributed Search, Google Maps, Twitter/X, Blockchain, Video Streaming — all as bare links to
the same external paywalled site (lldcoding.com), no canonical-name mapping attempted for the
ones with no established LLD identity (e.g. "Music Recognition System", "Blockchain") since they
read as high-level/distributed-systems prompts wearing LLD titles rather than classic machine-
coding problems.

**Table 2 — outline**: none — this source is a flat problem list, not a subject curriculum.

---

## InterviewReady/Low-Level-Design

URL: https://github.com/InterviewReady/Low-Level-Design
Licence / access: **no LICENSE file** (`contents/LICENSE` 404s); GitHub license field null.
Authority: maintained by the InterviewReady organisation (interviewready.io, a paid system-design
course platform); 889 stars — below the ~1,500-star bar for "any other repo" but included because
it was named as a required source.
Languages: **Java only** — 43 `.java` files found in the repo tree, 0 Python.
Fetched: 2026-09-20, via `gh api repos/.../readme` and `git/trees/HEAD?recursive=1`. No fetch
failures.

**Table 1 — problems**

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Cache | Cache with TTL | https://github.com/InterviewReady/Low-Level-Design/tree/main/distributed-cache | free | code (Java) | — |
| Event Bus | Event bus | https://github.com/InterviewReady/Low-Level-Design/tree/main/distributed-event-bus | free | code (Java) | — |
| Rate Limiter | Rate limiter | https://github.com/InterviewReady/Low-Level-Design/tree/main/rate-limiter | free | code (Java) | — |
| Service Orchestrator | (invented: **Service orchestrator**) | https://github.com/InterviewReady/Low-Level-Design/tree/main/service-orchestrator | free | code (Java) | — |

**Table 2 — outline**: none — README is a 4-item project list plus an external-links reading
list (Refactoring Guru, memory-model articles, rate-limiting/circuit-breaker articles), not a
structured curriculum of its own.

---

## donnemartin/system-design-primer (object_oriented_design folder only)

URL: https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design
Licence / access: **CC BY 4.0** (repo's `LICENSE.txt`: "Creative Commons Attribution 4.0
International License", copyright Donne Martin 2017; note the GitHub API's `license.spdx_id`
reports `NOASSERTION` because CC-BY isn't in GitHub's software-license detector, but the file
itself is unambiguous).
Authority: Donne Martin's system-design-primer is the best-known system design interview repo on
GitHub (370k+ stars total); this survey scopes to its `solutions/object_oriented_design/` folder
only, per instructions, since the rest of the repo is high-level/distributed design, out of scope.
Languages: **Python only** in this folder — every problem has a `.py` file and a matching
Jupyter `.ipynb` notebook.
Fetched: 2026-09-20, via `gh api repos/.../contents/LICENSE.txt` and
`git/trees/HEAD?recursive=1` filtered to the folder. No fetch failures.

**Table 1 — problems**

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design a hash table | (invented: **Hash table / dictionary implementation**) | https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/hash_table | free | code (Python) | — |
| Design a least recently used cache | LRU cache | https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/lru_cache | free | code (Python) | — |
| Design a call center | (invented: **Call center**) | https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/call_center | free | code (Python) | — |
| Design a deck of cards | Deck of cards / blackjack | https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/deck_of_cards | free | code (Python) | — |
| Design a parking lot | Parking lot | https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/parking_lot | free | code (Python) | — |
| Design an online chat system | (invented: **Online chat system**) | https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/online_chat | free | code (Python) | — |

**Table 2 — outline**: not applicable to this scoped folder (the parent repo's own top-level
outline is system design, out of scope for this survey).

---

## faif/python-patterns

URL: https://github.com/faif/python-patterns
Licence / access: **no LICENSE file** (root listing has no LICENSE; `contents/LICENSE` 404s);
GitHub license field null → default all-rights-reserved, despite being a widely-reused reference.
Authority: the highest-starred repo in this whole survey (42.9k stars); long-running community
collection of Python design-pattern implementations, actively maintained (mermaid diagrams, CI
lint/type-check added recently).
Languages: Python only (this is a pattern-idiom repo, not an LLD problem-solution repo).
Fetched: 2026-09-20, via `gh api repos/.../readme`. No fetch failures.

Not an LLD-problem source — no Table 1. Table 2 (pattern outline) only, per instructions.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Creational Patterns | abstract_factory, borg, builder, factory, lazy_evaluation, pool, prototype | https://github.com/faif/python-patterns#creational-patterns |
| Structural Patterns | 3-tier, adapter, bridge, composite, decorator, facade, flyweight, front_controller, mvc, proxy | https://github.com/faif/python-patterns#structural-patterns |
| Behavioral Patterns | chain_of_responsibility, catalog, chaining_method, command, interpreter, iterator (+ iterator_alt), mediator, memento, observer, publish_subscribe, registry, servant, specification, state, strategy, template, visitor | https://github.com/faif/python-patterns#behavioral-patterns |
| Design for Testability Patterns | dependency_injection (3 variants) | https://github.com/faif/python-patterns#design-for-testability-patterns |
| Fundamental Patterns | delegation_pattern | https://github.com/faif/python-patterns#fundamental-patterns |
| Others | blackboard, graph_search, hsm (hierarchical state machine) — labelled "non gang of four pattern" | https://github.com/faif/python-patterns#others |
| 🚫 Anti-Patterns | Singleton (why not, in Python), God Object, Inheritance overuse | https://github.com/faif/python-patterns#-anti-patterns |

---

## abhaypaswan/lld-python

URL: https://github.com/abhaypaswan/lld-python
Licence / access: **MIT** (repo's own LICENSE file).
Authority: newer, smaller repo (40 stars) by Abhay Paswan, built to back a paid practice platform
(goatengineer.com) but the repo itself is free/open; included per instructions' explicit rule to
cover "any repository with Python solutions regardless of stars" — this is the most rigorously
tested Python-only LLD repo found (every problem ships a pytest suite, and the README documents
specific invariants each suite checks, e.g. Splitwise splits summing exactly, chess perft-to-
depth-3 proving undo reverses apply).
Languages: **Python only**, standard-library only implementations; each problem is fully
self-contained (`src/`, `tests/`, `README.md` with mermaid class diagram, `meta.json`).
Fetched: 2026-09-20, via `gh api repos/.../readme`. No fetch failures.

**Table 1 — problems** (README's own numbered table, difficulty and design-pattern columns are
the source's own)

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design Tic Tac Toe | Tic-tac-toe | https://github.com/abhaypaswan/lld-python/tree/main/problems/tic-tac-toe | free | code (Python) | easy |
| Snake and Ladder | Snake and ladder | https://github.com/abhaypaswan/lld-python/tree/main/problems/snake-and-ladder | free | code (Python) | easy |
| Design Splitwise | Splitwise / expense sharing | https://github.com/abhaypaswan/lld-python/tree/main/problems/splitwise | free | code (Python) | medium |
| Design a Chat Room | (invented: **Chat room**) | https://github.com/abhaypaswan/lld-python/tree/main/problems/chat-room | free | code (Python) | medium |
| Design a Logging Framework | Logger / logging framework | https://github.com/abhaypaswan/lld-python/tree/main/problems/logging-framework | free | code (Python) | medium |
| Design a Notification Service | Notification service | https://github.com/abhaypaswan/lld-python/tree/main/problems/notification-service | free | code (Python) | medium |
| Design a Parking Lot | Parking lot | https://github.com/abhaypaswan/lld-python/tree/main/problems/parking-lot | free | code (Python) | medium |
| Design a Rate Limiter | Rate limiter | https://github.com/abhaypaswan/lld-python/tree/main/problems/rate-limiter | free | code (Python) | medium |
| Design a Text Editor with Undo | Text editor / undo-redo | https://github.com/abhaypaswan/lld-python/tree/main/problems/text-editor | free | code (Python) | medium |
| Design a Vending Machine | Vending machine | https://github.com/abhaypaswan/lld-python/tree/main/problems/vending-machine | free | code (Python) | medium |
| Design an ATM | ATM | https://github.com/abhaypaswan/lld-python/tree/main/problems/atm | free | code (Python) | medium |
| Design an In-Memory File System | In-memory file system | https://github.com/abhaypaswan/lld-python/tree/main/problems/file-system | free | code (Python) | medium |
| Design an LRU Cache | LRU cache | https://github.com/abhaypaswan/lld-python/tree/main/problems/lru-cache | free | code (Python) | medium |
| Design Chess | Chess | https://github.com/abhaypaswan/lld-python/tree/main/problems/chess | free | code (Python) | hard |
| Design a Movie Ticket Booking System | Movie ticket booking (BookMyShow) | https://github.com/abhaypaswan/lld-python/tree/main/problems/movie-ticket-booking | free | code (Python) | hard |
| Design a Payment Gateway | (invented: **Payment gateway**) | https://github.com/abhaypaswan/lld-python/tree/main/problems/payment-gateway | free | code (Python) | hard |
| Design an Elevator System | Elevator system | https://github.com/abhaypaswan/lld-python/tree/main/problems/elevator-system | free | code (Python) | hard |

**Table 2 — outline**: `docs/patterns.md` indexes "all 20" design patterns used across the 17
problems, generated from the per-problem `meta.json` files, not copied here since it's a
generated cross-index rather than the source's own hand-written subject outline.

---

## jkaus324/machine-coding-interview-questions

URL: https://github.com/jkaus324/machine-coding-interview-questions
Licence / access: **no LICENSE file** (`contents/LICENSE` 404s). The repo itself is free to read
and clone; it is the free "pilot" (20 of 105 problems) for a paid book + platform
("Crack LLD Interviews", topmate.io) — record this as **free (repo) / paid course (full 105-
problem set, upsold in the README)**.
Authority: small, new repo (98 stars) by Jatin Kaushal; included per instructions' rule to cover
Python-solution repos regardless of stars. Distinctive design: each problem ships a base
requirement plus two "extension" parts that unlock after tests pass, meant to simulate an
interviewer adding requirements mid-round.
Languages: **Python confirmed** — every problem folder has `solution.py` (plus `.cpp`, `.go`,
`.java`, `.js` — same problem solved in 5 languages against one language-agnostic test harness)
and `boilerplate/python/part{1,2,3}/{learning,guided,interview}.py` starter variants.
Fetched: 2026-09-20, via `gh api repos/.../readme` and `git/trees/HEAD?recursive=1`. No fetch
failures.

**Table 1 — problems** (README's own Tier 1 / Tier 2 tables; "Patterns" and company columns are
the source's own)

| Problem (source's title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Payment Method Ranker | (invented: **Payment method ranker**) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/001-payment-ranker | free | code (Python + C++, Go, Java, JS) | Tier 1 (foundation) |
| Notification System | Notification service | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/003-notification-system | free | code (5 languages) | Tier 1 |
| Vending Machine | Vending machine | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/004-vending-machine | free | code (5 languages) | Tier 1 |
| Customer Issue Resolution | (invented: **Support-ticket triage**) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/005-customer-issue-resolution | free | code (5 languages) | Tier 1 |
| Billing & Discount Engine | (invented: **Billing / discount engine**) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/006-billing-discount-engine | free | code (5 languages) | Tier 1 |
| Order Management System | (invented: **Order management system**) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/007-order-management | free | code (5 languages) | Tier 1 |
| File Search System | (invented: **File search system**) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/008-file-search | free | code (5 languages) | Tier 1 |
| API Rate Limiter | Rate limiter | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/011-api-rate-limiter | free | code (5 languages) | Tier 1 |
| Meeting Room Scheduler | Meeting scheduler / calendar | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/009-meeting-room-scheduler | free | code (5 languages) | Tier 2 (intermediate) |
| Ride Surge Pricing Engine | (invented: **Ride surge-pricing engine**) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/010-ride-surge-pricing | free | code (5 languages) | Tier 2 |
| Elevator System | Elevator system | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/012-elevator-system | free | code (5 languages) | Tier 2 |
| Parking Lot System | Parking lot | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/013-parking-lot | free | code (5 languages) | Tier 2 |
| Splitwise Expense-Sharing | Splitwise / expense sharing | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/014-splitwise | free | code (5 languages) | Tier 2 |
| BookMyShow Ticket Booking | Movie ticket booking (BookMyShow) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/015-bookmyshow | free | code (5 languages) | Tier 2 |
| Amazon Locker System | Amazon locker | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/016-amazon-locker | free | code (5 languages) | Tier 2 |
| LRU Cache | LRU cache | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/017-lru-cache | free | code (5 languages) | Tier 2 |
| Simplified Twitter | (invented: **Simplified Twitter feed**) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/018-simplified-twitter | free | code (5 languages) | Tier 2 |
| Online Auction System | Online auction | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/019-online-auction | free | code (5 languages) | Tier 2 |
| Logger System | Logger / logging framework | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/020-logger-system | free | code (5 languages) | Tier 2 |
| Ride-Sharing Application | Ride sharing (Uber) | https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/021-ride-sharing | free | code (5 languages) | Tier 2 |

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Design Pattern Primers | Strategy, Observer, State, Singleton (the only 4 written so far, out of a planned larger set) | https://github.com/jkaus324/machine-coding-interview-questions#design-pattern-primers |
| Difficulty modes (per problem) | Interview (blank slate), Guided (hinted interfaces), Learning (full class structure, TODO bodies) | https://github.com/jkaus324/machine-coding-interview-questions#three-difficulty-modes--same-problem-different-starting-point |

---

## RefactoringGuru/design-patterns-python

URL: https://github.com/RefactoringGuru/design-patterns-python
Licence / access: **CC BY-NC-ND 4.0** (Creative Commons Attribution-NonCommercial-NoDerivatives —
stated in the README's own License section; noncommercial and no-derivatives are unusually
restrictive for a code repo: forking to adapt/rewrite examples for a course is technically
outside the license's permission, since NoDerivatives forbids distributing modified versions).
Authority: official Python port of the refactoring.guru design-patterns reference, by Alexey
Pyltsyn and Alexander Shvets; 1,012 stars; refactoring.guru is one of the most widely cited
design-pattern explainer sites.
Languages: Python only in this repo (the wider refactoring.guru project has parallel repos per
language).
Fetched: 2026-09-20, via `gh api repos/.../readme` and `git/trees/HEAD?recursive=1`. No fetch
failures.

Not an LLD-problem source — no Table 1 (every example is a small conceptual/real-world pattern
demo, not a full interview-style system). Table 2 (pattern outline) only.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| All classic GoF patterns, each with a Conceptual and a RealWorld example | AbstractFactory, Adapter, Bridge, Builder, ChainOfResponsibility, Command, Composite, Decorator, Facade, FactoryMethod, Flyweight, Iterator, Mediator, Memento, Observer, Prototype, Proxy, Singleton, State, Strategy, TemplateMethod, Visitor | https://github.com/RefactoringGuru/design-patterns-python/tree/master/src |

---

## Notes

- **Repos actually reached, all 10**: no fetch failures across any of the 10 repositories — every
  README, LICENSE (or its absence), and `git/trees/HEAD?recursive=1` call succeeded on the first
  try via `gh api`.
- **Licence spread**: MIT (abhaypaswan/lld-python) and CC BY 4.0 (donnemartin, scoped folder) are
  the only two genuinely permissive licences found. GPL-3.0 (ashishps1) is permissive but
  copyleft. CC BY-NC-ND 4.0 (RefactoringGuru) is the most restrictive — noncommercial and no
  derivatives, worth flagging if any card or reading ever reuses its code verbatim. **Six of the
  ten repos have no LICENSE file at all**: tssovi, prasadgujar, kumaransg, InterviewReady, faif,
  jkaus324. Default copyright applies to unlicensed repos; treat their code as reference-only
  (read and re-derive, don't copy verbatim into cards).
- **Only-one-source problems** (canonical names that appeared in exactly one repo's Table 1):
  Voting system, In-memory file system (also in the taxonomy's own list but only abhaypaswan
  ships it), Text editor / undo-redo (abhaypaswan only), Event bus (InterviewReady only), Amazon
  locker (jkaus324 + kumaransg's solutions.md only), Call center, Hash table / dictionary
  implementation, Online chat system (all three donnemartin-only), Deck of cards / blackjack
  (donnemartin + tssovi only, not in the two biggest problem-tier repos ashishps1/abhaypaswan).
- **Newly popular / recently added**: ashishps1's `votingsystem` Python solution folder exists
  with no matching `problems/*.md` write-up yet — looks like a very recent addition, ahead of its
  own documentation. jkaus324's whole repo (98 stars) is new and explicitly framed as filling a
  gap ("no LeetCode for LLD") with an interview-realistic unlock-on-pass-tests structure — worth
  watching as it grows past its 20-problem pilot toward the advertised 105.
- **What is Python-specific**: donnemartin's `object_oriented_design` folder and
  abhaypaswan/lld-python are Python-only end to end. ashishps1 and tssovi are multi-language with
  a confirmed, complete Python folder alongside others. jkaus324 solves every problem in 5
  languages including Python from one shared spec. kumaransg and InterviewReady have **no Python
  at all** (pure Java) despite being required/well-known sources — worth noting explicitly since a
  Python-only learner gets zero problems from either.
- **How sources rank/tier problems**: ashishps1 uses Easy/Medium/Hard (7/15/11 problems).
  abhaypaswan uses Easy/Medium/Hard emoji tiers (2/11/4) plus an explicit expected-time-in-minutes
  column (40–90 min) sourced from the problem's own `meta.json`. jkaus324 uses "Tier 1 —
  Foundation" / "Tier 2 — Intermediate" (with a presumably-planned Tier 3, not yet published).
  prasadgujar, kumaransg, tssovi, InterviewReady, donnemartin give no difficulty labels at all.
- **Pattern-outline sources compared**: faif/python-patterns (42.9k stars, no licence, broadest —
  includes non-GoF "Others" and an explicit "Anti-Patterns" section arguing against Singleton in
  Python) vs. RefactoringGuru/design-patterns-python (1k stars, CC BY-NC-ND, strictly the 22
  classic GoF patterns, each with both a bare conceptual example and a "real-world" applied
  example — a good second angle on the same pattern for card-writing, license permitting only
  reading and re-explaining, not copying).
- **Sources not reached**: none — every one of the 10 targeted repos (the 6 explicitly required
  plus 4 chosen from search: faif/python-patterns required by name, abhaypaswan/lld-python,
  jkaus324/machine-coding-interview-questions, RefactoringGuru/design-patterns-python) was
  successfully fetched. Repos found in search but **not** covered in depth, for the record:
  kousiknath/LowLevelDesign (525 stars, 28 implemented OOD problems, but confirmed **pure Java**,
  596 `.java` files / 0 `.py` — skipped in favor of Python-bearing repos once its language was
  checked); arpit20adlakha/Data-Structure-Algorithms-LLD-HLD (2,656 stars, mixed DSA+LLD, not
  opened); armankhondker/best-low-level-design-resources (126 stars, a links-only resource list,
  not opened, below the "worked problems" bar). The literal GitHub search-string queries
  `"machine coding"` and `"LLD python"` were checked and confirmed unproductive (they surface
  machine-code compilers/decompilers and LLDB debugger scripts respectively, not LLD-interview
  repos) — that dead end is recorded here so a future run doesn't repeat it expecting different
  results.
