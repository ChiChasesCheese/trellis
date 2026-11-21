# ai-industry — build record

## Sources surveyed (step 1)

Surveyed 2026-11-20. GitHub has no useful curated list for the economics side (search hit the rate limit before a second try).

| # | Source | URL | Licence | Covers |
|---|---|---|---|---|
| 1 | Stanford HAI, AI Index Report 2025 (authoritative; 2026 edition not opened) | https://hai.stanford.edu/ai-index/2025-ai-index-report | free-online | 8 chapters: R&D, technical performance, responsible AI, economy, science and medicine, policy, education, public opinion. Fetched numbers: US private AI investment $109.1B vs China $9.3B (2024); 280-fold inference cost drop for GPT-3.5 level; open/closed gap 8% to 1.7% |
| 2 | Epoch AI data hub | https://epoch.ai/data | free-online (CC-BY data) | models database (3,700+), data centers, chip sales, chip components (wafer, CoWoS, HBM), chip owners and users, GPU clusters, company revenue, ChatGPT usage |
| 3 | State of AI Report | https://www.stateof.ai/ | free-online | latest is the 2026 edition (9th): research, industry, politics, safety, predictions with scorecard. Headline figures seen only on the landing page, not verified |
| 4 | Mary Meeker / BOND, Trends: Artificial Intelligence (May 2025, ~340 pages) | bondcap.com (PDF not opened) | free-online | adoption speed, capex, revenue vs compute cost, China. Only secondary coverage read |
| 5 | SemiAnalysis public posts | https://newsletter.semianalysis.com | mostly paywalled; free posts and InferenceX benchmark public | HBM, accelerator economics, GPU cloud, InferenceMAX/InferenceX benchmark. Only headlines seen |
| 6 | Anthropic Economic Index | https://www.anthropic.com/research/anthropic-economic-index-january-2026-report | free-online | task-level usage, automation vs augmentation split over time |
| 7 | Company filings: NVIDIA, Microsoft, Alphabet, Amazon, Meta 10-K and 10-Q | sec.gov EDGAR | free-online | segment revenue, capex, RPO, risk factors. Not opened this session; reading method only |
| 8 | a16z and Sequoia public essays, Menlo and similar enterprise surveys | not opened | free-online | named in brief; to cite when writing cards |

Authoritative outline: source 1 (AI Index chapter list) plus 2 (dataset taxonomy) and 3 (report sections). Three independent outlines: met.

Heading to leaf map: AI Index chapters 1/2 -> branches 7 and 4; chapter 4 (economy) -> branches 1, 4, 6; chapter 6 (policy) -> branch 8; chapters 3, 5, 7, 8 (responsible AI detail, science, education, public opinion) -> mostly out of scope; education touched in branch 6.

## Ledger
| Step | State |
|---|---|
| 1 survey | done 2026-11-20 |
| 2 outline draft | done, 61 leaves, 34 core; skeleton YAML not written |
| 3 terms rule | done 2026-11-20: 术语规则 added; 54 leaf titles and 6 theme headings rewritten to English terms; 61 leaves, 34 core |

## Not confirmed
- State of AI 2026 numbers (capex of about $733B, revenue run-rate of about $105B, 47% per quarter cost decline): read from a summary of the landing page; verify in the report before use.
- Everything about 10-K line items is from knowledge of how the filings are structured, not a fresh read.
- Whether Epoch publishes a training-compute growth rate on the data page: it did not appear; look in its trends articles.
- Meeker figures: only secondary coverage; treat as unverified.

## Next action
Chi decides: new domain (recommended) or extend ai-literacy industry; then skeleton.
