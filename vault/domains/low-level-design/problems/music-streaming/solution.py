"""音乐流媒体（Spotify）：曲库与播放列表、播放器状态机与播放队列、播放历史与派生统计。

设计要点：`Catalog` 只管艺人/专辑/曲目这些实体存不存在，不知道播放列表；`PlaylistStore` 只
持有播放列表和一份"哪些播放列表引用过某首曲目"的反向索引，不知道曲库内部怎么存；一首歌从
曲库下架时，`MusicLibrary` 门面先删曲库、再用反向索引把它从所有引用过它的播放列表里摘掉——
播放列表只持有对曲目的引用，不拥有曲目的生命周期。播放队列（`PlayQueue`）把"接下来播什么"
和"洗牌/循环"这两个修饰符分开：洗牌只重排还没播的部分，`history`记的是真实播放过的顺序，
`previous` 永远沿着 `history` 走，不受洗牌影响；repeat=ALL 用完时从来源重新生成一轮，不是
无限拼接，队列因此不会随重复的轮数无限变长。历史统计（最常播放、最近播放）都是对一份有界
的播放事件日志现算出来的，不是另存的计数字段。
"""

from __future__ import annotations

import itertools
import random
import threading
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


# --------------------------------------------------------------------------
# 失败路径


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


# --------------------------------------------------------------------------
# 曲库：艺人、专辑、曲目。只管这些实体存不存在、彼此怎么关联。


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
    """一首曲目。`downloaded` 是一个没有转移规则的简单标记（下没下载两个值都合法），因此是
    一个直接可写的字段，而不是一对受检的方法。"""

    id: str
    title: str
    album_id: str
    artist_id: str
    duration_seconds: int
    downloaded: bool = False


class Catalog:
    """曲库：艺人、专辑、曲目的存储与关联索引。不知道播放列表和播放器的存在。"""

    def __init__(self) -> None:
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._tracks: dict[str, Track] = {}
        self._album_tracks: dict[str, list[str]] = {}
        self._artist_tracks: dict[str, list[str]] = {}

    def add_artist(self, artist_id: str, name: str) -> Artist:
        artist = Artist(artist_id, name)
        self._artists[artist_id] = artist
        return artist

    def add_album(self, album_id: str, title: str, artist_id: str) -> Album:
        self.artist(artist_id)
        album = Album(album_id, title, artist_id)
        self._albums[album_id] = album
        self._album_tracks.setdefault(album_id, [])
        return album

    def add_track(self, track_id: str, title: str, album_id: str, duration_seconds: int) -> Track:
        album = self.album(album_id)
        track = Track(track_id, title, album_id, album.artist_id, duration_seconds)
        self._tracks[track_id] = track
        self._album_tracks.setdefault(album_id, []).append(track_id)
        self._artist_tracks.setdefault(album.artist_id, []).append(track_id)
        return track

    def artist(self, artist_id: str) -> Artist:
        try:
            return self._artists[artist_id]
        except KeyError:
            raise UnknownArtistError(artist_id) from None

    def album(self, album_id: str) -> Album:
        try:
            return self._albums[album_id]
        except KeyError:
            raise UnknownAlbumError(album_id) from None

    def track(self, track_id: str) -> Track:
        try:
            return self._tracks[track_id]
        except KeyError:
            raise UnknownTrackError(track_id) from None

    def tracks_of_album(self, album_id: str) -> tuple[str, ...]:
        return tuple(self._album_tracks.get(album_id, ()))

    def tracks_of_artist(self, artist_id: str) -> tuple[Track, ...]:
        return tuple(self._tracks[tid] for tid in self._artist_tracks.get(artist_id, ()))

    def remove_track(self, track_id: str) -> Track:
        """一首歌下架：从主表和两条关联索引里一起摘除。播放列表怎么应对由调用方（门面）编排——
        曲库不知道播放列表的存在，这不是它的职责。"""
        track = self.track(track_id)
        del self._tracks[track_id]
        self._album_tracks.get(track.album_id, []).remove(track_id)
        self._artist_tracks.get(track.artist_id, []).remove(track_id)
        return track


# --------------------------------------------------------------------------
# 播放列表：只持有对曲目的引用（track id），不拥有曲目的生命周期。


