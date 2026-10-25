// ld03 · Asynchronous TCP message channel — C++20 reference.  Statement: ../problem.md.
// Parts: 1 ByteRing + FrameCodec + FrameDecoder (pure memory)  2+3 TcpMessageChannel + MessageServer (poll(2) event loop, back-pressure)
//        4 Backoff + ReconnectingClient.  Real sockets on 127.0.0.1; POSIX only (poll, pipe, fcntl), no epoll / kqueue.
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

// ============================================================================================ Part 1
/// Bounded byte ring buffer (not thread-safe, any positive capacity).  Unlike ld01 this one is single-threaded (the caller holds a lock):
/// it only has to deal with PARTIAL writes / reads and with copying in two pieces when the data wraps around the end of the array.
class ByteRing {
public:
    explicit ByteRing(std::size_t capacity) : buf_(check(capacity)) {}

    std::size_t capacity() const { return buf_.size(); }
    std::size_t size() const { return size_; }
    std::size_t free() const { return buf_.size() - size_; }
    bool is_empty() const { return size_ == 0; }

    /// Write as much as fits; returns the number of bytes taken (the caller advances its own cursor by that much).
    std::size_t write(std::span<const std::uint8_t> src) {
        const std::size_t n = std::min(src.size(), free());
        const std::size_t tail = (head_ + size_) % buf_.size();
        const std::size_t first = std::min(n, buf_.size() - tail);
        if (first != 0) std::memcpy(buf_.data() + tail, src.data(), first);
        if (n > first) std::memcpy(buf_.data(), src.data() + first, n - first);  // wrapped: the second piece goes to the start of the array
        size_ += n;
        return n;
    }
    /// Read as much as dst can hold; returns the number of bytes produced.
    std::size_t read(std::span<std::uint8_t> dst) {
        const std::size_t n = std::min(dst.size(), size_);
        const std::size_t first = std::min(n, buf_.size() - head_);
        if (first != 0) std::memcpy(dst.data(), buf_.data() + head_, first);
        if (n > first) std::memcpy(dst.data() + first, buf_.data(), n - first);
        head_ = (head_ + n) % buf_.size();
        size_ -= n;
        return n;
    }
    /// All or nothing: it fits entirely, or not a single byte is written.
    bool write_all(std::span<const std::uint8_t> src) {
        if (src.size() > free()) return false;
        write(src);
        return true;
    }
    /// Big-endian int32 at `offset` from the head, not consumed.  Fewer than 4 bytes there -> StateError.
    std::int32_t peek_int(std::size_t offset = 0) const {
        if (size_ < 4 || offset > size_ - 4) throw StateError("fewer than 4 bytes at offset " + std::to_string(offset));
        std::uint32_t v = 0;
        for (std::size_t i = 0; i < 4; ++i) v = v << 8 | buf_[(head_ + offset + i) % buf_.size()];
        return static_cast<std::int32_t>(v);
    }
    /// Remove and return n bytes.  Fewer buffered -> StateError, state unchanged (and nothing is allocated: check BEFORE you allocate n bytes).
    Bytes take(std::size_t n) {
        require(n);
        Bytes out(n);
        read(out);
        return out;
    }
    void skip(std::size_t n) {
        require(n);
        head_ = (head_ + n) % buf_.size();
        size_ -= n;
    }
    void clear() { head_ = size_ = 0; }

private:
    static std::size_t check(std::size_t capacity) {
        if (capacity == 0) throw std::invalid_argument("capacity must be > 0");
        return capacity;
    }
    void require(std::size_t n) const {
        if (n > size_) throw StateError("only " + std::to_string(size_) + " bytes buffered, wanted " + std::to_string(n));
    }
    std::vector<std::uint8_t> buf_;
    std::size_t head_ = 0, size_ = 0;
};

/// Frame = [len: int32 big-endian][payload: len bytes].  TCP is a byte stream: message boundaries have to travel with the data.
struct FrameCodec {
    static constexpr int HEADER = 4;

