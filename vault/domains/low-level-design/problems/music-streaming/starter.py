"""音乐流媒体（Music Streaming）练习骨架：公开 API 与参考解一模一样，方法体留空。

把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/music-streaming -q`。
内部表示随你选：测试只看公开方法与属性（`now_playing`、`state`、`upcoming`、`history`、
`downloaded`、`referenced_track_count` 等），不碰任何下划线开头的东西。
"""

from __future__ import annotations

import itertools
import random
from collections import Counter, deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Callable

Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """默认时钟。"""
    return datetime.now(timezone.utc)


class MusicLibraryError(Exception):
    """本组件所有失败路径的公共基类。"""


class UnknownArtistError(MusicLibraryError, KeyError):
    """艺人 id 不存在。"""


class UnknownAlbumError(MusicLibraryError, KeyError):
    """专辑 id 不存在。"""


class UnknownTrackError(MusicLibraryError, KeyError):
    """曲目 id 不存在（可能从未存在，也可能已经从曲库下架）。"""


class UnknownPlaylistError(MusicLibraryError, KeyError):
    """播放列表 id 不存在。"""


class NotAnEditorError(MusicLibraryError):
    """操作者既不是播放列表的所有者也不是协作者。"""


class EmptyQueueError(MusicLibraryError):
    """播放器还没加载任何队列就被要求播放。"""


class IllegalPlayerTransitionError(MusicLibraryError):
    """播放器的三态之间没有这条边。"""


@dataclass(frozen=True, slots=True)
class Artist:
    id: str
    name: str


@dataclass(frozen=True, slots=True)
class Album:
    id: str
    title: str
    artist_id: str


@dataclass(slots=True)
class Track:
    id: str
    title: str
    album_id: str
    artist_id: str
    duration_seconds: int
    downloaded: bool = False


class Catalog:
    def __init__(self) -> None:
        raise NotImplementedError

    def add_artist(self, artist_id: str, name: str) -> Artist:
        raise NotImplementedError

    def add_album(self, album_id: str, title: str, artist_id: str) -> Album:
        raise NotImplementedError

    def add_track(self, track_id: str, title: str, album_id: str, duration_seconds: int) -> Track:
        raise NotImplementedError

    def artist(self, artist_id: str) -> Artist:
        raise NotImplementedError

    def album(self, album_id: str) -> Album:
        raise NotImplementedError

    def track(self, track_id: str) -> Track:
        raise NotImplementedError

    def tracks_of_album(self, album_id: str) -> tuple[str, ...]:
        raise NotImplementedError

    def tracks_of_artist(self, artist_id: str) -> tuple[Track, ...]:
        raise NotImplementedError

    def remove_track(self, track_id: str) -> Track:
        raise NotImplementedError


class Playlist:
    def __init__(self, playlist_id: str, name: str, owner_id: str) -> None:
        raise NotImplementedError

    @property
    def track_ids(self) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def editors(self) -> frozenset[str]:
        raise NotImplementedError

    def add_editor(self, user_id: str, actor: str) -> None:
        raise NotImplementedError

    def add_track(self, track_id: str, actor: str) -> None:
        raise NotImplementedError

    def remove_track(self, track_id: str, actor: str) -> None:
        raise NotImplementedError


class PlaylistStore:
    def __init__(self) -> None:
        raise NotImplementedError

    def create_playlist(self, playlist_id: str, name: str, owner_id: str) -> Playlist:
        raise NotImplementedError

    def add_editor(self, playlist_id: str, user_id: str, actor: str) -> None:
        raise NotImplementedError

    def add_track(self, playlist_id: str, track_id: str, actor: str) -> None:
        raise NotImplementedError

    def remove_track(self, playlist_id: str, track_id: str, actor: str) -> None:
        raise NotImplementedError

    def track_ids(self, playlist_id: str) -> tuple[str, ...]:
        raise NotImplementedError

    def scrub_track(self, track_id: str) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def referenced_track_count(self) -> int:
        raise NotImplementedError


