"""A corpus enters: seed a skeleton from its outline, triage its sections
onto the leaves, digest cards leaf by leaf, build the corpus view."""

import json
import sqlite3
import zipfile
from pathlib import Path

import pytest

from trellis.cli import main

# Section ids are what the markdown adapter derives: ordinal + ASCII slug.
SECTIONS = {
    "001-front": ("Front 前言", "本书是为工程师而写的。"),
    "002-3-4-2-acks": ("3.4.2 acks", "acks 指定了生产者在多少个分区副本收到消息时认为写入成功。"
                                     "acks=0 不等待；acks=1 首领收到即可；acks=all 全部同步副本。"),
    "003-4-1-groups": ("4.1 groups 消费者群组", "同一个 consumer group 里的消费者分摊一个主题的分区。"),
}


def _md_book(path: Path) -> Path:
    body = "\n\n".join(f"# {title}\n\n{text}" for title, text in SECTIONS.values())
    path.write_text(body + "\n", encoding="utf-8")
    return path


@pytest.fixture
def root(tmp_path):
    (tmp_path / "corpora").mkdir()
    (tmp_path / "corpora" / "kafka-test.yaml").write_text(
        "title: Kafka测试\nlicense: commercial\ndomain: kafka\nlang: zh\n"
        f"home: https://example.org/kafka\nfile: {_md_book(tmp_path / 'kafka.md')}\n",
        encoding="utf-8")
    (tmp_path / "vault").mkdir()
    return tmp_path


def run(root, *argv):
    return main(["--root", str(root), *argv])


SEED = {
    "corpus": "kafka-test",
    "skeleton": {"domain": "kafka", "title": "Kafka", "nodes": [
        {"id": "producer", "title": "生产者", "summary": "写入", "children": [
            {"id": "producer.acks", "title": "acks 与持久性", "summary": "多少副本确认才算写入成功。"}]},
        {"id": "consumer", "title": "消费者", "summary": "读取", "children": [
            {"id": "consumer.groups", "title": "consumer group", "summary": "分区如何在消费者间分摊。"},
            {"id": "consumer.rebalance", "title": "再均衡", "summary": "成员变动时分区如何重新分配。",
             "requires": ["producer.acks"]}]},
    ]},
    "uncovered": ["consumer.rebalance"],
}

TRIAGE = {"corpus": "kafka-test", "items": [
    {"section": "001-front", "verdict": "skip", "why": "front matter"},
    {"section": "002-3-4-2-acks", "verdict": "reading", "nodes": ["producer.acks"],
     "slug": "kt-acks", "title": "acks 的三个值", "body": "读它是为了知道写入成功意味着什么。"},
    {"section": "003-4-1-groups", "verdict": "reading", "nodes": ["consumer.groups"],
     "slug": "kt-groups", "title": "消费者群组", "body": "分区分摊的规则。"},
]}


def _seed_and_triage(root, capsys):
    assert run(root, "ingest", "kafka-test") == 0
    seed = root / "seed.json"
    seed.write_text(json.dumps(SEED, ensure_ascii=False), encoding="utf-8")
    assert run(root, "accept", str(seed)) == 0
    assert (root / "skeleton" / "kafka.yaml").exists()
    assert "uncovered: consumer.rebalance" in capsys.readouterr().out
    prop = root / "triage.json"
    prop.write_text(json.dumps(TRIAGE, ensure_ascii=False), encoding="utf-8")
    assert run(root, "accept", str(prop)) == 0


def test_seed_prompt_carries_the_outline_and_refuses_an_existing_skeleton(root, capsys):
    run(root, "ingest", "kafka-test")
    assert run(root, "seed", "kafka-test", "-o", str(root / "seed.md")) == 0
    prompt = (root / "seed.md").read_text(encoding="utf-8")
    assert "`002-3-4-2-acks` 3.4.2 acks" in prompt and "domain slug: `kafka`" in prompt
    assert "Chinese" in prompt
    _seed_and_triage(root, capsys)
    with pytest.raises(SystemExit):
        run(root, "seed", "kafka-test")