    /// Encode one message into `out`.  No room -> false and `out` is unchanged (never half a header).  Payload longer than max_frame ->
    /// std::invalid_argument.  Empty payload is legal.
    static bool encode(ByteRing& out, std::span<const std::uint8_t> payload, int max_frame) {
        if (payload.size() > static_cast<std::size_t>(max_frame)) throw std::invalid_argument("payload " + std::to_string(payload.size()) + " > max_frame " + std::to_string(max_frame));
        if (out.free() < HEADER + payload.size()) return false;
        const auto n = static_cast<std::uint32_t>(payload.size());
        const std::uint8_t header[HEADER] = {static_cast<std::uint8_t>(n >> 24), static_cast<std::uint8_t>(n >> 16), static_cast<std::uint8_t>(n >> 8), static_cast<std::uint8_t>(n)};
        out.write_all(header);
        out.write_all(payload);
        return true;
    }
};

/// Incremental decoder.  Bytes arrive in chunks of any size (1 byte, half a header, two and a half messages ...); next() returns only
/// whole frames.  Bounded: it owns a `capacity`-byte ring, feed() takes only what fits and the caller must next() before feeding more -
/// that IS the inbound back-pressure.  An invalid header (< 0 or > max_frame) throws FrameException and the decoder is failed for good.
class FrameDecoder {
public:
    FrameDecoder(int max_frame, int capacity) : ring_(check(max_frame, capacity)), max_frame_(max_frame) {}

    /// Number of bytes consumed from `src` (may be less than src.size() when the ring is full).
    std::size_t feed(std::span<const std::uint8_t> src) { return ring_.write(src); }

    /// The next whole message, or nullopt.  The header alone decides: do not wait for `len` bytes to arrive before rejecting a bad length.
    std::optional<Bytes> next() {
        if (failed_) throw *failed_;
        if (ring_.size() < FrameCodec::HEADER) return std::nullopt;
        const std::int32_t len = ring_.peek_int();
        if (len < 0 || len > max_frame_) {
            failed_ = FrameException("bad frame length " + std::to_string(len) + " (max_frame " + std::to_string(max_frame_) + ")");
            throw *failed_;
        }
        if (ring_.size() < FrameCodec::HEADER + static_cast<std::size_t>(len)) return std::nullopt;
        ring_.skip(FrameCodec::HEADER);
        return ring_.take(static_cast<std::size_t>(len));
    }
    /// Would next() return a message (or throw)?  Does not consume.
    bool has_frame() const {
        if (failed_) return true;
        if (ring_.size() < FrameCodec::HEADER) return false;
        const std::int32_t len = ring_.peek_int();
        if (len < 0 || len > max_frame_) return true;
        return ring_.size() >= FrameCodec::HEADER + static_cast<std::size_t>(len);
    }
    std::size_t buffered() const { return ring_.size(); }
    std::size_t free() const { return ring_.free(); }
    /// Is there an incomplete frame after the complete ones?  (When the peer closes: "was the stream cut in the middle?"  An invalid
    /// header is reported by next(), it does not count as truncation.)
    bool has_truncated_tail() const {
        std::size_t pos = 0;
        while (pos < ring_.size()) {
            if (ring_.size() - pos < FrameCodec::HEADER) return true;
            const std::int32_t len = ring_.peek_int(pos);
            if (len < 0 || len > max_frame_) return false;
            if (ring_.size() - pos < FrameCodec::HEADER + static_cast<std::size_t>(len)) return true;
            pos += FrameCodec::HEADER + static_cast<std::size_t>(len);
        }
        return false;
    }

private:
    static std::size_t check(int max_frame, int capacity) {
        if (max_frame < 0) throw std::invalid_argument("max_frame < 0");
        if (capacity < max_frame + FrameCodec::HEADER) throw std::invalid_argument("capacity must be >= max_frame + 4");
        return static_cast<std::size_t>(capacity);
    }
    ByteRing ring_;
    int max_frame_;
    std::optional<FrameException> failed_;
};

// ============================================================================================ Part 2 + 3


