// ld03 · Asynchronous TCP message channel — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Given: exception types, UniqueFd, Address, ChannelConfig and the POSIX plumbing in net::detail (WakePipe, set_nonblocking, kSendFlags).
// To write: ByteRing, FrameCodec, FrameDecoder, TcpMessageChannel, MessageServer, Backoff, ReconnectingClient.
#pragma once

#include <algorithm>
#include <atomic>
#include <cerrno>
#include <chrono>
#include <condition_variable>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <deque>
#include <exception>
#include <memory>
#include <mutex>
#include <optional>
#include <random>
#include <span>
#include <stdexcept>
#include <string>
#include <system_error>
#include <thread>
#include <utility>
#include <vector>

#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <poll.h>
#include <sys/socket.h>
#include <unistd.h>

namespace net {

using Bytes = std::vector<std::uint8_t>;
using Millis = std::chrono::milliseconds;

// ---------------------------------------------------------------------------------------------- errors
/// The byte stream does not follow the frame protocol (negative length, longer than max_frame).  Unrecoverable: the stream has lost
/// sync, the only fix is to reconnect.
struct FrameException : std::runtime_error {
    using std::runtime_error::runtime_error;
};
/// Java IllegalStateException: the object is in the wrong state for the call (closed channel, finish_sending() already called, take(n) with
/// fewer than n bytes buffered).  "Temporarily full" is NOT an error: that is offer() returning false.
struct StateError : std::logic_error {
    using std::logic_error::logic_error;
};
/// Java EOFException: the peer closed the connection in the middle of a frame (the stream is truncated).
struct EofError : std::runtime_error {
    using std::runtime_error::runtime_error;
};
// Other Java exceptions: IllegalArgumentException -> std::invalid_argument;  IOException -> std::system_error (carries errno).

[[noreturn]] inline void throw_errno(const std::string& what, int err = errno) { throw std::system_error(err, std::generic_category(), what); }

// ---------------------------------------------------------------------------------------------- UniqueFd, Address
/// Owns one file descriptor (a socket or a pipe end) and closes it in the destructor: move-only RAII, the C++ replacement for try/finally.
class UniqueFd {
public:
    UniqueFd() = default;
    explicit UniqueFd(int fd) : fd_(fd) {}
    UniqueFd(UniqueFd&& o) noexcept : fd_(std::exchange(o.fd_, -1)) {}
    UniqueFd& operator=(UniqueFd&& o) noexcept {
        if (this != &o) reset(std::exchange(o.fd_, -1));
        return *this;
    }
    UniqueFd(const UniqueFd&) = delete;
    UniqueFd& operator=(const UniqueFd&) = delete;
    ~UniqueFd() { reset(); }

