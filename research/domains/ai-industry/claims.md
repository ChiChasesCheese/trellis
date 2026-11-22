# ai-industry claims (card id | claim | source)
(all dated 2026-11-21; fetched this session)

aii-chain-money-flow-exam | NVIDIA FY2026 (ended 2026-01-25) revenue $215.9B; Data Center $193.7B | NVIDIA Q4/FY2026 press release, investor.nvidia.com
aii-margin-by-layer, aii-margin-read-exam | GAAP gross margin 71.1% FY2026 vs 75.0% FY2025; drivers: Hopper HGX -> Blackwell full-scale; $4.5B H20 charge; provisions $7.2B vs $3.7B; net GM effect 2.6 and 2.3 pts | NVIDIA FY2026 10-K MD&A (via MarketScreener copy of MD&A)
aii-circular-test, aii-nvda-rows | direct customers 22% and 14% of FY2026 revenue; FY2025 12%, 11%, 11% | NVIDIA FY2026 10-K (MarketScreener copy)
aii-nvda-rows | DC computing +59%, networking +142%; DC +68% ~90% of revenue | same
aii-nvda-guidance-china | Q1 FY27 guide $78.0B +-2%, no China DC compute assumed, GAAP GM 74.9% +-50bp | NVIDIA Q4 FY2026 press release
aii-hyperscaler-cloud-capex | Google Cloud Q3 2026 revenue $30.71B vs $15.16B, +103%; Pichai quote | 9to5google.com 2026-10-28 (Alphabet backlog/capex numbers NOT used: only secondary)
aii-chain-layers etc | circular, depreciation, capex-ratio examples use made-up numbers, labelled as such | n/a

# t02
aii-gpu-landscape, aii-gpu-share-read | NVIDIA GM 71.1%; DC +68%; customer 22% | NVIDIA FY2026 10-K/press release
aii-hbm-bottleneck | HBM suppliers SK hynix, Samsung, Micron; Samsung HBM4 yield <60% -> 80%; target ~38% share; TrendForce pricing power through 2027; 2027 HBM bit shipments +50-60% | TrendForce News 2026-08-10 (fetched)
aii-hbm-bottleneck | 70B params x 2 bytes = 140GB, 3 TB/s -> ~47ms: illustrative arithmetic
aii-hbm-read-exam | 56% vs 70% figures were seen only in search summaries; used only as hypothetical labels, not claimed | n/a
aii-packaging-bottleneck-exam | NVIDIA lead times >12 months, non-cancellable orders, premiums, deposits | NVIDIA FY2026 10-K MD&A (MarketScreener copy)
aii-chip-depreciation | perf per dollar 1.49x/yr (90% CI 1.36-1.66), doubling 1.7y, since 2023, constant 2025 dollars | epoch.ai/trends (fetched)
aii-export-controls-rule | BIS final rule effective 2026-01-15: TPP<21,000, DRAM bandwidth <6,500 GB/s, H200/MI325X named, 50% cap, third-party US testing, KYC | Federal Register 91 FR (2026-01-15) RIN 0694-AK43, govinfo.gov (fetched)
aii-export-controls-read | H20 $4.5B charge; Q1 FY27 guide excludes China DC compute | NVIDIA

# t03
aii-capex-scale-read | four US hyperscalers guide ~$733B 2026 capex | State of AI 2026 landing page (stateof.ai, fetched)
aii-capex-gw-cost | 1GW AI DC ~ $38B up-front capex; GW-scale build 2.1y (90% CI 1-3.6) | epoch.ai/trends (fetched); 7330/38 ~19GW illustrative
aii-power-bottleneck | largest AI DCs approaching 1GW; AI Index 2025 compute doubles every 5 months, power annually | epoch.ai/trends; AI Index 2025 page
aii-power-sizing-exam | arithmetic example, PUE 1.2 assumed
aii-epoch-compute-growth | compute 5x/yr (4-6x), 5.2 months; cost 3.5x/yr (2.8-4.4), 7 months; perf/$ 1.49x/yr since 2023; top-5 10,000x since 2020 | epoch.ai/trends
aii-epoch-trend-limits | stock ~300T tokens, 80% interval exhaustion 2026-2032 | Epoch data paper blog (fetched)

# t04
aii-labs-rotation | three-lab race Anthropic/OpenAI/Google; different leaders on Intelligence Index vs Arena | State of AI 2026 landing page
aii-bizmodel-taxonomy, aii-enterprise-adoption | API ~3/4 automation vs under half Claude.ai; work use 74% vs 46%; sample 1M conversations Nov 13-20 2025 | Anthropic Economic Index Jan 2026 (fetched)
aii-price-decline, aii-price-chart-read | 280x GPT-3.5 level Nov 2022-Oct 2024 | AI Index 2025 page; 47%/quarter (~13x/yr) five benchmarks per Epoch via State of AI 2026; OpenAI+Anthropic run-rate ~$30B -> ~$105B | State of AI 2026
aii-applayer-margin | Standard Metrics preliminary Q2: 256% vs 90%; 172% vs 53% (75th pct YoY) | State of AI 2026
aii-open-closed-gap, aii-open-closed-read | 8% -> 1.7% on some benchmarks | AI Index 2025 page
aii-enterprise-adoption | 78% orgs using AI 2024 vs 55% 2023 | AI Index 2025 page
aii-survey-bias-method | "95%" headline is hypothetical, labelled so
others in t04 | arithmetic examples hypothetical

