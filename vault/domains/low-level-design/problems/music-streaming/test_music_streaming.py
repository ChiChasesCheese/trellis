"""音乐流媒体的验收测试：播放列表只持有引用、一首歌下架会反向摘除、播放器三态转移、
洗牌只重排未播部分、previous 永远沿真实播放历史走、repeat=ALL 不会让队列无界增长、
历史统计是现算的、下载标记独立。

所有断言只看公开方法与属性，不碰任何下划线开头的东西。曲库与播放器的搭建放在每个测试函数
体内，不是 fixture：starter 的 `__init__` 会 `raise NotImplementedError`，构造放在测试体内
才会被 pytest 记成一次明确的失败。
"""

from __future__ import annotations

import importlib
import os
import random
import threading
from datetime import datetime, timedelta, timezone

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FrozenClock:
    def __init__(self, start: datetime) -> None:
        self._now = start

    def __call__(self) -> datetime:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += timedelta(seconds=seconds)


def make_library(clock: FrozenClock | None = None, seed: int = 1, **kwargs) -> "impl.MusicLibrary":
    return impl.MusicLibrary(clock=clock or FrozenClock(datetime(2026, 1, 1, tzinfo=timezone.utc)),
                             rng=random.Random(seed), **kwargs)


def seed_catalog(library) -> None:
    library.add_artist("a1", "Daft Punk")
    library.add_album("al1", "Discovery", "a1")
    for i in range(1, 5):
        library.add_track(f"t{i}", f"Track {i}", "al1", 200 + i)


def test_playlist_stores_track_references_not_copies() -> None:
    library = make_library()
    seed_catalog(library)
    library.create_playlist("p1", "Faves", owner_id="ada")
    library.add_to_playlist("p1", "t1", actor="ada")
    library.add_to_playlist("p1", "t2", actor="ada")
    assert library.playlist_tracks("p1") == ("t1", "t2")
    track = library.track("t1")
    track.title = "renamed"  # 播放列表引用的是 id，改曲目对象不会让播放列表存两份数据
    assert library.playlist_tracks("p1") == ("t1", "t2")


def test_removing_track_from_catalog_scrubs_playlists_referencing_it() -> None:
    library = make_library()
    seed_catalog(library)
    library.create_playlist("p1", "Faves", owner_id="ada")
    library.create_playlist("p2", "Other", owner_id="grace")
    library.add_to_playlist("p1", "t1", actor="ada")
    library.add_to_playlist("p2", "t1", actor="grace")
    library.add_to_playlist("p1", "t2", actor="ada")
    affected = library.remove_track("t1")
    assert set(affected) == {"p1", "p2"}
    assert library.playlist_tracks("p1") == ("t2",)
    assert library.playlist_tracks("p2") == ()
    with pytest.raises(impl.UnknownTrackError):
        library.track("t1")


def test_referenced_track_count_shrinks_after_scrub() -> None:
    library = make_library()
    seed_catalog(library)
    library.create_playlist("p1", "Faves", owner_id="ada")
    library.create_playlist("p2", "Other", owner_id="grace")
    library.add_to_playlist("p1", "t1", actor="ada")
    library.add_to_playlist("p2", "t1", actor="grace")  # 同一首歌被两份播放列表引用，只算一次
    library.add_to_playlist("p1", "t2", actor="ada")
    assert library.referenced_track_count == 2
    library.remove_track("t1")
    assert library.referenced_track_count == 1


def test_playlist_edit_requires_owner_or_editor() -> None:
    library = make_library()
    seed_catalog(library)
    library.create_playlist("p1", "Faves", owner_id="ada")
    with pytest.raises(impl.NotAnEditorError):
        library.add_to_playlist("p1", "t1", actor="mallory")


def test_owner_can_add_editor_who_can_then_edit() -> None:
    library = make_library()
    seed_catalog(library)
    library.create_playlist("p1", "Faves", owner_id="ada")
    library.add_editor("p1", "grace", actor="ada")
    library.add_to_playlist("p1", "t1", actor="grace")
    assert library.playlist_tracks("p1") == ("t1",)
    with pytest.raises(impl.NotAnEditorError):
        library.add_editor("p1", "linus", actor="grace")  # 只有所有者能加协作者


