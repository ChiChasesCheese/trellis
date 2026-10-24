# Task — TikTok / ByteDance interview research, Chinese platforms

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never switch branches, never spawn agents. You
write only `research/companies/tiktok/catalog/raw/forums_cn.md`, `catalog/raw/1p3a.md`, `catalog/raw/hellointerview.md`
and `catalog/raw/aggregators_cn.md`. Research area: provenance belongs here.

Target: Chi, backend engineer, preparing for TikTok / ByteDance **senior backend** loops in the US (TikTok US, USDS,
ByteDance US offices); also collect 字节跳动 China 社招 / 校招 backend reports when they show the same problem style,
marked as China. 字节 / TikTok / 抖音 / 飞书 / 头条 are all ByteDance.

Collect every interview report in the window: 1point3acres (面经 for TikTok and 字节跳动), nowcoder (牛客 字节 后端 面经),
CSDN / 掘金 / 知乎 snippets, Chinese aggregators and GitHub mirrors (`atomeocean/job-compass` and others found by
`gh api search`), Hello Interview community questions for TikTok and ByteDance. For each: date, URL, level / team /
location, round, each problem (LC number or precise description incl. follow-ups), system design prompts, behavioural
questions, confidence.

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

Reply ≤ 10 lines: per platform how many reports you got and how (or why not), the most frequent problems and system
design prompts, and anything that looks like a TikTok-specific variant of a LeetCode problem.
