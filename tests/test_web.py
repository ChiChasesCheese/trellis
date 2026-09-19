"""The Workbench: the loop as a page. Tested at the HTTP seam with Anki and
the Runner replaced by fakes, because the page is only allowed to do what
the API does."""

import json
import threading
import time
import urllib.request
from http.client import HTTPConnection

import pytest
import yaml

from trellis.traces import Trace, TraceFile, save_traces, traces_path
from trellis.web import serve

SKELETON = {
    "domain": "demo", "title": "Demo", "lang": "zh",
    "nodes": [
        {"id": "base", "title": "基础", "order": 1, "children": [
            {"id": "base.one", "title": "一", "summary": "第一件事。"},
            {"id": "base.two", "title": "二", "summary": "第二件事。"},
        ]},
        {"id": "mid", "title": "进阶", "order": 2, "children": [
            {"id": "mid.a", "title": "甲", "summary": "站在一之上。", "requires": ["base.one"]},
        ]},
    ],
}
CARD = "---\nid: {id}\nnode: {node}\ntype: qa\n---\n## Q\n{q}\n\n## A\n{a}\n"


def _card(root, cid, node, q, a):
    path = root / "vault" / "demo" / "cards" / node.split(".")[0] / f"{cid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CARD.format(id=cid, node=node, q=q, a=a), encoding="utf-8")


class FakeAnki:
    def __init__(self):
        self.calls: list[tuple[str, dict]] = []

    def __call__(self, action, url=None, **params):
        self.calls.append((action, params))
        if action == "findNotes":
            return []
        if action == "findCards":
            return [7, 8]
        if action in ("setDueDate", "guiBrowse", "guiDeckReview", "sync"):
            return True
        return None


class FakeRunner:
    """Answers any prompt with two cards; remembers what it was asked."""

    def __init__(self):
        self.prompts: list[str] = []

    def __call__(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return json.dumps([
            {"id": "grown-one", "type": "qa", "q": "从另一个角度看一？", "a": "这样看。"},
            {"id": "grown-two", "type": "qa", "q": "一失败时会怎样？", "a": "那样。"},
        ], ensure_ascii=False)


@pytest.fixture
def site(tmp_path):
    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "demo.yaml").write_text(
        yaml.safe_dump(SKELETON, allow_unicode=True), encoding="utf-8")
    for i in range(3):
        _card(tmp_path, f"one-{i}", "base.one", f"问一 {i}？", f"答一 {i}。")
        _card(tmp_path, f"two-{i}", "base.two", f"问二 {i}？", f"答二 {i}。")
    traces = {f"one-{i}": Trace(f"one-{i}", reps=6, lapses=4 - i, interval=1) for i in range(3)}
    traces |= {f"two-{i}": Trace(f"two-{i}", reps=3, lapses=0, interval=30) for i in range(3)}
    save_traces(traces_path(tmp_path, "demo"),
                TraceFile(domain="demo", pulled_at="2026-09-01T00:00:00+00:00", traces=traces))
    anki, runner = FakeAnki(), FakeRunner()
    server = serve(tmp_path, port=0, anki=anki, runner=runner, open_browser=False)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield tmp_path, server.server_address[1], anki, runner
    server.shutdown()