class PlayerState(Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class RepeatMode(Enum):
    OFF = "off"
    ONE = "one"
    ALL = "all"


@dataclass(frozen=True, slots=True)
class PlayEvent:
    track_id: str
    at: datetime


class PlayQueue:
    def __init__(self, source_track_ids: Sequence[str], rng: random.Random,
                history_capacity: int = 200) -> None:
        raise NotImplementedError

    @property
    def now_playing(self) -> str | None:
        raise NotImplementedError

    @property
    def upcoming(self) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def history(self) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def shuffle(self) -> bool:
        raise NotImplementedError

    @property
    def repeat(self) -> RepeatMode:
        raise NotImplementedError

    def set_repeat(self, mode: RepeatMode) -> None:
        raise NotImplementedError

    def set_shuffle(self, on: bool) -> None:
        raise NotImplementedError

    def add_track(self, track_id: str) -> None:
        raise NotImplementedError

    def advance(self) -> str | None:
        raise NotImplementedError

    def previous(self) -> str | None:
        raise NotImplementedError


class Player:
    def __init__(self, history: "PlayHistory", clock: Clock) -> None:
        raise NotImplementedError

    @property
    def state(self) -> PlayerState:
        raise NotImplementedError

    @property
    def queue(self) -> PlayQueue:
        raise NotImplementedError

    def load(self, queue: PlayQueue) -> None:
        raise NotImplementedError

    def play(self) -> str | None:
        raise NotImplementedError

    def pause(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def skip_next(self) -> str | None:
        raise NotImplementedError

    def skip_previous(self) -> str | None:
        raise NotImplementedError


class PlayHistory:
    def __init__(self, capacity: int = 500) -> None:
        raise NotImplementedError

    def record(self, track_id: str, at: datetime) -> None:
        raise NotImplementedError

    def recent(self, limit: int = 20) -> tuple[str, ...]:
        raise NotImplementedError

    def most_played(self, limit: int = 10) -> tuple[tuple[str, int], ...]:
        raise NotImplementedError

    @property
    def event_count(self) -> int:
        raise NotImplementedError


class MusicLibrary:
    def __init__(self, clock: Clock = utc_now, rng: random.Random | None = None,
                history_capacity: int = 500, queue_history_capacity: int = 200) -> None:
        raise NotImplementedError

    def add_artist(self, artist_id: str, name: str) -> Artist:
        raise NotImplementedError

    def add_album(self, album_id: str, title: str, artist_id: str) -> Album:
        raise NotImplementedError

    def add_track(self, track_id: str, title: str, album_id: str, duration_seconds: int) -> Track:
        raise NotImplementedError

    def track(self, track_id: str) -> Track:
        raise NotImplementedError

    def remove_track(self, track_id: str) -> tuple[str, ...]:
        raise NotImplementedError

    def create_playlist(self, playlist_id: str, name: str, owner_id: str) -> Playlist:
        raise NotImplementedError

    def add_editor(self, playlist_id: str, user_id: str, actor: str) -> None:
        raise NotImplementedError

    def add_to_playlist(self, playlist_id: str, track_id: str, actor: str) -> None:
        raise NotImplementedError

    def remove_from_playlist(self, playlist_id: str, track_id: str, actor: str) -> None:
        raise NotImplementedError

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def referenced_track_count(self) -> int:
        raise NotImplementedError

    def play_album(self, album_id: str) -> None:
        raise NotImplementedError

    def play_playlist(self, playlist_id: str) -> None:
        raise NotImplementedError

    def play_radio(self, seed_track_id: str, limit: int = 20) -> None:
        raise NotImplementedError

    def set_shuffle(self, on: bool) -> None:
        raise NotImplementedError

    def set_repeat(self, mode: RepeatMode) -> None:
        raise NotImplementedError

    def add_to_queue(self, track_id: str) -> None:
        raise NotImplementedError

    def play(self) -> str | None:
        raise NotImplementedError

    def pause(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def skip_next(self) -> str | None:
        raise NotImplementedError

    def skip_previous(self) -> str | None:
        raise NotImplementedError

    @property
    def state(self) -> PlayerState:
        raise NotImplementedError

    @property
    def now_playing(self) -> str | None:
        raise NotImplementedError

    @property
    def queue_upcoming(self) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def history_event_count(self) -> int:
        raise NotImplementedError

    def recently_played(self, limit: int = 20) -> tuple[str, ...]:
        raise NotImplementedError

    def most_played(self, limit: int = 10) -> tuple[tuple[str, int], ...]:
        raise NotImplementedError

    def download(self, track_id: str) -> None:
        raise NotImplementedError

    def remove_download(self, track_id: str) -> None:
        raise NotImplementedError
