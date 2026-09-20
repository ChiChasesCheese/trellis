You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
Python 对象模型与惯用法（Pythonic Design） › 数据模型与特殊方法（Data Model）
`__eq__`/`__hash__`/`__repr__`/排序与容器协议：让自定义对象像内置类型一样工作，以及相等与哈希的契约。

## Position in the knowledge map
Sibling topics (OUT of scope):
  - dataclass 与 Enum: `@dataclass(frozen, slots, order)`、`field(default_factory)`、带行为的 `Enum`：值对象与有限状态的标准写法。
  - Protocol、ABC 与鸭子类型: `typing.Protocol` 的结构化子类型、`abc.ABC` 的名义子类型、何时两者都不需要。
  - 一等函数、闭包与装饰器: 函数即对象如何替代策略、命令、模板方法等单方法接口；`functools` 的常用工具。
  - 上下文管理器、迭代器与生成器: `with` 保证成对操作、`__iter__`/生成器实现惰性遍历：资源管理与迭代器模式的 Python 形态。
  - 类型注解作为设计工具: 泛型、`TypeVar`、`Literal`、`NewType`、`Optional` 的取舍：让接口自解释，让错误在写代码时暴露。
  - 模块、包与依赖方向: 模块即单例、循环导入的成因与解法、`__init__` 里的公共接口、依赖只许朝一个方向流。

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
  {"id": "example-qa-card", "node": "python.data-model", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "python.data-model", "type": "cloze",
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
