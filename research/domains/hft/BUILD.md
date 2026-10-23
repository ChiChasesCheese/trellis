# HFT — BUILD

> Durable record for skill `building-study-domains`, started 2026-10-23 (task: `research/agents/HFT_DOMAIN_TASK.md`).
> Kept in the research area, not in `vault/domains/hft/`, so the survey and process never show in Obsidian (ADR 0011).
> Skeleton `skeleton/hft.yaml`, content `vault/domains/hft/`.

## Step 1 — survey

| Source | URL | Licence | Covers |
|---|---|---|---|
| Nasdaq TotalView-ITCH 5.0 spec (official) | https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf | free to read | message model, every message type and field, data types, timestamps |
| Nasdaq OUCH 5.0 / MoldUDP64 / SoupBinTCP specs (official) | https://www.nasdaqtrader.com/Trader.aspx?id=TradingUSEquities | free to read | order entry messages, UDP sequencing, gap request |
| CME MDP 3.0 + SBE (official) | https://www.cmegroup.com/confluence/display/EPICSANDBOX/MDP+3.0+-+Market+Data | free to read | SBE encoding, incremental + snapshot recovery, A/B feeds |
| penberg/awesome-low-latency | https://github.com/penberg/awesome-low-latency | none stated | patterns: measure correctly, avoid data movement / work / waiting, hide latency, tune OS, kernel bypass, FPGA |
| StateOfTheArt-quant/awesome-high-frequency-trading | https://github.com/StateOfTheArt-quant/awesome-high-frequency-trading | MIT | microstructure books, papers, courses |
| Larry Harris, *Trading and Exchanges* (2003) | book | commercial | traders and orders, market structures, dealers, informed traders, liquidity, spreads, volatility, regulation |
| Donadio, Ghosh, Rossier, *Developing High-Frequency Trading Systems* (Packt 2022) | book | commercial | HFT history and firms, system components, OS / network / hardware, C++, Java (GC, JIT, Disruptor, Chronicle), Python, FPGA |
| Carl Cook, *When a Microsecond Is an Eternity* (CppCon 2017) | https://www.youtube.com/watch?v=NH1Tta7purM | talk | hot path, no allocation, templates over virtual, exceptions, cache warming, measurement |
| David Gross, *Trading at Light Speed* (Meeting C++ 2022) | https://www.youtube.com/watch?v=8uAW5FQtcvE | talk | order book layout, SPSC queues, measurement, networking |
| LMAX Disruptor technical paper | https://lmax-exchange.github.io/disruptor/disruptor.html | free | ring buffer, sequencing, false sharing, wait strategies, batching |
| Martin Thompson, *Mechanical Sympathy* blog | https://mechanical-sympathy.blogspot.com/ | free | memory barriers, false sharing, queues, CPU caches |
| Ulrich Drepper, *What Every Programmer Should Know About Memory* | https://people.freebsd.org/~lstewart/articles/cpumemory.pdf | free | RAM, CPU caches, NUMA, virtual memory, what programmers can do |
| Brendan Gregg, *Systems Performance* 2e | book | commercial | methodology (USE), CPUs, memory, network, perf, flame graphs |
| Aeron / Agrona / Chronicle docs | https://aeron.io/docs/ , https://github.com/real-logic/agrona , https://chronicle.software/ | Apache-2.0 / free docs | Java low-latency messaging and off-heap |
| HdrHistogram + Gil Tene, *How NOT to Measure Latency* | http://hdrhistogram.org/ | public domain / talk | histograms, coordinated omission |
| Existing kits | `vault/interviews/companies/headlands/`, `core/system-design/headlands/sd03_low_latency_trading_system`, `core/foundations/headlands/cpu_cache_locality.md`, `quant-infra` and `markets` skeletons | — | order book, SPSC, memory pool, TCP channel lectures; company brief |

Mapping of outline headings to leaves (out of scope lines at the end):

