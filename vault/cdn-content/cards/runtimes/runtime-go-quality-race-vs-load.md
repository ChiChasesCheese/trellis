---
id: runtime-go-quality-race-vs-load
node: runtimes.go-quality
type: qa
---
## Q
A concurrent cache map passes unit and load tests. Is that evidence it is race-free? What test closes the gap?

## A
No. Timing-dependent data races can stay invisible while still corrupting state later. Run realistic concurrent tests under `go test -race`; the race detector instruments memory access and reports conflicting stacks, but only for executed paths. Combine it with high-contention tests and production-shaped traffic. Do not "fix" a report with sleeps; establish clear ownership or synchronization, then rerun the same workload.

## Q zh
一个并发 cache map 通过了 unit test 和 load test，这能证明它没有 race 吗？什么测试能补上缺口？

## A zh
不能。依赖时序的 data race 可能一直不显现，却在以后破坏状态。要在真实并发测试下运行 `go test -race`；race detector 会 instrument memory access 并报告冲突 stack，但只能发现实际执行到的路径。还要结合高竞争测试和 production-shaped traffic。不要用 sleep “修复”报告；应建立清晰 ownership 或 synchronization，再重跑同一 workload。