class Playlist:
    """一份播放列表：所有者、协作者、有序的曲目引用。曲目从曲库消失时，`_discard` 是系统
    动作，不检查协作权限——那不是一次"人的编辑"。"""

    def __init__(self, playlist_id: str, name: str, owner_id: str) -> None:
        self.id = playlist_id
        self.name = name
        self.owner_id = owner_id
        self._editors: set[str] = set()
        self._track_ids: list[str] = []

    @property
    def track_ids(self) -> tuple[str, ...]:
        return tuple(self._track_ids)

    @property
    def editors(self) -> frozenset[str]:
        return frozenset(self._editors)

    def _require_editor(self, actor: str) -> None:
        if actor != self.owner_id and actor not in self._editors:
            raise NotAnEditorError(f"{actor} is not the owner or an editor of playlist {self.id!r}")

    def add_editor(self, user_id: str, actor: str) -> None:
        if actor != self.owner_id:
            raise NotAnEditorError("only the owner can add editors")
        self._editors.add(user_id)

    def add_track(self, track_id: str, actor: str) -> None:
        self._require_editor(actor)
        if track_id not in self._track_ids:
            self._track_ids.append(track_id)

    def remove_track(self, track_id: str, actor: str) -> None:
        self._require_editor(actor)
        if track_id in self._track_ids:
            self._track_ids.remove(track_id)

    def _discard(self, track_id: str) -> None:
        if track_id in self._track_ids:
            self._track_ids.remove(track_id)


class PlaylistStore:
    """播放列表的存储，加一份"曲目 id -> 引用过它的播放列表 id 集合"的反向索引。一首歌下架
    时，靠这份索引直接找到受影响的播放列表，而不必扫描系统里的每一份播放列表。

    协作播放列表意味着好几个编辑者会并发改同一份播放列表，因此一份播放列表自己的曲目列表
    与这份反向索引必须在**同一次加锁**里一起更新——和 `CardStore` 是同一个纪律：写路径把
    "改内容"和"改索引"钉成一次原子操作，读路径也经过这把锁，不直接把播放列表对象交出去。
    """

    def __init__(self) -> None:
        self._playlists: dict[str, Playlist] = {}
        self._by_track: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    def _require(self, playlist_id: str) -> Playlist:
        try:
            return self._playlists[playlist_id]
        except KeyError:
            raise UnknownPlaylistError(playlist_id) from None

    def create_playlist(self, playlist_id: str, name: str, owner_id: str) -> Playlist:
        with self._lock:
            playlist = Playlist(playlist_id, name, owner_id)
            self._playlists[playlist_id] = playlist
            return playlist

    def add_editor(self, playlist_id: str, user_id: str, actor: str) -> None:
        with self._lock:
            self._require(playlist_id).add_editor(user_id, actor)

    def add_track(self, playlist_id: str, track_id: str, actor: str) -> None:
        with self._lock:
            self._require(playlist_id).add_track(track_id, actor)
            self._by_track.setdefault(track_id, set()).add(playlist_id)

    def remove_track(self, playlist_id: str, track_id: str, actor: str) -> None:
        with self._lock:
            self._require(playlist_id).remove_track(track_id, actor)
            self._by_track.get(track_id, set()).discard(playlist_id)

    def track_ids(self, playlist_id: str) -> tuple[str, ...]:
        with self._lock:
            return self._require(playlist_id).track_ids

    def scrub_track(self, track_id: str) -> tuple[str, ...]:
        """曲库删除了这首歌：把它从所有引用过它的播放列表里摘掉，返回受影响的播放列表 id。"""
        with self._lock:
            affected = tuple(self._by_track.pop(track_id, ()))
            for playlist_id in affected:
                self._playlists[playlist_id]._discard(track_id)
            return affected

    @property
    def referenced_track_count(self) -> int:
        """还被至少一份播放列表引用着的曲目数——一首歌下架并被摘除引用后，这个数会变小。"""
        with self._lock:
            return len(self._by_track)


# --------------------------------------------------------------------------
# 播放器：停止/播放/暂停三态，围绕一个 PlayQueue 转移。


