---
nodes: [problems.realtime.online-judge, async.queues, infra.containers]
tags: [problem]
---
# Drill: Design an online judge like LeetCode or Codeforces

Design a system where users submit code, the system compiles and runs it against a set of
test cases, and returns a verdict. The system also runs timed contests: a fixed start time,
a leaderboard ranking contestants by problems solved and penalty time, and a burst of
submissions right when the contest opens.

**Constraints to state and honor**
- A weekly contest has 100,000 registrants, 80,000 of whom actually show up at the start;
  50% of them submit to the first problem within the first 5 minutes.
- Every execution must run in a sandbox with zero tolerance for escape — the code is
  anonymous and untrusted.
- TLE must be judged consistently regardless of how busy the host is at the time.
- Contest start time and registrant count are known well in advance of the burst.

**Grading points**
- Uses Little's Law to size burst sandbox concurrency from arrival rate and average judge
  time, and pre-warms worker capacity ahead of the known contest start rather than relying
  only on reactive autoscaling ([[problems-online-judge-burst-littles-law-prewarm]]).
- Chooses a Firecracker microVM per submission over a plain container or gVisor for
  anonymous untrusted code, and can state what each option actually isolates and what it
  costs ([[problems-online-judge-firecracker-vs-container-vs-gvisor]]).
- Judges Time Limit Exceeded against CPU time from a cgroup, not wall-clock time, while
  still capping wall-clock time separately ([[problems-online-judge-cpu-time-vs-wallclock-fairness]]).
- Limits process count independently of CPU and memory via the cgroup pids controller to
  stop fork bombs ([[problems-online-judge-pids-limit-fork-bomb]]).
- Streams per-test-case verdicts over SSE rather than WebSocket, and explains why the
  channel only needs one direction ([[problems-online-judge-sse-not-websocket-verdict-stream]]).
- Partitions the judge queue by contestId for cache locality, and describes how tenant
  isolation must evolve into physically separate queues at 10x scale
  ([[problems-online-judge-queue-partition-by-contest-tenant-isolation]]).
- Destroys every sandbox after a single submission and explains why the Firecracker choice
  from the isolation deep dive is what makes that affordable
  ([[problems-online-judge-single-use-sandbox-leakage]]).
- Routes plagiarism-detection matches to human review instead of automated bans
  ([[problems-online-judge-plagiarism-review-not-autoban]]).

**Solution**: [[solution-online-judge]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
