from fanout.config_store import ConfigStore
from fanout.models import Channel


def test_channels_for_returns_only_enabled_channels_of_tenant():
    s = ConfigStore()
    s.add_channel(Channel("acme", "email", "a@example.com"))
    s.add_channel(Channel("acme", "slack", "#sec"), enabled=False)
    s.add_channel(Channel("globex", "email", "g@example.com"))
    assert [c.target for c in s.channels_for("acme")] == ["a@example.com"]