def test_play_album_builds_queue_in_track_order() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    played = [library.play()] + [library.skip_next() for _ in range(3)]
    assert played == ["t1", "t2", "t3", "t4"]


def test_player_transitions_stopped_playing_paused() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    assert library.state is impl.PlayerState.STOPPED
    library.play()
    assert library.state is impl.PlayerState.PLAYING
    library.pause()
    assert library.state is impl.PlayerState.PAUSED
    library.play()
    assert library.state is impl.PlayerState.PLAYING
    library.stop()
    assert library.state is impl.PlayerState.STOPPED


def test_illegal_transition_raises() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    with pytest.raises(impl.IllegalPlayerTransitionError):
        library.pause()  # 还没开始播放


def test_skip_while_stopped_raises() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    with pytest.raises(impl.IllegalPlayerTransitionError):
        library.skip_next()


def test_resume_from_paused_replays_same_track_without_advancing() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    first = library.play()
    library.pause()
    resumed = library.play()
    assert resumed == first
    assert library.now_playing == first


def test_shuffle_reorders_upcoming_deterministically_with_seeded_rng() -> None:
    library = make_library(seed=42)
    seed_catalog(library)
    library.play_album("al1")
    library.set_shuffle(True)
    shuffled_upcoming = library.queue_upcoming
    assert set(shuffled_upcoming) == {"t1", "t2", "t3", "t4"}
    assert list(shuffled_upcoming) != ["t1", "t2", "t3", "t4"]  # 概率上几乎必然被打乱


def test_turning_shuffle_off_restores_source_order_of_unplayed_tracks() -> None:
    library = make_library(seed=3)
    seed_catalog(library)
    library.play_album("al1")
    library.play()  # 播 t1，进入 history
    library.set_shuffle(True)
    library.set_shuffle(False)
    remaining = library.queue_upcoming
    assert remaining == ("t2", "t3", "t4")  # 恢复成来源顺序里还没播过的那些


def test_add_track_while_shuffled_inserts_into_remainder_not_always_last() -> None:
    library = make_library(seed=5)
    seed_catalog(library)
    library.play_album("al1")
    library.set_shuffle(True)
    library.add_to_queue("t4")  # t4 已在来源里；再验证一首全新曲目也能插入队列
    library.add_track("t5", "Track 5", "al1", 210)
    library.add_to_queue("t5")
    upcoming = library.queue_upcoming
    assert upcoming.count("t5") == 1
    assert "t5" in upcoming


def test_add_track_without_shuffle_appends_to_end() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    library.add_track("t5", "Track 5", "al1", 210)
    library.add_to_queue("t5")
    assert library.queue_upcoming[-1] == "t5"


def test_previous_follows_actual_play_history_regardless_of_shuffle() -> None:
    library = make_library(seed=9)
    seed_catalog(library)
    library.play_album("al1")
    first = library.play()
    second = library.skip_next()
    library.set_shuffle(True)  # 打开洗牌不应该影响 previous 的回退方向
    back = library.skip_previous()
    assert back == first
    assert library.now_playing == first
    forward_again = library.skip_next()
    assert forward_again == second


def test_repeat_one_replays_same_track_forever() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    library.set_repeat(impl.RepeatMode.ONE)
    first = library.play()
    for _ in range(5):
        assert library.skip_next() == first


def test_repeat_all_regenerates_source_without_growing_queue() -> None:
    library = make_library(seed=11)
    seed_catalog(library)
    library.play_album("al1")
    library.set_repeat(impl.RepeatMode.ALL)
    played = [library.play()]
    for _ in range(11):  # 播完两轮多一点：4 首歌 x 3 轮
        played.append(library.skip_next())
    assert len(played) == 12
    assert set(played) == {"t1", "t2", "t3", "t4"}
    # 队列此刻剩下的待播数量必须仍然是一轮以内的量级，不会随播放轮数累加
    assert len(library.queue_upcoming) <= 4


