# Task — research the TikTok / ByteDance software-engineer interview (senior backend), for an end-to-end kit

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never switch branches, never spawn agents. You
write only under `research/companies/tiktok/catalog/`. This is the research area: provenance belongs here (URLs, dates,
how sure each claim is). Nothing you write goes into `vault/`.

Target: Chi, a backend engineer (Java / Python, payments and data pipelines), considering **TikTok Senior Backend
Software Engineer** roles in the US (e.g. "Innovative Growth"); prepare to the senior bar. TikTok and ByteDance run the
same interview machine; treat them together and note real differences.

## Your half: GitHub + English platforms

GitHub first, then LeetCode Discuss, Reddit, Blind, HN, Glassdoor snippets, prachub / interviewdb / csoahelp / levels.fyi, official TikTok / ByteDance careers pages.
Write `catalog/raw/github_repos.md`, `catalog/raw/forums_en.md`, `catalog/raw/official.md`, and the synthesis files below.

## Collect (synthesis files)

1. `loop.md` — the process end to end: recruiter call, OA (platform, length, number and level of problems), phone
   screens, onsite / virtual rounds (how many, what each covers, length), whether every round has coding (incl. SD and
   HM rounds), language rules, whether code is run, team matching, timeline, level mapping (1-2 / 2-1 / 2-2 …), and
   what "senior" changes. Cite each claim; mark confidence (several independent reports / one report / unclear).
2. `coding.md` — what coding rounds look like: difficulty mix, follow-ups, whether interviewers want optimal first,
   typical recently reported problems (LC numbers where given), non-LC variants.
3. `system_design.md` — system design prompts reported for TikTok / ByteDance backend (e.g. video feed, upload and
   transcoding, live streaming and gifts, comments, likes / counters, notifications, ads click aggregation, rate
   limiter, leaderboard, search, recommendation serving, short URL…). For each: how often reported, what the
   interviewer pushed on.
4. `behavioral.md` — the culture and values interviewers probe (ByteStyle: "Always Day 1", "Champion Diverse
   Perspectives", "Be Candid and Clear", "Seek Truth and Be Grounded", "Have Courage to Think Big", "Aim for the
   Highest", "Be Open and Humble", "Be Courageous"… — get the current official list), typical HM questions, and how
   the HM round is weighted.
5. `company.md` — what the business and backend stack look like (products, scale numbers that are public, known
   tech: Go / Java / Python / C++, Kitex / Hertz / CloudWeGo, ByteHouse, Kafka, Flink, TiDB …), US entity and data
   (Project Texas / USDS) context only as far as an interviewer might ask.
6. `sources.md` — every source with URL, date, type (official / candidate report / blog / forum) and what it gave.

Rules: Chinese or English is fine in research files. Do not invent; if sources disagree, record both. No personal data
of interviewers or candidates. Reply ≤ 10 lines: files written, the 5 most important findings for preparation, and the
biggest open questions.

## How to reach each platform (verified on earlier kits — read before fetching)

| Platform | Method |
|---|---|
| GitHub | **first, always**: `gh api -X GET search/repositories -f q="tiktok interview"` (also "bytedance interview", "字节 面经", "tiktok oa", "tiktok system design", "company wise leetcode"), `search/code` with short queries ("tiktok" "phone screen", "字节跳动 面经 后端"); fetch every company-specific file; `git clone` works when the API is throttled |
| LeetCode Discuss | HTML is 403; `POST https://leetcode.com/graphql` works: list posts by search (`ugcArticleDiscussionArticles` / `discussQuestionTopicsList`, query "tiktok" / "bytedance") then `ugcArticleDiscussionArticle(topicId)` for the body |
| Reddit | `reddit.com` HTML/`.json` blocked; use `.rss` (`r/<sub>/search.rss?q=tiktok&restrict_sr=1&sort=new`, single post `/comments/<id>/.rss` includes comments) or the Arctic Shift archive API `arctic-shift.photon-reddit.com/api/posts/search?subreddit=leetcode&title=tiktok` (r/leetcode, r/csMajors, r/cscareerquestions, r/ExperiencedDevs, r/developersIndia) |
| Blind (teamblind.com) | works with a browser User-Agent header; bot UAs get 403 |
| Hacker News | Algolia API `hn.algolia.com/api/v1/search?query=tiktok%20interview` |
| prachub / interviewdb / csoahelp / programhelp / oavoservice / levels.fyi / nowcoder / CSDN | fetch directly; CSDN mixes AI content farms (fake dates) — judge each post |
| 1point3acres | Cloudflare blocks plain fetches. Try in order: the public tRPC list `www.1point3acres.com/interview/company/<slug>` (find the company slug for TikTok and for 字节跳动), the Playwright browser tools (`mcp__plugin_playwright_playwright__*`, load via ToolSearch) for list pages, and Chinese mirrors (`atomeocean/job-compass` on GitHub). Body text behind the points wall stays "隐藏" — record what is visible |
| Hello Interview | `hellointerview.com/community/questions?company=TikTok` (and ByteDance): try the page and the Playwright browser; record type (coding / system design / OOD / behavioral), approximate date, level, description |
| Glassdoor / 知乎 / 脉脉 / medium | mostly 403: use WebSearch snippets only, mark low confidence |
| 小红书 | search is a dead end without login; only fetch share links you find elsewhere |
| Never cite | lodely.com, vervecopilot.com (AI question farms) |

Window: reports from **2025-10 to today (2026-10-24)**, newest first; older only for process background. Record per report:
date, platform + URL, level / team / location, round (OA / phone / onsite n / HM), each problem (LC number if
identifiable, else a precise description incl. constraints and follow-ups), and confidence (high = first-hand post with
the problem text; medium = summary that names the problem; low = fragment or SEO).
