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

## Ledger

| Date | Step | Result | Evidence |
|---|---|---|---|
| 2026-10-23 | 1 survey | 15 sources, 3 official specs | table above |
| 2026-10-23 | 2 skeleton | 137 nodes / 122 leaves, 0 errors | `uv run trellis --domain hft validate` |

## Next action

Step 4: cards by six agent groups (`research/domains/hft/card_prompt.md`).
