// hc15 · Streaming median — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 StreamingMedian (two std::priority_queue), 2 WindowMedian (lazy deletion + compaction),
//        3 TwoHeapPercentile (fixed p) and OrderStatistics (treap in vectors, any p),
//        4 TickHistogram (Fenwick tree over a bounded tick range, zero allocation after construction).
#pragma once

#include <algorithm>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <queue>
#include <stdexcept>
#include <unordered_map>
#include <vector>

namespace median {

inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("addition overflow");
    return r;
}

/// Max-heap of the smaller half, min-heap of the larger half.
using MaxHeap = std::priority_queue<long long>;
using MinHeap = std::priority_queue<long long, std::vector<long long>, std::greater<>>;

// ============================================================================================ Part 1
/// Lower median (the ceil(n/2)-th smallest) of everything added so far.
class StreamingMedian {
public:
    void add(long long price) {
        if (lo_.empty() || price <= lo_.top()) lo_.push(price);
        else hi_.push(price);
        if (lo_.size() > hi_.size() + 1) {
            hi_.push(lo_.top());
            lo_.pop();
        } else if (hi_.size() > lo_.size()) {
            lo_.push(hi_.top());
            hi_.pop();
        }
    }
    /// std::out_of_range if empty.
    long long median() const {
        if (lo_.empty()) throw std::out_of_range("no prices yet");
        return lo_.top();
    }
    /// 2 x the true median: the sum of the two middle values (the one middle value twice if n is odd).
    /// std::overflow_error if that does not fit; std::out_of_range if empty.
    long long doubled_median() const {
        if (lo_.empty()) throw std::out_of_range("no prices yet");
        const long long upper = lo_.size() == hi_.size() ? hi_.top() : lo_.top();
        return add_exact(lo_.top(), upper);
    }
    std::size_t size() const noexcept { return lo_.size() + hi_.size(); }

private:
    MaxHeap lo_;
    MinHeap hi_;
};

// ============================================================================================ Part 3 helper
/// Nearest rank: the p-th percentile of n values is the ceil(p * n / 100)-th smallest.  n >= 0, 1 <= p <= 100,
/// else std::invalid_argument.  Never overflows: split n into n / 100 and n % 100 instead of computing p * n.
inline long long nearest_rank(long long n, int p) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    if (p < 1 || p > 100) throw std::invalid_argument("p must be in 1..100");
    return n / 100 * p + ((n % 100) * p + 99) / 100;
}

// ============================================================================================ Part 2
/// Lower median of the last k prices.  Lazy deletion: a price leaving the window is recorded in a per-heap
/// "delayed" table and only popped when it reaches the top.  Heaps are balanced by their valid counts, tops are
/// kept valid after every add.  Stale entries buried at the bottom would accumulate on an ascending stream, so
/// when more than 2k are stale the heaps are rebuilt from the window (at most one rebuild per 2k adds).
class WindowMedian {
public:
    /// k >= 1, else std::invalid_argument.
    explicit WindowMedian(int k) {
        if (k < 1) throw std::invalid_argument("k must be >= 1");
        ring_.resize(static_cast<std::size_t>(k));
    }

    void add(long long price) {
        long long old = 0;
        const bool evict = count_ == ring_.size();
        if (evict) {
            old = ring_[head_];
            ring_[head_] = price;
            head_ = (head_ + 1) % ring_.size();
        } else {
            ring_[(head_ + count_) % ring_.size()] = price;
            ++count_;
        }
        if (lo_valid_ == 0 || price <= lo_.top()) {
            lo_.push(price);
            ++lo_valid_;
        } else {
            hi_.push(price);
            ++hi_valid_;
        }
        if (evict) {
            if (old <= lo_.top()) {
                ++delayed_lo_[old];
                --lo_valid_;
            } else {
                ++delayed_hi_[old];
                --hi_valid_;
            }
        }
        if (lo_valid_ > hi_valid_ + 1) {
            prune(lo_, delayed_lo_);
            hi_.push(lo_.top());
            lo_.pop();
            --lo_valid_;
            ++hi_valid_;
        } else if (lo_valid_ < hi_valid_) {
            prune(hi_, delayed_hi_);
            lo_.push(hi_.top());
            hi_.pop();
            --hi_valid_;
            ++lo_valid_;
        }
        prune(lo_, delayed_lo_);
        prune(hi_, delayed_hi_);
        if (retained() - lo_valid_ - hi_valid_ > 2 * ring_.size()) rebuild();
    }

