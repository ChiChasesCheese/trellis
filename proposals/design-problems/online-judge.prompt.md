You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
Design Problems › Real-Time, Compute & AI Services › Online Judge (LeetCode)
Safely running untrusted code at contest scale: sandboxing, queues, and live leaderboards.

## Position in the knowledge map
Prerequisites (assume known):
  - Message Queues: Queues vs pub-sub, backpressure, consumer scaling, and when async is the wrong call.
  - Containers & Orchestration: Containers vs VMs, Kubernetes primitives (pods, services, autoscaling) at design-conversation depth.
Sibling topics (OUT of scope):
  - Online Multiplayer Game (Chess): Matchmaking, authoritative game state, low-latency moves and reconnection.
  - LLM Chat Service (ChatGPT): Streaming token delivery, GPU batching, conversation state, quotas and cost per request.
  - Calendar & Scheduling (Google Calendar): Recurring events, free/busy queries, invitations, reminders and time zones.
  - Real-Time Leaderboard: Rank millions of players live: sorted sets, sharded rankings and approximate rank.

## Rules
- Write 8 cards for THIS topic only. Sibling topics listed above are
  out of scope — never restate their material.
- One card = one retrievable fact, mechanism, trade-off, or number. If an
  answer needs more than ~4 sentences, split the card.
- Prefer questions that force discrimination ("when would you choose X
  over Y") over definitions, except for terms of art.
- Use `type: "cloze"` with {{c1::...}} syntax for formulas, sequences,
  and lists; `type: "qa"` otherwise.
- Markdown allowed in q/a/text (code spans, tables, lists).
- id: lowercase-hyphenated slug, unique, descriptive, stable.

## Output format (JSON array only, no prose)
[
  {"id": "example-qa-card", "node": "problems.realtime.online-judge", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.realtime.online-judge", "type": "cloze",
    "text": "The formula is {{c1::W + R > N}}.", "tags": []}
]

## Language and self-containment
- Write every card in English. Terms of art stay in English (the reader will
  meet them in code, configs and docs): write the English term and gloss
  it in English once per card, e.g. `consumer group（消费者群组）`.
- SELF-CONTAINED. A reader who has never heard of System Design must understand
  the card from the card alone: the question carries the situation it is
  asking about, the answer defines every term it uses and says WHY, not
  only what. Never "as discussed", "the book says", "see chapter 3" — nor
  their equivalents ("书中建议", "本书", "如前所述"): the importer refuses a
  card that leans on its source. State the advice as a fact.
- Prefer questions whose answer is a mechanism or a decision ("what happens
  when…", "why would you set…") over ones whose answer is a name.
- Do not set `source`; the importer records where these cards came from.

- This domain's cards also carry a Chinese translation, and its deck is
  reviewed in Chinese. Give every card one: `q_zh` and `a_zh` (for a cloze,
  `text_zh` with every `{{{{cN::…}}}}` deletion byte-identical), a faithful
  translation of your English — same structure, terms of art kept in
  English, nothing added or dropped.
