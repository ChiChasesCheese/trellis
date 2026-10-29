# Global Payment (ByteDance): company, organisation, role. Background for the "Software Engineer, Payment" loop

Research area. Collected 2026-10-29 for Chi's US interview with ByteDance **Global Payment** (req ids A128193, X6613). This file
**extends** the 2026-10-24 catalogue (`company.md`, `loop.md`, `behavioral.md`, `sources.md`), which was built for a different
target (Senior Backend, Innovative Growth). Reused facts cite the old ids (`[O5]`, `[LV]`, `[B3]` ...). New sources get `PC-*`
ids, listed at the end. Confidence: **high** = official text or a primary record read directly; **medium** = reputable
secondary source or two agreeing reports; **low** = one anonymous report, an SEO page, or my inference. Items older than
2025-10 are marked *(background)*.

## 1. The role

### 1.1 The posting Chi applied to (A128193)

- **Title / brand.** "Software Engineer, Financial Product and Solution - Global Payment (San Jose)", A128193, Backend,
  Regular. It is on **joinbytedance.com** (ByteDance brand; the jobs.bytedance.com link redirects there), not on
  lifeattiktok.com [PC-J1][PC-J5]. **high**
- **Age.** The id timestamp (id >> 32) gives **2026-09-02**: a fresh req [PC-J1]. **medium**
- **Team blurb.** Global Payment provides "payment acquisitions, disbursements, transaction monitoring, payment method
  management, foreign exchange conversion, accounting, reconciliations" for ByteDance platforms including TikTok [PC-J1]. **high**
- **Responsibilities (paraphrased).** Build *overseas consumer financial products*; architect complex payment systems with
  total cost in mind; fix bottlenecks for experience, performance, stability; design reviews and quality control [PC-J1]. **high**
- **Minimum qualifications.** HA distributed design; code review; Java/Python/Golang/C++/PHP; "in-depth understanding" of
  distributed, cache, message, search mechanisms; *online troubleshooting* (线上问题定位); cross-team coordination;
  "distributed systems with high availability and **financial security**" [PC-J1]. **high**
- **Preferred.** "Minimum 4 years" at a large internet company. Fintech or online-payment experience. International-team
  experience [PC-J1]. **high**
- **Base range (San Jose): $162,000 - $387,600** + bonus + RSUs [PC-J1]. **high**. Floor is $56k below Innovative Growth
  ($218,400 [O1]): the req spans entry (1-2 / L1) to senior (inference, **medium**).
- **What "Financial Product and Solution" (FPS) means**: consumer finance. A Global Payment intern posting lists "Buy Now
  Pay Later (BNPL), insurance, and consumer credit, TikTok Pay wallet, standalone payment apps" [PC-J6: A105173B]; the
  Singapore "FPS - Insurance" posting has A128193's exact text [PC-J6: A50978A]; the org hires BNPL, cash-loan, card-issuance,
  merchant-financing PMs and an Indonesia "Financial Products" lead for "digital lending, BNPL" [PC-J5]. **medium**: likely
  BNPL / credit / insurance / wallet products for markets **outside the US** (§2.3).

### 1.2 X6613 and the other US Global Payment engineering reqs (live 2026-10-29)

| Code | Title | Created (id) | Location | What it adds |
|---|---|---|---|---|
| X6613 | Software Engineer, Global Payment | 2022-11-01 | San Jose | **evergreen** catch-all req; 2026 blurb adds wallets, insurance, FX and "AI into risk control, credit decisioning"; asks for architecture design, massive-data distributed systems, DS&A, middleware depth; prefers internet finance / payment / e-commerce |
| V6789 | Software Engineer (Payments Architecture) | 2022-06-27 | San Jose | cross-region disaster tolerance, survive a data-centre failure "under the premise of ensuring data security and compliance", degradation strategies, peak readiness for "Double 11 and Black Friday" |
| A229949 | Software Engineer, Payment Risk | 2026-10-08 | San Jose | ~5 YOE; risk-signal monitoring, investigation tools, entity-relationship analysis, **LLM-powered agents** for risk intelligence; Python/Go/Java + SQL |
| A128193 | Software Engineer, Financial Product and Solution | 2026-09-02 | San Jose | see §1.1 |