    /// std::out_of_range if nothing was added yet.
    long long median() const {
        if (count_ == 0) throw std::out_of_range("no prices yet");
        return lo_.top();
    }
    std::size_t size() const noexcept { return count_; }
    /// Entries physically held by the two heaps, stale ones included.  Stays <= 4k.
    std::size_t retained() const noexcept { return lo_.size() + hi_.size(); }

    static std::vector<long long> slide(const std::vector<long long>& prices, int k) {
        WindowMedian w(k);
        std::vector<long long> out;
        out.reserve(prices.size());
        for (long long x : prices) {
            w.add(x);
            out.push_back(w.median());
        }
        return out;
    }

private:
    template <class Heap> static void prune(Heap& heap, std::unordered_map<long long, int>& delayed) {
        while (!heap.empty()) {
            const auto it = delayed.find(heap.top());
            if (it == delayed.end()) return;
            if (--it->second == 0) delayed.erase(it);
            heap.pop();
        }
    }

    void rebuild() {
        std::vector<long long> w(count_);
        for (std::size_t i = 0; i < count_; ++i) w[i] = ring_[(head_ + i) % ring_.size()];
        std::sort(w.begin(), w.end());
        lo_ = MaxHeap();
        hi_ = MinHeap();
        delayed_lo_.clear();
        delayed_hi_.clear();
        lo_valid_ = (count_ + 1) / 2;
        hi_valid_ = count_ - lo_valid_;
        for (std::size_t i = 0; i < count_; ++i) {
            if (i < lo_valid_) lo_.push(w[i]);
            else hi_.push(w[i]);
        }
    }

    std::vector<long long> ring_;
    std::size_t head_ = 0, count_ = 0;
    MaxHeap lo_;
    MinHeap hi_;
    std::unordered_map<long long, int> delayed_lo_, delayed_hi_;
    std::size_t lo_valid_ = 0, hi_valid_ = 0;
};

// ============================================================================================ Part 3a
/// Fixed percentile p by two heaps: lo = the nearest_rank(n, p) smallest values.  p is fixed at construction.
class TwoHeapPercentile {
public:
    /// 1 <= p <= 100, else std::invalid_argument.
    explicit TwoHeapPercentile(int p) : p_(p) { nearest_rank(1, p); }

    void add(long long price) {
        ++n_;
        if (lo_.empty() || price <= lo_.top()) lo_.push(price);
        else hi_.push(price);
        const auto target = static_cast<std::size_t>(nearest_rank(n_, p_));
        while (lo_.size() > target) {
            hi_.push(lo_.top());
            lo_.pop();
        }
        while (lo_.size() < target) {
            lo_.push(hi_.top());
            hi_.pop();
        }
    }
    /// std::out_of_range if empty.
    long long value() const {
        if (lo_.empty()) throw std::out_of_range("no prices yet");
        return lo_.top();
    }
    long long size() const noexcept { return n_; }

private:
    int p_;
    long long n_ = 0;
    MaxHeap lo_;
    MinHeap hi_;
};

// ============================================================================================ Part 3b
/// Order-statistics structure: any p at query time.  A treap (BST by value + heap by random priority) stored in
/// parallel vectors (index 0 = null); equal values share one node with a count; every node knows its subtree total.
class OrderStatistics {
public:
    static long long rank(long long n, int p) { return nearest_rank(n, p); }

    void add(long long price) { root_ = insert(root_, price); }

    int size() const noexcept { return total_[static_cast<std::size_t>(root_)]; }

    /// 1-based, duplicates count separately.  std::invalid_argument if rank is not in 1..size().
    long long kth(long long rank) const {
        if (rank < 1 || rank > size()) throw std::invalid_argument("rank out of range");
        auto t = static_cast<std::size_t>(root_);
        long long r = rank;
        while (true) {
            const long long l = total_[static_cast<std::size_t>(left_[t])];
            if (r <= l) t = static_cast<std::size_t>(left_[t]);
            else if (r <= l + cnt_[t]) return key_[t];
            else {
                r -= l + cnt_[t];
                t = static_cast<std::size_t>(right_[t]);
            }
        }
    }

    /// p outside 1..100 -> std::invalid_argument (checked first); empty -> std::out_of_range.
    long long percentile(int p) const {
        const long long r = nearest_rank(size(), p);
        if (size() == 0) throw std::out_of_range("no prices yet");
        return kth(r);
    }

