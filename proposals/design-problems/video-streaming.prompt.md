You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
Design Problems › Media, Files & Collaboration › Video Streaming (YouTube/Netflix)
Upload, transcoding pipelines, adaptive bitrate delivery and the economics of the CDN.

## Position in the knowledge map
Prerequisites (assume known):
  - CDN: Push vs pull CDNs, cache keys, and what belongs at the edge.
  - Object Storage & Separation: S3-style object stores, storage-compute separation, and the modern default of parking cold and big data there.
Sibling topics (OUT of scope):
  - Collaborative Editing (Google Docs): Concurrent edits converging through OT or CRDTs, cursors and presence, and document storage.
  - File Sync (Dropbox/Google Drive): Chunking, deduplication, delta sync, conflict handling and metadata consistency across devices.
  - Email Service (Gmail): Sending and receiving at scale: SMTP edges, mailbox storage, search, spam and threading.
  - Video Conferencing (Zoom): Real-time media: SFU vs MCU, signalling, NAT traversal, and degrading gracefully on bad networks.

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
  {"id": "example-qa-card", "node": "problems.media.video-streaming", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.media.video-streaming", "type": "cloze",
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