/// A bounded message channel over one TCP connection.
///
///   application threads                       I/O thread (one poll() loop)
///   offer(msg) -encode-> [out ring] -read-> wbuf -send()-> socket -> network
///   poll()    <-decode-  [in  ring] <-feed- rbuf <-recv()- socket <- network
///
///  * offer never blocks: no room for one whole frame -> false (back-pressure goes to the caller).  Accepted messages are written in order
///    unless the connection fails.
///  * inbound back-pressure: in ring full -> the I/O thread stops asking for POLLIN, the kernel receive buffer fills, the TCP window closes,
///    the peer's send() stops.  poll() frees space and MUST wake the I/O thread.
///  * partial I/O: send() may take only part of wbuf (the rest waits for POLLOUT), recv() may return half a message (it waits in the in ring).
///  * peer closed (EOF) != closed here: after EOF you can still poll() the remaining messages and still offer (half-close); is_drained() = no more
///    messages will ever come.  finish_sending(): refuse offers, flush, send FIN; when both sides are done the channel closes.  close(): now.
/// All mutable state is guarded by one mutex (critical sections only copy memory); every system call happens outside it, on the I/O thread.
class TcpMessageChannel {
public:
    /// Connect (non-blocking connect + poll, at most `timeout`).  Failure -> std::system_error.
    static std::unique_ptr<TcpMessageChannel> connect(const Address& addr, const ChannelConfig& cfg, Millis timeout = Millis(3000)) {
        UniqueFd fd(::socket(AF_INET, SOCK_STREAM, 0));
        if (!fd) throw_errno("socket");
        detail::set_nonblocking(fd.get());
        const sockaddr_in sa = detail::to_sockaddr(addr);
        if (::connect(fd.get(), reinterpret_cast<const sockaddr*>(&sa), sizeof sa) != 0) {
            if (errno != EINPROGRESS) throw_errno("connect");
            pollfd p{fd.get(), POLLOUT, 0};
            int rc;
            do { rc = ::poll(&p, 1, static_cast<int>(timeout.count())); } while (rc < 0 && errno == EINTR);
            if (rc == 0) throw_errno("connect (timeout)", ETIMEDOUT);
            if (rc < 0) throw_errno("poll");
            int err = 0;
            socklen_t len = sizeof err;
            ::getsockopt(fd.get(), SOL_SOCKET, SO_ERROR, &err, &len);
            if (err != 0) throw_errno("connect", err);
        }
        return wrap(std::move(fd), cfg);
    }

    /// Take over an already connected socket (accepted by the server, or tuned by a test).  The channel owns it from here on.
    static std::unique_ptr<TcpMessageChannel> wrap(UniqueFd connected, const ChannelConfig& cfg) {
        return std::unique_ptr<TcpMessageChannel>(new TcpMessageChannel(std::move(connected), cfg));
    }

    TcpMessageChannel(const TcpMessageChannel&) = delete;
    TcpMessageChannel& operator=(const TcpMessageChannel&) = delete;
    ~TcpMessageChannel() { close(); }  // the thread must be gone before the members it uses are destroyed

    // ---- application threads --------------------------------------------------------------------------------
    /// true = in the outbound buffer; false = buffer full (retry later: that is the back-pressure).
    /// Message longer than max_frame -> std::invalid_argument.  Closed / finish_sending() called -> StateError.
    bool offer(std::span<const std::uint8_t> msg) {
        bool was_empty;
        {
            std::lock_guard lk(m_);
            require_sendable();
            was_empty = out_.is_empty();
            if (!FrameCodec::encode(out_, msg, cfg_.max_frame())) return false;
        }
        if (was_empty) wake_.wake();  // if out_ was not empty the I/O thread is already waiting for POLLOUT
        return true;
    }
    /// Wait up to `timeout` until the frame fits.
    bool offer(std::span<const std::uint8_t> msg, Millis timeout) {
        const auto deadline = std::chrono::steady_clock::now() + timeout;
        std::unique_lock lk(m_);
        for (;;) {
            require_sendable();
            const bool was_empty = out_.is_empty();
            if (FrameCodec::encode(out_, msg, cfg_.max_frame())) {
                lk.unlock();
                if (was_empty) wake_.wake();
                return true;
            }
            if (changed_.wait_until(lk, deadline) == std::cv_status::timeout) {
                require_sendable();
                if (FrameCodec::encode(out_, msg, cfg_.max_frame())) { lk.unlock(); wake_.wake(); return true; }
                return false;
            }
        }
    }

