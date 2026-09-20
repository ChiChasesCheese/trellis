You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
设计题（Design Problems） › 游戏与规则 › 井字棋（Tic-Tac-Toe）
N×N 棋盘 O(1) 胜负判定、玩家轮转与可扩展规则——最常见的热身题。

## Position in the knowledge map
Prerequisites (assume known):
  - 从需求到对象（Requirements to Objects）: 名词-动词抽取、找实体与不变量（invariant）、先画交互序列再画类图。
Sibling topics (OUT of scope):
  - 国际象棋（Chess）: 棋子多态的走法生成、将军与将死判定、特殊着法与悔棋。
  - 蛇梯棋（Snake and Ladder）: 可配置棋盘与骰子策略、多人回合与胜利条件。
  - 体育比分系统（Cricinfo）: 比赛-局-回合的事件流建模，实时比分与统计的派生。
  - 扑克牌与二十一点（Deck of Cards / Blackjack）: 通用牌组抽象，在其上实现具体游戏规则而不改动牌组。

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
  {"id": "example-qa-card", "node": "problems.games.tic-tac-toe", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.games.tic-tac-toe", "type": "cloze",
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
