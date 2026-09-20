# LLD / OOD / machine-coding prep sites — survey

Inventory of what each widely-used LLD prep source teaches: which problems, and how it
outlines the subject. Built per `LLD_SURVEY_AGENT.md`. Every row is something actually seen
on the cited page; nothing here is invented.

## Hello Interview — Low-Level Design

- `URL:` https://www.hellointerview.com/learn/low-level-design/in-a-hurry/introduction (guide) and
  https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/ (breakdowns index —
  this exact index URL 404'd; the breakdown list was instead read off the sidebar navigation
  rendered on https://www.hellointerview.com/learn/low-level-design).
- `Licence / access:` free tier (guide fundamentals + 3 problem breakdowns) plus a paid
  subscription that unlocks the concurrency deep-dives and 6 more problem breakdowns.
- `Authority:` Hello Interview is a paid mock-interview / interview-prep platform (System Design
  and LLD tracks) run by ex-FAANG engineers/interviewers; widely cited in 2024–2026 interview-prep
  circles as one of the more rigorous, interviewer-written LLD resources.
- `Languages:` Python. The free problem breakdowns (Connect Four, Amazon Locker, Elevator) each
  ship a complete Python implementation alongside pseudocode; no other language was observed.
- `Fetched:` 2026-09-20, via WebFetch on each page directly (introduction, delivery, design-principles,
  oop-concepts, patterns, concurrency/intro, and the three free problem-breakdown pages). The
  `problem-breakdowns/` index page itself returned HTTP 404; the sidebar on the parent
  `/learn/low-level-design` page supplied the full list of breakdown titles and lock status instead.
  `site:hellointerview.com` search was not attempted — WebSearch budget for this session was
  already exhausted before this source was reached.

**Table 1 — problems**

| Problem (the source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Connect Four | Connect Four | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/connect-four | free | code (Python) | — |
| Amazon Locker | Amazon locker | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/amazon-locker | free | code (Python) | — |
| Elevator | Elevator system | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/elevator | free | code (Python) | — |
| Parking Lot | Parking lot | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/parking-lot | paywalled | outline (locked; not fetchable) | — |
| File System | In-memory file system | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/file-system | paywalled | outline (locked; not fetchable) | — |
| Movie Ticket Booking | Movie ticket booking (BookMyShow) | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/bookmyshow | paywalled | outline (locked; not fetchable) | — |
| Logging Service | Logger / logging framework | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/logging-service | paywalled | outline (locked; not fetchable) | — |
| Rate Limiter | Rate limiter | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/rate-limiter | paywalled | outline (locked; not fetchable) | — |
| Inventory Management | Inventory management | https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/inventory-management | paywalled | outline (locked; not fetchable) | — |

No difficulty labels (easy/medium/hard) were observed anywhere on Hello Interview's LLD track;
the guide instead labels expected depth per level (Junior / Mid-level / Senior) inside each
problem breakdown, which is a different axis than difficulty.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Introduction | What is this guide? · Difference between LLD and System Design · Variants of LLD interviews · Interview assessment | https://www.hellointerview.com/learn/low-level-design/in-a-hurry/introduction |
| Delivery Framework | 1) Requirements (~5 min) · 2) Entities and Relationships (~3 min): Identify Entities, Define Relationships, How to Represent This on the Whiteboard · 3) Class Design (~10–15 min): Deriving State from Requirements, Deriving Behavior from Requirements, What About UML Diagrams? · 4) Implementation (~10 min): Verification — Walk Through a Specific Scenario · 5) Extensibility (~5 min, if time and level allow) | https://www.hellointerview.com/learn/low-level-design/in-a-hurry/delivery |
| Design Principles | General Software Design Principles: KISS, DRY, YAGNI, Separation of Concerns, Law of Demeter · Object-Oriented Design Principles (SOLID): SRP, OCP, LSP, ISP, DIP · Putting It All Together · Test Your Knowledge | https://www.hellointerview.com/learn/low-level-design/in-a-hurry/design-principles |
| OOP Concepts | Encapsulation · Abstraction · Polymorphism · Inheritance (When Inheritance Works, When Inheritance Breaks Down) · Putting It Together · Test Your Knowledge | https://www.hellointerview.com/learn/low-level-design/in-a-hurry/oop-concepts |
| Design Patterns | Creational: Factory Method, Builder, Singleton · Structural: Decorator, Facade · Behavioral: Strategy, Observer, State Machine · Wrapping Up · Test Your Knowledge (the page states only a subset of the classic Gang-of-Four patterns remain relevant for modern LLD interviews) | https://www.hellointerview.com/learn/low-level-design/in-a-hurry/patterns |
| Concurrency — Introduction | Concurrency Fundamentals · The Toolbox: Atomics, Locks (Mutexes), Semaphores, Condition Variables, Blocking Queues · Language Reference · Three Problem Types · What's Next | https://www.hellointerview.com/learn/low-level-design/concurrency/intro |
| Concurrency — Correctness (🔒 premium) | not fetchable (locked) | https://www.hellointerview.com/learn/low-level-design/concurrency/correctness |
| Concurrency — Coordination (🔒 premium) | not fetchable (locked) | https://www.hellointerview.com/learn/low-level-design/concurrency/coordination |
| Concurrency — Scarcity (🔒 premium) | not fetchable (locked) | https://www.hellointerview.com/learn/low-level-design/concurrency/scarcity |

