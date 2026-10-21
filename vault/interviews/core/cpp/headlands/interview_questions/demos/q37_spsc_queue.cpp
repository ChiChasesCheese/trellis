// Single-producer single-consumer lock-free ring buffer (in-process).
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <mutex>
#include <queue>
#include <thread>
#include <new>

template <class T, std::size_t N, bool CacheIndex = true>
class SpscQueue {
    static_assert((N & (N - 1)) == 0, "N must be a power of two: index & (N-1) replaces modulo");
    alignas(128) std::atomic<std::size_t> head_{0};         // written by the consumer only
    alignas(128) std::atomic<std::size_t> tail_{0};         // written by the producer only
    alignas(128) std::size_t head_cache_ = 0;               // producer's last-seen copy of head_
    alignas(128) std::size_t tail_cache_ = 0;               // consumer's last-seen copy of tail_
    alignas(128) T buf_[N];
public:
    bool push(const T& v) {
        auto t = tail_.load(std::memory_order_relaxed);
        if constexpr (CacheIndex) {
            if (t - head_cache_ == N) {                                          // looks full: refresh the copy
                head_cache_ = head_.load(std::memory_order_acquire);
                if (t - head_cache_ == N) return false;
            }
        } else {
            if (t - head_.load(std::memory_order_acquire) == N) return false;    // read the other core's line every time
        }
        buf_[t & (N - 1)] = v;
        tail_.store(t + 1, std::memory_order_release);                          // publish the element
        return true;
    }
    bool pop(T& out) {
        auto h = head_.load(std::memory_order_relaxed);
        if constexpr (CacheIndex) {
            if (h == tail_cache_) {                                              // looks empty: refresh the copy
                tail_cache_ = tail_.load(std::memory_order_acquire);
                if (h == tail_cache_) return false;
            }
        } else {
            if (h == tail_.load(std::memory_order_acquire)) return false;
        }
        out = buf_[h & (N - 1)];
        head_.store(h + 1, std::memory_order_release);                          // free the slot
        return true;
    }
};

struct MutexQueue {
    std::mutex m; std::queue<std::int64_t> q;
    void push(std::int64_t v) { std::lock_guard g(m); q.push(v); }
    bool pop(std::int64_t& v) { std::lock_guard g(m); if (q.empty()) return false; v = q.front(); q.pop(); return true; }
};

template <class Q, class Push>
double run(Q& q, Push push, int count, std::int64_t& sum) {
    auto t0 = std::chrono::steady_clock::now();
    std::thread prod([&] { for (std::int64_t i = 1; i <= count; ++i) while (!push(q, i)) {} });
    sum = 0;
    std::int64_t v;
    for (int got = 0; got < count;) if (q.pop(v)) { sum += v; ++got; }
    prod.join();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    const int N = 5'000'000;
    std::int64_t s0 = 0, s1 = 0, s2 = 0;
    auto* naive = new SpscQueue<std::int64_t, 1024, false>;
    double t0 = run(*naive, [](auto& q, std::int64_t v) { return q.push(v); }, N, s0);
    delete naive;
    auto* spsc = new SpscQueue<std::int64_t, 1024>;
    double t1 = run(*spsc, [](auto& q, std::int64_t v) { return q.push(v); }, N, s1);
    delete spsc;
    MutexQueue mq;
    double t2 = run(mq, [](auto& q, std::int64_t v) { q.push(v); return true; }, N, s2);
    std::printf("sums equal and correct: %s\n", (s0 == s1 && s1 == s2 && s1 == static_cast<std::int64_t>(N) * (N + 1) / 2) ? "yes" : "no");
    std::printf("SPSC ring, read other index every time: %6.0f ms for %d items (%.0f ns/item)\n", t0, N, t0 * 1e6 / N);
    std::printf("SPSC ring, cached index   : %6.0f ms for %d items (%.0f ns/item)\n", t1, N, t1 * 1e6 / N);
    std::printf("mutex + std::queue          : %6.0f ms for %d items (%.0f ns/item)\n", t2, N, t2 * 1e6 / N);
}
