# Surveying low-level design (LLD / OOD / machine coding) — instructions for one agent

Goal: an honest inventory of **(a) which low-level design interview problems each source
teaches** and **(b) how each source outlines the subject**, with a URL for every row. The
first decides which problems become leaves of a study domain; the second decides the concept
skeleton. A missing row is a real loss and an invented one is worse: record only what you
actually saw on a page or in a repository.

"Low-level design" here means the interview round also called object-oriented design or machine
coding: model a system as classes and working code in ~45–90 minutes (parking lot, elevator,
LRU cache, Splitwise, in-memory key-value store, rate limiter…). It does not mean distributed
system design. The learner works in **Python**, so note Python material whenever you see it.

You own exactly one output file (named in your task). Write nothing else. Do not run git. Do not
start other agents.

## Resume rule

If your output file already exists, read it, keep what is there, and continue from the first
source that has no section yet.

## What to write

One `## <Source name>` section per source, each with:

- `URL:` the page that lists the problems or the table of contents.
- `Licence / access:` e.g. `MIT`, `CC-BY-4.0`, `free to read`, `partly paywalled`, `paid course`,
  `paid book`. For a GitHub repo, read its LICENSE file.
- `Authority:` one sentence — who wrote it and why it is taken seriously.
- `Languages:` which programming languages its solutions use; say explicitly whether **Python**
  solutions exist and where.
- `Fetched:` today's date and how. If a fetch failed, say which path failed and what you fell
  back to; one failed fetch never condemns a site.
- **Table 1 — problems**, one row per problem the source teaches:

  | Problem (the source's own title) | Canonical name | URL | Access | Depth | Difficulty |
  |---|---|---|---|---|---|

  - **Canonical name**: a short normalised name so the same problem lines up across sources,
    e.g. `Parking lot`, `Elevator system`, `Vending machine`, `ATM`, `Library management`,
    `LRU cache`, `LFU cache`, `Rate limiter`, `Logger / logging framework`, `Pub-sub / message broker`,
    `In-memory key-value store`, `In-memory file system`, `Tic-tac-toe`, `Chess`, `Snake and ladder`,
    `Deck of cards / blackjack`, `Splitwise / expense sharing`, `Movie ticket booking (BookMyShow)`,
    `Hotel booking`, `Car rental`, `Ride sharing (Uber)`, `Food delivery`, `Online shopping (Amazon)`,
    `Stack Overflow`, `Social network`, `LinkedIn`, `Meeting scheduler / calendar`, `Task scheduler`,
    `Job scheduler`, `Thread pool`, `Bounded blocking queue`, `Connection pool`, `Notification service`,
    `URL shortener (LLD)`, `Text editor / undo-redo`, `Spreadsheet`, `Bank account system`,
    `Stock brokerage`, `Digital wallet`, `Inventory management`, `Amazon locker`, `Traffic signal`,
    `Coffee machine`, `Airline management`, `Restaurant management`, `Cricinfo / sports scoreboard`,
    `Music streaming (Spotify)`, `Course registration`, `Snake game`, `Minesweeper`, `Elevator`,
    `Cache with TTL`, `Event bus`, `Dependency injection container`, `State machine / workflow engine`.
    Invent a new canonical name when none fits; keep names consistent within your file.
  - **Access**: `free`, `paywalled`, or `book`.
  - **Depth**: `outline` (requirements and class names only), `walkthrough` (a worked design with a
    class diagram), or `code` (a worked design with runnable code — say the language, e.g.
    `code (Java, Python)`).
  - **Difficulty**: the source's own label if it gives one (easy / medium / hard), else `—`.

- **Table 2 — outline**, only for sources that teach the *subject* (a course, a book, a guide, a
  curated roadmap), one row per top-level heading and its notable sub-headings:

  | Section | Sub-topics the source lists | URL |
  |---|---|---|

  Copy the source's own headings; do not tidy them. This is what the concept skeleton is built from.

- Never cite AI content farms or generated listicles with no identifiable author.
- End the file with `## Notes`: problems only one source has, problems that seem newly popular,
  what is Python-specific, how sources rank or tier problems, and sources you could not reach.

Finish by replying with: the number of sources covered, the number of rows in each table, and the
path of your file.
