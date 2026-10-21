// condition_variable_any::wait(lock, stop_token, pred) wakes up when stop is requested; a plain wait would sleep forever.
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <stop_token>
#include <thread>

int main() {
    std::mutex mu;
    std::condition_variable_any cv;
    bool has_item = false;  // nobody ever sets it

    std::stop_source stop;
    std::jthread worker([&, token = stop.get_token()] {
        std::unique_lock lock(mu);
        const bool got = cv.wait(lock, token, [&] { return has_item; });
        std::cout << "worker woke up, predicate true? " << std::boolalpha << got << ", stop requested? " << token.stop_requested() << "\n";
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    stop.request_stop();  // the worker is released although the predicate is still false
    worker.join();
}