    int get() const { return fd_; }
    explicit operator bool() const { return fd_ >= 0; }
    int release() { return std::exchange(fd_, -1); }
    void reset(int fd = -1) {
        if (fd_ >= 0) ::close(fd_);
        fd_ = fd;
    }

private:
    int fd_ = -1;
};

/// IPv4 address (Java InetSocketAddress).  Everything here runs on 127.0.0.1.
struct Address {
    std::string host;
    std::uint16_t port = 0;
    friend bool operator==(const Address&, const Address&) = default;
};
inline Address loopback(std::uint16_t port) { return Address{"127.0.0.1", port}; }

// ---------------------------------------------------------------------------------------------- ChannelConfig
/// Channel parameters, in bytes.  max_frame: the largest payload (without the 4-byte length header).  out_capacity / in_capacity: the
/// outbound ring (holds ENCODED frames, header included) and the inbound ring; both must be >= max_frame + 4, otherwise a maximum-size
/// message could never be assembled / never fit.
class ChannelConfig {
public:
    ChannelConfig(int max_frame, int out_capacity, int in_capacity) : max_frame_(max_frame), out_capacity_(out_capacity), in_capacity_(in_capacity) {
        if (max_frame < 0) throw std::invalid_argument("max_frame < 0");
        if (max_frame > INT32_MAX - 4) throw std::invalid_argument("max_frame too large");
        if (out_capacity < max_frame + 4) throw std::invalid_argument("out_capacity must be >= max_frame + 4");
        if (in_capacity < max_frame + 4) throw std::invalid_argument("in_capacity must be >= max_frame + 4");
    }
    static ChannelConfig of(int max_frame) { return ChannelConfig(max_frame, 64 * 1024, 64 * 1024); }
    int max_frame() const { return max_frame_; }
    int out_capacity() const { return out_capacity_; }
    int in_capacity() const { return in_capacity_; }
    friend bool operator==(const ChannelConfig&, const ChannelConfig&) = default;

private:
    int max_frame_, out_capacity_, in_capacity_;
};

// ---------------------------------------------------------------------------------------------- plumbing (given)
namespace detail {
inline void set_nonblocking(int fd) {
    const int flags = ::fcntl(fd, F_GETFL, 0);
    if (flags < 0 || ::fcntl(fd, F_SETFL, flags | O_NONBLOCK) != 0) throw_errno("fcntl(O_NONBLOCK)");
}
inline void set_cloexec(int fd) { ::fcntl(fd, F_SETFD, FD_CLOEXEC); }
inline sockaddr_in to_sockaddr(const Address& a) {
    sockaddr_in sa{};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(a.port);
    if (::inet_pton(AF_INET, a.host.c_str(), &sa.sin_addr) != 1) throw std::invalid_argument("not an IPv4 address: " + a.host);
    return sa;
}
inline Address from_sockaddr(const sockaddr_in& sa) {
    char buf[INET_ADDRSTRLEN] = {};
    ::inet_ntop(AF_INET, &sa.sin_addr, buf, sizeof buf);
    return Address{buf, ntohs(sa.sin_port)};
}
/// A self-pipe: writing one byte to `write_end` makes poll() on `read_end` return.  It is how another thread wakes the I/O thread
/// (Java: Selector.wakeup()).  A pipe, not eventfd: portable to macOS.
struct WakePipe {
    UniqueFd read_end, write_end;
    WakePipe() {
        int fds[2];
        if (::pipe(fds) != 0) throw_errno("pipe");
        read_end.reset(fds[0]);
        write_end.reset(fds[1]);
        for (int fd : fds) { set_nonblocking(fd); set_cloexec(fd); }
    }
    void wake() const {
        const char b = 1;
        [[maybe_unused]] const auto rc = ::write(write_end.get(), &b, 1);  // EAGAIN = pipe already full of wake-ups: fine
    }
    void drain() const {
        char buf[64];
        while (::read(read_end.get(), buf, sizeof buf) > 0) {}
    }
};
#ifdef MSG_NOSIGNAL
inline constexpr int kSendFlags = MSG_NOSIGNAL;  // a write to a reset connection returns EPIPE instead of killing the process with SIGPIPE
#else
inline constexpr int kSendFlags = 0;  // macOS: SO_NOSIGPIPE is set on the socket instead
#endif
}  // namespace detail

// ================================================================================================ To write
// Everything above is given.  Below, the signatures and what each must do; the full rules are in ../problem.md.

// ============================================================================================ Part 1
/// Bounded byte ring (single-threaded, ANY positive capacity - not a power of two), so index = (head + offset) % capacity.
/// write / read take as much as fit and return the count (the caller advances its own cursor); data that wraps around the end of the array is
/// copied in TWO pieces.  write_all is all-or-nothing.  peek_int: big-endian int32 at `offset` from the head, not consumed, fewer than 4 bytes
/// there -> StateError.  take / skip with more than size() bytes -> StateError and nothing changes - check BEFORE allocating n bytes
/// (take(static_cast<std::size_t>(-1)) must throw, not try to allocate 2^64).  capacity 0 -> std::invalid_argument.
class ByteRing {
public:
    explicit ByteRing(std::size_t) { throw std::logic_error("TODO"); }
    std::size_t capacity() const { throw std::logic_error("TODO"); }
    std::size_t size() const { throw std::logic_error("TODO"); }
    std::size_t free() const { throw std::logic_error("TODO"); }
    bool is_empty() const { throw std::logic_error("TODO"); }
    std::size_t write(std::span<const std::uint8_t>) { throw std::logic_error("TODO"); }
    std::size_t read(std::span<std::uint8_t>) { throw std::logic_error("TODO"); }
    bool write_all(std::span<const std::uint8_t>) { throw std::logic_error("TODO"); }
    std::int32_t peek_int(std::size_t = 0) const { throw std::logic_error("TODO"); }
    Bytes take(std::size_t) { throw std::logic_error("TODO"); }
    void skip(std::size_t) { throw std::logic_error("TODO"); }
    void clear() { throw std::logic_error("TODO"); }
};

/// Frame = [len: int32 big-endian][payload].  encode: no room -> false and the ring is unchanged (never half a header); payload longer than
/// max_frame -> std::invalid_argument; empty payload is legal.
struct FrameCodec {
    static constexpr int HEADER = 4;
    static bool encode(ByteRing&, std::span<const std::uint8_t>, int) { throw std::logic_error("TODO"); }
};

/// Incremental decoder over an owned ByteRing.  capacity < max_frame + 4 -> std::invalid_argument.  feed takes only what fits (returns the count);
/// next() returns a whole frame or nullopt; an invalid header (len < 0 or > max_frame) is detected from the 4 header bytes ALONE and throws
/// FrameException - sticky: every later next() throws too.  has_frame() = next() would return a message or throw.  has_truncated_tail() = an
/// incomplete frame follows the complete ones (an invalid header does not count as truncated).
class FrameDecoder {
public:
    FrameDecoder(int, int) { throw std::logic_error("TODO"); }
    std::size_t feed(std::span<const std::uint8_t>) { throw std::logic_error("TODO"); }
    std::optional<Bytes> next() { throw std::logic_error("TODO"); }
    bool has_frame() const { throw std::logic_error("TODO"); }
    std::size_t buffered() const { throw std::logic_error("TODO"); }
    std::size_t free() const { throw std::logic_error("TODO"); }
    bool has_truncated_tail() const { throw std::logic_error("TODO"); }
};

// ============================================================================================ Parts 2 + 3
/// A bounded message channel over one TCP connection.
///  * ONE I/O thread running a poll(2) loop over [socket, detail::WakePipe]; application threads only touch two bounded buffers (the out ByteRing
///    with encoded frames, the in FrameDecoder) under one mutex, and never make a system call themselves (except the wake-up write).
///  * offer: never blocks; StateError when closed / finish_sending() called / failed; std::invalid_argument when longer than max_frame; false when
///    the frame does not fit.  offer(msg, timeout) waits on a condition variable until it fits.  Wake the I/O thread when the out ring was empty.
///  * partial writes: keep the unsent remainder of the staging buffer (wbuf) and its position, wait for POLLOUT.  Partial reads: feed the decoder;
///    poll() returns only whole frames, still returns buffered ones after close; a bad header -> poll throws FrameException and the channel fails.
///  * back-pressure in: in ring full -> do NOT ask for POLLIN; poll() / poll(timeout) must wake the I/O thread when they free room.
///  * recv() == 0 (EOF) is not close(): is_peer_closed(), you can still poll the rest and still offer.  EOF in the middle of a frame -> failure() is
///    EofError, channel closed, earlier complete frames stay pollable.
///  * finish_sending(): flush, shutdown(SHUT_WR); once the peer is done too the channel closes with failure() == null.  close(): immediately, drop
///    unsent data, wake blocked callers, idempotent, join the I/O thread.  TCP_NODELAY on.  Never SIGPIPE (see detail::kSendFlags).
///  * failure() is a std::exception_ptr (inspect with std::rethrow_exception in a try / catch).
class TcpMessageChannel {
public:
    static std::unique_ptr<TcpMessageChannel> connect(const Address&, const ChannelConfig&, Millis = Millis(3000)) { throw std::logic_error("TODO"); }
    static std::unique_ptr<TcpMessageChannel> wrap(UniqueFd, const ChannelConfig&) { throw std::logic_error("TODO"); }
    TcpMessageChannel(const TcpMessageChannel&) = delete;
    TcpMessageChannel& operator=(const TcpMessageChannel&) = delete;
    ~TcpMessageChannel() = default;

