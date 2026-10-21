// mutex, scoped_lock, condition_variable: a bounded producer/consumer queue.
#include <condition_variable>
#include <cstdio>
#include <deque>
#include <mutex>
#include <thread>
#include <vector>

class BoundedQueue {
    std::mutex m_;
    std::condition_variable not_full_, not_empty_;
    std::deque<int> q_;
    const std::size_t cap_;
public:
    explicit BoundedQueue(std::size_t cap) : cap_(cap) {}
    void push(int v) {
        std::unique_lock lk(m_);
        not_full_.wait(lk, [&] { return q_.size() < cap_; });      // predicate guards against spurious wakeups
        q_.push_back(v);
        not_empty_.notify_one();
    }
    int pop() {
        std::unique_lock lk(m_);
        not_empty_.wait(lk, [&] { return !q_.empty(); });
        int v = q_.front(); q_.pop_front();
        not_full_.notify_one();
        return v;
    }
};

struct Account { std::mutex m; long balance = 1000; };
void transfer(Account& from, Account& to, long amt) {
    std::scoped_lock lk(from.m, to.m);                              // locks both without deadlock, any argument order
    from.balance -= amt; to.balance += amt;
}

int main() {
    BoundedQueue q(8);
    long total = 0;
    std::thread prod([&] { for (int i = 1; i <= 100000; ++i) q.push(i); q.push(-1); });
    std::thread cons([&] { for (int v; (v = q.pop()) != -1;) total += v; });
    prod.join(); cons.join();
    std::printf("consumed sum = %ld (expected %ld)\n", total, 100000L * 100001L / 2);

    Account a, b;
    std::thread t1([&] { for (int i = 0; i < 100000; ++i) transfer(a, b, 1); });
    std::thread t2([&] { for (int i = 0; i < 100000; ++i) transfer(b, a, 1); });   // opposite order: would deadlock with two lock_guards
    t1.join(); t2.join();
    std::printf("balances: %ld + %ld = %ld\n", a.balance, b.balance, a.balance + b.balance);
}
