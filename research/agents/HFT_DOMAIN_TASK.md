# Long task — HFT / low-latency trading systems domain (queued 2026-10-23)

**Start only after** the repo refactor in progress is finished (kit tools → `trellis kit`, AGENTS.md command update,
path-filtered CI + pre-commit). Follow `.claude/skills/building-study-domains/SKILL.md` for the procedure and
`proposals/WRITING_RULES.md` for every learning page and card.

## What Chi asked for (2026-10-23)

- A new trellis domain on HFT / low-latency trading systems engineering, **beginner tone**, Pareto: the ~20% of material
  that carries ~80% of the insight, so Chi can understand the whole field and talk about it confidently.
- **~500 cards**, all in **Chinese, with domain terms kept in English** (tick-to-trade, order book, kernel bypass …).
- **Every card self-contained and informative** — not terse: Chi must fully understand it from the card alone
  (define the terms it uses, give the why, a concrete number or example). No provenance on cards (rule 11).
- **Ordered by prerequisite**: branches and leaves in a normal learning sequence; within a deck, cards arrive so each
  card's prerequisites came before it (skeleton `requires` edges, `core`/`study`/`step`, ADR 0010).
- Cover the sources Chi listed (as the corpus / reading list, not cited on cards):
  1. Overview — Carl Cook, *When a Microsecond Is an Eternity* (CppCon 2017); David Gross, *Trading at Light Speed* (Meeting C++ 2022).
  2. How markets work — Larry Harris, *Trading and Exchanges*.
  3. How systems are built — Donadio et al., *Developing High-Frequency Trading Systems* (2022); LMAX Disruptor paper;
     Martin Thompson's *Mechanical Sympathy*.
  4. The machine — Ulrich Drepper, *What Every Programmer Should Know About Memory*; Brendan Gregg, *Systems Performance*.
  5. Protocols — Nasdaq TotalView-ITCH 5.0.
- **A dedicated deck: why Headlands (and HFT firms generally) hire Java engineers** — what Java is used for there
  (research platform, distributed compute farm, storage, monitoring, tooling, risk, some trading paths), which language /
  JVM characteristics matter (JIT, GC choices incl. ZGC/Shenandoah/Epsilon, off-heap, Chronicle/Aeron/Agrona/Disruptor,
  garbage-free coding, mechanical sympathy, JFR), how Java and C++ split work in such firms, related stacks
  (Kafka-style logs, columnar stores like kdb+/q, ClickHouse, Parquet, Python research, FPGA), and Chi's own insights
  framed as talking points for the interview.
- Reuse what already exists instead of rewriting: Headlands kit lectures (hc05 order book, hc07 ticker map, hc13 memory
  pool, ld01 SPSC, ld03 TCP channel), `core/cpp/headlands/lessons`, `core/foundations/headlands/cpu_cache_locality.md`,
  `core/system-design/headlands/sd03_low_latency_trading_system`, and the existing `quant-infra` / `markets` skeletons
  (link, don't duplicate; this domain is the engineering of the live trading path).

## Suggested shape (to refine in the skeleton step)

Market microstructure → exchanges & protocols (ITCH/OUCH/FIX, multicast + gap fill, MoldUDP64) → order book & matching →
tick-to-trade architecture (single-threaded event loop, sequencer, journal + replay, risk checks) → low-latency C++ →
low-latency Java → the machine (caches, NUMA, branch prediction, TLB/huge pages) → OS & network (pinning, isolcpus,
IRQ affinity, kernel bypass, PTP) → measurement (histograms, percentiles, coordinated omission, JFR/perf) →
reliability & compliance (15c3-5, kill switch, determinism) → FPGA & hardware overview → careers & how firms work
(roles, Java's place, interviews).

## Acceptance

`uv run trellis --domain <id> validate` 0 errors; every leaf has cards; cards pass `scripts/plain_style.py`
(and `phone_diagrams.py` for any diagram); `trellis --domain <id> steps` shows an order for every leaf;
build the deck and `anki-push` it on chi-mini (AnkiConnect at 127.0.0.1:8765).