    bool offer(std::span<const std::uint8_t>) { throw std::logic_error("TODO"); }
    bool offer(std::span<const std::uint8_t>, Millis) { throw std::logic_error("TODO"); }
    std::optional<Bytes> poll() { throw std::logic_error("TODO"); }
    std::optional<Bytes> poll(Millis) { throw std::logic_error("TODO"); }
    void finish_sending() { throw std::logic_error("TODO"); }
    void close() { throw std::logic_error("TODO"); }
    bool is_open() const { throw std::logic_error("TODO"); }
    bool is_peer_closed() const { throw std::logic_error("TODO"); }
    bool is_drained() const { throw std::logic_error("TODO"); }
    std::exception_ptr failure() const { throw std::logic_error("TODO"); }
    std::size_t unsent_bytes() const { throw std::logic_error("TODO"); }
    bool await_closed(Millis) { throw std::logic_error("TODO"); }
    Address local_address() const { throw std::logic_error("TODO"); }
    Address remote_address() const { throw std::logic_error("TODO"); }

private:
    TcpMessageChannel() = default;
};

/// Listens on 127.0.0.1 (port 0 = ephemeral), SO_REUSEADDR (a restarted server may reuse the port), one accept thread that poll()s
/// [listening socket, wake pipe]; every connection becomes a TcpMessageChannel::wrap and is queued for accept(timeout) (null on timeout).
/// close(): stop the thread, close connections nobody picked up.  Idempotent.
class MessageServer {
public:
    MessageServer(std::uint16_t, const ChannelConfig&) { throw std::logic_error("TODO"); }
    MessageServer(const MessageServer&) = delete;
    MessageServer& operator=(const MessageServer&) = delete;
    std::uint16_t port() const { throw std::logic_error("TODO"); }
    Address address() const { throw std::logic_error("TODO"); }
    std::unique_ptr<TcpMessageChannel> accept(Millis) { throw std::logic_error("TODO"); }
    void close() { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 4
/// next() = initial, initial*m, initial*m^2 ... capped at max, never overflowing (compare against max / multiplier BEFORE multiplying);
/// reset() starts over; next(rng) = full jitter, uniform in [0, next()].  initial <= 0, max < initial, multiplier < 1 -> std::invalid_argument.
class Backoff {
public:
    Backoff(long long, long long, int) { throw std::logic_error("TODO"); }
    long long next() { throw std::logic_error("TODO"); }
    template <std::uniform_random_bit_generator G> long long next(G&) { throw std::logic_error("TODO"); }
    void reset() { throw std::logic_error("TODO"); }
};

/// Background manager thread: connect -> move `pending` into the channel in order -> channel dead (!is_open() or is_peer_closed()) -> drop it,
/// back off, reconnect; a successful connect resets the backoff.  offer(): always into the bounded pending queue first (bytes 4 + len summed,
/// limit cfg.out_capacity(); false when full; after close() StateError; longer than max_frame std::invalid_argument).  Messages already handed to
/// the dead channel may be lost: count them in abandoned_bytes() (at-most-once, best effort).  poll() = the current channel's poll, nullopt while
/// disconnected (hold a shared_ptr copy of the channel while using it).  close(): close the channel, interrupt the sleep, no more reconnects.
class ReconnectingClient {
public:
    ReconnectingClient(const Address&, const ChannelConfig&, Backoff) { throw std::logic_error("TODO"); }
    ReconnectingClient(const ReconnectingClient&) = delete;
    ReconnectingClient& operator=(const ReconnectingClient&) = delete;
    bool offer(std::span<const std::uint8_t>) { throw std::logic_error("TODO"); }
    std::optional<Bytes> poll() { throw std::logic_error("TODO"); }
    bool is_connected() const { throw std::logic_error("TODO"); }
    int connect_count() const { throw std::logic_error("TODO"); }
    int failed_attempts() const { throw std::logic_error("TODO"); }
    long long abandoned_bytes() const { throw std::logic_error("TODO"); }
    std::size_t pending_bytes() const { throw std::logic_error("TODO"); }
    void close() { throw std::logic_error("TODO"); }
};

}  // namespace net