    /// The next complete message, or nullopt.  Messages already buffered stay available after the channel closed.
    /// A bad frame header -> FrameException (and the channel fails).
    std::optional<Bytes> poll() {
        std::optional<Bytes> m;
        bool wake = false;
        {
            std::lock_guard lk(m_);
            m = next_locked();
            if (m && read_paused_) { read_paused_ = false; wake = true; }
        }
        if (wake) wake_.wake();  // the reader was paused because the in ring was full: it can run again
        return m;
    }
    /// Wait until there is a message, or no message can ever come (drained), or the timeout.
    std::optional<Bytes> poll(Millis timeout) {
        const auto deadline = std::chrono::steady_clock::now() + timeout;
        std::optional<Bytes> m;
        bool wake = false;
        {
            std::unique_lock lk(m_);
            for (;;) {
                m = next_locked();
                if (m || inbound_finished_locked()) break;
                if (changed_.wait_until(lk, deadline) == std::cv_status::timeout) { m = next_locked(); break; }
            }
            if (m && read_paused_) { read_paused_ = false; wake = true; }
        }
        if (wake) wake_.wake();
        return m;
    }

    /// No more offers; after everything accepted is flushed, send FIN.  When the peer is done too, the channel closes.
    void finish_sending() {
        {
            std::lock_guard lk(m_);
            if (state_ == State::Open) state_ = State::Finishing;
        }
        wake_.wake();
    }
    /// Close now, dropping unsent data.  Idempotent; wakes every thread blocked in poll(timeout) / offer(msg, timeout) / await_closed.
    void close() {
        {
            std::lock_guard lk(m_);
            state_ = State::Closed;
            changed_.notify_all();
        }
        wake_.wake();
        std::call_once(joined_, [this] {
            if (io_thread_.joinable() && io_thread_.get_id() != std::this_thread::get_id()) io_thread_.join();
        });
    }

    bool is_open() const { std::lock_guard lk(m_); return state_ != State::Closed; }
    bool is_peer_closed() const { std::lock_guard lk(m_); return peer_closed_; }
    /// No new message will arrive (peer closed, or we closed) and no complete message is buffered.
    bool is_drained() const { std::lock_guard lk(m_); return inbound_finished_locked() && !in_.has_frame(); }
    /// Why the channel closed abnormally (FrameException, EofError, system_error ...); null for a normal close or while open.
    /// Inspect it with std::rethrow_exception in a try / catch.
    std::exception_ptr failure() const { std::lock_guard lk(m_); return failure_; }
    /// Bytes accepted by offer() but not yet handed to the kernel (out ring + the part of wbuf not yet sent).
    std::size_t unsent_bytes() const { std::lock_guard lk(m_); return out_.size() + (wlen_ - wpos_); }
    bool await_closed(Millis timeout) {
        std::unique_lock lk(m_);
        return changed_.wait_for(lk, timeout, [this] { return state_ == State::Closed; });
    }
    /// Local / remote address.  A closed channel has no socket any more -> StateError.
    Address local_address() const { return address_of(::getsockname); }
    Address remote_address() const { return address_of(::getpeername); }

private:
    enum class State { Open, Finishing, Closed };
    static constexpr std::size_t kIoBuf = 16 * 1024;

    TcpMessageChannel(UniqueFd sock, const ChannelConfig& cfg)
        : fd_(std::move(sock)), cfg_(cfg), out_(static_cast<std::size_t>(cfg.out_capacity())), in_(cfg.max_frame(), cfg.in_capacity()),
          wbuf_(kIoBuf), rbuf_(kIoBuf) {
        detail::set_nonblocking(fd_.get());
        const int one = 1;
        if (::setsockopt(fd_.get(), IPPROTO_TCP, TCP_NODELAY, &one, sizeof one) != 0) throw_errno("TCP_NODELAY");  // small messages must not wait for Nagle
#ifdef SO_NOSIGPIPE
        ::setsockopt(fd_.get(), SOL_SOCKET, SO_NOSIGPIPE, &one, sizeof one);
#endif
        io_thread_ = std::jthread([this] { io_loop(); });  // last: everything the thread uses is constructed
    }

