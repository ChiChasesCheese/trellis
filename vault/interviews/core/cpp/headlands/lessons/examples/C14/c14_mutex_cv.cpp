// C14: mutex + condition_variable: a bounded blocking queue (Java: ArrayBlockingQueue), plus scoped_lock and shared_mutex.
#include <condition_variable>
#include <deque>
#include <iostream>
#include <mutex>
#include <optional>
#include <shared_mutex>
#include <thread>
#include <vector>

// [[snip:queue]]
template <class T>
class BlockingQueue {
    std::mutex m_;
    std::condition_variable not_empty_, not_full_;
    std::deque<T> q_;
    const std::size_t cap_;
    bool closed_ = false;
public:
    explicit BlockingQueue(std::size_t cap) : cap_(cap) {}

    void push(T v) {
        std::unique_lock<std::mutex> lk(m_);                         // unique_lock: wait() must be able to unlock/relock it
        not_full_.wait(lk, [&] { return q_.size() < cap_; });        // predicate form: re-checked after every wakeup
        q_.push_back(std::move(v));
        lk.unlock();                                                 // notify without holding the lock: the woken thread can run at once
        not_empty_.notify_one();
    }
    std::optional<T> pop() {                                         // empty optional = queue closed and drained
        std::unique_lock<std::mutex> lk(m_);
        not_empty_.wait(lk, [&] { return !q_.empty() || closed_; });
        if (q_.empty()) return std::nullopt;
        T v = std::move(q_.front());
        q_.pop_front();
        lk.unlock();
        not_full_.notify_one();
        return v;
    }
    void close() { { std::lock_guard<std::mutex> g(m_); closed_ = true; } not_empty_.notify_all(); }
};
// [[/snip]]

// [[snip:scoped]]
struct Account { std::mutex m; long balance = 0; };

void transfer(Account& from, Account& to, long amt) {
    std::scoped_lock lock(from.m, to.m);          // locks BOTH with a deadlock-avoidance algorithm, whatever the argument order
    from.balance -= amt; to.balance += amt;
}
// [[/snip]]

// [[snip:shared]]
class Prices {
    mutable std::shared_mutex m_;                 // many readers OR one writer (Java: ReentrantReadWriteLock)
    long px_ = 100;
public:
    long read() const { std::shared_lock<std::shared_mutex> g(m_); return px_; }
    void write(long v) { std::unique_lock<std::shared_mutex> g(m_); px_ = v; }
};
// [[/snip]]

int main() {
    BlockingQueue<int> q(4);                      // small capacity so the producer really blocks
    long consumed = 0, count = 0;
    std::thread consumer([&] { while (auto v = q.pop()) { consumed += *v; ++count; } });
    std::thread producer([&] { for (int i = 1; i <= 1000; ++i) q.push(i); q.close(); });
    producer.join(); consumer.join();
    std::cout << "consumed " << count << " items, sum " << consumed << "\n";

    Account a, b; a.balance = 1000; b.balance = 1000;
    std::thread t1([&] { for (int i = 0; i < 10000; ++i) transfer(a, b, 1); });
    std::thread t2([&] { for (int i = 0; i < 10000; ++i) transfer(b, a, 1); });   // opposite order: classic deadlock with two lock_guards
    t1.join(); t2.join();
    std::cout << "balances " << a.balance << " + " << b.balance << " = " << a.balance + b.balance << "\n";

    Prices p;
    std::vector<std::thread> rs;
    for (int i = 0; i < 3; ++i) rs.emplace_back([&] { for (int k = 0; k < 1000; ++k) (void)p.read(); });
    std::thread w([&] { for (int k = 0; k < 100; ++k) p.write(100 + k); });
    for (auto& t : rs) t.join();
    w.join();
    std::cout << "final price " << p.read() << "\n";
}