- awesome-low-latency: measure → `measurement.*`; data movement → `machine.cache-lines`, `machine.numa`, `cpp.containers`;
  avoid work → `cpp.no-alloc`, `machine.tlb-hugepages`, `cpp.compiler`; avoid waiting → `architecture.threading`,
  `cpp.spsc-seqlock`, `architecture.event-loop`, `os-network.tcp-udp`; hide latency → `machine.simd`; tune →
  `os-network.cpu-isolation`, `os-network.interrupts`; advanced → `os-network.kernel-bypass`, `fpga.*`.
- Harris: traders / orders / market structures → `microstructure.participants`, `.order-types`, `.matching`,
  `market-structure.fragmentation`; dealers / informed traders / spreads → `microstructure.spread`,
  `.adverse-selection`, `.market-making-pnl`; regulation → `market-structure.reg-nms`, `.rules`, `.halts`.
- Donadio: history and firms → `overview.*`; components → `architecture.*`; OS / network / hardware → `machine.*`,
  `os-network.*`; C++ → `cpp.*`; Java → `java.*`, `java-at-hft.*`; FPGA → `fpga.*`.
- ITCH 5.0: data types → `protocols.binary-encoding`; message formats → `protocols.itch-messages`; architecture →
  `protocols.itch-model`, `protocols.moldudp64`.
- Drepper: RAM / caches / NUMA / virtual memory → `machine.*`; Gregg: methodology / perf → `measurement.*`.

Out of scope here (lives elsewhere or below Pareto): alpha research, backtest statistics, portfolio construction
(`quant-infra`); asset-class detail and options pricing (`markets`); ITCH administrative messages (Reg SHO, MPID position,
IPO quoting, NOII detail, RPII, DLCR); Python HFT implementation (Donadio part 3); crypto exchange specifics.

## Step 2 — skeleton

`skeleton/hft.yaml`: 15 branches, 122 leaves, `lang: zh`, core = overview, architecture, java, java-at-hft and the four
microstructure basics + `machine.memory-hierarchy` (closed under `requires`). `validate` 0 errors.

## Step 3 — corpus

Not ingested in the first pass: the books are commercial, the talks are video, and the free specs and papers are long
PDFs. Cards are written grounded in the authors' knowledge and checked in step 5. Next pass: declare `drepper-memory`,
`lmax-disruptor`, `nasdaq-itch5` as `free-online` corpora and digest them against their leaves.

## Step 5 — claims the card agents were least sure of

Checked by the orchestrator against what is publicly documented; ✓ = holds as written, ✎ = card edited.