class PlayerState(Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class RepeatMode(Enum):
    OFF = "off"
    ONE = "one"
    ALL = "all"


_PLAYER_TRANSITIONS: Mapping[PlayerState, frozenset[PlayerState]] = {
    PlayerState.STOPPED: frozenset({PlayerState.PLAYING}),
    PlayerState.PLAYING: frozenset({PlayerState.PAUSED, PlayerState.STOPPED}),
    PlayerState.PAUSED: frozenset({PlayerState.PLAYING, PlayerState.STOPPED}),
}


@dataclass(frozen=True, slots=True)
class PlayEvent:
    """一次真实发生过的播放：播的是哪首、什么时候。"""

    track_id: str
    at: datetime


class PlayQueue:
    """播放队列：由一个来源（专辑/播放列表/电台此刻的一份不可变快照）加 shuffle、repeat 两个
    修饰符生成。`_upcoming` 是接下来会播的顺序，`_history` 是已经播放过的顺序（有界，不
    无限增长）。repeat=ALL 用完 `_upcoming` 后不是把整份来源再拼接一次，而是从来源重新生成
    一轮（洗牌开着就重新洗一次牌），队列因此不会随着重复播放的轮数无限变长。
    """

    def __init__(self, source_track_ids: Sequence[str], rng: random.Random,
                history_capacity: int = 200) -> None:
        self._source = tuple(source_track_ids)
        self._rng = rng
        self._shuffle = False
        self._repeat = RepeatMode.OFF
        self._upcoming: deque[str] = deque(self._source)
        self._history: deque[str] = deque(maxlen=history_capacity)
        self._now_playing: str | None = None

    @property
    def now_playing(self) -> str | None:
        return self._now_playing

    @property
    def upcoming(self) -> tuple[str, ...]:
        return tuple(self._upcoming)

    @property
    def history(self) -> tuple[str, ...]:
        return tuple(self._history)

    @property
    def shuffle(self) -> bool:
        return self._shuffle

    @property
    def repeat(self) -> RepeatMode:
        return self._repeat

    def set_repeat(self, mode: RepeatMode) -> None:
        self._repeat = mode

    def set_shuffle(self, on: bool) -> None:
        """打开洗牌：把接下来要播的部分原地打乱一次。关掉洗牌：剩下没播的部分恢复成来源顺序
        里"还没播过"的那些曲目——不是恢复成打乱前的顺序，那份顺序已经不存在了。
        """
        self._shuffle = on
        if on:
            upcoming = list(self._upcoming)
            self._rng.shuffle(upcoming)
            self._upcoming = deque(upcoming)
        else:
            played = set(self._history)
            if self._now_playing is not None:
                played.add(self._now_playing)
            self._upcoming = deque(t for t in self._source if t not in played)

    def add_track(self, track_id: str) -> None:
        """加一首歌到接下来要播的部分。洗牌开着时插进剩余队列里的一个随机位置——如果永远
        加在末尾，"刚加的歌总是排在最后"这个可预测的顺序会破坏"这是洗过的"这句承诺；洗牌
        关着时按听众的直觉排到末尾。
        """
        if self._shuffle and self._upcoming:
            self._upcoming.insert(self._rng.randint(0, len(self._upcoming)), track_id)
        else:
            self._upcoming.append(track_id)

    def advance(self) -> str | None:
        """前进到下一首。repeat=ONE 时原地重复当前曲目；repeat=ALL 且 `_upcoming` 耗尽时，
        从来源重新生成一轮（洗牌开着就重新洗），不是无限拼接——这正是队列不会无界增长的原因。
        """
        if self._repeat is RepeatMode.ONE and self._now_playing is not None:
            return self._now_playing
        if self._now_playing is not None:
            self._history.append(self._now_playing)
        if not self._upcoming and self._repeat is RepeatMode.ALL and self._source:
            refreshed = list(self._source)
            if self._shuffle:
                self._rng.shuffle(refreshed)
            self._upcoming = deque(refreshed)
        if not self._upcoming:
            self._now_playing = None
            return None
        self._now_playing = self._upcoming.popleft()
        return self._now_playing

    def previous(self) -> str | None:
        """回退：永远按"实际播放过的顺序"（`history`）走，不管此刻洗牌开没开——洗牌只重排
        "还没播的"那部分，`history` 记的是真实发生过的顺序，因此 `previous` 不需要关心此刻
        `shuffle`/`repeat` 是什么。
        """
        if not self._history:
            return None
        if self._now_playing is not None:
            self._upcoming.appendleft(self._now_playing)
        self._now_playing = self._history.pop()
        return self._now_playing


class Player:
    """播放器：停止/播放/暂停三态，只管这三态之间哪条边合法。"下一首具体是谁"完全委托给
    `PlayQueue`——播放器不重复维护任何顺序信息。
    """

    def __init__(self, history: "PlayHistory", clock: Clock) -> None:
        self._state = PlayerState.STOPPED
        self._queue: PlayQueue | None = None
        self._history = history
        self._clock = clock

    @property
    def state(self) -> PlayerState:
        return self._state

    @property
    def queue(self) -> PlayQueue:
        if self._queue is None:
            raise EmptyQueueError("no queue has been loaded")
        return self._queue

    def load(self, queue: PlayQueue) -> None:
        self._queue = queue
        self._state = PlayerState.STOPPED

    def _move(self, target: PlayerState) -> None:
        if target not in _PLAYER_TRANSITIONS[self._state]:
            raise IllegalPlayerTransitionError(f"{self._state.value} -> {target.value} is not a transition")
        self._state = target

    def play(self) -> str | None:
        """从 `STOPPED` 播放会推进到队列的下一首；从 `PAUSED` 恢复播放的是同一首，不重新
        `advance`。队列此刻没有下一首可播（来源为空，或非循环模式下已经放完）时，`advance`
        返回 `None`，播放器**留在原状态不转移**——播放一个此刻拿不出任何曲目的队列不是一次
        成功的"开始播放"，不该把播放器切成"正在播放"却什么都没有在放。
        """
        if self._state is PlayerState.PAUSED:
            self._move(PlayerState.PLAYING)
            return self.queue.now_playing
        track_id = self.queue.advance()
        if track_id is None:
            return None
        self._move(PlayerState.PLAYING)
        self._history.record(track_id, self._clock())
        return track_id

    def pause(self) -> None:
        self._move(PlayerState.PAUSED)

    def stop(self) -> None:
        self._move(PlayerState.STOPPED)

    def skip_next(self) -> str | None:
        if self._state is PlayerState.STOPPED:
            raise IllegalPlayerTransitionError("cannot skip while stopped")
        track_id = self.queue.advance()
        if track_id is not None:
            self._history.record(track_id, self._clock())
        return track_id

    def skip_previous(self) -> str | None:
        if self._state is PlayerState.STOPPED:
            raise IllegalPlayerTransitionError("cannot skip while stopped")
        track_id = self.queue.previous()
        if track_id is not None:
            self._history.record(track_id, self._clock())
        return track_id


class PlayHistory:
    """播放历史：一份有界的、按时间顺序的播放事件日志。"最常播放""最近播放"都是对这份日志
    现算出来的，不是另存的计数字段——历史被淘汰（`maxlen`）之后，统计会诚实地跟着变。
    """

    def __init__(self, capacity: int = 500) -> None:
        self._events: deque[PlayEvent] = deque(maxlen=capacity)

    def record(self, track_id: str, at: datetime) -> None:
        self._events.append(PlayEvent(track_id, at))

    def recent(self, limit: int = 20) -> tuple[str, ...]:
        return tuple(e.track_id for e in list(self._events)[-limit:][::-1])

    def most_played(self, limit: int = 10) -> tuple[tuple[str, int], ...]:
        counts = Counter(e.track_id for e in self._events)
        return tuple(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:limit])

    @property
    def event_count(self) -> int:
        return len(self._events)