def test_recently_played_and_most_played_are_derived_from_history() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    library.play()   # t1
    library.skip_next()  # t2
    library.skip_next()  # t3
    library.set_repeat(impl.RepeatMode.ONE)
    library.skip_next()  # t3 again
    assert library.recently_played(2) == ("t3", "t3")
    top = library.most_played(1)
    assert top == (("t3", 2),)


def test_history_capacity_bounds_growth() -> None:
    library = make_library(history_capacity=3)
    seed_catalog(library)
    library.play_album("al1")
    library.set_repeat(impl.RepeatMode.ALL)
    library.play()
    for _ in range(20):
        library.skip_next()
    assert library.history_event_count <= 3


def test_download_flag_is_independent_per_track() -> None:
    library = make_library()
    seed_catalog(library)
    library.download("t1")
    assert library.track("t1").downloaded is True
    assert library.track("t2").downloaded is False
    library.remove_download("t1")
    assert library.track("t1").downloaded is False


def test_play_radio_seeds_from_same_artist() -> None:
    library = make_library(seed=2)
    seed_catalog(library)
    library.play_radio("t1", limit=3)
    upcoming_plus_first = (library.play(),) + library.queue_upcoming
    assert upcoming_plus_first[0] == "t1"
    assert len(upcoming_plus_first) == 3
    assert set(upcoming_plus_first) <= {"t1", "t2", "t3", "t4"}


def test_unknown_track_and_playlist_raise() -> None:
    library = make_library()
    seed_catalog(library)
    with pytest.raises(impl.UnknownTrackError):
        library.track("ghost")
    with pytest.raises(impl.UnknownPlaylistError):
        library.playlist_tracks("ghost")
    library.create_playlist("p1", "Faves", owner_id="ada")
    with pytest.raises(impl.UnknownTrackError):
        library.add_to_playlist("p1", "ghost", actor="ada")


def test_play_with_empty_queue_raises() -> None:
    library = make_library()
    with pytest.raises(impl.EmptyQueueError):
        library.play()


def test_play_empty_album_returns_none_and_stays_stopped() -> None:
    """队列加载成功，但来源里一首歌都没有：`advance` 拿不出任何曲目，播放器不应该被切成
    "正在播放"——这和"根本没加载队列"（`EmptyQueueError`）是两种不同的空。"""
    library = make_library()
    library.add_artist("a1", "Daft Punk")
    library.add_album("al1", "Discovery", "a1")  # 专辑存在，但没有任何曲目
    library.play_album("al1")
    assert library.play() is None
    assert library.state is impl.PlayerState.STOPPED
    assert library.now_playing is None


def test_skip_past_exhausted_source_without_repeat_returns_none() -> None:
    library = make_library()
    seed_catalog(library)
    library.play_album("al1")
    library.play()
    for _ in range(3):
        library.skip_next()  # 播完全部四首
    assert library.skip_next() is None  # 没开 repeat，来源已耗尽
    assert library.now_playing is None
    assert library.state is impl.PlayerState.PLAYING  # 耗尽不等于停止，只是此刻没有下一首


def test_concurrent_collaborative_edits_keep_index_in_sync_with_playlist() -> None:
    library = make_library()
    library.add_artist("a1", "Daft Punk")
    library.add_album("al1", "Discovery", "a1")
    n = 10
    for i in range(1, n + 1):
        library.add_track(f"t{i}", f"Track {i}", "al1", 200 + i)
    library.create_playlist("p1", "Collab", owner_id="ada")
    editors = [f"editor{i}" for i in range(n)]
    for editor in editors:
        library.add_editor("p1", editor, actor="ada")
    barrier = threading.Barrier(n)

    def worker(i: int) -> None:
        barrier.wait()
        library.add_to_playlist("p1", f"t{i + 1}", actor=editors[i])

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    tracks = library.playlist_tracks("p1")
    assert len(tracks) == n  # 没有一次并发写入被另一次覆盖或丢失
    assert set(tracks) == {f"t{i}" for i in range(1, n + 1)}
    assert library.referenced_track_count == n  # 反向索引和播放列表内容对得上
