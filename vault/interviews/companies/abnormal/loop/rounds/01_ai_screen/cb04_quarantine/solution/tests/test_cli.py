from __future__ import annotations

import io
import json

from quarantine.actions import FakeMailbox
from quarantine.cli import main


def test_analyzers_lists_the_registry():
    out = io.StringIO()
    assert main(["analyzers"], out=out) == 0
    assert "link_reputation" in out.getvalue()


def test_ingest_fixtures(tmp_path, reports_dir):
    out = io.StringIO()
    db = tmp_path / "q.db"
    assert main(["ingest", str(reports_dir), "--tenant", "acme", "--db", str(db)], out=out, mailbox=FakeMailbox()) == 0
    assert out.getvalue().startswith("ingested 6 reports:")
    assert "QUARANTINE=" in out.getvalue()


def test_show_prints_the_report(tmp_path, reports_dir, capsys):
    db = tmp_path / "q.db"
    from quarantine.app import create_app

    app = create_app(db_path=db)
    report = app.intake.submit("acme", json.loads((reports_dir / "r001_payroll_phish.json").read_text())).report
    app.conn.close()
    out = io.StringIO()
    assert main(["show", report.id, "--tenant", "acme", "--db", str(db)], out=out) == 0
    assert json.loads(out.getvalue())["disposition"] == "QUARANTINE"


def test_show_unknown_report_exits_1(tmp_path, capsys):
    assert main(["show", "rpt_nope", "--tenant", "acme", "--db", str(tmp_path / "q.db")]) == 1
    assert "no report" in capsys.readouterr().err


def test_unknown_tenant_is_a_clean_error(tmp_path, reports_dir, capsys):
    code = main(["ingest", str(reports_dir), "--tenant", "nobody", "--db", str(tmp_path / "q.db")])
    assert code == 1
    assert "unknown tenant" in capsys.readouterr().err


def test_drain_outbox_delivers_what_ingest_queued(tmp_path, reports_dir):
    db = tmp_path / "q.db"
    mailbox = FakeMailbox()
    main(["ingest", str(reports_dir), "--tenant", "acme", "--db", str(db)], out=io.StringIO(), mailbox=mailbox)
    assert mailbox.receipts == []
    out = io.StringIO()
    assert main(["drain-outbox", "--db", str(db)], out=out, mailbox=mailbox) == 0
    assert out.getvalue().strip() == "delivered 6 receipts, 0 failed"
    assert len(mailbox.receipts) == 6


def test_drain_outbox_exits_1_when_the_provider_is_down(tmp_path, reports_dir):
    db = tmp_path / "q.db"
    mailbox = FakeMailbox(fail_receipts=True)
    main(["ingest", str(reports_dir), "--tenant", "acme", "--db", str(db)], out=io.StringIO(), mailbox=mailbox)
    out = io.StringIO()
    assert main(["drain-outbox", "--db", str(db), "--tenant", "acme"], out=out, mailbox=mailbox) == 1
    assert "6 failed" in out.getvalue()