    // ---- under the lock ---------------------------------------------------------------------------------------
    std::optional<Bytes> next_locked() {
        try {
            return in_.next();
        } catch (const FrameException&) {
            fail_locked(std::current_exception());
            throw;
        }
    }
    bool inbound_finished_locked() const { return peer_closed_ || state_ == State::Closed; }
    void require_sendable() const {
        if (state_ == State::Open) return;
        throw StateError(state_ == State::Finishing ? "finish_sending() was called" : "channel closed");
    }
    void fail_locked(std::exception_ptr e) {
        if (!failure_) failure_ = std::move(e);
        state_ = State::Closed;
        changed_.notify_all();
    }
    template <class F> Address address_of(F getname) const {
        std::lock_guard lk(m_);
        if (!fd_) throw StateError("channel closed");
        sockaddr_in sa{};
        socklen_t len = sizeof sa;
        if (getname(fd_.get(), reinterpret_cast<sockaddr*>(&sa), &len) != 0) throw_errno("getsockname/getpeername");
        return detail::from_sockaddr(sa);
    }

    // ---- the I/O thread ---------------------------------------------------------------------------------------
    void io_loop() {
        try {
            for (;;) {
                short events = 0;
                {
                    std::lock_guard lk(m_);
                    if (state_ == State::Closed) break;
                    if (state_ == State::Finishing && !fin_sent_ && out_.is_empty() && wpos_ == wlen_) {
                        ::shutdown(fd_.get(), SHUT_WR);  // FIN: the peer's recv() returns 0
                        fin_sent_ = true;
                    }
                    if (fin_sent_ && peer_closed_) { state_ = State::Closed; changed_.notify_all(); break; }
                    read_paused_ = !peer_closed_ && in_.free() == 0;
                    if (!peer_closed_ && in_.free() > 0) events |= POLLIN;
                    if (!fin_sent_ && (wpos_ < wlen_ || !out_.is_empty())) events |= POLLOUT;
                }
                pollfd fds[2] = {{wake_.read_end.get(), POLLIN, 0}, {fd_.get(), events, 0}};
                // events == 0: leave the socket out entirely (POLLHUP would be reported even with no interest and the loop would spin)
                const int rc = ::poll(fds, events != 0 ? 2 : 1, -1);
                if (rc < 0) {
                    if (errno == EINTR) continue;
                    throw_errno("poll");
                }
                if (fds[0].revents != 0) wake_.drain();
                const short rev = events != 0 ? fds[1].revents : short{0};
                if ((events & POLLIN) && (rev & (POLLIN | POLLHUP | POLLERR))) do_read();
                if ((events & POLLOUT) && (rev & (POLLOUT | POLLHUP | POLLERR))) do_write();
            }
        } catch (...) {
            std::lock_guard lk(m_);
            fail_locked(std::current_exception());
        }
        std::lock_guard lk(m_);
        fd_.reset();  // the peer sees EOF / RST now, not when this object is destroyed
        state_ = State::Closed;
        changed_.notify_all();
    }