All four: base **$162,000 - $387,600** [PC-J1-J4]. **high**. 4 of 30 non-intern Global Payment engineering postings are US
(23 Singapore, 3 Jakarta) [PC-J5]. San Jose intern reqs name US-side teams: Payment Product (payments, refunds, settlement,
merchant services, billing), Payment Solutions, Risk & Compliance, Infra & SRE [PC-J6: A161297, A143726A, A53108]. **high**

### 1.3 Languages and stack

- Postings accept any of Java/Python/Go/C++/PHP. The Singapore merchant-payment postings say "Proficient in **Java/Go**"
  [PC-J6: A224815, A25777A]. **high**
- No Global Payment posting names a middleware product (MySQL, Redis, Kafka, TiDB, Kitex: 0 mentions in 52 engineering
  postings) [PC-J5 keyword scan]. **high** for absence.
- An insider on Blind (2023): "Coding is in golang, a lot of the rest of the stack is internal tooling" [PC-B1]. **low**
  *(background)*. This fits ByteDance's Go-first microservices (Kitex >60k services, Hertz >10k) [O6]. Assume Go plus
  ByteDance-internal middleware on the job. Interviews accept any mainstream language [G1].

## 2. The Global Payment organisation

### 2.1 What it builds

- **Pay-in / pay-out platform for all of ByteDance outside China**: acquiring, disbursements (creator and seller payouts),
  payment-method management, FX, accounting, reconciliation, transaction monitoring [PC-J1]. **high**
- **Sub-teams named in 2026 postings** [PC-J5][PC-J6]. **high**
  - *Payment Network*: "unblock payment channels" for overseas expansion, a "payment instruction orchestration engine" (PSP/bank routing).
  - *Payments Architecture*: cross-region disaster recovery, degradation, peak readiness.
  - *Payment Product and Solution / Merchant Product*: merchant onboarding, transaction processing, **clearing and settlement,
    revenue sharing, billing reconciliation, fee calculation, tax invoicing**; "capital flow and information flow" (资金流 /
    信息流, how money moves vs how the records move).
  - *Account membership, merchant services, wallet products, operational platforms* (Senior Backend, Singapore, A25530).
  - *Financial Product and Solution*: BNPL, consumer credit, insurance, TikTok Pay wallet (§1.1).
  - *Payment Risk* (fraud, ATO models, LLM investigation agents). *Compliance Platform*: KYC, AML, sanctions screening, case
    management, review workflows, used by "TikTok LIVE, TikTok Shop" (A78990).
  - *Infrastructure & Stability*: SRE shifts for "critical payment system service", observability, DR (A125687).