| Card | Claim | Verdict |
|---|---|---|
| hft-fees-tick-size-maker-taker | access fee cap $0.003 | ✎ added the 2024 SEC amendment lowering it to $0.001 for most stocks |
| hft-java-at-hft-where-java-where | Headlands Java roles; tick data "数百 GB" | ✎ worded as the job description; "数百 GB 到 TB 级" |
| hft-reliability-knight-capital-* | 7 of 8 servers, 45 min, ~$440M, repurposed flag, 97 warning emails, rollback widened the damage, GETCO merger | ✓ |
| hft-economics-sharpe | Virtu 1 losing day in ~1238 | ✓ (2014 S-1) |
| hft-history-flash-crash | Dow ~9%, $4.1B E-mini sale, 1¢ / $100,000 prints, LULD after | ✓ |
| hft-history-electronification, hft-fees-tick-size-tick-change | Reg ATS 1998, decimalization 2001 from 1/16, tick pilot 2016–2018 | ✓ |
| hft-fees-tick-size-inverted | BX and BYX inverted | ✓ |
| hft-java-gc-choices-gen-zgc | ZGenerational in 21, default in 23, non-generational removed in 24 | ✓ (JEP 439 / 474 / 490) |
| hft-java-safepoints-hidden-pauses, hft-java-tuning-legacy-flags | biased locking off in 15, removed in 18 | ✓ |
| hft-java-modern-upgrade | Leyden AOT cache from JDK 24 | ✓ (JEP 483) |
| hft-java-disruptor-vs-abq, hft-java-at-hft-how-fast-lmax | ABQ tens of µs vs Disruptor tens of ns; LMAX ~6M orders/s | ✓ |
| hft-java-agrona-aeron-backpressure | offer() codes −1…−5 | ✓ |
| hft-java-safepoints-ttsp | counted loops without poll; loop strip mining | ✓ (JDK 10) |
| hft-architecture-pre-trade-risk-three-layers | 15c3-5 "direct and exclusive control" | ✓ |
| hft-os-network-time-sync-why-needed | MiFID II: HFT within 100 µs of UTC, 1 µs granularity | ✓ (RTS 25) |
| hft-machine-simd-wide-vector-side-effects | wide-vector warm-up, AVX-512 down-clocking on Skylake-X | ✓ |
| hft-os-network-nic-switch-layer1-switch | L1 switch ~5 ns, cut-through switch hundreds of ns | ✓ |
| hft-os-network-kernel-bypass-options | Solarflare now AMD (via Xilinx) | ✓ |
| hft-os-network-wan-chicago-nj | ~1200 km, microwave ~4 ms, fibre ~6.5–7 ms one way | ✓ |
| group D magnitudes (C6 exit, NUMA remote, STLB size, lock cost, vDSO, coalescing, HZ) | typical figures | ✓ as magnitudes |
| group E (exception cost, seq_cst store as xchg, C2 threshold ~10k, JFR ~1%, nanoTime → CLOCK_MONOTONIC, ClickHouse ASOF JOIN) | typical figures | ✓ |
| group E arithmetic (coordinated omission p99 ≈ 0.9 s, 0.99^10, 694 days, 800 s per TB, 2.9 TB/day) | re-derived | ✓ |
| magnitudes (tick-to-trade software µs / FPGA ns, sleep-wake µs, shared memory vs loopback TCP, failover heartbeats, colo fees) | rough orders of magnitude, worded with 约 / 量级 | ✓ as magnitudes |

## Ledger

| Date | Step | Result | Evidence |
|---|---|---|---|
| 2026-10-23 | 1 survey | 15 sources, 3 official specs | table above |
| 2026-10-23 | 2 skeleton | 137 nodes / 122 leaves, 0 errors | `uv run trellis --domain hft validate` |
| 2026-10-23 | 6 readings | 69 readings, 95/122 leaves (78%) | `vault/domains/hft/readings/` |
| 2026-10-23 | 4 cards, groups A C F | 254 cards (overview, microstructure, architecture, reliability, java, java-at-hft) | commit b7893c7f |
| 2026-10-23 | 4 cards, groups D E | 89 + 96 cards (machine, os-network, cpp, measurement, fpga, research-infra) | commits 45c8622c, 0e6ca0d7 |
| 2026-10-23 | 4 cards, group B | 92 cards (market-structure, protocols, orderbook); dedupe scan: no duplicates, two intro-vs-deep pairs kept | commit 2b42d399 |
| 2026-10-23 | 7 drills | 15 drills, one per branch, grading points wikilinked to cards | commit 63e7392b |
| 2026-10-23 | 6 clip | 62 clipped, 7 index pages skipped (aeron-docs, arrow-overview, hdrhistogram, kernel-irq-affinity, kx-q-learn, sbe-wiki, shipilev-jvm-anatomy); PDFs stay local (gitignored) | `trellis --domain hft clip` |
| 2026-10-23 | 8 ship | build 531 notes / 122 decks; anki-push published; Anki shows 531 cards | `trellis --domain hft anki-push` |

## State (2026-10-23)

`stats`: 531 cards, 69 readings, 15 drills, link coverage 78%, readable sources 92/122 leaves; `validate` 0 errors,
1 warning (30 leaves without an archived readable source); `steps` 122/122 leaves ordered.

## Next action

1. Step 6: a readable source for the 30 leaves the warning lists (mostly orderbook, cpp, java-at-hft, architecture):
   replace the 7 skipped index pages with article-level pages, or write vault articles (readings with no `url:`).
2. Step 3: ingest `drepper-memory`, `lmax-disruptor`, `nasdaq-itch5` as free-online corpora and digest them against
   their leaves to put a source behind the grown cards.
3. The loop: after Chi reviews, `trellis pull` → `trellis brief` → `trellis grow --next`.
