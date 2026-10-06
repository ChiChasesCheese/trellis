import io

from fanout.models import Alert, Channel
from fanout.senders import EmailSender, SlackSender, WebhookSender

ALERT = Alert("acme", "a1", "r", 4, "T", "ann@example.com", "2026-10-01T12:00:00Z")


def test_email_sender_uses_transport():
    got = []
    EmailSender(transport=lambda to, subj, body: got.append((to, subj))).send(Channel("acme", "email", "a@example.com"), ALERT)
    assert got == [("a@example.com", "Alert: T")]


def test_slack_sender_uses_transport():
    got = []
    SlackSender(transport=lambda ch, text: got.append(ch)).send(Channel("acme", "slack", "#sec"), ALERT)
    assert got == ["#sec"]


def test_webhook_sender_posts_json(monkeypatch):
    import urllib.request

    seen = {}

    class Resp(io.BytesIO):
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, *a, **kw):
        seen["url"] = req.full_url
        return Resp()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    WebhookSender().send(Channel("acme", "webhook", "https://hooks.example.com/x", secret="k"), ALERT)
    assert seen["url"] == "https://hooks.example.com/x"