- **Adjacent teams on the TikTok portal** (likely Global Payment's internal customers): LIVE "Fund Safety", "Money
  Platform", "Transaction", "Wallet" (Singapore); TikTok Shop "Global Settlement" [PC-J5]; "Global LIVE Wallet" [O-jobs].
  **medium**
- In market: **TikTok Pay** wallet (VN, MY, TH; Shop checkout) [PC-N1]; **TikTok PayLater** BNPL (self-run MY since
  2024-10, PH via PIPO Financing, partner-funded TH, Klarna in MX; Klarna/Clearpay for EU/US Shop) [PC-N4]; **TikTok One
  Pay** creator brand-deal payouts (2026-09) [PC-N2]; **P2P in DMs** found in US app code (2026-08; "not being tested")
  [PC-N1]. **medium**

### 2.2 Scale (dated, all third-party)

| Figure | Date | Source | Conf |
|---|---|---|---|
| TikTok Shop GMV $64.3B global 2025 (+94%), US $15.1B (+68%); H1 2026 $50.3B global, $11.8B US | 2026-08-06 | Momentum Works / Tabcut [PC-N13] | medium (estimates; other trackers differ) |
| ByteDance revenue ~ $200B in 2025 (other estimates ~$186B); H1 2026 ~ $120B (+~30%), profit ~ $20B | 2026-09 | The Information via secondary [PC-N11] | medium |
| J.P. Morgan: central account structure, API bank links, virtual accounts with automated reconciliation | 2023-01 | Forbes [PC-N5] | medium *(background)* |
| "100+" open international-payment roles in China + overseas | 2025-09-08 | mpaypass [PC-N6] | medium |

No ByteDance number on payment TPS, payment volume, or ledger size was found.

### 2.3 Licences and legal entities (the "PIPO" family)

- Payment affiliates are branded **PIPO**: PIPO (SG) holds a MAS **Major Payment Institution** licence; PIPO Fintech MY holds
  a BNM payment licence (2024) and has applied for a BNPL licence under Malaysia's Consumer Credit Act (Jun 2026); PIPO
  Financing (PH) is a former lending company that now runs TikTok PayLater; PIPO (HK) and PIPO (PH) appear in TikTok Shop
  partner terms [PC-N4]. **medium**
- **Brazil** (2026-03-31, Reuters): applications to the central bank for an *electronic money issuer* and a *direct credit
  company* licence. The Global Payments head met the central bank governor [PC-N3]. **medium**
- **Indonesia**: social commerce was barred from processing payments in 2023, which led to the Tokopedia deal [PC-N4] *(background)*.
  **Luxembourg** EMI bid "rebooted" Aug 2024 [search result, paymentexpert] **low** *(background)*.
- **US**: no money-transmitter licence for TikTok/ByteDance was found. P2P would need state MTLs [PC-N1]. **medium**
- **Compliance history**: HSBC reportedly closed accounts in 2023 over AML-control gaps in the payments division (The
  Information, paywalled) [PC-N7] **low-medium** *(background)*. 2026 hiring (MLRO, AML, financial-crime, payments tech
  audit) fits a regulator-facing build-out [PC-J5].

### 2.4 Where the teams sit, and who they report to

- 148 "Global Payment" postings: Singapore 98, San Jose 14, Jakarta 11, Kuala Lumpur 5, São Paulo 4, others [PC-J5]
  **high**. China-side roles in **Beijing / Shanghai** [PC-N6] **medium**. Reporting lines to "SG HQ and ShenZhen HQ"
  (Dublin, 2023) [PC-B1] and "a team in China" (San Jose, 2022) [PC-B2] **low** *(background)*.
- US engineers also sit in **Bellevue** (Payment Network, Data Privacy, Payments Architecture LCAs 2024-2026) [PC-H1]. **high**
- The Global Payments head named by Reuters (2026-03) is still in role later in 2026 [PC-N3]. **medium**

### 2.5 Relation to TikTok, TikTok Shop and the USDS JV

- A **ByteDance-level** platform serving "ByteDance platforms including TikTok"; a 2023 insider: it "solely belongs to
  ByteDance", "less involvement with TikTok side" [PC-J1][PC-B1]. **medium-high**. Customers: Shop checkout and settlement,
  LIVE coins and creator payouts, advertiser settlement, subscriptions [PC-N6][PC-J6 A78990]. **medium**
- The **USDS JV has its own payment teams** (2026 LCAs: Payment AI Platform SWE, Payments SRE, Payment Data Intelligence,
  Payment Risk, Global Payment Decision Science, all "- USDS") [PC-H1]. **high**. A separate hiring track from A128193
  (inference, **medium**).

## 3. The company now (2026)

### 3.1 Which entity hires a Global Payment engineer in the US

- Global Payment SWE LCAs (2024-2026) are filed by **ByteDance Inc.**; 2026 Global Payment PM roles also by **TT Commerce &
  Global Services LLC** (ByteDance-owned affiliate around the JV close); one 2026 Risk & Compliance SWE by **TikTok Inc.**
  [PC-H1]. **high** for filings. Likely employer: ByteDance Inc., **not** the JV. Confirm with the recruiter [G1].
- **Contradicts** `company.md` §2 ("target posting appears under TikTok proper"): this role is ByteDance proper, a third brand.
- JV recap, unchanged: formed 2026-01-22; Oracle / Silver Lake / MGX 15% each; ByteDance 19.9%; "TikTok global's U.S.
  entities" keep e-commerce, ads and marketing [O5].

### 3.2 Business lines and money

ByteDance: TikTok (ads, Shop, LIVE), CapCut, Lark, Douyin and others; 150k+ staff [O4]. Revenue growth is ~30% YoY,
driven by TikTok international ads and e-commerce. AI capex is squeezing profit [PC-N11]. **medium**

### 3.3 Hiring climate (2025-10 .. 2026-10)

- Late-2025 to early-2026 **pause around the JV close** [R7][R5]. Mid-2026 reports show interviews resuming (old catalogue).
- **Layoffs** on adjacent teams: WARN notice 2026-08-18, 75 jobs at TT Commerce & Global Services LLC in Bellevue (TikTok
  Shop / e-commerce, including SWEs and anti-fraud ops), "recent restructuring" [PC-N8] **high**. Nashville content-moderation
  office closure (250) [search summary] **medium**. No payment-team cuts reported.
- **Global Payment is hiring**: 148 live postings, new San Jose reqs Sep/Oct 2026, licence expansion [PC-J5][PC-N3][PC-N4].
  Mid-loop req closures and rematches remain common [A1][R-1omb].

### 3.4 Culture as practised

- **ByteStyle** (six values, `behavioral.md` §1 [O3]) now feeds ratings directly. The H1 2026 review used "字节范" (ByteStyle)
  for everyone and the **leadership principles**, which the CEO rewrote in late June 2026 for the first time in four years, for
  managers [PC-N10]. **medium**
- **Hours / time zones**: Blind WLB 2.3/5; a Glassdoor review tied to Global Payment cites "nights and overnights" from
  US/Asia overlap [PC-W] **low**. 2022-24 Blind threads on this team: "late night meetings", "less terrible than many other
  parts", "political", "dead end" [PC-B1][PC-B3] **low** *(background)*.
- **Office**: most TikTok US staff **5 days/week from Sep 2026** (Business Insider via [PC-N9]) **medium**; a 2026 Global
  Payment posting says "5-day onsite" (Singapore, A43121) **high**. Supersedes "3-5 days" in `loop.md` §8 [O2]; coverage of
  ByteDance Inc. San Jose unconfirmed.
- **Mandarin**: no Global Payment posting asks for Chinese (0 of 52 engineering postings); they prefer "international team
  work experience" [PC-J5] **high**. In practice, leads and many partner teams are in Singapore / China; 2023 insiders say CN
  teams "learnt to speak good Eng" [PC-B1] **low**. See `loop.md` §3 on HM rounds switching to Mandarin.
- **Performance review**: two cycles a year (half-year and full-year). Eight ratings: F, I, M-, M, M+, E, E+, O. Most
  people land between I and E. Mid-2025 change: more M and E, fewer M+, sharper M-/I split [PC-N10] **medium**. Unofficial
  distribution talk ("3331") is low. Half-year incentive from H1 2026 for E and above is computed on monthly *total* pay and
  paid **25% cash / 75% RSU or options, vesting monthly** [PC-N10] **medium**. OKRs are used and run top-down; peer (360) input
  is reported but not documented [Glassdoor snippets] **low**.
- **Promotion**: the Dec 2025 ladder reform raised band floors and ceilings so pay can grow without promotion. No public promo
  rubric was found (§4).

## 4. Levels and pay for this role

### 4.1 Ladder and mapping

- **Official reform (internal email 2025-12-19)**: the "5 levels × 2 grades" ladder (1-1 .. 5-2) becomes **L1-L10**. 1-1 and
  1-2 merge into **L1**. A new **L10** sits at the top. The full mapping was not published. 2025 bonus pool +35%, raise pool
  ×1.5, band floors and ceilings up [PC-N10]. **medium** (36Kr / Jiemian from the email). This confirms the direction of the
  Blind relabel claim [B3]. B3's "2-2 = L3 ≈ Meta IC5" mapping is consistent with this (1-2→L1, 2-1→L2, 2-2→L3) and a levels.fyi
  entry dated 2026-10-21 is already labelled "L3" (8 YOE, $250k base, $100k/yr stock) [PC-L1]. **medium**
- **External mapping** (levels.fyi convention, old catalogue): 1-2 ≈ Google L3 / Meta E3; 2-1 ≈ L4 / E4; 2-2 ≈ L5 / E5
  (senior); 3-1 ≈ L6 / E6 [LV][G1]. Downlevelling one step from big-tech titles is commonly reported [B2][R1]. **medium**
- levels.fyi typical YOE: 1-2 = 0-2 yrs, 2-1 = 3-4 yrs [PC-L1]. **medium**

### 4.2 Pay data (US)

levels.fyi ByteDance SWE, US (data date 2026-10-23, fetched 2026-10-29) [PC-L1]. **medium** (small samples):

| Level | n | Median TC | Base | Stock/yr | Bonus |
|---|---|---|---|---|---|
| 1-2 (L1) | 12 | $207k | $161k | $22k | $25k |
| 2-1 (L2?) | 22 | $310k | $231k | $37k | $42k |
| 2-2 (L3?) | 9 | $423k | $299k | $85k | $39k |
| 3-1 | 7 | $549k | $331k | $189k | $29k |

**H-1B LCA base salaries for Global Payment engineering titles** (offered base, San Jose unless noted) [PC-H1]. **high** (public
filings; level not shown):

| Title | 2024 | 2025 | 2026 (to date) |
|---|---|---|---|
| Software Engineer, Global Payment(s) | $185k (Bellevue), $210k, $225k | $145k, $185k, $205k, $210k ×2, $277k | $203k |
| Senior SWE, Payment Solution | $180k, $200k | $272k | $285k ×2 |
| (Backend) SWE, Payments Architecture | $204k, $205k | — | $232k ×2 (Bellevue) |
| Senior SWE, Global Payment Risk & Compliance | $320k | — | $355k ×2 (TikTok Inc.) |
| Fullstack SWE, Global Payments | $215k | — | $176k |

Reading: "Software Engineer, Global Payment" bases of ~$185-225k sit in the 1-2 / 2-1 band; "Senior" titles at $270-355k sit
at 2-2 and above (inference from the levels.fyi bases, **medium**). All ByteDance Inc. SWE LCAs: 2025 median $205k
(n=360), 2026 median $215k (n=181) [PC-H1].

### 4.3 RSUs, buyback, negotiation

- Vesting 20/25/25/30 over 4 years, 1-year cliff, then quarterly (since 2024) [B9][LV]. **medium**
- **Buyback**: Aug 2025 $200.41/share (Reuters) **medium**; Oct 2026 **$241.35/share** (single relay) **low**; grants from
  2026-01-01 may sell only part of each vested tranche (55% +15%/yr, or 50% +10%/yr: sources conflict) **low**
  [PC-N12]. RSUs are liquid only via buybacks: value them at the buyback price; ask for the sell-back cap.
- **Negotiation** (anecdotal): ~25% target bonus in most 2025-26 offers [L1][R-offer2]; sign-on $35-50k common; the level
  call is the main lever, so ask the band before round one [R1][G1]; competing offers help.
- **For Chi** (inference, **medium**): ~1.7 years full-time at PayPal plus an internship. The posting prefers 4+ years. The
  realistic band is **1-2 (L1) or 2-1 (L2)**, ~$200-310k TC. Prepare at senior depth anyway (system design and ownership
  stories); a strong design round is what moves a candidate up a level [G1].

## 5. What the team likely values in Chi (inference from postings; label: inferred)

1. **Money-movement correctness under financial-grade constraints.** Postings keep returning to "financial security",
   "fund risk control", "data consistency", "financial transaction correctness" [PC-J1][PC-J6]. Expect idempotency, double-entry /
   append-only ledgers, state machines, exactly-once effects, reconciliation (old SD row #1 [P2][R3b]).
2. **Settlement, fees, reconciliation: Chi's PayPal fee pipeline maps one-to-one** onto the merchant-payment list "clearing
   and settlement, revenue sharing, billing reconciliation, fee calculation, tax invoicing" [PC-J6: A25777A]. Have one story
   with numbers on fee-calculation correctness and one on a reconciliation break.
3. **Consumer finance basics for FPS** (BNPL / credit / insurance / wallet): loan or instalment lifecycle, repayment schedules,
   interest and fee accrual, overdue handling, partner funding, credit-decision call-outs, wallet balance vs ledger, multi-currency
   / FX. A design prompt in this area is plausible but **not reported** (low).
4. **Stability and incident handling.** "Online troubleshooting", disaster tolerance, degradation, peak readiness, on-call
   shifts [PC-J1][PC-J4][PC-J6: A125687]. Chi's on-call ownership and tracing stack (Sentry/Datadog) is directly relevant.
5. **Business understanding**: separating capital flow from information flow; PSP / channel differences across markets; licence
   constraints (why a feature can launch in Malaysia but not the US) [PC-J6][PC-N4].
6. **Cross-region, cross-time-zone collaboration** and project drive across teams [PC-J1]. Answer "how do you work with a
   Singapore/China team at 9 pm" concretely.
7. **AI in payments operations** (risk agents, compliance review, AI-assisted engineering) is in every 2026 posting
   [PC-J2][PC-J3][PC-J6]. Have one sentence on how Chi uses AI tools and where he would not trust them with money.

## Sources added by this file (fetched 2026-10-29 unless stated)

| id | URL / identifier | date | type |
|---|---|---|---|
| PC-J1 | https://joinbytedance.com/search/7680893707407558917 (A128193) | created 2026-09-02 | official posting |
| PC-J2 | joinbytedance.com/search/7161162479660976414 (X6613) | 2022-11, live | official posting |
| PC-J3 | joinbytedance.com/search/7694175737054923061 (A229949) | 2026-10-08 | official posting |
| PC-J4 | joinbytedance.com/search/7114043364341762341 (V6789) | 2022-06, live | official posting |
| PC-J5 | `POST https://jobs.bytedance.com/api/v1/public/supplier/search/job/posts` (header `website-path: en`, keyword "Global Payment", 148 posts) and `api.lifeattiktok.com` (same path, `website-path: tiktok`, 89 posts); scratch `/tmp/bg_A/data/` | 2026-10-29 | official ATS API |
| PC-J6 | postings A224815, A25777A, A25530, A78990, A125687, A22436A, 25CV, A50978A, A105173B, A43121, A186133B (SG/ID); A161297, A143726A, A53108 (San Jose interns) from PC-J5 | 2026 | official postings |
| PC-H1 | https://h1bdata.info/index.php?em=bytedance+inc (also tiktok+inc, tt+commerce+%26+global+services+llc, tiktok+usds+joint+venture+llc), years 2024-2026 | 2026-10-29 | DOL LCA mirror |
| PC-L1 | https://www.levels.fyi/companies/bytedance/salaries/software-engineer (`__NEXT_DATA__`) | data 2026-10-23 | aggregator |
| PC-N1 | https://techcrunch.com/2026/08/18/tiktok-explores-peer-to-peer-payments-via-dms-report-says/ | 2026-08-18 | news |
| PC-N2 | https://www.tubefilter.com/2026/09/29/tiktok-one-pay-creator-brand-deal-compensation/ | 2026-09-29 | news |
| PC-N3 | Reuters "TikTok seeks Brazil fintech license" via https://www.marketscreener.com/news/tiktok-seeks-brazil-fintech-license-to-offer-credit-ce7e51ded18cff20 and https://www.paymentsjournal.com/tiktok-aspires-to-fintech-status-with-payments-credit-bids-in-brazil/ | 2026-03-31 | news |
| PC-N4 | https://eu.36kr.com/en/p/3934685659518855 (ByteDance overseas credit / PIPO licences) | 2026 (after Aug) | news analysis |
| PC-N5 | https://www.forbes.com/sites/alexandralevine/2023/01/05/bytedance-jpmorgan-tiktok/ | 2023-01-05 | news *(background)* |
| PC-N6 | https://m.mpaypass.com.cn/news/202509/08184001.html | 2025-09-08 | trade news |
| PC-N7 | https://feature.theinformation.com/articles/how-bytedance-bungled-a-money-laundering-probe-into-tiktok-payments (paywalled; intro only) | ~2024 | news *(background)* |
| PC-N8 | https://komonews.com/news/local/tiktok-layoffs-bellevue-washington-tech-mass-layoffs-... (WARN, TT Commerce & Global Services LLC) | 2026-08-19 | news |
| PC-N9 | https://commercialobserver.com/2026/08/tiktok-employees-5-days-office/ | 2026-08 | news |
| PC-N10 | https://eu.36kr.com/en/p/3603180661933059 (2025-12-20, L1-L10); https://wallstreetcn.com/articles/3776564 (2026-07, H1 review); ifeng / ithome 2025-07 (rating scale, via search summary) | 2025-07 .. 2026-07 | news |
| PC-N11 | https://aiweekly.co/alerts/bytedance-h1-2026-profit-slides-to-20b-even-as-revenue-jumps-30-to-120b-on-ai (relaying The Information) | 2026-09 | news (secondary) |
| PC-N12 | https://www.kucoin.com/news/flash/bytedance-launches-new-stock-option-buyback-at-241-35-per-share ; Reuters Aug 2025 buyback via search | 2026-10-13 | news flash (low) |
| PC-N13 | https://thelowdown.momentum.asia/new-report-tiktok-shop-u-s-gmv-grew-68-to-reach-us15-1b-in-2025/ | 2026 | industry report |
| PC-B1 | https://www.teamblind.com/post/tiktok-global-payment-team-frwyhlq4 | 2023-09..11 | forum *(background)* |
| PC-B2 | https://www.teamblind.com/post/anyone-from-the-mountain-view-office-at-the-global-payments-team-for-bytedance-sbdybnww | 2022-08 | forum *(background)* |
| PC-B3 | teamblind.com/post/ tiktok-e-commerce-supply-chain-vs-bytedance-global-payments-isbs5tmw (2024-06); now-hiring-global-payments-team-at-tiktok-hxmznyad (2023-09); tiktok-is-hiring-swe-mle-ds-tech-leads-and-more-for-global-payments-team-zqjtfn52 (2023-07) | 2023-2024 | forum *(background)* |
| PC-W | Blind / Glassdoor ByteDance WLB pages via search summary | undated | reviews (low) |
| PC-O1 | https://joinbytedance.com/interview , https://joinbytedance.com/faq ("several interviews", ~1 month, 6-month re-apply gap for same role, English CV) | 2026-10-29 | official |

## Gaps

- **No ByteDance engineering blog post, paper or conference talk** on its payment, ledger or reconciliation systems was found
  (InfoQ, QCon/ArchSummit, CloudWeGo, CN blogs searched). Nothing public describes the Global Payment architecture or stack beyond
  postings and one 2023 Blind comment (Go + internal tooling).
- **Which US product A128193 serves** is unclear. FPS products (BNPL, credit, insurance, wallet) are live in SEA/LATAM, not the
  US. The San Jose team may build for overseas markets from the US. Ask the recruiter or HM.
- **Employing entity** (ByteDance Inc. vs TT Commerce & Global Services LLC) is inferred from LCAs, not stated in the posting.
- **Level mapping after the L1-L10 reform** is only partly public (1-1/1-2 → L1). 2-1→L2 and 2-2→L3 are inferred.
- **Payment-team scale numbers** (TPS, volume, ledger size, headcount) were not found. GMV and revenue are third-party estimates.
- **Oct 2026 buyback price and sell-back caps** rest on one low-quality relay with conflicting percentages.
- Whether the **5-day office rule** covers ByteDance Inc. San Jose payment staff is not confirmed.
- No **2025-10 .. 2026-10 first-hand** Blind or Reddit report on Global Payment team culture or WLB. Every team-specific forum
  item is 2022-2024. (Interview reports are part B's scope: `payment_loop.md`.)
- levels.fyi has no team filter; no Global Payment-specific offer was found. LCAs give base only (no stock or bonus).
