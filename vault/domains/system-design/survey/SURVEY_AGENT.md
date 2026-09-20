# Surveying system design interview problems — instructions for one agent

Goal: an honest inventory of **which system design interview problems each source
teaches**, with a URL for every row. This inventory decides which problems become
leaves of a study domain, so a missing problem is a real loss and an invented one is
worse. Record only what you actually saw on a page or in a repository.

You own exactly one output file (named in your task). Write nothing else. Do not run
git. Do not start other agents.

## Resume rule

If your output file already exists, read it, keep what is there, and continue from the
first source that has no section yet.

## What to write

One `## <Source name>` section per source, each with:

- `URL:` the page that lists the problems (table of contents, problem index, README).
- `Licence / access:` e.g. `CC-BY-4.0`, `MIT`, `free to read`, `partly paywalled`,
  `paid book`. For a GitHub repo, read its LICENSE.
- `Authority:` one sentence — who wrote it and why it is taken seriously (stars, authors'
  background, how widely it is cited).
- `Fetched:` today's date and how (WebFetch, gh api, search result). If a fetch failed,
  say which path failed and what you fell back to; one failed fetch never condemns a site.
- A table, one row per problem the source teaches:

  | Problem (the source's own title) | Canonical name | URL | Access | Depth |
  |---|---|---|---|---|

  - **Canonical name**: a short normalised name so the same problem lines up across
    sources, e.g. `URL shortener`, `News feed / timeline`, `Chat / messaging`,
    `Rate limiter`, `Web crawler`, `Notification system`, `Typeahead / autocomplete`,
    `Video streaming (YouTube/Netflix)`, `File sync (Dropbox/Drive)`, `Ride hailing (Uber)`,
    `Proximity / nearby search (Yelp)`, `Ticket booking (Ticketmaster)`, `Payment system`,
    `Distributed cache`, `Key-value store`, `Unique ID generator`, `Distributed job scheduler`,
    `Ad click aggregation`, `Metrics / monitoring`, `Stock exchange`, `Digital wallet`,
    `Hotel reservation`, `Email service`, `Distributed message queue`, `Object storage (S3)`,
    `Leaderboard`, `Google Docs / collaborative editing`, `Search engine`, `Top-K / heavy hitters`,
    `Online judge (LeetCode)`, `Pastebin`, `Instagram / photo sharing`, `Tinder`, `WhatsApp`,
    `Live comments`, `Web analytics`, `Price tracker`, `Auction`, `Food delivery`.
    Invent a new canonical name when none fits; keep names consistent within your file.
  - **Access**: `free`, `paywalled`, or `book`.
  - **Depth**: `outline` (a list of bullets), `walkthrough` (a full worked answer), or
    `deep` (worked answer plus deep dives / alternatives / numbers).

- Skip pure concept pages (CAP theorem, consistent hashing as a topic). Only *design X*
  problems. A building-block design problem such as "design a rate limiter" or "design a
  distributed cache" does count.
- Never cite AI content farms (lodely, vervecopilot and similar generated listicles).
- End the file with `## Notes`: anything surprising — problems only one source has,
  problems that seem newly popular, sources you could not reach.

Finish by replying with: the number of sources covered, the number of table rows, and the
path of your file.
