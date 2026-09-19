"""The Workbench: the loop as a page, served from the repository it sits in.

`trellis serve` starts a small HTTP server on this machine and opens the
page. Everything the page does is a command the CLI already has — pull,
brief, grow, focus, open in Obsidian or Anki — so the API is thin and the
tests drive it with Anki and the Runner replaced by fakes (ADR 0007).

    GET  /                       the page
    GET  /api/state?domain=      every domain's standing; one domain's leaves and targets
    GET  /api/history?domain=    Hold over past pulls, from the traces file's git history
    POST /api/pull               {domain} — read Anki into traces/
    POST /api/grow               {key, count, guidance, model} — start a Runner job
    GET  /api/jobs               every job; GET /api/jobs/<id> one
    POST /api/jobs/<id>/accept   {push} — validate and write the cards, optionally push
    POST /api/focus              {keys, action: today|browse|review}
"""

from __future__ import annotations

import json
import subprocess
import threading
import uuid
import webbrowser
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .anki import AnkiConnectError, invoke
from .brief import brief_body
from .build import build_package
from .grow import Target, grow_prompt, import_grown, plan as grow_plan, shortlist
from .hold import LeafStanding, assess, grown_query
from .obsidian import open_uri, vault_name
from .project import domains, load_loop
from .runner import ClaudeRunner, RunnerError, cards_from
from .sequence import sequence
from .traces import load_traces, save_traces, traces_path

JOBS_DIRNAME = ".trellis/jobs"
PAGE = Path(__file__).with_name("workbench.html")


@dataclass
class Job:
    id: str
    key: str
    kind: str
    count: int
    guidance: str
    model: str
    status: str = "running"          # running | review | done | failed
    prompt: str = ""
    cards: list[dict] = field(default_factory=list)
    written: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    pushed: str = ""
    created: str = ""
    finished: str = ""


_CLOZE = __import__("re").compile(r"\{\{c\d+::(.*?)(?:::[^}]*)?\}\}")


def _front(card) -> str:
    """A card's front as a person would read it: a cloze shows its text
    with the deletions filled in, since on the page there is nothing to
    hide."""
    text = (card.question or card.text or "").strip()
    return _CLOZE.sub(r"\1", text)[:120]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _public(job: "Job") -> dict:
    """A job as the page sees it: everything but the prompt, which is
    long and lives in the job file for anyone who wants to read it."""
    row = asdict(job)
    row.pop("prompt", None)
    return row


class StillSettling(ValueError):
    """The leaf was grown on already and its new cards are not yet judged."""


def _graft(domain: str, s: LeafStanding) -> dict | None:
    g = s.graft
    if g is None:
        return None
    return {"state": g.state, "grown": g.grown, "unseen": g.unseen, "young": g.young,
            "taken": g.taken, "slipped": g.slipped, "query": grown_query(domain, s.node.id)}