## Grokking the Low Level Design Interview Using OOD Principles (Educative)

- `URL:` https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles
- `Licence / access:` paid course (Educative subscription); a free preview of the first module is
  typical for Educative but was not separately verified.
- `Authority:` written for Educative, credited to Fahim ul Haq (Educative co-founder/CEO); one of
  the original "Grokking" LLD courses and widely referenced as a baseline curriculum for the round
  (215 lessons, 28 quizzes, 19 mock interviews, rated 4.7/5, last updated "2 weeks ago" at fetch time).
- `Languages:` the course page states solutions are covered in **Java, Python, C++, C#, and
  JavaScript** — Python is explicitly included.
- `Fetched:` 2026-09-20, via WebFetch directly on the course page (the page itself renders the full
  module/lesson table of contents; no fallback needed).

**Table 1 — problems**

| Problem (the source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Designing a Parking Lot | Parking lot | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code (Java, Python, C++, C#, JS) | — |
| Designing an Elevator System | Elevator system | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Library Management System | Library management | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing the Amazon Locker Service | Amazon locker | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Vending Machine | Vending machine | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing an Online Blackjack Game | Deck of cards / blackjack | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Meeting Scheduler | Meeting scheduler / calendar | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Movie Ticket Booking System | Movie ticket booking (BookMyShow) | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Car Rental System | Car rental | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing ATM | ATM | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Chess Game | Chess | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Hotel Management System | Hotel booking | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing the Amazon Online Shopping System | Online shopping (Amazon) | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing Stack Overflow | Stack Overflow | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Restaurant Management System | Restaurant management | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing Facebook | Social network | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing an Online Stock Brokerage System | Stock brokerage | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing a Jigsaw Puzzle | Jigsaw puzzle (new canonical name — not in the seed list) | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing an Airline Management System | Airline management | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing ESPNcricinfo | Cricinfo / sports scoreboard | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Designing LinkedIn | LinkedIn | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | code | — |
| Design a Ride Sharing System (breakout session) | Ride sharing (Uber) | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | outline (breakout session, no lesson count given) | — |
| Design a Food Delivery System (breakout session) | Food delivery | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles | paywalled | outline (breakout session, no lesson count given) | — |

No difficulty labels were reported on the course page; each design problem module carries a
lesson count (8–9 lessons) and most (16 of 21 main modules) include a "Mock Interview" lesson.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Introduction (2 lessons) | Overview · Introduction to the Course | https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles |
| Cornerstones of Object-Oriented Programming (7 lessons) | Background of OOP · Encapsulation · Abstraction · Inheritance · Generalization · Polymorphism · Quiz: Object-Oriented Basics | same |
| Object-Oriented Design (8 lessons) | UML diagrams and analysis techniques | same |
| Object-Oriented Design Principles (7 lessons) | SOLID principles coverage | same |
| Design Patterns (7 lessons) | Creational, structural, behavioral patterns | same |
| Real-World Design Problems (1 lesson) | Problem-solving approach framework | same |
| Designing a Parking Lot … through … Designing LinkedIn (21 modules, 8–9 lessons each) | one module per problem (see Table 1), most ending in a "Mock Interview" lesson | same |
| Wrapping Up (2 lessons) | course close-out | same |
| Additional Practice Sessions | OOD Basics (Breakout Session) · Design a Ride Sharing System (Breakout Session) · Design a Food Delivery System (Breakout Session) | same |

## Grokking the Object Oriented Design Interview (DesignGurus)

- `URL:` https://www.designgurus.io/course/grokking-the-object-oriented-design-interview
- `Licence / access:` paid course, $75 one-time payment for lifetime access (not a subscription).
- `Authority:` written by Arslan Ahmad, DesignGurus founder and ex-FAANG engineering manager;
  DesignGurus' OOD course is a commonly cited alternative/successor to the original Educative
  "Grokking" course (49 lessons, 156 "playgrounds", 123 assessments, rated 4.2/5 from 10,939 ratings
  at fetch time).
- `Languages:` the course page states **Python, Java, and C++** for code/solutions.
- `Fetched:` 2026-09-20, via WebFetch directly on the course page (full table of contents rendered
  on-page; no fallback needed).

**Table 1 — problems**

| Problem (the source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design a Parking Lot | Parking lot | https://www.designgurus.io/course/grokking-the-object-oriented-design-interview | paywalled | code (Python, Java, C++) | — |
| Design a Library Management System | Library management | same | paywalled | code | — |
| Design an ATM | ATM | same | paywalled | code | — |
| Design an Elevator System | Elevator system | same | paywalled | code | — |
| Design a Vending Machine | Vending machine | same | paywalled | code | — |
| Design a Movie Ticket Booking System | Movie ticket booking (BookMyShow) | same | paywalled | code | — |
| Design a Hotel Management System | Hotel booking | same | paywalled | code | — |
| Design a Car Rental System | Car rental | same | paywalled | code | — |
| Design a Restaurant Management System | Restaurant management | same | paywalled | code | — |
| Design an Airline Management System | Airline management | same | paywalled | code | — |
| Design Blackjack and a Deck of Cards | Deck of cards / blackjack | same | paywalled | code | — |
| Design Chess | Chess | same | paywalled | code | — |
| Design Stack Overflow | Stack Overflow | same | paywalled | code | — |
| Design Cricinfo | Cricinfo / sports scoreboard | same | paywalled | code | — |
| Design LinkedIn | LinkedIn | same | paywalled | code | — |
| Design Facebook (Social Network) | Social network | same | paywalled | code | — |
| Design Amazon (Online Shopping System) | Online shopping (Amazon) | same | paywalled | code | — |
| Design an Online Stock Brokerage System | Stock brokerage | same | paywalled | code | — |
| Design Splitwise | Splitwise / expense sharing | same | paywalled | code | — |
| Design a Notification Service | Notification service | same | paywalled | code | — |
| Design an In-Memory Cache | In-memory key-value store | same | paywalled | code | — |
| Design a Ride Sharing Service | Ride sharing (Uber) | same | paywalled | code | — |

No per-problem difficulty labels were seen; problems are grouped into five themed clusters
("Everyday Objects", "Booking and Inventory", "Games and Rules", "Platforms and Feeds",
"Pattern-Driven Components"), each closed with its own chapter assessment, which is this
course's difficulty/organisation signal instead of an easy/medium/hard tag.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Chapter 1: Introduction (4 lessons) | What This Course Covers · A Complete Answer in Five Minutes · How to Use This Course · A Study Plan | https://www.designgurus.io/course/grokking-the-object-oriented-design-interview |
| Chapter 2: Object Oriented Design and UML (8 lessons) | Object-Oriented Basics · OO Analysis and Design · What is UML? · Use Case Diagrams · Class Diagram · Activity Diagrams · Sequence Diagram · Chapter Assessment | same |
| Chapter 3: How to Answer an Object Oriented Design Question (7 lessons) | How the Interview Runs · From One Line to a List of Requirements · Finding the Classes · Choosing the Relationship Between Two Classes · Keeping the Design Honest with SOLID · The Design Patterns That Come Up in This Round · Chapter Assessment | same |
| Chapter 4: Object Oriented Design Case Studies (27 lessons) | five sub-groups — Everyday Objects; Booking and Inventory; Games and Rules; Platforms and Feeds; Pattern-Driven Components (see Table 1 for the problems in each, each sub-group ends in its own Assessment) | same |
| Chapter 5: Final Exam (1 lesson) | Final Exam — 60 questions with explanations | same |
| Chapter 6: Appendix (2 lessons) | Contact Us · Other Courses | same |

## AlgoMaster — LLD (Ashish Pratap Singh)

- `URL:` https://algomaster.io/learn/lld
- `Licence / access:` mixed — the homepage (https://algomaster.io/) advertises a "Get Premium"
  tier, but the LLD course page itself showed no per-course price and appeared browsable; treated
  as `free` in Table 1 below since no paywall/lock indicator was observed on the fetched outline,
  with the caveat that some content may sit behind AlgoMaster Premium not visible from this fetch.
- `Authority:` Ashish Pratap Singh, ex-Amazon/Adobe software engineer, built AlgoMaster after
  extensive interview prep of his own; the site is a well-known free-leaning DSA/LLD/HLD resource
  in 2024–2026 interview-prep circles, cross-linked from his newsletter/blog.
- `Languages:` Java — the outline page states solutions are available on GitHub in Java; no Python
  solutions were observed for this source.
- `Fetched:` 2026-09-20, via WebFetch directly on https://algomaster.io/learn/lld (full 80-lesson
  curriculum, including 33 named interview problems tiered Easy/Medium/Hard, rendered on-page) and
  on https://algomaster.io/ for pricing/author confirmation. His blog's separate "LLD roadmap"
  posts were not additionally fetched — the course page already subsumes the same problem list.

**Table 1 — problems**

| Problem (the source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design Tic Tac Toe | Tic-tac-toe | https://algomaster.io/learn/lld | free | outline/walkthrough (exact depth not fetched per-problem) | Easy |
| Design Snake and Ladder game | Snake and ladder | https://algomaster.io/learn/lld | free | — | Easy |
| Design LRU Cache | LRU cache | https://algomaster.io/learn/lld | free | — | Easy |
| Design Parking Lot | Parking lot | https://algomaster.io/learn/lld | free | — | Easy |
| Design Task Management System | Task scheduler | https://algomaster.io/learn/lld | free | — | Easy |
| Design Stack Overflow | Stack Overflow | https://algomaster.io/learn/lld | free | — | Medium |
| Design ATM | ATM | https://algomaster.io/learn/lld | free | — | Medium |
| Design Logging Framework | Logger / logging framework | https://algomaster.io/learn/lld | free | — | Medium |
| Design Pub Sub System | Pub-sub / message broker | https://algomaster.io/learn/lld | free | — | Medium |
| Design Elevator System | Elevator system | https://algomaster.io/learn/lld | free | — | Medium |
| Design Splitwise | Splitwise / expense sharing | https://algomaster.io/learn/lld | free | — | Medium |
| Design Vending Machine | Vending machine | https://algomaster.io/learn/lld | free | — | Medium |
| Design Car Rental System | Car rental | https://algomaster.io/learn/lld | free | — | Medium |
| Design Hotel Management System | Hotel booking | https://algomaster.io/learn/lld | free | — | Medium |
| Design a Digital Wallet Service | Digital wallet | https://algomaster.io/learn/lld | free | — | Medium |
| Design Airline Management System | Airline management | https://algomaster.io/learn/lld | free | — | Medium |
| Design Library Management System | Library management | https://algomaster.io/learn/lld | free | — | Medium |
| Design Traffic Signal Control System | Traffic signal | https://algomaster.io/learn/lld | free | — | Medium |
| Design Concert Ticket Booking System | Movie ticket booking (BookMyShow) (concert variant — noted separately in Notes) | https://algomaster.io/learn/lld | free | — | Medium |
| Design Social Network Service like Facebook | Social network | https://algomaster.io/learn/lld | free | — | Medium |
| Design Spotify | Music streaming (Spotify) | https://algomaster.io/learn/lld | free | — | Hard |
| Design Amazon | Online shopping (Amazon) | https://algomaster.io/learn/lld | free | — | Hard |
| Design LinkedIn | LinkedIn | https://algomaster.io/learn/lld | free | — | Hard |
| Design CricInfo | Cricinfo / sports scoreboard | https://algomaster.io/learn/lld | free | — | Hard |
| Design Chess Game | Chess | https://algomaster.io/learn/lld | free | — | Hard |
| Design Coffee Vending Machine | Coffee machine | https://algomaster.io/learn/lld | free | — | Hard |
| Design Restaurant Management System | Restaurant management | https://algomaster.io/learn/lld | free | — | Hard |
| Design Online Stock Exchange | Stock brokerage | https://algomaster.io/learn/lld | free | — | Hard |
| Design Course Registration System | Course registration | https://algomaster.io/learn/lld | free | — | Hard |
| Design Movie Ticket Booking System | Movie ticket booking (BookMyShow) | https://algomaster.io/learn/lld | free | — | Hard |
| Design Online Auction System | Online auction system (new canonical name — not in the seed list) | https://algomaster.io/learn/lld | free | — | Hard |
| Design Online Food Delivery Service | Food delivery | https://algomaster.io/learn/lld | free | — | Hard |
| Design Ride-Sharing Service like Uber | Ride sharing (Uber) | https://algomaster.io/learn/lld | free | — | Hard |

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Object Oriented Programming (9 lessons) | Classes & Objects · Interfaces · Inheritance · Polymorphism · Abstraction · Encapsulation · Aggregation · Composition · Association | https://algomaster.io/learn/lld |
| Design Principles (10 lessons) | DRY · KISS · YAGNI · Law of Demeter · SRP · OCP · LSP · ISP · DIP · SOLID Principles - Summary | same |
| UML Diagrams (5 lessons) | Class Diagram · Use Case Diagram · Sequence Diagram · Activity Diagram · State Machine Diagram | same |
| Design Patterns - Creational (5 lessons) | Singleton · Factory Method · Abstract Factory · Builder · Prototype | same |
| Design Patterns - Structural (7 lessons) | Adapter · Facade · Decorator · Composite · Proxy · Bridge · Flyweight | same |
| Design Patterns - Behavioral (10 lessons) | Iterator · Observer · Strategy · Command · State · Template Method · Visitor · Mediator · Memento · Chain of Responsibility | same |
| Interview Guidance (1 lesson) | "How to Answer a LLD Interview Question" | same |
| Interview Problems - Easy (5 problems) | see Table 1 | same |
| Interview Problems - Medium (15 problems) | see Table 1 | same |
| Interview Problems - Hard (13 problems) | see Table 1 | same |

## Codemia — Object-Oriented / Low-Level Design

- `URL:` https://codemia.io/object-oriented-design
- `Licence / access:` freemium platform — "free access to selected problems," premium subscription
  for "unlimited access to all problems, solutions, and mock interviews" (per https://codemia.io/).
  On the object-oriented-design listing itself every problem showed as "To Do" (unpurchased) with
  premium/company-tag gating; which specific problems are in the free tier was not distinguishable
  from the fetched list.
- `Authority:` Codemia is a dedicated interview-prep platform (system design, DSA, OOD, ML system
  design, agentic AI, peer mock interviews); the homepage gives no founder/team bio or credentials,
  so authority here rests on the platform's own scale and reputation rather than a named author.
- `Languages:` not stated for the OOD/LLD track specifically; the separate DSA track advertises "8
  Programming Languages" but Codemia's homepage does not enumerate them, and no Python-specific
  claim was seen for OOD problems.
- `Fetched:` 2026-09-20, via WebFetch on https://codemia.io/object-oriented-design (full 71-problem
  list with difficulty tiers rendered on-page) and https://codemia.io/ (pricing/authority check).

**Table 1 — problems**

| Problem (the source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design a Parking Lot | Parking lot | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Vending Machine | Vending machine | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Tic-Tac-Toe Game | Tic-tac-toe | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Deck of Cards | Deck of cards / blackjack | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Logger System | Logger / logging framework | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Stack and Queue | Stack and queue (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Traffic Light System | Traffic signal | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Coffee Machine | Coffee machine | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Bank Account System | Bank account system | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Shape Calculator | Shape calculator (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Easy |
| Design a Warehouse Management System | Warehouse management (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Banking System | Bank account system | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design an Elevator System | Elevator system | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design an Online Shopping System | Online shopping (Amazon) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Learning Management System | Learning management system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design an ATM | ATM | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Social Media Platform | Social network | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design an IoT Smart Home System | IoT smart home system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Chess Game | Chess | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Hotel Booking System | Hotel booking | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Ride-Sharing Service | Ride sharing (Uber) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Library Management System | Library management | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Movie Ticket Booking System | Movie ticket booking (BookMyShow) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Restaurant Order System | Restaurant management | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Car Rental System | Car rental | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design an Airline Booking System | Airline management | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Task Management System | Task scheduler | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design an Online Auction System | Online auction system | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Bowling Alley System | Bowling alley system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Pharmacy Management System | Pharmacy management system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Contact Management System | Contact management system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Music Player | Music streaming (Spotify) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Voting Booth System | Voting booth system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Coupon and Discount System | Coupon and discount system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Warehouse Inventory Tracker | Inventory management | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Chat Application | Chat application (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Snake Game | Snake and ladder (Snake-only variant) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Blackjack Game | Deck of cards / blackjack | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design an Event Emitter | Event bus | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a Workout Planner | Workout planner (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Medium |
| Design a File Sharing Platform | File sharing platform (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Food Delivery System | Food delivery | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a File System | In-memory file system | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Calendar System | Meeting scheduler / calendar | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Payment Gateway System | Payment gateway system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Notification System | Notification service | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Video Streaming Platform | Video streaming platform (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Text Editor with Undo/Redo | Text editor / undo-redo | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Spreadsheet | Spreadsheet | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Workflow Engine | State machine / workflow engine | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Business Rule Engine | Business rule engine (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Plugin System | Plugin system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Stock Portfolio Manager | Stock brokerage | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Multi-player Card Game Framework | Multi-player card game framework (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design an Object Pool | Object pool (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design an Email Client | Email client (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Music Streaming App | Music streaming (Spotify) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design an E-commerce Cart and Checkout | E-commerce cart and checkout (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Middleware Chain | Middleware chain (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Parking Garage with Dynamic Pricing | Parking lot (dynamic-pricing variant) | https://codemia.io/object-oriented-design | paywalled | outline | Hard |
| Design a Resource Management System | Resource management system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design a Game State Management System | Game state management system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design an Entity-Component System | Entity-component system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design an Operating System Task Scheduler | Job scheduler | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design a Compiler Lexer and Parser | Compiler lexer and parser (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design an LRU Cache | LRU cache | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design a Code Editor | Code editor (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design a Permission and Role System | Permission and role system (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design a Board Game Framework | Board game framework (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |
| Design a Game Physics Engine | Game physics engine (new canonical name — not in the seed list) | https://codemia.io/object-oriented-design | paywalled | outline | Advanced |

Depth is marked `outline` for all 71 because the listing page shows only title + difficulty +
lock state; individual problem pages (with their actual class diagrams/code) were not fetched.

Codemia has no Table 2: the object-oriented-design page is a flat, difficulty-tiered problem
catalogue with no concept curriculum (no OOP/patterns/principles module structure observed), so
it is a problem list, not a subject-teaching source.

## workat.tech — Machine Coding

- `URL:` https://workat.tech/machine-coding (guide/article hub) and
  https://workat.tech/machine-coding/practice (problem list).
- `Licence / access:` all problems and guide articles fetched showed as **free**; no lock/premium
  indicator was observed on either page (workat.tech is known to also sell company-specific
  interview-prep bundles elsewhere on the site, but nothing on these two pages was paywalled).
- `Authority:` workat.tech (formerly "Interview Bit"-adjacent / IIT-founder-run prep platform) is a
  widely used Indian SDE-interview-prep site; its machine-coding track is commonly recommended
  alongside Educative/DesignGurus in LLD prep roundups for its India-market SDE-I/II/III framing.
- `Languages:` not stated on either fetched page — no programming language was named for the
  practice-problem solutions or editorials.
- `Fetched:` 2026-09-20, via WebFetch directly on both pages; both rendered fully, no fallback needed.

**Table 1 — problems**

| Problem (the source's own title) | Canonical name | URL | Access | Depth | Difficulty |
|---|---|---|---|---|---|
| Design a Parking Lot | Parking lot | https://workat.tech/machine-coding/practice/design-parking-lot-qm6hwq4wkhp8/index.html | free | outline | SDE I/II |
| Design Splitwise | Splitwise / expense sharing | https://workat.tech/machine-coding/practice/splitwise-problem-0kp2yneec2q2/index.html | free | outline | SDE I/II |
| Design Chess Validator | Chess | https://workat.tech/machine-coding/practice/design-chess-validator-to77d8oqpx2h/index.html | free | outline | SDE I/II |
| Design Snake And Ladder | Snake and ladder | https://workat.tech/machine-coding/practice/snake-and-ladder-problem-zgtac9lxwntg/index.html | free | outline | SDE I |
| Design 2048 Game | 2048 game (new canonical name — not in the seed list) | https://workat.tech/machine-coding/practice/design-2048-game-osycd22zpn1y/index.html | free | outline | SDE I |
| Design Tic-Tac-Toe | Tic-tac-toe | https://workat.tech/machine-coding/practice/design-tic-tac-toe-smyfi9x064ry/index.html | free | outline | SDE I |
| Design a Library Management System | Library management | https://workat.tech/machine-coding/practice/design-library-management-system-jgjrv8q8b136/index.html | free | outline | SDE II |
| Design Trello | Task scheduler (Trello/kanban-board variant) | https://workat.tech/machine-coding/practice/trello-problem-t0nwwqt61buz/index.html | free | outline | SDE II |
| Design an In-Memory Key-Value Store | In-memory key-value store | https://workat.tech/machine-coding/practice/design-key-value-store-6gz6cq124k65/index.html | free | outline | SDE II/III |
| Design a Distributed Queue \| Kafka | Distributed queue / Kafka-style broker (new canonical name — not in the seed list; overlaps Pub-sub / message broker) | https://workat.tech/machine-coding/practice/design-distributed-queue-cuudq0sk0v14/index.html | free | outline | SDE II/III |
| How to design Snake and Ladder? (editorial) | Snake and ladder | https://workat.tech/machine-coding/editorial/how-to-design-snake-and-ladder-machine-coding-ehskk9c40x2w/ | free | walkthrough | — |
| How to design Splitwise? (editorial) | Splitwise / expense sharing | https://workat.tech/machine-coding/editorial/how-to-design-splitwise-machine-coding-ayvnfo1tfst6/ | free | walkthrough | — |

Depth is `outline` for the practice-list entries because the listing page shows only title +
difficulty + link (the problem statement pages themselves were not individually fetched); the two
editorial articles are `walkthrough` since editorials by definition explain a worked design.

**Table 2 — outline**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Getting-started guides | What is a Machine Coding Round? · How to prepare for machine coding round? · Machine Coding Round Practice Questions for Interviews · How to ace the machine coding round? | https://workat.tech/machine-coding |
| Editorials | How to design Snake and Ladder? · How to design Splitwise? | https://workat.tech/machine-coding |
| Clean Code / Software Design tutorial series | Introduction to Clean Code and Software Design Principles · How to Write Meaningful Variable Names · How to Design Good Functions and Classes · Software Design Principles (DRY, YAGNI, KISS) · Software Design Principles (Abstraction, Extensibility, Cohesion) · SOLID Design Principles · Introduction to Software Design Patterns | https://workat.tech/machine-coding |

## Exponent (Aced) and interviewing.io — checked, no dedicated OOD/LLD material found

- `URL:` https://www.tryexponent.com/courses/software-engineering,
  https://www.tryexponent.com/courses/system-design-interviews (Exponent rebranded to "Aced" —
  both URLs now redirect into the Aced platform), https://interviewing.io/, and
  https://interviewing.io/questions?topic=object-oriented-design.
- `Licence / access:` n/a — no dedicated content to assess.
- `Authority:` n/a.
- `Languages:` n/a.
- `Fetched:` 2026-09-20, via WebFetch on all four URLs above. `/courses/object-oriented-design` on
  Aced does not exist (renders only the site's generic nav/footer template, confirming no such
  course page); `interviewing.io/guides/object-oriented-design-interview` returned HTTP 404.
- **Finding:** Aced's Software Engineering and System Design course pages list high-level modules
  (System Design, Software Engineering, Product Management, Machine Learning, Data Engineering,
  etc.) but their fetched navigation/footer content named no object-oriented-design or low-level-
  design module, and no dedicated LLD problems (parking lot, elevator, LRU cache as a *design*
  problem) were listed anywhere reachable. interviewing.io's question database is organized by
  Data Structures and Algorithms / System Design / Mathematics, with general problems like
  "LRU Cache" appearing as a DSA/coding question rather than tagged as object-oriented design; no
  OOD/LLD-specific guide, course, or question bank was found on interviewing.io. Neither source
  gets a Table 1 or Table 2 — there is nothing on either site that teaches this subject or lists
  LLD problems as such, at least not through the pages this fetch could reach (both sites likely
  render more content client-side or behind login than WebFetch could see).

## Refactoring.Guru — design patterns catalogue and refactoring/code-smells catalogue

- `URL:` https://refactoring.guru/design-patterns/catalog and https://refactoring.guru/refactoring/smells
- `Licence / access:` the catalogue pages (patterns and smells) are free to read; the site upsells
  a paid "Design Patterns eBook" and a paid "Refactoring Course" as premium products, but the
  catalogue content itself is public reference material.
- `Authority:` Refactoring.Guru is Alexander Shvets's long-running, widely cited reference for the
  Gang-of-Four design patterns and Martin Fowler's refactoring/code-smells catalogue, extensively
  linked from interview-prep material (including several sources above) as the canonical plain-
  language explanation of each pattern/smell.
- `Languages:` the design-patterns catalogue explicitly offers code examples in multiple languages
  including **Python** (confirmed on the catalogue page); per-pattern example pages were not
  individually fetched to confirm Python coverage pattern-by-pattern.
- `Fetched:` 2026-09-20, via WebFetch directly on both catalogue pages; both rendered fully, no
  fallback needed.

Per the task instructions this source gets **Table 2 only** (it teaches the subject as a
reference catalogue, not as a list of LLD interview problems).

**Table 2 — outline (design patterns catalogue)**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Creational Patterns | Factory Method · Abstract Factory · Builder · Prototype · Singleton | https://refactoring.guru/design-patterns/catalog |
| Structural Patterns | Adapter · Bridge · Composite · Decorator · Facade · Flyweight · Proxy | https://refactoring.guru/design-patterns/catalog |
| Behavioral Patterns | Chain of Responsibility · Command · Iterator · Mediator · Memento · Observer · State · Strategy · Template Method · Visitor | https://refactoring.guru/design-patterns/catalog |

**Table 2 — outline (refactoring / code smells catalogue)**

| Section | Sub-topics the source lists | URL |
|---|---|---|
| Bloaters | Long Method · Large Class · Primitive Obsession · Long Parameter List · Data Clumps | https://refactoring.guru/refactoring/smells |
| Object-Orientation Abusers | Alternative Classes with Different Interfaces · Refused Bequest · Switch Statements · Temporary Field | https://refactoring.guru/refactoring/smells |
| Change Preventers | Divergent Change · Parallel Inheritance Hierarchies · Shotgun Surgery | https://refactoring.guru/refactoring/smells |
| Dispensables | Comments · Duplicate Code · Data Class · Dead Code · Lazy Class · Speculative Generality | https://refactoring.guru/refactoring/smells |
| Couplers | Feature Envy · Inappropriate Intimacy · Incomplete Library Class · Message Chains · Middle Man | https://refactoring.guru/refactoring/smells |

## Other widely recommended sources — one attempted, several checked and found inaccessible or without LLD content

### ashishps1/awesome-low-level-design (GitHub)

- `URL:` https://github.com/ashishps1/awesome-low-level-design
- `Licence / access:` **GPL-3.0**, confirmed by reading the repo's `LICENSE` file (GNU General
  Public License, Version 3, 29 June 2007). Free to read on GitHub.
- `Authority:` maintained by GitHub user `ashishps1` — Ashish Pratap Singh, the same author as the
  AlgoMaster.io course above; this repo is his free, independently-starred GitHub companion list
  and is one of the most-forked "awesome" LLD problem lists on GitHub, cited across many other prep
  blogs' "resources" sections.
- `Languages:` the `solutions/` folder contains one subdirectory per language — `cpp`, `csharp`,
  `golang`, `java`, `python`, `typescript` — confirming **Python** solutions exist.
- `Fetched:` 2026-09-20, via WebFetch on the repo README, the `LICENSE` file, and the
  `solutions/` directory tree.
- **Overlap note:** this problem list is near-identical to the AlgoMaster.io "Interview Problems"
  tiers above (same author, same 33 problems, same Easy/Medium/Hard split) — see the AlgoMaster
  section for the canonical-name mapping; not re-tabulated here to avoid duplicating identical rows.
  The one addition not observed on the algomaster.io course page: "Design Online Food Delivery
  Service like **Swiggy**" (branded variant of Food delivery) and "Design a Concert Ticket Booking
  System" moved from Medium (algomaster.io) — difficulty tiers differ slightly between the two
  even though the problem set is the same, e.g. this repo lists 7 Easy / 15 Medium / 11 Hard (33
  total) versus algomaster.io's 5 Easy / 15 Medium / 13 Hard (33 total).

### Sites checked and found to have no reachable / no dedicated LLD content

- **CodeZym** (https://codezym.com/) — headline confirms it is an LLD/machine-coding practice
  site ("Practice machine coding of top low level design (LLD) interview questions using design
  patterns"), but the homepage is JS-rendered with no problem list in the fetched HTML, and guessed
  problem-list paths (`/problems`, `/design-problems`, `/lld-problems`) all returned HTTP 404.
  Could not produce a table for this source.
- **InterviewReady** (https://interviewready.io/) — despite its homepage headline claiming to
  teach "System Design, AI, and LLD," the only courses actually listed are **System Design Course**
  and **AI Engineering**; the System Design Course's full curriculum (fetched from
  https://interviewready.io/course-page/system-design-course — Basics, Concepts, High-Level Design,
  Research Paper Analysis, $170/one-year-access) contains **no low-level-design module** — no
  parking lot, elevator, LRU cache, or any classic OOD problem. Its "LLD" marketing claim is not
  backed by the fetched curriculum.
- **SudoCode** — `sudocode.in` does not resolve (DNS lookup failure); no working URL found for
  this source without a working web search.
- **Udit Agarwal's LLD material** and **Concept&&Coding (YouTube)** — not reachable: YouTube
  channel/playlist pages render no content through WebFetch (JS-only rendering), and no other URL
  for "Udit Agarwal LLD" could be located without WebSearch, whose budget for this session was
  already exhausted (200/200) before this source was reached.
- **GeeksforGeeks** low-level-design hub and a known parking-lot article — every guessed URL
  (`/low-level-design/`, `/system-design/low-level-design-tutorial/`,
  `/system-design/design-parking-lot-using-object-oriented-analysis/`) returned HTTP 404; GFG
  appears to block or redirect this fetch tool's requests.
- **Naukri Code360 (Coding Ninjas)** guided path — both the specific guided-path URL and the
  guided-paths index returned HTTP 403 Forbidden.
- **interviewbit.com** machine-coding page — guessed URL returned HTTP 404.
- **Udemy — "Mastering LLD with Real Life Case Studies"** (a widely recommended paid course by
  Sandeep Kaila, commonly cited in LLD prep roundups alongside the Grokking courses) — returned
  HTTP 403 Forbidden; could not verify its curriculum directly.

None of the above six inaccessible attempts are cited as a source in Tables 1/2 anywhere in this
file — only the one entry that was actually read (ashishps1/awesome-low-level-design) is recorded
with data. This section exists per the task's fallback instruction to record which path failed
when a source could not be reached.

## Notes

- **Sources actually covered with data:** Hello Interview, Educative "Grokking the Low Level
  Design Interview Using OOD Principles", DesignGurus "Grokking the Object Oriented Design
  Interview", AlgoMaster.io LLD, Codemia, workat.tech, Refactoring.Guru (patterns + smells), and
  GitHub's ashishps1/awesome-low-level-design — 8 sources with real rows. Exponent/Aced and
  interviewing.io were checked and confirmed to have no dedicated OOD/LLD material reachable.
  CodeZym, InterviewReady (confirmed no LLD content despite marketing), SudoCode, Udit Agarwal,
  Concept&&Coding, GeeksforGeeks, Naukri Code360, interviewbit.com, and one Udemy course were
  attempted and could not be reached — see the "sources checked and found inaccessible" list above.
- **WebSearch was unavailable for most of this survey.** The session's WebSearch budget (200/200)
  was already exhausted before this agent's second source (Hello Interview's problem-breakdowns
  index page, which 404'd), so every source after that point relied solely on WebFetch against
  direct or guessed URLs plus sidebar/navigation link-following. This is the main reason several
  "any other source" candidates in §9 could not be located — a `site:` search would very likely
  have found working URLs for CodeZym, SudoCode, Udit Agarwal's material, and GFG's LLD hub.
- **The five problems every curriculum-style source agrees on:** Parking lot, Elevator system,
  ATM, Vending machine, and either Chess or Tic-tac-toe appear in nearly every source that
  publishes a problem list (Hello Interview's free tier, Educative, DesignGurus, AlgoMaster,
  Codemia, and the GitHub repo). Splitwise / expense sharing, Movie ticket booking (BookMyShow),
  and Library management are the next-most-universal tier.
- **Problems only one source has (as fetched):** In-memory Key-Value Store and Distributed
  Queue|Kafka (workat.tech only); Jigsaw Puzzle (Educative only); Dependency Injection Container
  and Cache with TTL (neither appeared on any fetched source — both are in the seed canonical list
  but were not observed on any page this survey reached); many of Codemia's Hard/Advanced-tier
  problems are unique to Codemia among the sources fetched — Object Pool, Entity-Component System,
  Game Physics Engine, Board Game Framework, Permission and Role System, Middleware Chain,
  Business Rule Engine, Plugin System, Compiler Lexer and Parser, Code Editor, Email Client,
  E-commerce Cart and Checkout, Resource Management System, Game State Management System — none of
  these were seen on Hello Interview, Educative, DesignGurus, AlgoMaster, workat.tech, or the
  GitHub repo.
- **Newly popular / not in the seed canonical-name list:** Codemia alone contributes roughly 20 new
  canonical names not in the seed list (see its Table 1 — Warehouse management, IoT Smart Home
  System, Event Emitter/Event bus, Business Rule Engine, Entity-Component System, Game Physics
  Engine, etc.), suggesting Codemia's catalogue is broader/more speculative than the other
  curriculum sources, which converge on a tighter ~20–33-problem core.
- **Python coverage:** Hello Interview's three free problem breakdowns are Python-only (no other
  language observed). Educative's course and DesignGurus' course both explicitly advertise Python
  among several languages (Java/C++/C#/JS also listed). AlgoMaster's solutions are Java-only (on
  GitHub) per its course page, but ashishps1/awesome-low-level-design — the same author's separate
  GitHub repo — does carry a `python/` solutions folder alongside cpp/csharp/golang/java/typescript.
  Refactoring.Guru's pattern catalogue explicitly lists Python among its multi-language code
  examples. Codemia and workat.tech state no language for their problem/solution content.
- **How sources rank/tier problems, and the axis used:** AlgoMaster and the GitHub repo both use
  Easy/Medium/Hard, but disagree on where several problems sit (see the AlgoMaster section's
  overlap note — 5/15/13 vs. 7/15/11 for the same 33-problem set). Codemia uses a four-tier
  Easy/Medium/Hard/Advanced scheme with far more problems (71) and its own tiering, not obviously
  aligned with AlgoMaster's. workat.tech tiers by candidate seniority (SDE I / SDE I,II / SDE II,III)
  rather than problem difficulty. Hello Interview and the two Grokking courses (Educative,
  DesignGurus) give no difficulty label at all — Hello Interview instead labels *expected depth
  per candidate level* inside each problem breakdown, and both Grokking courses organize by
  problem theme/category instead of difficulty.
- **Sources that teach the subject as a curriculum (got Table 2) vs. pure problem lists (Table 1
  only):** Hello Interview, Educative, DesignGurus, AlgoMaster, workat.tech, and Refactoring.Guru
  all publish a concept curriculum. Codemia and the GitHub awesome-list are flat problem catalogues
  with no OOP/patterns/principles teaching content observed, so neither got a Table 2.
- **Sources you could not reach (full list, consolidated):** Hello Interview's
  `problem-breakdowns/` index URL (404; recovered via sidebar navigation instead) and its four
  concurrency deep-dive pages (Correctness, Coordination, Scarcity all 🔒 premium — only the free
  Introduction page was readable); CodeZym; InterviewReady's actual LLD content (site exists but
  has none); SudoCode (DNS failure); Udit Agarwal's material and Concept&&Coding (YouTube,
  unfetchable); GeeksforGeeks LLD hub and article (404 on every guessed URL); Naukri Code360
  (403); interviewbit.com (404); one Udemy LLD course (403). A working `site:` search would
  likely resolve most of these.
