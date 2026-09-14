---
id: infra-two-phase-format-rollout
node: infra.delivery
type: cloze
---
To change a persisted or on-the-wire data format safely, serialize the change across **two releases** — the deploy-time twin of expand–contract schema migration. Release 1 ({{c1::"prepare": ship code that can *read* the new format but still *writes* the old one}}) rolls out everywhere first; only then does release 2 ({{c2::"activate": start *writing* the new format — ideally behind a feature flag, so activation is a runtime toggle, not a deploy}}) go out. The ordering rule to memorize: {{c3::readers before writers}} — at every instant, including mid-rollout and after a rollback of release 2, every running version can read everything any version writes.

## zh
要安全地更改持久化或线上传输（on-the-wire）的数据格式，把变更串行化到**两个 release** — 这是 expand–contract schema migration 在部署期的孪生兄弟。Release 1（{{c1::"prepare"：发布能*读*新格式、但仍然*写*旧格式的代码}}）先全量铺开；然后 release 2（{{c2::"activate"：开始*写*新格式 — 最好放在 feature flag 后面，让激活是一次运行时开关而不是一次部署}}）才出发。要背下来的顺序规则：{{c3::readers before writers（先上读者，再上写者）}} — 在每一个瞬间，包括铺开中途和 release 2 回滚之后，每个在跑的版本都能读懂任何版本写下的东西。