def test_seed_is_validated_with_the_real_loader(root, capsys):
    run(root, "ingest", "kafka-test")
    bad = json.loads(json.dumps(SEED))
    bad["skeleton"]["nodes"][1]["children"][1]["requires"] = ["nowhere"]
    (root / "bad.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(SystemExit):
        run(root, "accept", str(root / "bad.json"))
    assert not (root / "skeleton" / "kafka.yaml").exists()
    assert "requires unknown node" in capsys.readouterr().err


def test_triage_writes_readings_with_provenance_and_no_clipping_for_a_paid_book(root, capsys):
    _seed_and_triage(root, capsys)
    reading = (root / "vault/kafka/readings/kt-acks.md").read_text(encoding="utf-8")
    assert "corpus: kafka-test" in reading and "section: 002-3-4-2-acks" in reading
    assert "url: https://example.org/kafka" in reading and "- book" in reading
    assert not (root / "vault/kafka/clippings").exists()
    assert run(root, "--domain", "kafka", "validate") == 0


def test_triage_prompt_lists_sections_beside_leaves(root, capsys):
    run(root, "ingest", "kafka-test")
    (root / "seed.json").write_text(json.dumps(SEED, ensure_ascii=False), encoding="utf-8")
    run(root, "accept", str(root / "seed.json"))
    assert run(root, "triage", "kafka-test", "-o", str(root / "t.md")) == 0
    prompt = (root / "t.md").read_text(encoding="utf-8")
    assert "`producer.acks`" in prompt and "`002-3-4-2-acks` (L1) 3.4.2 acks" in prompt
    assert "acks 指定了" in prompt, "the excerpt shows the section's opening"


def test_digest_status_prompt_and_import(root, capsys):
    _seed_and_triage(root, capsys)
    assert run(root, "digest", "kafka-test") == 0
    out = capsys.readouterr().out
    assert "0/2 leaves digested" in out and "todo  producer.acks" in out

    assert run(root, "digest", "kafka-test", "--next", "-o", str(root / "p.md")) == 0
    prompt = (root / "p.md").read_text(encoding="utf-8")
    assert "acks 与持久性" in prompt                      # the scaffold context
    assert "acks=all 全部同步副本" in prompt              # the grounding text
    assert "SELF-CONTAINED" in prompt and "Chinese" in prompt

    answer = [{"id": "kt-acks-all", "type": "qa",
               "q": "生产者把 acks 设为 all 时，什么情况下才收到写入成功？",
               "a": "所有同步副本（in-sync replicas）都收到消息之后。"},
              {"id": "kt-acks-zero", "type": "cloze",
               "text": "acks=0 时生产者{{c1::不等待任何 broker 响应}}，所以消息可能丢失。"}]
    (root / "a.json").write_text(json.dumps(answer, ensure_ascii=False), encoding="utf-8")
    assert run(root, "digest", "kafka-test", "--import", str(root / "a.json"),
               "--leaf", "producer.acks") == 0
    card = (root / "vault/kafka/cards/producer/kt-acks-all.md").read_text(encoding="utf-8")
    assert "node: producer.acks" in card and "source: kafka-test" in card
    assert "## Q\n生产者把 acks" in card, "written in the domain's language, no English original"

    run(root, "digest", "kafka-test", "--status")
    out = capsys.readouterr().out
    assert "1/2 leaves digested" in out and "done  producer.acks" in out
    # The next prompt moves on to the leaf still to do.
    run(root, "digest", "kafka-test", "--next", "-o", str(root / "p2.md"))
    assert "consumer group" in (root / "p2.md").read_text(encoding="utf-8")

    # A card aimed at a different leaf is refused whole.
    wrong = [{"id": "kt-stray", "node": "consumer.groups", "type": "qa", "q": "x?", "a": "y."}]
    (root / "w.json").write_text(json.dumps(wrong), encoding="utf-8")
    with pytest.raises(SystemExit):
        run(root, "digest", "kafka-test", "--import", str(root / "w.json"), "--leaf", "producer.acks")
    assert not (root / "vault/kafka/cards/producer/kt-stray.md").exists()


def test_corpus_build_is_a_filter_and_the_note_annotates_the_outline(root, capsys):
    _seed_and_triage(root, capsys)
    answer = [{"id": "kt-acks-all", "type": "qa", "q": "q?", "a": "a."}]
    (root / "a.json").write_text(json.dumps(answer), encoding="utf-8")
    run(root, "digest", "kafka-test", "--import", str(root / "a.json"), "--leaf", "producer.acks")
    hand = root / "vault/kafka/cards/consumer/hand-written.md"
    hand.parent.mkdir(parents=True)
    hand.write_text("---\nid: hand-written\nnode: consumer.groups\ntype: qa\n---\n## Q\nq?\n\n## A\na.\n",
                    encoding="utf-8")

    assert run(root, "--domain", "kafka", "build", "--corpus", "kafka-test") == 0
    apkg = root / "dist" / "kafka.kafka-test.apkg"
    assert apkg.exists()
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", root / "x")
    con = sqlite3.connect(root / "x" / "collection.anki2")
    tags = [row[0] for row in con.execute("select tags from notes")]
    assert len(tags) == 1 and "src::kafka-test" in tags[0]

    assert run(root, "--domain", "kafka", "sync") == 0
    note = (root / "vault/Corpora/kafka-test.md").read_text(encoding="utf-8")
    assert "**3.4.2 acks** — [[kt-acks|acks 的三个值]] → [[producer.acks|acks 与持久性]] · 1 cards" in note
    assert "- Front 前言 — *skipped*" in note
    assert "never reached (1)" in note and "[[consumer.rebalance|再均衡]]" in note
    assert "2/3 leaves reached" in note
