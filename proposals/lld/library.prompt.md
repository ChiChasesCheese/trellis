You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
设计题（Design Problems） › 预订与库存 › 图书馆管理（Library Management）
书目与馆藏副本的区分、借还与预约队列、逾期罚金。

## Position in the knowledge map
Prerequisites (assume known):
  - 类之间的关系（Class Relationships）: 关联、聚合、组合、依赖的区别；生命周期归属，以及各自的 UML 箭头。
Sibling topics (OUT of scope):
  - 电影订票（BookMyShow）: 影院-影厅-场次-座位的层级模型，选座锁定、超时释放与并发下单。
  - 酒店预订（Hotel Booking）: 按房型与日期区间的可订量、预订生命周期与取消规则。
  - 租车系统（Car Rental）: 车辆库存按门店与时间段可用性查询、预订、取还车与计费。
  - 航班管理（Airline Management）: 航班-航段-座位的建模、订座与值机、改签与取消。
  - 会议室预订（Meeting Scheduler）: 时间区间冲突检测、会议室容量匹配、周期会议与通知。
  - 餐厅管理（Restaurant Management）: 桌位预订、点单到后厨的订单流转、结账拆单。

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
  {"id": "example-qa-card", "node": "problems.booking.library", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.booking.library", "type": "cloze",
    "text": "The formula is {{c1::W + R > N}}.", "tags": []}
]

## Language and self-containment
- Write every card in Chinese (简体中文). Terms of art stay in English (the reader will
  meet them in code, configs and docs): write the English term and gloss
  it in Chinese (简体中文) once per card, e.g. `consumer group（消费者群组）`.
- SELF-CONTAINED. A reader who has never heard of 低层设计（LLD） must understand
  the card from the card alone: the question carries the situation it is
  asking about, the answer defines every term it uses and says WHY, not
  only what. Never "as discussed", "the book says", "see chapter 3" — nor
  their equivalents ("书中建议", "本书", "如前所述"): the importer refuses a
  card that leans on its source. State the advice as a fact.
- Prefer questions whose answer is a mechanism or a decision ("what happens
  when…", "why would you set…") over ones whose answer is a name.
- Do not set `source`; the importer records where these cards came from.
