You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
作答方法（Machine Coding Method） › 白板上的 UML（Class & Sequence Diagrams）
面试里真正用得上的 UML 子集：类图的四种箭头、时序图、状态图，画到什么粒度为止。

## Position in the knowledge map
Prerequisites (assume known):
  - 从需求到对象（Requirements to Objects）: 名词-动词抽取、找实体与不变量（invariant）、先画交互序列再画类图。
Sibling topics (OUT of scope):
  - 作答节奏（Delivery Framework）: 澄清需求、选核心流程、设计/编码/演示的时间盒，以及如何主导这一小时。
  - 评分标准（Evaluation Rubric）: 面试官打分的维度：可扩展、可读、可测，以及在对方之前先验证自己的代码。
  - 从需求到对象（Requirements to Objects）: 名词-动词抽取、找实体与不变量（invariant）、先画交互序列再画类图。

## Rules
- Write 5 cards for THIS topic only. Sibling topics listed above are
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
  {"id": "example-qa-card", "node": "method.diagrams", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "method.diagrams", "type": "cloze",
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
