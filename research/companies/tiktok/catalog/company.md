# Company and backend-stack context an interviewer may probe

Source ids as in `sources.md`. Official or peer-reviewed sources are tagged `[O*]`; blogs, aggregators and candidate posts are marked as such. Numbers are dated because ByteDance publishes few current figures; most hard numbers below are 2022-2024.

## 1. Business in one page

- **ByteDance** (private, Beijing-founded, global): "more than a dozen products and services" — TikTok, CapCut, TikTok Shop, Lark, Pico, Mobile Legends: Bang Bang; China: Toutiao, Douyin, Fanqie, Xigua, Feishu, Douyin E-commerce; "over 150,000 employees based out of nearly 120 cities" (bytedance.com/en, fetched 2026-10-24) [O4]. Mission: "Inspire Creativity, Enrich Life" [O3].
- **TikTok**: short-video app; "over a billion people around the world" (TikTok careers, tech teams page) [O1]; HQ Los Angeles and Singapore, offices incl. New York, London, Dublin, Paris, Berlin, Dubai, Jakarta, Seoul, Tokyo [O1]. US reach per the JV announcement: "more than 200 million Americans and 7.5 million businesses" (reported by a search summary of the announcement; the PDF copy could not be decoded — **verify**) [O5].
- Revenue lines a backend engineer touches: **ads/monetization** (Global Monetization Product & Technology), **TikTok Shop / Global E-commerce** ("discovery-driven e-commerce ... shoppable videos and interactive livestreams"), **TikTok LIVE** (virtual gifts, coins, creator earnings, wallet; "Live revenue engineering", "Global LIVE Wallet" teams in postings) [O1][O-jobs], **user growth** (the target role), **trust & safety R&D** (LLMs, moderation tools, rule engines, risk insights), **recommendation** (LLMs/GenAI/"LRMs", large-scale ML systems), **Global Security** [O1].
- The target team: "Innovative Growth" (San Jose) builds "growth and content optimization systems for TikTok, powered by AIGC technologies and innovative search and discovery strategies" across "Web, Lite, and other emerging platforms"; preferred skills: AIGC/LLM applications, agent frameworks, AI coding tools, experimentation platforms, SEO/GEO ("emerging AI-driven traffic channels") [O1]. This is a growth / experimentation / content-optimization backend — closer to feed/search/experiment platforms than to payments, so expect the design prompt to be product-flavored even though the most reported prompt in the pool is a payment system.

## 2. US entity, Project Texas / USDS — only as far as an interviewer might ask