class Workbench:
    """The application: state reads, and the few actions. Holds nothing
    the vault does not, except the job list."""

    def __init__(self, root: Path, anki=None, runner=None):
        self.root = Path(root)
        self.anki = anki or invoke
        self.runner = runner
        self.jobs: dict[str, Job] = {}
        self.lock = threading.Lock()
        self._load_jobs()

    # -- jobs on disk, so a reload of the page still shows them
    def _jobs_dir(self) -> Path:
        d = self.root / JOBS_DIRNAME
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _load_jobs(self) -> None:
        for path in sorted(self._jobs_dir().glob("*.json")):
            if path.stem.startswith("_") or path.name.endswith(".answer.json"):
                continue
            try:
                job = Job(**json.loads(path.read_text(encoding="utf-8")))
            except (ValueError, TypeError):
                continue
            if job.status == "running":
                # Its thread died with the server that started it.
                job.status, job.errors = "failed", ["the Workbench was restarted while this job ran"]
                job.finished = _now()
                self._save(job)
            self.jobs[job.id] = job

    def _save(self, job: Job) -> None:
        (self._jobs_dir() / f"{job.id}.json").write_text(
            json.dumps(asdict(job), ensure_ascii=False, indent=1), encoding="utf-8")

    # -- reads
    def state(self, selected: str | None) -> dict:
        names = domains(self.root)
        projects, assessments, traces, ages = load_loop(self.root, names)
        vault = vault_name(self.root / "vault")
        out = {"domains": [], "selected": None, "brief": ""}
        for name in names:
            a, p = assessments[name], projects[name]
            out["domains"].append({
                "id": name, "title": p.skeleton.title, "lang": p.skeleton.lang,
                "cards": a.total, "reviewed": a.reviewed,
                "adopted": sum(1 for c in p.cards if c.adopted),
                "hold": a.hold, "weak": len(a.weaknesses()),
                "uncovered": len(a.uncovered()), "sealed": len(a.sealed()),
                "settling": len(a.settling()),
                "age_days": ages[name], "leaves": len(p.skeleton.leaves()),
                "readings": len(p.readings), "drills": len(p.drills),
            })
        skeletons = {n: projects[n].skeleton for n in names}
        drills, readings = {}, {}
        for p in projects.values():
            for d in p.drills:
                for n in d.nodes:
                    drills.setdefault(n, []).append(d)
            for r in p.readings:
                for n in r.nodes:
                    readings.setdefault(n, []).append(r)
        if assessments:
            out["brief"] = brief_body(assessments, skeletons, drills, readings, ages)
        if selected and selected in names:
            p, a = projects[selected], assessments[selected]
            targets = grow_plan(self.root, {selected: p}, {selected: a}, {selected: traces[selected]})
            by_leaf = {t.standing.node.id: t for t in targets}
            cards_by_node: dict[str, list] = {}
            for c in p.cards:
                cards_by_node.setdefault(c.node, []).append(c)
            leaves = []
            for s in a.leaves:
                node = s.node
                t = by_leaf.get(node.id)
                leaves.append({
                    "id": node.id, "title": node.title, "summary": node.summary,
                    "branch": node.path()[0].id, "branch_title": node.path()[0].title,
                    "cards": s.cards, "seen": s.seen, "hold": s.hold, "bearing": s.bearing,
                    "weak": s.weak, "uncovered": s.uncovered, "unproven": s.unproven,
                    "sealed": s.sealed, "sealed_by": s.sealed_by,
                    "settling": s.settling, "graft": _graft(selected, s),
                    "adopted": sum(1 for c in cards_by_node.get(node.id, []) if c.adopted),
                    "grown": sum(1 for c in cards_by_node.get(node.id, []) if "grown" in c.tags),
                    "readings": [r.title for r in readings.get(node.id, [])][:3],
                    "drills": [d.title for d in drills.get(node.id, [])][:3],
                    "grounding": t.grounding if t else "",
                    "slipped": [{"id": c.id, "q": _front(c),
                                 "reps": tr.reps, "lapses": tr.lapses, "interval": tr.interval}
                                for c, tr in (t.slipped if t else [])],
                    "obsidian": open_uri(vault, node.id),
                    "deck": p.skeleton.deck_name(node),
                })
            branches = [{"id": r.id, "title": r.title, "hold": a.node_hold.get(r.id),
                         "leaves": [l.id for l in p.skeleton.leaves() if l.path()[0] is r]}
                        for r in p.skeleton.roots]
            out["selected"] = {
                "id": selected, "title": p.skeleton.title, "leaves": leaves,
                "branches": branches,
                "targets": [{"key": t.key, "kind": t.kind, "grounding": t.grounding,
                             "title": t.standing.node.title}
                            for t in shortlist(targets, cap=12, limit=12)],
            }
        return out

    def history(self, domain: str) -> dict:
        """Hold after every pull that was committed: the traces file's git
        history, each version assessed against the cards of today."""
        path = self.root / "traces" / f"{domain}.json"
        points = []
        try:
            log = subprocess.run(
                ["git", "log", "--format=%H|%cI", "--", str(path.relative_to(self.root))],
                cwd=self.root, capture_output=True, text=True, timeout=30)
        except (OSError, ValueError, subprocess.TimeoutExpired):
            log = None
        if log and log.returncode == 0 and log.stdout.strip():
            projects, _, _, _ = load_loop(self.root, [domain])
            project = projects[domain]
            for line in reversed(log.stdout.strip().splitlines()):
                sha, when = line.split("|", 1)
                shown = subprocess.run(["git", "show", f"{sha}:traces/{domain}.json"],
                                       cwd=self.root, capture_output=True, text=True)
                if shown.returncode != 0:
                    continue
                tmp = self._jobs_dir() / f"_hist-{sha[:8]}.json"
                tmp.write_text(shown.stdout, encoding="utf-8")
                file = load_traces(tmp)
                tmp.unlink(missing_ok=True)
                a = assess(project.skeleton, project.cards, file.traces if file else {})
                points.append({"sha": sha[:8], "at": when, "hold": a.hold,
                               "reviewed": a.reviewed, "weak": len(a.weaknesses())})
        return {"domain": domain, "points": points}

    # -- actions
    def pull(self, domain: str | None) -> dict:
        from .anki import pull as anki_pull
        names = [domain] if domain else domains(self.root)
        projects, _, _, _ = load_loop(self.root, names)
        rows = []
        for name in names:
            file = anki_pull(projects[name].skeleton, call=self.anki)
            save_traces(traces_path(self.root, name), file)
            rows.append({"domain": name, "traced": len(file.traces),
                         "reviewed": sum(1 for t in file.traces.values() if t.seen),
                         "unmapped": file.unmapped})
        return {"domains": rows}

    def _target(self, key: str) -> tuple[Target, dict]:
        domain = key.split(":", 1)[0]
        projects, assessments, traces, _ = load_loop(self.root, [domain])
        for s in assessments[domain].settling():
            if f"{domain}:{s.node.id}" == key:
                g = s.graft
                raise StillSettling(
                    f"这个叶子已经长出 {g.grown} 张新卡，其中 {g.unseen + g.young} 张还没复习到能下结论；"
                    f"先复习它们：{grown_query(domain, s.node.id)}")
        for t in grow_plan(self.root, projects, assessments, traces):
            if t.key == key:
                return t, projects
        raise KeyError(key)

    def start_grow(self, key: str, count: int, guidance: str, model: str) -> Job:
        target, projects = self._target(key)
        prompt = grow_prompt(projects[target.domain], target, self.root, count=count)
        if guidance.strip():
            prompt += ("\n## Guidance from the learner\n"
                       "Follow this above every default in the rules:\n" + guidance.strip() + "\n")
        job = Job(id=uuid.uuid4().hex[:8], key=key, kind=target.kind, count=count,
                  guidance=guidance, model=model, prompt=prompt, created=_now())
        with self.lock:
            self.jobs[job.id] = job
        self._save(job)
        threading.Thread(target=self._run, args=(job,), daemon=True).start()
        return job

    def _run(self, job: Job) -> None:
        runner = self.runner or ClaudeRunner(model=job.model)
        try:
            job.cards = cards_from(runner(job.prompt))
            job.status = "review"
        except RunnerError as exc:
            job.errors = [str(exc)]
            job.status = "failed"
        job.finished = _now()
        self._save(job)

    def accept(self, job_id: str, push: bool) -> Job:
        job = self.jobs[job_id]
        if job.status != "review":
            raise ValueError(f"job {job_id} is {job.status}, not awaiting review")
        target, projects = self._target(job.key)
        project = projects[target.domain]
        answer = self._jobs_dir() / f"{job.id}.answer.json"
        answer.write_text(json.dumps(job.cards, ensure_ascii=False), encoding="utf-8")
        written, errors = import_grown(project, target, answer, project.content_dir(self.root) / "cards")
        if errors:
            job.errors = errors
            self._save(job)
            raise ValueError("; ".join(errors))
        job.written = [str(p.relative_to(self.root)) for p in written]
        job.status = "done"
        if push:
            job.pushed = self._push(target.domain)
        job.finished = _now()
        self._save(job)
        return job

    def _push(self, domain: str) -> str:
        from .anki import push as anki_push
        projects, _, _, _ = load_loop(self.root, [domain])
        project = projects[domain]
        lang = "" if project.skeleton.lang != "en" else ("zh" if any(c.tr.get("zh") for c in project.cards) else "")
        apkg = self.root / "dist" / f"{domain}{'.' + lang if lang else ''}.apkg"
        build_package(project.skeleton, project.cards, apkg, project.readings,
                      vault=vault_name(self.root / "vault"), clippings=project.clippings,
                      cases=project.cases, lang=lang, order=project.skeleton.study.order)
        ordered = [c.id for c in sequence(project.skeleton, project.cards,
                                          project.skeleton.study.order)]
        result = anki_push(project.skeleton, apkg, call=self.anki, ordered=ordered)
        return "; ".join(result["steps"])

    def focus(self, keys: list[str], action: str) -> dict:
        """Act on the collection for a few leaves at once."""
        queries, decks = [], []
        for key in keys:
            domain, node_id = key.split(":", 1)
            tag = f"{domain}::{node_id.replace('.', '::')}"
            queries.append(f"(tag:{tag} -tag:{tag}::*)")
            projects, _, _, _ = load_loop(self.root, [domain])
            node = projects[domain].skeleton.by_id.get(node_id)
            if node is not None:
                decks.append(projects[domain].skeleton.deck_name(node))
        query = " or ".join(queries)
        if action == "today":
            cards = self.anki("findCards", query=query)
            if cards:
                self.anki("setDueDate", cards=cards, days="0")
            return {"action": action, "cards": len(cards), "query": query}
        if action == "browse":
            self.anki("guiBrowse", query=query)
            return {"action": action, "query": query}
        if action == "review":
            for deck in decks[:1]:
                self.anki("guiDeckReview", name=deck)
            return {"action": action, "deck": decks[:1]}
        raise ValueError(f"unknown focus action {action!r}")


