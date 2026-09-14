---
nodes: [patterns.behavioral]
url: https://gameprogrammingpatterns.com/observer.html
tags: [canonical]
---
# Observer (Game Programming Patterns, Bob Nystrom)

The best free critical treatment of a behavioral pattern: Nystrom implements
observer from scratch, then spends the rest of the chapter on what actually
bites — synchronous dispatch on the caller's thread, who owns whose lifetime,
destroyed observers left in subject lists, and when an event queue is the
right answer instead. Exactly the reasoning an interviewer wants when you
reach for observer in a notification/leaderboard/logging requirement.

**Extract on read:**
- Observer decouples *what happened* from *who cares*; the subject must not
  know its observers' types — that's the whole point, and the test of whether
  you have used it right.
- The failure modes: reentrancy during notification, observers mutating the
  subject, dangling observers (register/unregister must be symmetric), and
  the fact that notify runs synchronously in the caller's stack.
- When to stop: if you need buffering, ordering, or cross-thread delivery,
  the pattern you want is an event queue, not more observers.

%% trellis:begin %%
## Source
[Open the original ↗](https://gameprogrammingpatterns.com/observer.html)

## Archived copy
![[gpp-observer-clip]]
%% trellis:end %%