- **Project Texas** (2022-2024): the earlier arrangement that put US user data in Oracle cloud under a ring-fenced "TikTok U.S. Data Security (USDS)" organization. [Background from general knowledge; the sources I fetched cover the 2026 outcome, not Project Texas itself.]
- **TikTok USDS Joint Venture LLC**, formed 2026-01-22 (announced 2026-01-23): "dedicated to the safety and security of millions of Americans ... a comprehensive data privacy and cybersecurity program ... to protect national security and secure U.S. user data, apps and the algorithm" [O5]. Ownership (The Register 2026-01-23, Wikipedia quoting the announcement): **Oracle, Silver Lake, MGX 15% each (managing investors); ByteDance 19.9%**; Dell family office and other investors the rest (sources disagree on how the remaining ~50% splits: "affiliates of certain existing ByteDance investors" vs named funds); seven-member majority-American board incl. TikTok CEO Shou Chew; CEO Adam Presser, CSO Will Farrell; Oracle hosts US user data and is "trusted security partner"; the JV will "retrain, test, and update the content recommendation algorithm on U.S. user data" in Oracle's cloud [O5]. The JV has decision authority on trust & safety and content moderation; "TikTok global's U.S. entities" (ByteDance-controlled) manage global product interoperability and "certain commercial activities, including e-commerce, advertising, and marketing" [O5, via search summary; verify against the newsroom page].
- Consequences visible in the interview data: (1) **two hiring tracks** — USDS JV roles (data security, T&S, US-infra; recruited separately; "Pinterest IC14 vs TikTok USDS 2-1" offers; one USDS senior candidate was told "pretty much the same process" as ByteDance's) and TikTok proper (ads, e-commerce, growth, LIVE); (2) a **hiring pause** around the transaction (Nov 2025 to early 2026) [R7][R5]; (3) candidates ask recruiters "which entity is this role in?" [G1 advises: "confirm which entity a US role belongs to"]. The target posting appears under TikTok proper, not the JV page [O1].
- Possible interviewer questions (inferred, none reported): why join now; how data-locality shapes design (data residency appears in the moderation design deep dive [H1]); how you handle US/China-team collaboration.

## 3. Engineering stack — what is public

Languages: **Go is the main backend language** at ByteDance ("tens of thousands of Go microservices") [O6]; postings for the target role accept **Go, Python, Java, or C++** [O1]; e-commerce postings list Java/Golang/Python/Scala/C++ [O1]; TikTok Shop transaction postings list Redis, MySQL, Linux, Java, Go [O-jobs, low]. Interviews accept any mainstream language [G1]. Platform-leaning teams name Go/C++ [G1]. So Chi's Java/Python is fine for interviews; Go would help on the job.

Frameworks (CloudWeGo, open-sourced by ByteDance) [O6]:
- **Kitex** (RPC; Thrift/gRPC): "supports over 60,000 internal services ... peak QPS in the hundreds of millions" (2022-09-30 blog). **Hertz** (HTTP): "more than 10,000 online services and a peak QPS of more than 40 million" (2022-06-21 blog). Other CloudWeGo projects (Netpoll, Volo, Eino) are from my background knowledge, not from a fetched source. Numbers are 2022; no newer official count found.

Storage and data (peer-reviewed / arXiv):
- **ByteGraph** (VLDB 2022): distributed graph DB for TikTok/Douyin/Toutiao-scale social graphs — "tens of billions of vertices and trillions of edges", two-tier (durable storage + cache layer), edge-trees for adjacency lists, geo-replication; later BG3 (SIGMOD 2024) and ByteGraph-Dione (SIGMOD Companion 2026) [O7].
- **ByteHTAP** (VLDB 2022): HTAP built on ByteDance's own OLTP system **ByteNDB** + Apache Flink, < 1 s freshness, global timestamps [O7]. (Whether TiDB is used at ByteDance: **no source confirms**; the paper cites TiDB only as related work. The brief's "TiDB" is unverified.)
- **ByteHouse** (arXiv 2602.08226, Feb 2026): cloud-native data warehouse for real-time multimodal analytics, ClickHouse lineage; open-source sibling **ByConity** (2023); an internal KV store "ByteKV" is mentioned in passing [O7]. Krypton (VLDB 2023): real-time serving + analytical SQL engine [O7 title only].
- **Messaging and streaming:** ByteDance runs a Kafka-API-compatible cloud-native layer **ByteMQ/BMQ** (SoCC 2024) — secondary summary: "tens of TB/s" consume throughput, 99.76% of former Kafka workloads migrated, ~70% resource saving (**verify against the paper**) [O7, blog]; **Flink** at very large scale — StreamShield (arXiv 2602.03189, Feb 2026): "over 70,000 concurrent streaming jobs", "more than 11 million resource slots"; StreamOps (VLDB 2023) [O7]. BitSail (open-source data integration) is cited with "hundreds of trillions of records per day" by a secondary article [blog]. Interviews still ask Kafka concepts (partitions, rebalancing, retained log vs queue, ordering/durability) [G1][P1].
- **Recommendation:** Monolith (arXiv 2209.07663, 2022): real-time online training with a collisionless cuckoo-hash embedding table, expirable embeddings, parameter sync between training and serving; Kafka action/feature queues + Flink joiner (as described by secondary summaries) [O7, blog]. The Fahim ul Haq article suggests reading it for constraints, not predictions [SU].
- Observed in interview questions rather than documentation: MySQL clustered/secondary indexes, Redis persistence and sorted sets, Elasticsearch inverted index/mapping, MongoDB migration question, Hadoop (an infra candidate was matched to a Hadoop team), Linux/networking basics [G1][P3].
- Candidates and sources mention Lark (internal suite) for code pads and meetings [G1].

## 4. Scale numbers you can quote (with year and strength)

| Claim | Year | Source | Strength |
|---|---|---|---|
| ByteDance >150,000 employees, ~120 cities | 2026 | bytedance.com [O4] | official |
| TikTok serves "over a billion people" | 2026 | lifeattiktok.com [O1] | official, vague |
| >200M Americans, 7.5M US businesses | 2026-01 | JV announcement via search summary [O5] | secondary |
| ByteGraph: tens of billions of vertices, trillions of edges | 2022 | VLDB [O7] | peer-reviewed |
| Hertz: >10,000 services, >40M peak QPS; Kitex: >60,000 services, hundreds of millions peak QPS | 2022 | CloudWeGo blog [O6] | official, old |
| Flink: >70,000 concurrent jobs, >11M slots | 2026-02 | arXiv (via secondary summary) [O7] | medium |
| BMQ: tens of TB/s consume; ~70% cost cut | 2024 | SoCC paper (via secondary) [O7] | medium |
| Douyin and Toutiao "hundreds of millions of daily active users"; analytics "petabytes of data" | 2022 | ByteHTAP paper [O7] | peer-reviewed |
| Compensation anchors | 2026 | see `loop.md` §8 | candidate-reported |

## 5. Organization and working conditions that show up in interviews

- Teams hire for themselves; interviewers come from the hiring team, many in China/Singapore; some rounds at night US time; recruiters often Asia-based [G1][B-tl].
- Office rule: minimum three days/week, up to five by team [O2].
- Reorg and headcount churn are the main sources of loop disruption: reqs closed mid-loop, rematches, pause/freeze rumors, "reorg ... the company is growing too fast" (insider comment, Reddit 2026-01) [R7][A1].
- Stock/liquidity: RSUs vest 4 years (20/25/25/30 after 2024 change) with limited buybacks; critics say "the stock is worth pennies"; levels.fyi shows stock at ~$84K/yr for 2-2 [LV][B9][B-comp]. No IPO.
- Culture (official list in `behavioral.md`) vs reputation (Blind: long hours, Mandarin advantage) — opinions only.