# --------------------------------------------------------------------------

def _handler(app: Workbench):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # quiet
            pass

        def _json(self, status: int, payload: dict) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _body(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n else b""
            try:
                return json.loads(raw or b"{}")
            except json.JSONDecodeError:
                return {}

        def do_GET(self):
            url = urlsplit(self.path)
            q = {k: v[0] for k, v in parse_qs(url.query).items()}
            try:
                if url.path == "/":
                    page = PAGE.read_bytes() if PAGE.exists() else "<h1>Trellis 工作台</h1>".encode()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(page)))
                    self.end_headers()
                    self.wfile.write(page)
                elif url.path == "/api/state":
                    self._json(200, app.state(q.get("domain")))
                elif url.path == "/api/history":
                    self._json(200, app.history(q.get("domain", "")))
                elif url.path == "/api/jobs":
                    self._json(200, {"jobs": [_public(j) for j in
                                              sorted(app.jobs.values(), key=lambda j: j.created, reverse=True)]})
                elif url.path.startswith("/api/jobs/"):
                    job = app.jobs.get(url.path.rsplit("/", 1)[-1])
                    self._json(200, _public(job)) if job else self._json(404, {"error": "no such job"})
                else:
                    self._json(404, {"error": "not found"})
            except AnkiConnectError as exc:
                self._json(503, {"error": str(exc)})

        def do_POST(self):
            url = urlsplit(self.path)
            body = self._body()
            try:
                if url.path == "/api/pull":
                    self._json(200, app.pull(body.get("domain") or None))
                elif url.path == "/api/grow":
                    job = app.start_grow(str(body.get("key", "")), int(body.get("count") or 4),
                                         str(body.get("guidance", "")), str(body.get("model") or "sonnet"))
                    self._json(202, _public(job))
                elif url.path.startswith("/api/jobs/") and url.path.endswith("/accept"):
                    job_id = url.path.split("/")[3]
                    try:
                        self._json(200, _public(app.accept(job_id, bool(body.get("push")))))
                    except ValueError as exc:
                        self._json(422, {"errors": app.jobs[job_id].errors or [str(exc)]})
                elif url.path == "/api/focus":
                    self._json(200, app.focus(list(body.get("keys") or []), str(body.get("action", "today"))))
                else:
                    self._json(404, {"error": "not found"})
            except StillSettling as exc:
                self._json(409, {"error": str(exc)})
            except KeyError as exc:
                self._json(404, {"error": f"no such target or job: {exc}"})
            except AnkiConnectError as exc:
                self._json(503, {"error": str(exc)})
            except ValueError as exc:
                self._json(400, {"error": str(exc)})

    return Handler


def serve(root: Path, port: int = 8777, anki=None, runner=None,
          open_browser: bool = True) -> ThreadingHTTPServer:
    app = Workbench(root, anki=anki, runner=runner)
    server = ThreadingHTTPServer(("127.0.0.1", port), _handler(app))
    server.app = app
    if open_browser:
        webbrowser.open(f"http://127.0.0.1:{server.server_address[1]}/")
    return server