    void do_read() {
        std::size_t room;
        {
            std::lock_guard lk(m_);
            room = in_.free();
        }
        if (room == 0) return;
        const ssize_t n = ::recv(fd_.get(), rbuf_.data(), std::min(rbuf_.size(), room), 0);
        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR) return;
            throw_errno("recv");
        }
        std::lock_guard lk(m_);
        if (n == 0) {
            peer_closed_ = true;
            if (in_.has_truncated_tail())
                fail_locked(std::make_exception_ptr(EofError("peer closed in the middle of a frame (" + std::to_string(in_.buffered()) + " bytes buffered)")));
        } else {
            in_.feed(std::span<const std::uint8_t>(rbuf_.data(), static_cast<std::size_t>(n)));  // room >= n: it all fits
        }
        changed_.notify_all();
    }

    void do_write() {
        for (int round = 0; round < 16; ++round) {  // bounded per wake-up so that reading is not starved
            const std::uint8_t* from;
            std::size_t count;
            {
                std::lock_guard lk(m_);
                if (wpos_ == wlen_) {  // wbuf is empty: refill it from the out ring
                    wlen_ = out_.read(wbuf_);
                    wpos_ = 0;
                    changed_.notify_all();  // the ring has room again: wake offer(msg, timeout)
                    if (wlen_ == 0) return;
                }
                from = wbuf_.data() + wpos_;
                count = wlen_ - wpos_;
            }
            const ssize_t n = ::send(fd_.get(), from, count, detail::kSendFlags);
            if (n < 0) {
                if (errno == EAGAIN || errno == EWOULDBLOCK) return;  // kernel buffer full: the rest waits for the next POLLOUT
                if (errno == EINTR) continue;
                throw_errno("send");
            }
            {
                std::lock_guard lk(m_);
                wpos_ += static_cast<std::size_t>(n);
            }
            if (n == 0) return;
        }
    }

    UniqueFd fd_;
    detail::WakePipe wake_;
    ChannelConfig cfg_;
    mutable std::mutex m_;
    std::condition_variable changed_;
    ByteRing out_;
    FrameDecoder in_;
    std::vector<std::uint8_t> wbuf_, rbuf_;
    std::size_t wpos_ = 0, wlen_ = 0;  // wbuf_[wpos_, wlen_) is encoded data waiting for the kernel
    State state_ = State::Open;
    bool peer_closed_ = false, fin_sent_ = false, read_paused_ = false;
    std::exception_ptr failure_;
    std::once_flag joined_;
    std::jthread io_thread_;  // declared last: destroyed (joined) first
};

/// Listens on 127.0.0.1:port (0 = an ephemeral port chosen by the kernel) and wraps every new connection into a TcpMessageChannel that
/// accept() hands out.  One accept thread; poll() on [listening socket, wake pipe] so that close() can end it without relying on
/// close()-ing an fd another thread is blocked on.
class MessageServer {
public:
    MessageServer(std::uint16_t port, const ChannelConfig& cfg) : cfg_(cfg) {
        listen_.reset(::socket(AF_INET, SOCK_STREAM, 0));
        if (!listen_) throw_errno("socket");
        const int one = 1;
        ::setsockopt(listen_.get(), SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);  // a restarted server can reuse the port while old connections linger in TIME_WAIT
        const sockaddr_in sa = detail::to_sockaddr(loopback(port));
        if (::bind(listen_.get(), reinterpret_cast<const sockaddr*>(&sa), sizeof sa) != 0) throw_errno("bind");
        if (::listen(listen_.get(), 128) != 0) throw_errno("listen");
        detail::set_nonblocking(listen_.get());
        sockaddr_in bound{};
        socklen_t len = sizeof bound;
        ::getsockname(listen_.get(), reinterpret_cast<sockaddr*>(&bound), &len);
        address_ = detail::from_sockaddr(bound);
        thread_ = std::jthread([this] { accept_loop(); });
    }
    MessageServer(const MessageServer&) = delete;
    MessageServer& operator=(const MessageServer&) = delete;
    ~MessageServer() { close(); }

    std::uint16_t port() const { return address_.port; }
    Address address() const { return address_; }

    /// The next connection, or null on timeout.
    std::unique_ptr<TcpMessageChannel> accept(Millis timeout) {
        std::unique_lock lk(m_);
        if (!cv_.wait_for(lk, timeout, [this] { return !accepted_.empty(); })) return nullptr;
        auto c = std::move(accepted_.front());
        accepted_.pop_front();
        return c;
    }