# t05/t06
aii-china-labs-gap | notable models 2024 US 40, China 15, Europe 3; MMLU/HumanEval gap double digits 2023 -> near parity 2024 | AI Index 2025 page; State of AI 2026: prediction "Chinese lab topped a major task leaderboard" a hit
aii-china-compute-constraints | H20 $4.5B; no China DC compute in Q1 FY27 guide; BIS 50% cap | NVIDIA; Federal Register
aii-china-efficiency-exam | MoE arithmetic hypothetical (60B total, 10B active)
aii-exposure-method | 1M Claude.ai + 1M API, Nov 13-20 2025, O*NET, thresholds 15 convs / 5 accounts, "directionally accurate" | Anthropic Economic Index Jan 2026
aii-exposure-swing | 56/41 (Jan 2025), 52/45 (Nov 2025), directive 27/39/32; API ~3/4 automation | same
aii-canaries-evidence, aii-diff-in-diff | ages 22-25, 19% gap, ADP through June 2026, caveats | Canaries page (revised Aug 2026)
aii-swe-evidence | comp&math 34% (peak 40% Mar 2025) Claude.ai; API 44% -> 46%; top task fixing software errors 6% / ~1 in 10 API | Anthropic Economic Index Jan 2026
aii-roles-substitute-complement | no specific occupation named on Canaries page; outline's customer-service/translation examples NOT used (unverified)

# t07/t08
aii-bench-saturation | benchmarks saturate in months; GLM-5.1 52.5% -> 65.5% on 100 SWE-bench Verified tasks, weights unchanged | State of AI 2026 landing page
aii-arr-news-method | OpenAI+Anthropic run-rate ~$30B -> ~$105B; 1050/300=3.5 | State of AI 2026
aii-scorecard | 2 hits, 5 partial, 3 misses (=10); hits listed; data-center opposition partial | State of AI 2026 (page lists 2+5+3)
aii-reports-biases | State of AI: 9th edition, Nathan Benaich/Air Street Capital, 244 slides | State of AI page; AI Index 2025 edition covers 2024; BOND not opened, no numbers used
aii-report-read-exam | US $109.1B vs China $9.3B 2024; ~12x | AI Index 2025 page; "Chinese state money outside private investment" is explanatory framing, not sourced
aii-primary-secondary | 22%+14%=36%; the 36% appeared in a secondary summary (InvestSkill) | MarketScreener 10-K copy; search result
aii-primary-trace-exam | 307.1 / 151.6 = 2.03 | 9to5google
aii-regulation-three | EU tiers, 10^25 FLOP, dates 2025-02-02, 2025-08-02, 2026-08-02 (Art. 50), 2027-12-02 (Annex III) ; EO signed 2025-12-11; China measures 2023-08-15, CAC + six regulators, security assessment/filing | artificialintelligenceact.eu; DLA Piper x2 (fetched)

# non-core batch 1
aii-unit-econ-gpu-hour | all numbers hypothetical (30k GPU, 0.5/h, 4y)
aii-valuation-bubble | $285B wiped from software stocks in two weeks in February ("SaaSpocalypse") | State of AI 2026 landing page
aii-interconnect | DC networking +142%, computing +59% | NVIDIA FY2026 10-K (MarketScreener copy)
aii-dc-financing | 1GW ~$38B, 2.1y | Epoch trends; NVIDIA partnership with six financial institutions to mobilize >$500B; CoreWeave 4.2GW contracted by Aug 11 | State of AI 2026
aii-local-opposition | Gallup March: 71% oppose local AI DC vs 53% nuclear; Data Center Watch Q2: >=45 projects, ~$68B | State of AI 2026
aii-data-wall | 300T tokens (100T-1000T 90%), 80% interval 2026-2032, 5x overtrain 2027, Llama 3-70B 10x overtrained, 2022 paper predicted 2024 | Epoch blog (fetched)
aii-agents-economics | Standard Metrics figures | State of AI 2026
aii-energy-routes, aii-cooling-pue, aii-platform-distribution, aii-model-licenses, aii-inference-chips | mechanism cards, no numbers; delivery-time statements are general rules flagged as such

# non-core batch 2
aii-china-app-regulation | CAC + six regulators, effective 2023-08-15, filing/assessment, obligations | DLA Piper 2023-07 (fetched)
aii-us-china-investment | $109.1B / $9.3B / UK $4.5B 2024; 40 vs 15 models | AI Index 2025 page. "government capital not counted" is a framing statement (private investment definition), not sourced
aii-productivity-lag | Solow 1987 remark (economic history); 78% organisations 2024 | AI Index
aii-education-evidence | educational instruction 9% Jan -> 15% Nov (Claude.ai); API 4% vs Claude.ai 16% | Anthropic Economic Index Jan 2026
aii-regional-diffusion | 0.7%, 50% vs 38%, Gini .37->.32, 0.36%, 2-5 years caveat | same
aii-capability-curve | METR 2025-03: 7-month doubling over 6 years; ~4 min ~100%, >4h <10%; page flagged partly out of date | METR (fetched)
aii-vendor-interest | GLM-5.1 52.5 -> 65.5 | State of AI 2026
aii-copyright-bartz | $1.5B, ~$3,000/book, ~500k works, final approval 2026-07-20, Alsup June 2025 ruling, no binding precedent | thenextweb 2026-07-21 (fetched); Sept 2025 preliminary approval from search summary only (Bloomberg Law snippets)
aii-sovereign-ai | ~$138B pledged; NVIDIA >$30B sovereign FY2026; EU gigafactories EUR1B/10B/20B | State of AI 2026
aii-safety-industry | systemic-risk GPAI incident reporting >10^25 FLOP | artificialintelligenceact.eu
aii-china-price-war, aii-china-chips-checkpoints, aii-skills-premium, aii-panic-hype-teardown, aii-dashboard-ten | method cards, no new numbers
| (orchestrator 2026-11-21) NVIDIA FY2026 DC computing +59%, networking +142%, direct customers 22% / 14% | confirmed in the SEC original | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm |
