// C14: std::thread basics: start, join, argument passing, results via future, exceptions, thread_local.
#include <future>
#include <stdexcept>
#include <iostream>
#include <numeric>
#include <string>
#include <thread>
#include <vector>

// [[snip:args]]
void add_to(int& target, int amount) { target += amount; }

void passing_arguments() {
    int total = 0;
    std::thread t1(add_to, std::ref(total), 5);      // arguments are COPIED into the thread; std::ref asks for a reference
    t1.join();                                       // forgetting join()/detach() => std::terminate in ~thread
    std::cout << "  total after thread with std::ref: " << total << "\n";
    // std::thread t2(add_to, total, 5);             // does not compile: copies cannot bind to int&
}
// [[/snip]]

// [[snip:future]]
long parallel_sum(const std::vector<int>& v) {
    auto mid = v.begin() + static_cast<std::ptrdiff_t>(v.size() / 2);
    auto left = std::async(std::launch::async, [&] { return std::accumulate(v.begin(), mid, 0L); });   // runs on another thread
    long right = std::accumulate(mid, v.end(), 0L);                                                    // meanwhile, this thread
    return left.get() + right;                       // get() waits, and rethrows any exception the task threw
}
// [[/snip]]

// [[snip:exc]]
void exceptions_cross_threads() {
    auto f = std::async(std::launch::async, []() -> int { throw std::runtime_error("worker failed"); });
    try { (void)f.get(); } catch (const std::exception& e) { std::cout << "  caught from worker: " << e.what() << "\n"; }
    // An exception that escapes a plain std::thread function calls std::terminate() instead.
}
// [[/snip]]

// [[snip:tls]]
thread_local int per_thread_counter = 0;              // every thread has its own copy (Java: ThreadLocal<Integer>)

void thread_local_demo() {
    std::vector<std::thread> ts;
    std::vector<int> results(3);
    for (int i = 0; i < 3; ++i)
        ts.emplace_back([i, &results] { for (int k = 0; k <= i; ++k) ++per_thread_counter; results[i] = per_thread_counter; });
    for (auto& t : ts) t.join();
    std::cout << "  thread_local results: " << results[0] << " " << results[1] << " " << results[2] << ", main's copy: " << per_thread_counter << "\n";
}
// [[/snip]]

int main() {
    passing_arguments();
    std::vector<int> v(1000);
    std::iota(v.begin(), v.end(), 1);
    std::cout << "  parallel_sum(1..1000) = " << parallel_sum(v) << "\n";
    exceptions_cross_threads();
    thread_local_demo();
    std::cout << "  hardware_concurrency >= 1: " << (std::thread::hardware_concurrency() >= 1) << "\n";
}