    /// Number of values <= price.
    long long count_at_most(long long price) const {
        long long c = 0;
        auto t = static_cast<std::size_t>(root_);
        while (t != 0) {
            if (price < key_[t]) t = static_cast<std::size_t>(left_[t]);
            else {
                c += total_[static_cast<std::size_t>(left_[t])] + cnt_[t];
                t = static_cast<std::size_t>(right_[t]);
            }
        }
        return c;
    }

private:
    int insert(int t, long long x) {
        if (t == 0) return new_node(x);
        const auto ti = static_cast<std::size_t>(t);
        if (x == key_[ti]) {
            ++cnt_[ti];
        } else if (x < key_[ti]) {
            const int c = insert(left_[ti], x);  // key_/left_ may reallocate inside insert: index again afterwards, no stale reference
            left_[ti] = c;
            if (prio_[static_cast<std::size_t>(c)] > prio_[ti]) {  // rotate right
                left_[ti] = right_[static_cast<std::size_t>(c)];
                right_[static_cast<std::size_t>(c)] = t;
                pull(t);
                pull(c);
                return c;
            }
        } else {
            const int c = insert(right_[ti], x);
            right_[ti] = c;
            if (prio_[static_cast<std::size_t>(c)] > prio_[ti]) {  // rotate left
                right_[ti] = left_[static_cast<std::size_t>(c)];
                left_[static_cast<std::size_t>(c)] = t;
                pull(t);
                pull(c);
                return c;
            }
        }
        pull(t);
        return t;
    }

    int new_node(long long x) {
        key_.push_back(x);
        cnt_.push_back(1);
        left_.push_back(0);
        right_.push_back(0);
        total_.push_back(1);
        seed_ ^= seed_ << 13;  // xorshift32, deterministic
        seed_ ^= seed_ >> 17;
        seed_ ^= seed_ << 5;
        prio_.push_back(seed_);
        return static_cast<int>(key_.size()) - 1;
    }

    void pull(int t) {
        const auto ti = static_cast<std::size_t>(t);
        total_[ti] = cnt_[ti] + total_[static_cast<std::size_t>(left_[ti])] + total_[static_cast<std::size_t>(right_[ti])];
    }

    // index 0 is the null node: total 0
    std::vector<long long> key_{0};
    std::vector<int> cnt_{0}, left_{0}, right_{0}, total_{0};
    std::vector<std::uint32_t> prio_{0};
    int root_ = 0;
    std::uint32_t seed_ = 0x2545F491u;
};

// ============================================================================================ Part 4
/// Prices 0..max_tick-1 counted in a Fenwick tree: add and k-th are O(log T); everything is allocated in the constructor.
class TickHistogram {
public:
    static constexpr int MAX_TICKS = 1 << 22;

    /// 1 <= max_tick <= MAX_TICKS, else std::invalid_argument.
    explicit TickHistogram(int max_tick) : max_tick_(max_tick) {
        if (max_tick < 1 || max_tick > MAX_TICKS) throw std::invalid_argument("max_tick out of range");
        tree_.assign(static_cast<std::size_t>(max_tick) + 1, 0);
        top_ = static_cast<int>(std::bit_floor(static_cast<unsigned>(max_tick)));
    }

    /// price outside 0..max_tick-1 -> std::invalid_argument.
    void add(long long price) {
        if (price < 0 || price >= max_tick_) throw std::invalid_argument("price out of range");
        for (int i = static_cast<int>(price) + 1; i <= max_tick_; i += i & -i) ++tree_[static_cast<std::size_t>(i)];
        ++total_;
    }
    long long count() const noexcept { return total_; }

    /// Values <= price; price < 0 -> 0, price >= max_tick -> count().
    long long count_at_most(long long price) const {
        if (price < 0) return 0;
        if (price >= max_tick_) return total_;
        long long c = 0;
        for (int i = static_cast<int>(price) + 1; i > 0; i -= i & -i) c += tree_[static_cast<std::size_t>(i)];
        return c;
    }

    /// 1-based k-th smallest price; rank outside 1..count() -> std::invalid_argument.
    long long kth(long long rank) const {
        if (rank < 1 || rank > total_) throw std::invalid_argument("rank out of range");
        int pos = 0;
        long long r = rank;
        for (int step = top_; step > 0; step >>= 1) {
            const int next = pos + step;
            if (next <= max_tick_ && tree_[static_cast<std::size_t>(next)] < r) {
                pos = next;
                r -= tree_[static_cast<std::size_t>(next)];
            }
        }
        return pos;
    }

    long long percentile(int p) const {
        const long long r = nearest_rank(total_, p);
        if (total_ == 0) throw std::out_of_range("no prices yet");
        return kth(r);
    }
    long long median() const { return percentile(50); }

private:
    int max_tick_;
    int top_;
    long long total_ = 0;
    std::vector<long long> tree_;
};

}  // namespace median
