---
nodes: [problems.realtime.multiplayer-game, networking.realtime]
tags: [problem]
---
# Drill: Design an online multiplayer game like online chess

Design the backend for an online chess platform: players get matched by rating, play a
game where every move is validated by the server, each side has a countdown clock, either
player can disconnect mid-game, and a popular game can attract a large number of
spectators.

**Constraints to state and honor**
- 5M DAU, 10% play at least one game a day averaging 5 games each — about 2.5M games/day,
  the same order of magnitude as Lichess's real ~1.5-2M games/day.
- An active game averages a move roughly every 7 seconds; peak concurrent players run
  around 80,000, in the same order of magnitude as Lichess's reported 100K+ concurrent.
- The server is the sole authority on board state, clocks, and outcome — never the client.
- Disconnection must not mean an instant loss, but must not allow indefinite stalling either.

**Grading points**
- Widens the matchmaking rating window with wait time instead of using one fixed window
  ([[problems-multiplayer-game-widening-rating-window]]).
- States and defends the authoritative-server principle — the server never trusts a
  client's report of board state, clocks, or outcome
  ([[problems-multiplayer-game-never-trust-client-state]]).
- Contrasts turn-based chess's event-driven server against a fast-paced real-time game's
  fixed-tick-rate server, and can quantify roughly how much more often the real-time
  server has to work ([[problems-multiplayer-game-turnbased-vs-realtime-tick-rate]]).
- Gives each in-progress game its own single-threaded state owner so concurrent moves for
  the same game don't need a distributed lock
  ([[problems-multiplayer-game-per-game-actor-serializes-moves]]).
- Times moves from server-observed receipt with a small fixed lag-compensation allowance,
  rather than trusting client-reported elapsed time
  ([[problems-multiplayer-game-clock-lag-compensation]]).
- Uses a disconnection grace pool separate from the game clock, sized to the time control,
  handing the opponent the decision once it's exhausted
  ([[problems-multiplayer-game-disconnect-grace-pool]]).
- Recognizes that broadcasting a viral game to spectators is the same fan-out shape as a
  live-comment stream and reuses that architecture instead of reinventing it
  ([[problems-multiplayer-game-spectator-fanout-reuse-live-comments]]).
- Designs anti-cheat as a statistical model that routes suspicious players to human review,
  not an automatic ban rule ([[problems-multiplayer-game-statistical-anticheat-review-queue]]).

**Solution**: [[solution-multiplayer-game]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
