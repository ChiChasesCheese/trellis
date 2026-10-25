# Task — C++ versions of the three LLD problems (ld01, ld02, ld03), group H1

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never switch branches, never spawn agents. Kit:
`vault/interviews/companies/headlands/` (run its tools from there). Chi will write every kit problem twice tomorrow
(Java, then C++); the three LLD problems have Java only.

You own only: `loop/rounds/03_lld/ld01_spsc_channel/cpp/`, `loop/rounds/03_lld/ld02_trading_ood/cpp/`,
`loop/rounds/03_lld/ld03_async_tcp_channel/cpp/`, and new study articles `study/30-articles/ld01_spsc_channel_cpp.md`,
`ld02_trading_ood_cpp.md`, `ld03_async_tcp_channel_cpp.md`. Do not edit the Java files or `problem.md`.

For each problem: read `problem.md`, the Java `starter/`, `reference/`, `test/` and the Java study article; write
`cpp/starter.hpp` (same API, idiomatic C++20: RAII, `std::atomic` with explicit memory orders for the SPSC ring,
`std::jthread` / `std::condition_variable` or a small event loop for ld03 — no real sockets needed if the Java version
simulates them; mirror whatever the Java tests exercise), `cpp/reference.hpp`, and `cpp/test.cpp` porting the Java tests
(same Parts as tags, `perf` tag for timing tests). Layout and test macros: `CPP_CONVENTIONS.md`, `tools/cpp/minitest.hpp`,
and an existing port such as `loop/rounds/01_video/hc13_fixed_memory_pool/cpp/` (concurrency in C++). The `_cpp.md`
article follows `study/30-articles/hc13_fixed_memory_pool_cpp.md`: what changes from Java to C++ and why (memory model,
ownership, false sharing, `alignas(64)`), pitfalls, follow-ups. Learning-page rules: `proposals/WRITING_RULES.md`.

Acceptance: `python3 tools/cpptest.py verify "loop/rounds/03_lld/ld0*"` — reference green under ASan/UBSan (and TSan
if the tool supports it for that test), starter compiles with at least one red test; `uv run python
scripts/plain_style.py` (repo root) on the three articles. Reply ≤ 8 lines.
