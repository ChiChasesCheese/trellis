"""No test may reach the Anki on this machine.

Desktop Anki is usually running while this suite is, and AnkiConnect
answers anyone on localhost — so a test that forgets to replace the
client does not fail, it imports its fixture deck into a real collection
and syncs it to a phone. That happened once. Now the default client
refuses, and a test that needs Anki has to hand in a fake.
"""

import pytest

import trellis.anki


@pytest.fixture(autouse=True)
def no_real_anki(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("a test reached for the real AnkiConnect; pass a fake client")
    monkeypatch.setattr(trellis.anki.urllib.request, "urlopen", refuse)