    void close() {
        closed_ = true;
        wake_.wake();
        std::call_once(joined_, [this] { if (thread_.joinable()) thread_.join(); });
        std::lock_guard lk(m_);
        for (auto& c : accepted_) c->close();  // connections nobody picked up are closed too
        accepted_.clear();
        listen_.reset();
    }

private:
    void accept_loop() {
        while (!closed_) {
            pollfd fds[2] = {{wake_.read_end.get(), POLLIN, 0}, {listen_.get(), POLLIN, 0}};
            if (::poll(fds, 2, -1) < 0 && errno != EINTR) return;
            if (closed_) return;
            if (!(fds[1].revents & POLLIN)) continue;
            const int cfd = ::accept(listen_.get(), nullptr, nullptr);
            if (cfd < 0) continue;  // EAGAIN (the client gave up) etc.: look again
            UniqueFd sock(cfd);
            try {
                auto channel = TcpMessageChannel::wrap(std::move(sock), cfg_);
                std::lock_guard lk(m_);
                accepted_.push_back(std::move(channel));
                cv_.notify_one();
            } catch (...) {  // could not set up this connection: the UniqueFd already closed it
            }
        }
    }

    ChannelConfig cfg_;
    UniqueFd listen_;
    detail::WakePipe wake_;
    Address address_;
    std::mutex m_;
    std::condition_variable cv_;
    std::deque<std::unique_ptr<TcpMessageChannel>> accepted_;
    std::atomic<bool> closed_{false};
    std::once_flag joined_;
    std::jthread thread_;
};

// ============================================================================================ Part 4
/// Exponential backoff: next() returns initial, initial*m, initial*m^2 ... capped at max; reset() starts over.  next(rng) is "full jitter":
/// uniform in [0, the current cap], so that many clients do not reconnect in the same instant (thundering herd).
class Backoff {
public:
    Backoff(long long initial_ms, long long max_ms, int multiplier) : initial_(initial_ms), max_(max_ms), multiplier_(multiplier), current_(initial_ms) {
        if (initial_ms <= 0) throw std::invalid_argument("initial_ms must be > 0");
        if (max_ms < initial_ms) throw std::invalid_argument("max_ms must be >= initial_ms");
        if (multiplier < 1) throw std::invalid_argument("multiplier must be >= 1");
    }
    /// How long to wait this time; the following delay is multiplied (capped; the multiplication cannot overflow).
    long long next() {
        const long long d = current_;
        current_ = current_ > max_ / multiplier_ ? max_ : std::min(max_, current_ * multiplier_);
        return d;
    }
    /// Full jitter: uniform in [0, next()], both ends included.
    template <std::uniform_random_bit_generator G> long long next(G& rng) {
        const long long cap = next();
        return std::uniform_int_distribution<long long>(0, cap)(rng);
    }
    void reset() { current_ = initial_; }

private:
    long long initial_, max_;
    int multiplier_;
    long long current_;
};

/// A client that reconnects by itself.
///   offer(msg) -> [pending queue, bounded] -> manager thread -> current TcpMessageChannel -> network
/// While disconnected offer() still succeeds (until the queue is full) and the messages go out in order after the reconnect.  What was
/// already handed to the old channel (its out ring or the kernel buffers) when the connection broke MAY BE LOST: TCP guarantees order and
/// delivery only while a connection lives, not that the peer application processed it.  Not losing messages needs application-level
/// sequence numbers + acks + retransmission (at-least-once + de-duplication).  This class is at-most-once, best effort; the lost bytes are
/// counted in abandoned_bytes().  Unpolled inbound messages of the old connection are dropped.
class ReconnectingClient {
public:
    ReconnectingClient(const Address& addr, const ChannelConfig& cfg, Backoff backoff) : addr_(addr), cfg_(cfg), backoff_(backoff) {
        manager_ = std::jthread([this] { run(); });
    }
    ReconnectingClient(const ReconnectingClient&) = delete;
    ReconnectingClient& operator=(const ReconnectingClient&) = delete;
    ~ReconnectingClient() { close(); }