def call(port, method, path, body=None):
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    data = json.dumps(body).encode() if body is not None else None
    conn.request(method, path, body=data, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    raw = resp.read()
    return resp.status, (json.loads(raw) if resp.getheader("Content-Type", "").startswith("application/json") else raw)


def test_the_page_and_the_state_speak_chinese_and_show_the_weakness(site):
    root, port, _, _ = site
    status, page = call(port, "GET", "/")
    assert status == 200 and "工作台".encode() in page
    status, state = call(port, "GET", "/api/state?domain=demo")
    assert status == 200
    demo = state["domains"][0]
    assert demo["id"] == "demo" and demo["cards"] == 6 and demo["reviewed"] == 6
    assert demo["weak"] == 1 and demo["uncovered"] == 1
    leaves = {l["id"]: l for l in state["selected"]["leaves"]}
    assert leaves["base.one"]["weak"] and leaves["base.one"]["slipped"][0]["id"] == "one-0"
    assert leaves["mid.a"]["uncovered"] and leaves["mid.a"]["sealed"]
    assert leaves["base.one"]["obsidian"].startswith("obsidian://open?vault=vault&file=base.one")
    assert state["selected"]["targets"][0]["key"] == "demo:base.one"


def test_grow_runs_the_runner_with_guidance_and_lands_on_accept(site):
    root, port, anki, runner = site
    status, job = call(port, "POST", "/api/grow",
                       {"key": "demo:base.one", "count": 2, "guidance": "多举失败的例子"})
    assert status == 202 and job["status"] in ("running", "review")
    for _ in range(50):
        status, job = call(port, "GET", f"/api/jobs/{job['id']}")
        if job["status"] == "review":
            break
        time.sleep(0.1)
    assert job["status"] == "review", job
    assert "多举失败的例子" in runner.prompts[0] and "不合法" not in runner.prompts[0]
    assert [c["id"] for c in job["cards"]] == ["grown-one", "grown-two"]

    status, done = call(port, "POST", f"/api/jobs/{job['id']}/accept", {"push": False})
    assert status == 200 and done["status"] == "done" and len(done["written"]) == 2
    card = (root / "vault" / "demo" / "cards" / "base" / "grown-one.md").read_text(encoding="utf-8")
    assert "tags: [grown]" in card and "node: base.one" in card


def test_a_runner_answer_that_leans_on_the_source_is_refused_at_accept(site, monkeypatch):
    root, port, anki, runner = site
    # through monkeypatch, so the class answers properly again for the next test
    monkeypatch.setattr(FakeRunner, "__call__", lambda self, prompt: json.dumps(
        [{"id": "bad", "type": "qa", "q": "如前所述，一是什么？", "a": "一。"}], ensure_ascii=False))
    _, job = call(port, "POST", "/api/grow", {"key": "demo:base.one", "count": 1})
    for _ in range(50):
        _, job = call(port, "GET", f"/api/jobs/{job['id']}")
        if job["status"] == "review":
            break
        time.sleep(0.1)
    status, result = call(port, "POST", f"/api/jobs/{job['id']}/accept", {})
    assert status == 422 and "如前所述" in result["errors"][0]


def test_focus_makes_a_leafs_cards_due_today_and_opens_anki(site):
    root, port, anki, _ = site
    status, out = call(port, "POST", "/api/focus", {"keys": ["demo:base.one"], "action": "today"})
    assert status == 200 and out["cards"] == 2
    actions = [a for a, _ in anki.calls]
    assert "setDueDate" in actions
    query = next(p["query"] for a, p in anki.calls if a == "findCards")
    assert "tag:demo::base::one" in query
    status, out = call(port, "POST", "/api/focus", {"keys": ["demo:base.one"], "action": "browse"})
    assert status == 200 and any(a == "guiBrowse" for a, _ in anki.calls)


def test_pull_writes_traces_and_history_reads_them_back(site):
    root, port, anki, _ = site
    status, out = call(port, "POST", "/api/pull", {"domain": "demo"})
    assert status == 200 and out["domains"][0]["traced"] == 0
    status, hist = call(port, "GET", "/api/history?domain=demo")
    assert status == 200 and isinstance(hist["points"], list)


def test_a_leaf_just_grown_on_shows_its_graft_and_is_not_offered_again(site):
    root, port, _, _ = site
    _, job = call(port, "POST", "/api/grow", {"key": "demo:base.one", "count": 2, "guidance": ""})
    for _ in range(50):
        _, job = call(port, "GET", f"/api/jobs/{job['id']}")
        if job["status"] == "review":
            break
        time.sleep(0.1)
    status, done = call(port, "POST", f"/api/jobs/{job['id']}/accept", {"push": False})
    assert status == 200, done

    _, state = call(port, "GET", "/api/state?domain=demo")
    one = {l["id"]: l for l in state["selected"]["leaves"]}["base.one"]
    assert one["weak"] and one["settling"]
    assert one["graft"] == {"state": "settling", "grown": 2, "unseen": 2, "young": 0,
                            "taken": 0, "slipped": 0, "query": "tag:demo::base::one tag:grown"}
    assert "demo:base.one" not in [t["key"] for t in state["selected"]["targets"]]
    assert state["domains"][0]["settling"] == 1

    status, refused = call(port, "POST", "/api/grow", {"key": "demo:base.one", "count": 2})
    assert status == 409 and "2 张新卡" in refused["error"]
