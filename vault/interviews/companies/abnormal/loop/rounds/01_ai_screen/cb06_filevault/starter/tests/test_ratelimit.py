import pytest

from filevault.ratelimit import TokenBucket


class Ticker:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def test_starts_full_and_drains():
    clock = Ticker()
    bucket = TokenBucket(rate=1, capacity=2, clock=clock)
    assert bucket.try_take() and bucket.try_take()
    assert not bucket.try_take()


def test_refills_over_time_up_to_capacity():
    clock = Ticker()
    bucket = TokenBucket(rate=2, capacity=3, clock=clock)
    for _ in range(3):
        assert bucket.try_take()
    clock.t += 1.0  # +2 tokens
    assert bucket.try_take() and bucket.try_take()
    assert not bucket.try_take()
    clock.t += 100
    assert [bucket.try_take() for _ in range(4)] == [True, True, True, False]


def test_seconds_until_rounds_up():
    clock = Ticker()
    bucket = TokenBucket(rate=0.5, capacity=1, clock=clock)
    assert bucket.try_take()
    assert bucket.seconds_until() == 2
    clock.t += 1.5
    assert bucket.seconds_until() == 1


def test_rejects_nonsense():
    with pytest.raises(ValueError):
        TokenBucket(rate=0, capacity=1)