    /// true = accepted (queued); false = pending queue full (bytes counted as 4 + len, the same unit as the out ring).
    /// Longer than max_frame -> std::invalid_argument; after close() -> StateError.
    bool offer(std::span<const std::uint8_t> msg) {
        if (msg.size() > static_cast<std::size_t>(cfg_.max_frame())) throw std::invalid_argument("message larger than max_frame");
        const std::size_t framed = FrameCodec::HEADER + msg.size();
        std::lock_guard lk(m_);
        if (closed_) throw StateError("client closed");
        if (pending_bytes_ + framed > static_cast<std::size_t>(cfg_.out_capacity())) return false;
        pending_.emplace_back(msg.begin(), msg.end());
        pending_bytes_ += framed;
        wake_.notify_all();
        return true;
    }
    /// The next inbound message of the current connection; nullopt while disconnected.
    std::optional<Bytes> poll() {
        std::shared_ptr<TcpMessageChannel> c;
        {
            std::lock_guard lk(m_);
            c = current_;  // a shared_ptr copy: the channel cannot be destroyed under us even if the manager drops it meanwhile
        }
        return c ? c->poll() : std::nullopt;
    }
    bool is_connected() const { std::lock_guard lk(m_); return current_ != nullptr; }
    int connect_count() const { std::lock_guard lk(m_); return connect_count_; }
    int failed_attempts() const { std::lock_guard lk(m_); return failed_attempts_; }
    long long abandoned_bytes() const { std::lock_guard lk(m_); return abandoned_bytes_; }
    std::size_t pending_bytes() const { std::lock_guard lk(m_); return pending_bytes_; }

    void close() {
        std::shared_ptr<TcpMessageChannel> c;
        {
            std::lock_guard lk(m_);
            closed_ = true;
            c = current_;
            wake_.notify_all();
        }
        if (c) c->close();
        std::call_once(joined_, [this] { if (manager_.joinable() && manager_.get_id() != std::this_thread::get_id()) manager_.join(); });
    }

private:
    void run() {
        while (!is_closed()) {
            std::unique_ptr<TcpMessageChannel> fresh;
            try {
                fresh = TcpMessageChannel::connect(addr_, cfg_, Millis(2000));
            } catch (const std::system_error&) {
                {
                    std::lock_guard lk(m_);
                    ++failed_attempts_;
                }
                if (!sleep(Millis(backoff_.next()))) return;
                continue;
            }
            std::shared_ptr<TcpMessageChannel> ch = std::move(fresh);
            {
                std::lock_guard lk(m_);
                if (closed_) { ch->close(); return; }
                current_ = ch;
                ++connect_count_;
                backoff_.reset();  // a successful connect starts the next outage from the shortest delay
            }
            pump(*ch);
            {
                std::lock_guard lk(m_);
                current_.reset();
                abandoned_bytes_ += static_cast<long long>(ch->unsent_bytes());
            }
            ch->close();
        }
    }

    /// Move `pending_` into the channel until it dies or the client closes.
    void pump(TcpMessageChannel& ch) {
        std::unique_lock lk(m_);
        while (!closed_ && ch.is_open() && !ch.is_peer_closed()) {
            while (!pending_.empty()) {
                bool accepted;
                try {
                    accepted = ch.offer(pending_.front());
                } catch (const StateError&) {  // the channel died under us
                    return;
                }
                if (!accepted) break;  // its out ring is full: try again in a moment
                pending_bytes_ -= FrameCodec::HEADER + pending_.front().size();
                pending_.pop_front();
            }
            wake_.wait_for(lk, Millis(10));  // wake up regularly: is the connection still alive, did the out ring drain?
        }
    }

    bool is_closed() const { std::lock_guard lk(m_); return closed_; }
    /// Sleep that close() can interrupt.  false = the client was closed.
    bool sleep(Millis d) {
        std::unique_lock lk(m_);
        wake_.wait_for(lk, d, [this] { return closed_; });
        return !closed_;
    }

    Address addr_;
    ChannelConfig cfg_;
    Backoff backoff_;
    mutable std::mutex m_;
    std::condition_variable wake_;
    std::deque<Bytes> pending_;
    std::size_t pending_bytes_ = 0;  // encoded size: 4 + len summed, the same unit as the out ring
    std::shared_ptr<TcpMessageChannel> current_;
    bool closed_ = false;
    int connect_count_ = 0, failed_attempts_ = 0;
    long long abandoned_bytes_ = 0;
    std::once_flag joined_;
    std::jthread manager_;
};

}  // namespace net