# --------------------------------------------------------------------------
# MusicLibrary：门面。曲库、播放列表、播放器、历史统计，以及"电台"这个简单的来源。


class MusicLibrary:
    """整个客户端模型的入口。只有它同时知道 `Catalog` 和 `PlaylistStore`，因此"歌从曲库
    消失"的编排（先删曲库、再摘引用）钉在这里，两者互不知道对方存在。
    """

    def __init__(self, clock: Clock = utc_now, rng: random.Random | None = None,
                history_capacity: int = 500, queue_history_capacity: int = 200) -> None:
        self._catalog = Catalog()
        self._playlists = PlaylistStore()
        self._history = PlayHistory(history_capacity)
        self._rng = rng or random.Random()
        self._player = Player(self._history, clock)
        self._queue_history_capacity = queue_history_capacity

    # ---- 第 1 关：曲库与播放列表 ----

    def add_artist(self, artist_id: str, name: str) -> Artist:
        return self._catalog.add_artist(artist_id, name)

    def add_album(self, album_id: str, title: str, artist_id: str) -> Album:
        return self._catalog.add_album(album_id, title, artist_id)

    def add_track(self, track_id: str, title: str, album_id: str, duration_seconds: int) -> Track:
        return self._catalog.add_track(track_id, title, album_id, duration_seconds)

    def track(self, track_id: str) -> Track:
        return self._catalog.track(track_id)

    def remove_track(self, track_id: str) -> tuple[str, ...]:
        """一首歌从曲库下架：立刻从曲库摘除，并从所有引用过它的播放列表里摘掉——播放列表不
        拥有曲目的生命周期，只持有引用，引用失效时播放列表缩短，不留一个悬空 id。
        """
        self._catalog.remove_track(track_id)
        return self._playlists.scrub_track(track_id)

    def create_playlist(self, playlist_id: str, name: str, owner_id: str) -> Playlist:
        return self._playlists.create_playlist(playlist_id, name, owner_id)

    def add_editor(self, playlist_id: str, user_id: str, actor: str) -> None:
        self._playlists.add_editor(playlist_id, user_id, actor)

    def add_to_playlist(self, playlist_id: str, track_id: str, actor: str) -> None:
        self._catalog.track(track_id)
        self._playlists.add_track(playlist_id, track_id, actor)

    def remove_from_playlist(self, playlist_id: str, track_id: str, actor: str) -> None:
        self._playlists.remove_track(playlist_id, track_id, actor)

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        return self._playlists.track_ids(playlist_id)

    @property
    def referenced_track_count(self) -> int:
        """还被至少一份播放列表引用着的曲目数——下架一首被引用的歌之后应当变小。"""
        return self._playlists.referenced_track_count

    # ---- 第 2 关：播放器与队列 ----

    def _load_source(self, track_ids: Sequence[str]) -> None:
        self._player.load(PlayQueue(track_ids, self._rng, self._queue_history_capacity))

    def play_album(self, album_id: str) -> None:
        self._load_source(self._catalog.tracks_of_album(album_id))

    def play_playlist(self, playlist_id: str) -> None:
        self._load_source(self._playlists.track_ids(playlist_id))

    def play_radio(self, seed_track_id: str, limit: int = 20) -> None:
        """"电台"：以一首种子曲目为起点，拼上同一艺人的其它曲目，打乱后作为来源——一个简单、
        无需真正推荐系统的"由历史/口味种子生成来源"实现。
        """
        seed = self._catalog.track(seed_track_id)
        pool = [t.id for t in self._catalog.tracks_of_artist(seed.artist_id) if t.id != seed_track_id]
        self._rng.shuffle(pool)
        self._load_source((seed_track_id, *pool[:max(0, limit - 1)]))

    def set_shuffle(self, on: bool) -> None:
        self._player.queue.set_shuffle(on)

    def set_repeat(self, mode: RepeatMode) -> None:
        self._player.queue.set_repeat(mode)

    def add_to_queue(self, track_id: str) -> None:
        self._catalog.track(track_id)
        self._player.queue.add_track(track_id)

    def play(self) -> str | None:
        return self._player.play()

    def pause(self) -> None:
        self._player.pause()

    def stop(self) -> None:
        self._player.stop()

    def skip_next(self) -> str | None:
        return self._player.skip_next()

    def skip_previous(self) -> str | None:
        return self._player.skip_previous()

    @property
    def state(self) -> PlayerState:
        return self._player.state

    @property
    def now_playing(self) -> str | None:
        return self._player.queue.now_playing

    @property
    def queue_upcoming(self) -> tuple[str, ...]:
        """当前队列里接下来会播的顺序快照——测试与 UI 都只看这个公开视图，不碰播放器内部。"""
        return self._player.queue.upcoming

    @property
    def history_event_count(self) -> int:
        """播放历史日志里此刻还留着的事件数——受 `history_capacity` 限制，验证它不会无界增长。"""
        return self._history.event_count

    # ---- 第 3 关：历史、统计、离线 ----

    def recently_played(self, limit: int = 20) -> tuple[str, ...]:
        return self._history.recent(limit)

    def most_played(self, limit: int = 10) -> tuple[tuple[str, int], ...]:
        return self._history.most_played(limit)

    def download(self, track_id: str) -> None:
        self._catalog.track(track_id).downloaded = True

    def remove_download(self, track_id: str) -> None:
        self._catalog.track(track_id).downloaded = False


def _demo() -> None:
    library = MusicLibrary(rng=random.Random(7))
    library.add_artist("artist-1", "Daft Punk")
    library.add_album("album-1", "Discovery", "artist-1")
    for i, title in enumerate(("One More Time", "Aerodynamic", "Digital Love"), start=1):
        library.add_track(f"track-{i}", title, "album-1", 240)
    library.play_album("album-1")
    library.set_repeat(RepeatMode.ALL)
    print("now playing:", library.play())
    print("next:", library.skip_next())
    print("recently played:", library.recently_played())


if __name__ == "__main__":
    _demo()
