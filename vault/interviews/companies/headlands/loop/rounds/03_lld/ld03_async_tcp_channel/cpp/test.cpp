// ld03 · Asynchronous TCP message channel — C++20 tests.  Same cases as test/FramingTest.java, TcpMessageChannelTest.java and
// ReconnectTest.java (real sockets on 127.0.0.1, ephemeral ports) plus C++-only edge cases (tag "cpp"): RAII file descriptors,
// take(size_t(-1)), no SIGPIPE, failure() as std::exception_ptr, non-movable channels, destructor = close.
// Correctness is never judged by sleeping: tests wait for "eventually true" conditions with a deadline (until()).
#include <algorithm>
#include <atomic>
#include <chrono>
#include <climits>
#include <deque>
#include <functional>
#include <future>
#include <iostream>
#include <random>
#include <string>
#include <string_view>
#include <thread>
#include <type_traits>

#include <sys/socket.h>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace net;
using namespace std::chrono_literals;

namespace {
using Clock = std::chrono::steady_clock;

Bytes B(std::initializer_list<int> v) {
    Bytes b;
    for (int x : v) b.push_back(static_cast<std::uint8_t>(x));
    return b;
}
Bytes S(std::string_view s) { return Bytes(s.begin(), s.end()); }
using Opt = std::optional<Bytes>;

/// Poll until `cond` holds or fail after timeout_ms: only for "this will eventually happen", never to guess timing.
void until(const std::string& what, int timeout_ms, const std::function<bool()>& cond) {
    const auto deadline = Clock::now() + std::chrono::milliseconds(timeout_ms);
    while (!cond()) {
        REQUIRE(Clock::now() <= deadline, "timed out waiting for: " + what);
        std::this_thread::sleep_for(1ms);
    }
}

/// Deterministic test message: length 4..64, first 4 bytes = sequence number (big-endian), the rest a function of the sequence number.
Bytes msg(int seq) {
    const std::size_t len = 4 + static_cast<std::size_t>((seq * 31LL) % 61);
    Bytes b(len);
    for (int i = 0; i < 4; ++i) b[i] = static_cast<std::uint8_t>(static_cast<unsigned>(seq) >> (24 - 8 * i));
    for (std::size_t i = 4; i < len; ++i) b[i] = static_cast<std::uint8_t>(seq + static_cast<int>(i));
    return b;
}
bool is_msg(const Opt& m, int seq) { return m.has_value() && *m == msg(seq); }

template <class E> bool failure_is(const TcpMessageChannel& ch) {
    const std::exception_ptr p = ch.failure();
    if (!p) return false;
    try { std::rethrow_exception(p); } catch (const E&) { return true; } catch (...) { return false; }
}

// ---- raw sockets (the "other end" for the tests that need to control individual bytes) --------------------------------
struct RawListener {
    UniqueFd fd;
    std::uint16_t port = 0;
};
void set_buf(int fd, int opt, int size) { if (size > 0) ::setsockopt(fd, SOL_SOCKET, opt, &size, sizeof size); }
RawListener listen_raw(int rcvbuf = 0) {
    RawListener l;
    l.fd.reset(::socket(AF_INET, SOCK_STREAM, 0));
    REQUIRE(l.fd.get() >= 0);
    const int one = 1;
    ::setsockopt(l.fd.get(), SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    set_buf(l.fd.get(), SO_RCVBUF, rcvbuf);
    sockaddr_in sa{};
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    REQUIRE(::bind(l.fd.get(), reinterpret_cast<sockaddr*>(&sa), sizeof sa) == 0);
    REQUIRE(::listen(l.fd.get(), 16) == 0);
    socklen_t len = sizeof sa;
    ::getsockname(l.fd.get(), reinterpret_cast<sockaddr*>(&sa), &len);
    l.port = ntohs(sa.sin_port);
    return l;
}
UniqueFd connect_raw(std::uint16_t port, int sndbuf = 0) {
    UniqueFd fd(::socket(AF_INET, SOCK_STREAM, 0));
    REQUIRE(fd.get() >= 0);
    set_buf(fd.get(), SO_SNDBUF, sndbuf);
    sockaddr_in sa{};
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    sa.sin_port = htons(port);
    REQUIRE(::connect(fd.get(), reinterpret_cast<sockaddr*>(&sa), sizeof sa) == 0);
    return fd;
}
UniqueFd accept_raw(const RawListener& l) {
    UniqueFd fd(::accept(l.fd.get(), nullptr, nullptr));
    REQUIRE(fd.get() >= 0);
    return fd;
}
void send_raw(const UniqueFd& fd, const Bytes& b) {
    std::size_t off = 0;
    while (off < b.size()) {
        const ssize_t n = ::send(fd.get(), b.data() + off, b.size() - off, 0);
        REQUIRE(n > 0, "raw send failed");
        off += static_cast<std::size_t>(n);
    }
}
Bytes be32(std::uint32_t v) { return B({static_cast<int>(v >> 24), static_cast<int>(v >> 16 & 0xFF), static_cast<int>(v >> 8 & 0xFF), static_cast<int>(v & 0xFF)}); }
Bytes cat(std::initializer_list<Bytes> parts) {
    Bytes out;
    for (const auto& p : parts) out.insert(out.end(), p.begin(), p.end());
    return out;
}

const ChannelConfig CFG(1024, 16 * 1024, 16 * 1024);

struct Pair {
    std::unique_ptr<TcpMessageChannel> client, server;
};
Pair connected_pair(const ChannelConfig& cfg) {
    MessageServer srv(0, cfg);
    Pair p;
    p.client = TcpMessageChannel::connect(srv.address(), cfg);
    p.server = srv.accept(5000ms);
    REQUIRE(p.server != nullptr, "server did not accept");
    return p;
}
/// Kernel buffers squeezed to 4 KiB so that "the kernel buffer is full" happens after a few tens of KB.
Pair tiny_pair(const ChannelConfig& cfg) {
    auto lst = listen_raw(4096);
    UniqueFd c = connect_raw(lst.port, 4096);
    UniqueFd s = accept_raw(lst);
    set_buf(s.get(), SO_RCVBUF, 4096);
    Pair p;
    p.client = TcpMessageChannel::wrap(std::move(c), cfg);
    p.server = TcpMessageChannel::wrap(std::move(s), cfg);
    return p;
}
}  // namespace

// ================================================ Part 1: ByteRing

TEST(ring_basic_write_read, "part1") {
    ByteRing r(8);
    CHECK_EQ(r.capacity(), 8u);
    CHECK_EQ(r.size(), 0u);
    CHECK_EQ(r.free(), 8u);
    CHECK(r.is_empty());
    CHECK_EQ(r.write(B({1, 2, 3})), 3u);
    CHECK_EQ(r.size(), 3u);
    Bytes dst(10);
    CHECK_EQ(r.read(dst), 3u);
    CHECK_EQ(Bytes(dst.begin(), dst.begin() + 3), B({1, 2, 3}));
    CHECK(r.is_empty());
    Bytes four(4);
    CHECK_EQ(r.read(four), 0u);
}

TEST(ring_wraps_around_and_splits_the_copy, "part1,edge") {
    ByteRing r(8);
    r.write(B({1, 2, 3, 4, 5, 6}));
    CHECK_EQ(r.take(4), B({1, 2, 3, 4}));
    CHECK_EQ(r.write(B({7, 8, 9, 10, 11})), 5u);  // 2 slots at the end + 4 at the start: two copies
    CHECK_EQ(r.size(), 7u);
    CHECK_EQ(r.take(7), B({5, 6, 7, 8, 9, 10, 11}));
}

TEST(ring_partial_write_when_full, "part1,edge") {
    ByteRing r(4);
    const Bytes src = B({1, 2, 3, 4, 5, 6});
    CHECK_EQ(r.write(src), 4u);  // only 4 fit; the caller advances its own cursor by 4
    CHECK_EQ(r.write(std::span<const std::uint8_t>(src).subspan(4)), 0u);  // full: not one byte
    CHECK_EQ(r.free(), 0u);
}

TEST(ring_partial_read_into_small_buffer, "part1,edge") {
    ByteRing r(8);
    r.write(B({1, 2, 3, 4, 5}));
    Bytes dst(2);
    CHECK_EQ(r.read(dst), 2u);
    CHECK_EQ(r.size(), 3u);
    CHECK_EQ(r.take(3), B({3, 4, 5}));
}

TEST(ring_write_all_is_atomic, "part1") {
    ByteRing r(5);
    CHECK(r.write_all(B({1, 2, 3})));
    CHECK(!r.write_all(B({4, 5, 6})));  // only 2 slots left: nothing is written
    CHECK_EQ(r.size(), 3u);
    CHECK(r.write_all(B({4, 5})));
    CHECK_EQ(r.take(5), B({1, 2, 3, 4, 5}));
}

TEST(ring_peek_int_is_big_endian_across_wrap_and_does_not_consume, "part1,edge") {
    ByteRing r(6);
    r.write(B({0, 0, 0, 0}));
    r.skip(4);
    r.write(B({0x12, 0x34, 0x56, 0x78, 0x9A}));  // the data starts at slot 4 and wraps
    CHECK_EQ(r.peek_int(), 0x12345678);
    CHECK_EQ(r.peek_int(1), 0x3456789A);
    CHECK_EQ(r.size(), 5u);
    CHECK_THROWS_AS(r.peek_int(2), StateError);
    ByteRing neg(4);
    neg.write(B({0xFF, 0xFF, 0xFF, 0xFF}));
    CHECK_EQ(neg.peek_int(), -1);  // the sign bit
}

TEST(ring_take_skip_errors_leave_state_untouched, "part1,edge") {
    ByteRing r(4);
    r.write(B({1, 2}));
    CHECK_THROWS_AS(r.take(3), StateError);
    CHECK_THROWS_AS(r.skip(3), StateError);
    CHECK_EQ(r.size(), 2u);
    r.skip(2);
    CHECK(r.is_empty());
    CHECK_EQ(r.take(0), Bytes{});
    r.write(B({7}));
    r.clear();
    CHECK(r.is_empty());
    CHECK_THROWS_AS(ByteRing(0), std::invalid_argument);
}

TEST(ring_matches_a_deque_model_on_random_ops, "part1,edge") {
    std::mt19937 rnd(3);
    for (std::size_t cap : {1u, 2u, 7u, 16u, 100u}) {
        ByteRing r(cap);
        std::deque<std::uint8_t> model;
        for (int i = 0; i < 3000; ++i) {
            if (rnd() % 2 == 0) {
                Bytes data(rnd() % (cap + 3));
                for (auto& b : data) b = static_cast<std::uint8_t>(rnd());
                const std::size_t n = r.write(data);
                CHECK_EQ(n, std::min(data.size(), cap - model.size()));
                for (std::size_t k = 0; k < n; ++k) model.push_back(data[k]);
            } else {
                Bytes dst(rnd() % (cap + 3));
                const std::size_t n = r.read(dst);
                CHECK_EQ(n, std::min(dst.size(), model.size()));
                for (std::size_t k = 0; k < n; ++k) { CHECK_EQ(dst[k], model.front()); model.pop_front(); }
            }
            CHECK_EQ(r.size(), model.size());
        }
    }
}

// ================================================ Part 1: FrameCodec

TEST(encode_writes_big_endian_length_then_payload, "part1") {
    ByteRing r(32);
    CHECK(FrameCodec::encode(r, B({10, 20, 30}), 100));
    CHECK_EQ(r.take(7), B({0, 0, 0, 3, 10, 20, 30}));
    ByteRing r2(400);
    CHECK(FrameCodec::encode(r2, Bytes(300), 300));
    CHECK_EQ(r2.take(4), B({0, 0, 1, 44}));  // 300 = 0x012C
}

TEST(encode_empty_payload_is_legal, "part1,edge") {
    ByteRing r(8);
    CHECK(FrameCodec::encode(r, Bytes{}, 10));
    CHECK_EQ(r.take(4), B({0, 0, 0, 0}));
}

TEST(encode_returns_false_without_a_partial_write_when_full, "part1,edge") {
    ByteRing r(10);
    CHECK(FrameCodec::encode(r, Bytes(3), 10));  // 7 bytes
    CHECK(!FrameCodec::encode(r, Bytes(2), 10));  // needs 6, 3 left
    CHECK_EQ(r.size(), 7u);                       // no half header was written
    CHECK(!FrameCodec::encode(r, Bytes{}, 10));   // needs 4, 3 left
    r.skip(7);
    CHECK(FrameCodec::encode(r, Bytes(6), 10));   // exactly 10
    CHECK_EQ(r.free(), 0u);
}

TEST(encode_rejects_oversized_payload, "part1,edge") {
    ByteRing r(64);
    CHECK_THROWS_AS(FrameCodec::encode(r, Bytes(11), 10), std::invalid_argument);
    CHECK(FrameCodec::encode(r, Bytes(10), 10));  // exactly max_frame
}

// ================================================ Part 1: FrameDecoder

namespace {
Bytes encode_all(int max_frame, const std::vector<Bytes>& msgs) {
    std::size_t total = 0;
    for (const auto& m : msgs) total += 4 + m.size();
    ByteRing r(std::max<std::size_t>(1, total));
    for (const auto& m : msgs) REQUIRE(FrameCodec::encode(r, m, max_frame));
    return r.take(total);
}
std::vector<Bytes> drain(FrameDecoder& d) {
    std::vector<Bytes> out;
    while (auto m = d.next()) out.push_back(std::move(*m));
    return out;
}
}  // namespace

TEST(decoder_returns_whole_frames_and_nullopt_when_incomplete, "part1") {
    FrameDecoder d(100, 256);
    CHECK(!d.next());
    const Bytes stream = encode_all(100, {B({1, 2}), B({3}), Bytes{}});
    CHECK_EQ(d.feed(stream), stream.size());
    CHECK_EQ(d.next(), Opt(B({1, 2})));
    CHECK_EQ(d.next(), Opt(B({3})));
    CHECK_EQ(d.next(), Opt(Bytes{}));
    CHECK(!d.next());
    CHECK_EQ(d.buffered(), 0u);
}

TEST(decoder_handles_every_split_point_of_a_stream, "part1,edge") {
    const std::vector<Bytes> msgs = {S("hello"), Bytes{}, S("w"), Bytes(20)};
    const Bytes stream = encode_all(50, msgs);
    for (std::size_t cut = 0; cut <= stream.size(); ++cut) {
        FrameDecoder d(50, 128);
        std::vector<Bytes> got;
        d.feed(std::span<const std::uint8_t>(stream).first(cut));
        for (auto& m : drain(d)) got.push_back(std::move(m));
        d.feed(std::span<const std::uint8_t>(stream).subspan(cut));
        for (auto& m : drain(d)) got.push_back(std::move(m));
        CHECK_EQ(got, msgs, "cut=" + std::to_string(cut));
    }
}

TEST(decoder_byte_at_a_time, "part1,edge") {
    const std::vector<Bytes> msgs = {S("abc"), S("defgh")};
    const Bytes stream = encode_all(10, msgs);
    FrameDecoder d(10, 14);
    std::vector<Bytes> got;
    for (std::uint8_t b : stream) {
        CHECK_EQ(d.feed(std::span<const std::uint8_t>(&b, 1)), 1u);
        if (auto m = d.next()) got.push_back(*m);
    }
    CHECK_EQ(got, msgs);
}

TEST(decoder_accepts_a_frame_of_exactly_max_frame, "part1,edge") {
    FrameDecoder d(5, 9);  // capacity exactly max_frame + 4
    const Bytes stream = encode_all(5, {B({1, 2, 3, 4, 5})});
    CHECK_EQ(d.feed(stream), 9u);
    CHECK_EQ(d.next(), Opt(B({1, 2, 3, 4, 5})));
    CHECK_THROWS_AS(FrameDecoder(5, 8), std::invalid_argument);
}

TEST(decoder_feed_is_bounded_and_resumes_after_drain, "part1,edge") {
    FrameDecoder d(4, 12);
    const Bytes stream = encode_all(4, {B({1}), B({2, 2}), B({3, 3, 3}), B({4})});
    std::span<const std::uint8_t> src(stream);
    const std::size_t fed = d.feed(src);
    src = src.subspan(fed);
    CHECK_EQ(fed, 12u);  // only 12 bytes fit
    CHECK_EQ(src.size(), stream.size() - 12);
    CHECK_EQ(d.free(), 0u);
    std::vector<Bytes> got;
    for (int guard = 0; guard < 20 && got.size() < 4; ++guard) {
        for (auto& m : drain(d)) got.push_back(std::move(m));
        src = src.subspan(d.feed(src));
    }
    CHECK_EQ(got.size(), 4u);
    CHECK_EQ(got[2], B({3, 3, 3}));
    CHECK(src.empty());
}

TEST(decoder_rejects_negative_and_oversized_lengths_and_stays_failed, "part1,edge") {
    FrameDecoder neg(10, 64);
    neg.feed(cat({B({0xFF, 0xFF, 0xFF, 0xFF}), B({1, 2, 3})}));
    CHECK_THROWS_AS(neg.next(), FrameException);
    CHECK_THROWS_AS(neg.next(), FrameException);  // sticky
    CHECK(neg.has_frame());

    FrameDecoder big(10, 64);
    big.feed(B({0, 0, 0, 11}));  // max_frame + 1: the header alone must be enough to reject, do not wait for 11 bytes
    CHECK_THROWS_AS(big.next(), FrameException);

    FrameDecoder huge(10, 64);
    huge.feed(B({0x7F, 0xFF, 0xFF, 0xFF}));  // 2^31 - 1: never try to allocate that
    CHECK_THROWS_AS(huge.next(), FrameException);
}

TEST(decoder_has_frame_and_truncated_tail, "part1") {
    FrameDecoder d(10, 64);
    CHECK(!d.has_frame());
    CHECK(!d.has_truncated_tail());
    d.feed(B({0, 0}));  // half a header
    CHECK(!d.has_frame());
    CHECK(d.has_truncated_tail());
    d.feed(B({0, 2, 7}));  // header complete, payload 1 of 2
    CHECK(!d.has_frame());
    CHECK(d.has_truncated_tail());
    d.feed(B({8, 0, 0, 0, 0}));  // completes the first frame + one empty frame
    CHECK(d.has_frame());
    CHECK(!d.has_truncated_tail());
    d.feed(B({0, 0}));  // half a header after the complete frames
    CHECK(d.has_truncated_tail());
    CHECK_EQ(d.next(), Opt(B({7, 8})));
    CHECK(d.has_truncated_tail());  // the empty frame is still there, and then half a header
    CHECK_EQ(d.next(), Opt(Bytes{}));
    CHECK(d.has_truncated_tail());
    CHECK(!d.next());
}

TEST(decoder_random_chunking_round_trip, "part1,edge") {
    std::mt19937 rnd(5);
    for (int round = 0; round < 40; ++round) {
        const int max_frame = 1 + static_cast<int>(rnd() % 60);
        std::vector<Bytes> msgs;
        for (int i = 0; i < 100; ++i) {
            Bytes m(rnd() % static_cast<unsigned>(max_frame + 1));
            for (auto& b : m) b = static_cast<std::uint8_t>(rnd());
            msgs.push_back(std::move(m));
        }
        const Bytes stream = encode_all(max_frame, msgs);
        FrameDecoder d(max_frame, max_frame + 4 + static_cast<int>(rnd() % 40));
        std::span<const std::uint8_t> src(stream);
        std::vector<Bytes> got;
        for (int guard = 0; got.size() < msgs.size(); ++guard) {
            REQUIRE(guard < 100'000, "decoder stuck");
            const std::size_t chunk = 1 + rnd() % 30;
            const std::size_t used = d.feed(src.first(std::min(chunk, src.size())));
            src = src.subspan(used);
            for (auto& m : drain(d)) got.push_back(std::move(m));
        }
        CHECK_EQ(got, msgs);
    }
}

TEST(million_messages_through_ring_and_decoder_fast, "part1,perf") {
    ByteRing ring(1 << 16);
    FrameDecoder d(64, 1 << 12);
    Bytes msg_bytes(32);
    Bytes chunk(1 << 12);
    long long got = 0;
    bool ring_full = false;
    CHECK_WITHIN_MS(2000,
        for (int i = 0; i < 1'000'000; ++i) {
            msg_bytes[0] = static_cast<std::uint8_t>(i);
            if (!FrameCodec::encode(ring, msg_bytes, 64)) { ring_full = true; break; }
            if ((i & 63) == 63) {  // every 64 messages move one batch, like a socket delivering a burst
                const std::size_t n = ring.read(chunk);
                std::span<const std::uint8_t> rest(chunk.data(), n);
                while (!rest.empty()) {
                    rest = rest.subspan(d.feed(rest));
                    while (d.next()) ++got;
                }
            }
        });
    CHECK(!ring_full);
    CHECK_EQ(got, 1'000'000 - (1'000'000 % 64));
}

// ---- C++-only, Part 1

TEST(take_with_a_huge_count_fails_before_allocating, "part1,cpp,edge") {
    // Java's int n < 0 is an IllegalArgumentException.  An unsigned parameter makes "negative" unrepresentable, but static_cast<size_t>(-1)
    // is 2^64 - 1: the check must come BEFORE `Bytes out(n)`, or this throws std::bad_alloc / length_error (or is killed) instead of StateError.
    ByteRing r(4);
    r.write(B({1, 2}));
    CHECK_THROWS_AS(r.take(static_cast<std::size_t>(-1)), StateError);
    CHECK_THROWS_AS(r.skip(static_cast<std::size_t>(-1)), StateError);
    CHECK_THROWS_AS(r.peek_int(static_cast<std::size_t>(-1)), StateError);  // offset + 4 would wrap around to 3
    CHECK_EQ(r.size(), 2u);
}

TEST(ring_and_decoder_are_plain_values, "part1,cpp") {
    // A copy is an independent buffer (std::vector inside): no aliasing between the original and the copy.
    ByteRing a(8);
    a.write(B({1, 2, 3}));
    ByteRing b = a;
    b.write(B({4}));
    CHECK_EQ(a.size(), 3u);
    CHECK_EQ(b.size(), 4u);
    CHECK_EQ(a.take(3), B({1, 2, 3}));
    CHECK_EQ(b.take(4), B({1, 2, 3, 4}));
    CHECK_THROWS_AS(ChannelConfig(10, 13, 14), std::invalid_argument);
    CHECK_THROWS_AS(ChannelConfig(10, 14, 13), std::invalid_argument);
    CHECK_THROWS_AS(ChannelConfig(-1, 4, 4), std::invalid_argument);
    CHECK_NOTHROW(ChannelConfig(10, 14, 14));
    CHECK_EQ(ChannelConfig::of(100).out_capacity(), 64 * 1024);
}

// ================================================ Part 2: one connection

TEST(request_reply, "part2,io") {
    auto p = connected_pair(CFG);
    CHECK(!p.server->poll());
    CHECK(p.client->offer(S("hello")));
    CHECK_EQ(p.server->poll(5000ms), Opt(S("hello")));
    CHECK(p.server->offer(S("world")));
    CHECK_EQ(p.client->poll(5000ms), Opt(S("world")));
    CHECK(p.client->is_open());
    CHECK(!p.client->failure());
}

TEST(empty_and_max_size_messages, "part2,io,edge") {
    auto p = connected_pair(CFG);
    Bytes max(static_cast<std::size_t>(CFG.max_frame()));
    std::mt19937 rnd(1);
    for (auto& b : max) b = static_cast<std::uint8_t>(rnd());
    CHECK(p.client->offer(Bytes{}));
    CHECK(p.client->offer(max));
    CHECK(p.client->offer(Bytes{}));
    CHECK_EQ(p.server->poll(5000ms), Opt(Bytes{}));
    CHECK_EQ(p.server->poll(5000ms), Opt(max));
    CHECK_EQ(p.server->poll(5000ms), Opt(Bytes{}));
    CHECK_THROWS_AS(p.client->offer(Bytes(static_cast<std::size_t>(CFG.max_frame()) + 1)), std::invalid_argument);
    CHECK(p.client->is_open());  // a bad argument does not break the channel
}

TEST(poll_timeout_returns_nullopt_when_nothing_arrives, "part2,io") {
    auto p = connected_pair(CFG);
    CHECK(!p.server->poll(30ms));
    CHECK(!p.server->is_drained());
}

TEST(ten_thousand_messages_arrive_in_order, "part2,io,conc") {
    auto p = connected_pair(CFG);
    constexpr int n = 10'000;
    mt::ThreadErrors errs;
    auto sender = errs.spawn([&] {
        for (int i = 0; i < n; ++i)
            if (!p.client->offer(msg(i), 10'000ms)) throw std::runtime_error("offer timed out at " + std::to_string(i));
    });
    int bad = -1;
    for (int i = 0; i < n && bad < 0; ++i)
        if (!is_msg(p.server->poll(10'000ms), i)) bad = i;
    sender.join();
    CHECK_NO_THREAD_ERRORS(errs);
    CHECK_EQ(bad, -1, "message wrong or missing");
    CHECK(!p.server->poll());
}

TEST(two_hundred_thousand_messages_through_loopback_fast, "part2,io,perf") {
    auto p = connected_pair(ChannelConfig(1024, 64 * 1024, 64 * 1024));
    constexpr int n = 200'000;
    const Bytes payload(32);
    mt::ThreadErrors errs;
    int missing = -1;
    CHECK_WITHIN_MS(5000,
        auto sender = errs.spawn([&] { for (int i = 0; i < n; ++i) if (!p.client->offer(payload, 10'000ms)) throw std::runtime_error("offer timed out"); });
        for (int i = 0; i < n && missing < 0; ++i) if (!p.server->poll(10'000ms)) missing = i;
        sender.join(););
    CHECK_NO_THREAD_ERRORS(errs);
    CHECK_EQ(missing, -1);
}

TEST(both_directions_at_once, "part2,io,conc") {
    auto p = connected_pair(CFG);
    constexpr int n = 5000;
    mt::ThreadErrors errs;
    std::vector<std::thread> threads;
    TcpMessageChannel* ends[2] = {p.client.get(), p.server.get()};
    for (int side = 0; side < 2; ++side) {
        TcpMessageChannel* me = ends[side];
        const int base = side * 1'000'000, peer_base = (1 - side) * 1'000'000;
        threads.push_back(errs.spawn([=] {
            for (int i = 0; i < n; ++i) if (!me->offer(msg(base + i), 10'000ms)) throw std::runtime_error("offer timed out at " + std::to_string(i));
        }));
        threads.push_back(errs.spawn([=] {
            for (int i = 0; i < n; ++i) if (!is_msg(me->poll(10'000ms), peer_base + i)) throw std::runtime_error("wrong or missing message " + std::to_string(i));
        }));
    }
    for (auto& t : threads) t.join();
    CHECK_NO_THREAD_ERRORS(errs);
}

/// A raw socket plays the peer and sends the frame one byte at a time: the channel must not hand out half a message.
TEST(partial_reads_are_reassembled, "part2,io,edge") {
    auto lst = listen_raw();
    UniqueFd raw = connect_raw(lst.port);
    auto ch = TcpMessageChannel::wrap(accept_raw(lst), CFG);
    const Bytes payload = S("split-me-into-pieces");
    const Bytes frame = cat({be32(static_cast<std::uint32_t>(payload.size())), payload});
    for (std::size_t i = 0; i < 4 + 6; ++i) send_raw(raw, B({frame[i]}));  // header + first 6 bytes
    CHECK(!ch->poll(100ms));                                               // incomplete: nothing to hand out
    for (std::size_t i = 10; i < frame.size(); ++i) send_raw(raw, B({frame[i]}));
    CHECK_EQ(ch->poll(5000ms), Opt(payload));
    // two and a half messages in one write
    send_raw(raw, cat({be32(1), S("a"), be32(2), S("bc"), be32(3), S("d")}));
    CHECK_EQ(ch->poll(5000ms), Opt(S("a")));
    CHECK_EQ(ch->poll(5000ms), Opt(S("bc")));
    CHECK(!ch->poll(100ms));  // the third has its header and 1 of 3 bytes
    send_raw(raw, S("ef"));
    CHECK_EQ(ch->poll(5000ms), Opt(S("def")));
}

TEST(large_write_is_split_across_partial_writes_and_stays_intact, "part2,io,edge") {
    // Several MB at once: send() takes only part of the staging buffer, the rest has to wait for POLLOUT.
    const ChannelConfig big(1 << 20, 4 << 20, 2 << 20);
    auto p = connected_pair(big);
    std::mt19937 rnd(9);
    std::vector<Bytes> msgs(6);
    for (auto& m : msgs) {
        m.resize((1u << 19) + rnd() % (1u << 19));
        for (auto& b : m) b = static_cast<std::uint8_t>(rnd());
    }
    for (const auto& m : msgs) CHECK(p.client->offer(m, 10'000ms));
    for (const auto& m : msgs) {
        auto got = p.server->poll(10'000ms);
        CHECK(got.has_value() && *got == m, "message corrupted or missing");
    }
}

TEST(invalid_frame_header_fails_the_channel_but_keeps_earlier_messages, "part2,io,edge") {
    auto lst = listen_raw();
    UniqueFd raw = connect_raw(lst.port);
    auto ch = TcpMessageChannel::wrap(accept_raw(lst), CFG);
    send_raw(raw, cat({be32(2), S("ok"), be32(static_cast<std::uint32_t>(CFG.max_frame()) + 1)}));
    CHECK_EQ(ch->poll(5000ms), Opt(S("ok")));
    CHECK_THROWS_AS(ch->poll(5000ms), FrameException);
    CHECK(failure_is<FrameException>(*ch));
    CHECK(!ch->is_open());
    CHECK_THROWS_AS(ch->offer(S("x")), StateError);
}

TEST(peer_closing_mid_frame_is_an_error_but_complete_frames_survive, "part2,io,edge") {
    auto lst = listen_raw();
    UniqueFd raw = connect_raw(lst.port);
    auto ch = TcpMessageChannel::wrap(accept_raw(lst), CFG);
    send_raw(raw, cat({be32(3), S("abc"), be32(10), S("xyz")}));
    raw.reset();  // close
    CHECK_EQ(ch->poll(5000ms), Opt(S("abc")));
    until("channel closed", 5000, [&] { return !ch->is_open(); });
    CHECK(failure_is<EofError>(*ch));
    CHECK(!ch->poll());
    CHECK(ch->is_drained());
}

TEST(finish_sending_flushes_then_peer_sees_drained, "part2,io") {
    auto p = connected_pair(CFG);
    constexpr int n = 2000;
    for (int i = 0; i < n; ++i) CHECK(p.client->offer(msg(i), 10'000ms));
    p.client->finish_sending();
    CHECK_THROWS_AS(p.client->offer(S("late")), StateError);
    int got = 0;
    while (auto m = p.server->poll(10'000ms)) {
        CHECK(is_msg(m, got), "at " + std::to_string(got));
        ++got;
    }
    CHECK_EQ(got, n);  // everything arrives first; only then does poll return nullopt, because of the EOF
    CHECK(p.server->is_drained());
    CHECK(p.server->is_peer_closed());
    CHECK(p.server->is_open());  // half-close: the server can still talk
    CHECK(p.server->offer(S("bye")));
    CHECK_EQ(p.client->poll(5000ms), Opt(S("bye")));
    p.server->finish_sending();  // both sides done -> both channels close
    CHECK(p.server->await_closed(5000ms));
    CHECK(p.client->await_closed(5000ms));
    CHECK(!p.client->failure());
    CHECK(!p.server->failure());
}

TEST(abrupt_close_is_seen_by_the_peer, "part2,io,edge") {
    auto p = connected_pair(CFG);
    p.client->offer(S("last"));
    until("flushed", 5000, [&] { return p.client->unsent_bytes() == 0; });
    p.client->close();
    CHECK(!p.client->is_open());
    CHECK_THROWS_AS(p.client->offer(S("x")), StateError);
    CHECK_EQ(p.server->poll(5000ms), Opt(S("last")));
    until("peer EOF seen", 5000, [&] { return p.server->is_peer_closed(); });
    CHECK(p.server->is_drained());
    p.client->close();  // idempotent
}

TEST(close_wakes_a_blocked_poll, "part2,io,edge") {
    auto p = connected_pair(CFG);
    auto result = std::async(std::launch::async, [&] { return p.server->poll(30'000ms); });
    std::this_thread::sleep_for(50ms);  // not a correctness dependency: only makes it likely that the poll is already blocked
    p.server->close();
    CHECK(result.wait_for(5000ms) == std::future_status::ready, "poll(timeout) must return when the channel is closed");
    CHECK(!result.get());
}

TEST(close_wakes_a_blocked_offer, "part2,io,edge") {
    auto p = tiny_pair(ChannelConfig(256, 4 * 1024, 4 * 1024));
    int accepted = 0;
    while (accepted < 2'000'000 && p.client->offer(msg(accepted), 100ms)) ++accepted;
    auto result = std::async(std::launch::async, [&]() -> std::string {
        try { return p.client->offer(msg(accepted), 30'000ms) ? "true" : "false"; } catch (const StateError&) { return "StateError"; }
    });
    std::this_thread::sleep_for(50ms);
    p.client->close();
    CHECK(result.wait_for(5000ms) == std::future_status::ready, "offer(msg, timeout) must return when the channel is closed");
    CHECK_EQ(result.get(), "StateError");
}

TEST(accept_times_out_and_a_port_cannot_be_bound_twice, "part2,io,edge") {
    MessageServer srv(0, CFG);
    CHECK(srv.port() != 0);
    CHECK_EQ(srv.address(), loopback(srv.port()));
    CHECK(srv.accept(20ms) == nullptr);
    CHECK_THROWS_AS(MessageServer(srv.port(), CFG), std::system_error);  // EADDRINUSE
    srv.close();
    srv.close();  // idempotent
}

// ---- C++-only, Part 2

static_assert(!std::is_move_constructible_v<TcpMessageChannel> && !std::is_copy_constructible_v<TcpMessageChannel>,
              "a channel owns a thread, a mutex and a socket: it is created on the heap and handed around as unique_ptr");
static_assert(!std::is_copy_constructible_v<MessageServer> && !std::is_copy_constructible_v<ReconnectingClient>);
static_assert(!std::is_copy_constructible_v<UniqueFd> && std::is_nothrow_move_constructible_v<UniqueFd>);

TEST(unique_fd_closes_exactly_once, "part2,cpp") {
    int fds[2];
    REQUIRE(::pipe(fds) == 0);
    const int raw_fd = fds[0];
    {
        UniqueFd a(fds[0]);
        UniqueFd b(fds[1]);
        UniqueFd moved = std::move(a);
        CHECK(!a);  // NOLINT(bugprone-use-after-move): a moved-from UniqueFd is empty by contract
        CHECK(moved);
        CHECK_EQ(moved.get(), raw_fd);
        UniqueFd target;
        target = std::move(moved);
        CHECK_EQ(target.get(), raw_fd);
    }  // both descriptors closed here
    CHECK(::fcntl(raw_fd, F_GETFD) == -1 && errno == EBADF, "the descriptor must be closed after the last owner is gone");
}

TEST(destroying_the_channel_closes_the_connection, "part2,io,cpp") {
    auto p = connected_pair(CFG);
    CHECK(p.client->offer(S("bye")));
    until("flushed", 5000, [&] { return p.client->unsent_bytes() == 0; });
    p.client.reset();  // no explicit close(): the destructor is the close
    CHECK_EQ(p.server->poll(5000ms), Opt(S("bye")));
    until("peer EOF seen", 5000, [&] { return p.server->is_peer_closed(); });
}

TEST(addresses_match_on_both_ends, "part2,io,cpp") {
    auto p = connected_pair(CFG);
    CHECK_EQ(p.client->remote_address(), p.server->local_address());
    CHECK_EQ(p.server->remote_address(), p.client->local_address());
    CHECK_EQ(p.client->local_address().host, "127.0.0.1");
    p.client->close();
    CHECK_THROWS_AS(p.client->local_address(), StateError);
}

TEST(a_reset_connection_fails_the_channel_without_sigpipe, "part2,io,cpp,edge") {
    // The peer slams the door (RST, not FIN).  Writing to a reset connection raises SIGPIPE, whose default action kills the whole process,
    // unless send() is called with MSG_NOSIGNAL / the socket has SO_NOSIGPIPE.  Surviving this test IS the assertion.
    auto lst = listen_raw();
    UniqueFd raw = connect_raw(lst.port);
    auto ch = TcpMessageChannel::wrap(accept_raw(lst), CFG);
    const linger lg{1, 0};
    ::setsockopt(raw.get(), SOL_SOCKET, SO_LINGER, &lg, sizeof lg);  // close() now sends RST
    raw.reset();
    bool refused = false;
    const auto deadline = Clock::now() + 5s;
    while (!refused && Clock::now() < deadline) {
        try { ch->offer(Bytes(100)); } catch (const StateError&) { refused = true; }
        std::this_thread::sleep_for(1ms);
    }
    CHECK(refused, "the channel should have failed after the reset");
    CHECK(!ch->is_open());
    CHECK(ch->failure() != nullptr);
    CHECK(failure_is<std::system_error>(*ch));
}

// ================================================ Part 3: back-pressure and bounds

TEST(offer_returns_false_when_receiver_does_not_read_then_recovers_without_loss, "part3,io") {
    auto p = tiny_pair(ChannelConfig(256, 8 * 1024, 8 * 1024));
    int accepted = 0;
    constexpr int limit = 2'000'000;
    // false can mean "the I/O thread has not made room yet"; if it is still false after 200 ms the pipeline is really full
    // (out ring + kernel send/receive buffers + in ring)
    while (accepted < limit && p.client->offer(msg(accepted), 200ms)) ++accepted;
    CHECK(accepted < limit, "outbound buffer is unbounded: " + std::to_string(accepted) + " messages accepted with nobody reading");
    CHECK(accepted > 0);
    CHECK(!p.client->offer(msg(accepted), 20ms));  // the timed version agrees
    // the receiver starts reading: every accepted message arrives, in order, once
    for (int i = 0; i < accepted; ++i) REQUIRE(is_msg(p.server->poll(10'000ms), i), "at " + std::to_string(i) + " of " + std::to_string(accepted));
    CHECK(!p.server->poll(50ms));
    // room again
    CHECK(p.client->offer(msg(accepted), 5000ms));
    CHECK(is_msg(p.server->poll(5000ms), accepted));
}

TEST(blocking_offer_waits_for_space_and_succeeds_once_the_receiver_reads, "part3,io") {
    auto p = tiny_pair(ChannelConfig(256, 4 * 1024, 4 * 1024));
    int accepted = 0;
    while (accepted < 2'000'000 && p.client->offer(msg(accepted), 200ms)) ++accepted;
    const int total = accepted;
    auto blocked = std::async(std::launch::async, [&] { return p.client->offer(msg(total), 20'000ms); });
    std::this_thread::sleep_for(50ms);  // only makes it likely that the offer is blocked already
    for (int i = 0; i < total; ++i) REQUIRE(is_msg(p.server->poll(10'000ms), i), "at " + std::to_string(i));
    CHECK(blocked.wait_for(10'000ms) == std::future_status::ready);
    CHECK(blocked.get());
    CHECK(is_msg(p.server->poll(5000ms), total));
}

/// Minimum legal buffers (capacity = max_frame + 4): every message is cut at the ring boundary and the inbound ring is full all the time.
TEST(minimal_buffers_still_deliver_everything_in_order, "part3,io,conc") {
    auto p = tiny_pair(ChannelConfig(64, 68, 68));
    constexpr int n = 20'000;
    mt::ThreadErrors errs;
    auto sender = errs.spawn([&] {
        for (int i = 0; i < n; ++i) if (!p.client->offer(msg(i), 20'000ms)) throw std::runtime_error("offer " + std::to_string(i));
    });
    int bad = -1;
    for (int i = 0; i < n && bad < 0; ++i) if (!is_msg(p.server->poll(20'000ms), i)) bad = i;
    sender.join();
    CHECK_NO_THREAD_ERRORS(errs);
    CHECK_EQ(bad, -1, "message wrong or missing");
}

/// Spinning on the non-blocking poll(): the in ring fills, the I/O thread stops asking for POLLIN; poll() has to wake it again.
TEST(spinning_non_blocking_poll_resumes_a_paused_reader, "part3,io,conc") {
    auto p = tiny_pair(ChannelConfig(64, 68, 68));
    constexpr int n = 5000;
    mt::ThreadErrors errs;
    auto sender = errs.spawn([&] { for (int i = 0; i < n; ++i) p.client->offer(msg(i), 20'000ms); });
    const auto deadline = Clock::now() + 20s;
    int got = 0, bad = -1;
    while (got < n && bad < 0) {
        REQUIRE(Clock::now() < deadline, "stalled after " + std::to_string(got) + " messages");
        auto m = p.server->poll();
        if (!m) { std::this_thread::yield(); continue; }
        if (!is_msg(m, got)) bad = got;
        ++got;
    }
    sender.join();
    CHECK_NO_THREAD_ERRORS(errs);
    CHECK_EQ(bad, -1);
}

TEST(slow_reader_never_makes_the_inbound_buffer_grow_beyond_its_bound, "part3,io,edge") {
    // The reader pauses now and then; the in ring holds two messages: the sender has to be slowed down, memory must not grow.
    auto p = tiny_pair(ChannelConfig(64, 1024, 136));
    constexpr int n = 3000;
    mt::ThreadErrors errs;
    auto sender = errs.spawn([&] { for (int i = 0; i < n; ++i) if (!p.client->offer(msg(i), 30'000ms)) throw std::runtime_error("offer " + std::to_string(i)); });
    int bad = -1;
    for (int i = 0; i < n && bad < 0; ++i) {
        if (i % 500 == 0) std::this_thread::sleep_for(20ms);
        if (!is_msg(p.server->poll(30'000ms), i)) bad = i;
    }
    sender.join();
    CHECK_NO_THREAD_ERRORS(errs);
    CHECK_EQ(bad, -1);
}

// ================================================ Part 4: Backoff

TEST(backoff_doubles_up_to_cap_then_stays_there, "part4") {
    Backoff b(100, 1000, 2);
    for (long long e : {100, 200, 400, 800, 1000, 1000, 1000}) CHECK_EQ(b.next(), e);
}

TEST(backoff_reset_starts_over, "part4") {
    Backoff b(5, 100, 3);
    CHECK_EQ(b.next(), 5);
    CHECK_EQ(b.next(), 15);
    CHECK_EQ(b.next(), 45);
    CHECK_EQ(b.next(), 100);
    b.reset();
    CHECK_EQ(b.next(), 5);
}

TEST(backoff_caps_exactly_and_never_overflows, "part4,edge") {
    Backoff b(1, LLONG_MAX, 10);
    long long prev = 0;
    for (int i = 0; i < 100; ++i) {
        const long long d = b.next();
        CHECK(d >= prev && d > 0, "step " + std::to_string(i) + " -> " + std::to_string(d));
        prev = d;
    }
    CHECK_EQ(prev, LLONG_MAX);
    Backoff c(7, 7, 2);
    CHECK_EQ(c.next(), 7);
    CHECK_EQ(c.next(), 7);
    Backoff flat(10, 1000, 1);
    for (int i = 0; i < 5; ++i) CHECK_EQ(flat.next(), 10);
}

TEST(backoff_full_jitter_stays_within_zero_and_current_cap, "part4,edge") {
    std::mt19937 rnd(42);
    Backoff b(10, 80, 2);
    bool saw_non_cap = false;
    for (long long cap : {10, 20, 40, 80, 80, 80}) {
        const long long d = b.next(rnd);
        CHECK(d >= 0 && d <= cap, std::to_string(d) + " not in [0," + std::to_string(cap) + "]");
        if (d != cap) saw_non_cap = true;
    }
    CHECK(saw_non_cap);
    Backoff huge(1, LLONG_MAX, 2);  // the distribution's upper bound is LLONG_MAX: cap + 1 would overflow if written the Java way
    for (int i = 0; i < 70; ++i) CHECK_NOTHROW(huge.next(rnd));
}

TEST(backoff_rejects_bad_parameters, "part4,edge") {
    CHECK_THROWS_AS(Backoff(0, 10, 2), std::invalid_argument);
    CHECK_THROWS_AS(Backoff(10, 5, 2), std::invalid_argument);
    CHECK_THROWS_AS(Backoff(1, 10, 0), std::invalid_argument);
}

// ================================================ Part 4: ReconnectingClient

namespace {
const ChannelConfig RCFG(256, 4 * 1024, 4 * 1024);
/// A port nobody listens on: bind to 0, read the port, close.
std::uint16_t dead_port() {
    auto l = listen_raw();
    return l.port;
}
}  // namespace

TEST(reconnects_after_the_server_drops_the_connection, "part4,io") {
    MessageServer srv(0, RCFG);
    ReconnectingClient client(srv.address(), RCFG, Backoff(2, 50, 2));
    auto first = srv.accept(5000ms);
    REQUIRE(first != nullptr);
    CHECK(client.offer(S("one")));
    CHECK_EQ(first->poll(5000ms), Opt(S("one")));
    CHECK_EQ(client.connect_count(), 1);

    first->close();  // the server hangs up
    auto second = srv.accept(5000ms);  // the client reconnected on its own
    REQUIRE(second != nullptr, "client did not reconnect");
    until("client sees the second connection", 5000, [&] { return client.connect_count() == 2 && client.is_connected(); });
    CHECK(client.offer(S("two")));
    CHECK_EQ(second->poll(5000ms), Opt(S("two")));
    CHECK(second->offer(S("pong")));  // and the other direction works
    until("inbound on the new connection", 5000, [&] {
        auto m = client.poll();
        return m && *m == S("pong");
    });
}

TEST(messages_offered_while_the_server_is_down_arrive_in_order_after_it_comes_back, "part4,io") {
    auto srv1 = std::make_unique<MessageServer>(0, RCFG);
    const std::uint16_t port = srv1->port();
    ReconnectingClient client(srv1->address(), RCFG, Backoff(2, 20, 2));
    auto c1 = srv1->accept(5000ms);
    REQUIRE(c1 != nullptr);
    CHECK(client.offer(S("before")));
    CHECK_EQ(c1->poll(5000ms), Opt(S("before")));

    c1->close();
    srv1.reset();  // the whole server goes away: the port stops listening
    until("client notices the disconnect", 5000, [&] { return !client.is_connected(); });
    for (int i = 0; i < 5; ++i) CHECK(client.offer(msg(i)), "offer while disconnected must be accepted");
    until("client retried and failed", 5000, [&] { return client.failed_attempts() >= 3; });
    CHECK(client.pending_bytes() > 0);

    MessageServer srv2(port, RCFG);  // back online on the same port
    auto c2 = srv2.accept(10'000ms);
    REQUIRE(c2 != nullptr, "client did not reconnect to the restarted server");
    for (int i = 0; i < 5; ++i) CHECK(is_msg(c2->poll(5000ms), i), "message " + std::to_string(i));
    CHECK(!c2->poll(50ms));
    until("pending drained", 5000, [&] { return client.pending_bytes() == 0; });
}

TEST(pending_queue_is_bounded_while_disconnected, "part4,io,edge") {
    const ChannelConfig small(100, 500, 500);
    ReconnectingClient client(loopback(dead_port()), small, Backoff(5, 20, 2));
    int accepted = 0;
    while (client.offer(Bytes(46))) ++accepted;  // 50 encoded bytes each -> 10 fit into 500
    CHECK_EQ(accepted, 10);
    CHECK_EQ(client.pending_bytes(), 500u);
    CHECK(!client.offer(Bytes{}));  // not even 4 more bytes
    CHECK_THROWS_AS(client.offer(Bytes(101)), std::invalid_argument);
    until("keeps retrying", 5000, [&] { return client.failed_attempts() >= 3; });
    CHECK(!client.is_connected());
    CHECK(!client.poll());
}

TEST(close_stops_reconnecting_and_rejects_offers, "part4,io,edge") {
    MessageServer srv(0, RCFG);
    ReconnectingClient client(srv.address(), RCFG, Backoff(2, 10, 2));
    auto c = srv.accept(5000ms);
    REQUIRE(c != nullptr);
    client.close();
    CHECK_THROWS_AS(client.offer(S("x")), StateError);
    until("server sees EOF", 5000, [&] { return c->is_peer_closed(); });
    const int count = client.connect_count();
    CHECK(srv.accept(150ms) == nullptr, "a closed client must not reconnect");
    CHECK_EQ(client.connect_count(), count);
    client.close();  // idempotent
}

TEST(backoff_resets_after_a_successful_connect, "part4,io,edge") {
    // Fail a few times with nobody listening, then bring a server up; after it kicks the client out, the reconnect should be quick
    // (the delay starts from the initial value again), not continue from the long delay reached during the outage.
    const std::uint16_t port = dead_port();
    ReconnectingClient client(loopback(port), RCFG, Backoff(5, 2000, 4));
    until("failed a few times", 5000, [&] { return client.failed_attempts() >= 3; });
    MessageServer srv(port, RCFG);
    auto c1 = srv.accept(10'000ms);
    REQUIRE(c1 != nullptr);
    c1->close();
    const auto t0 = Clock::now();
    auto c2 = srv.accept(1500ms);  // without the reset this would take >= 320 ms and grow towards 2 s
    REQUIRE(c2 != nullptr, "reconnect after a successful session should start from the initial delay");
    CHECK(Clock::now() - t0 < 1500ms);
}

TEST(destroying_the_client_is_a_close, "part4,io,cpp") {
    MessageServer srv(0, RCFG);
    std::unique_ptr<TcpMessageChannel> c;
    {
        ReconnectingClient client(srv.address(), RCFG, Backoff(2, 10, 2));
        c = srv.accept(5000ms);
        REQUIRE(c != nullptr);
        CHECK(client.offer(S("last words")));
        CHECK_EQ(c->poll(5000ms), Opt(S("last words")));
    }  // scope end: the destructor stops the manager thread and closes the channel - no leaked thread, no reconnect
    until("server sees EOF", 5000, [&] { return c->is_peer_closed(); });
    CHECK(srv.accept(150ms) == nullptr);
}

MT_MAIN()
