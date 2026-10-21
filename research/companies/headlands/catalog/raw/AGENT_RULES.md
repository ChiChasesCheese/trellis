# Research agent rules — Headlands kit (P1)

Context: Chi passed the Headlands Technologies HackerRank coding test (Java, Software Engineer)
and is invited to a **one-hour technical video call (phone screen)**. We are building the kit at
`vault/interviews/companies/headlands/`, same methodology as `companies/millennium/` (read its
`catalog/raw/sources_index.md` and `catalog/raw/coding_first_round.md` for the expected shape).

1. You own exactly one output file (named in your task). Never write anywhere else. Do not commit.
   Do not spawn agents.
2. Resume rule: if your output file already exists, read it and only add what is missing.
3. Every fact carries the source URL and the post/fetch date. Nothing rewritten: quote or
   closely paraphrase, and mark your own inference as `推断`.
4. Each source row gets reachability (200 / 摘要 = search snippet only / 403 / 429 / CF / login wall)
   and confidence: 高 first-hand or official · 中 first-hand but snippet-only, or dated aggregator ·
   低 SEO. lodely.com and vervecopilot are never cited. A single failed fetch never condemns a site:
   record which path failed and try a mirror (Google cache, archive.org, 1p3a mobile `m.1point3acres.com`,
   jina reader `r.jina.ai/<url>`).
5. The repo is public: no names of Chi's interviewers/recruiters, no email content, no personal data.
6. Focus order: SWE phone screen / technical video call content > HackerRank coding test content >
   onsite / superday > everything else. Separate SWE from quant researcher / trader reports.
7. File language: tables and headings in Chinese, quoted source text in its original language.
8. End your file with a "缺口" section: what you could not reach and which URL Chi should open by hand.
9. Final reply to the orchestrator: ≤ 15 lines — row counts, the 3 strongest findings with URLs,
   your weakest claims.
