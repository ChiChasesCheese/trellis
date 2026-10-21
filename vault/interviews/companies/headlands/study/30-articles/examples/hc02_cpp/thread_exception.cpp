// An exception that leaves a thread body calls std::terminate.  Catch it in the thread, carry it out as an exception_ptr.
#include <exception>
#include <iostream>
#include <stdexcept>
#include <thread>

int main() {
    std::exception_ptr failure;
    std::thread t([&] {
        try {
            throw std::runtime_error("the source failed");
        } catch (...) {
            failure = std::current_exception();  // without this catch: std::terminate(), the whole process dies
        }
    });
    t.join();  // join() orders the write to `failure` before the read below
    try {
        if (failure) std::rethrow_exception(failure);
    } catch (const std::exception& e) {
        std::cout << "main rethrew: " << e.what() << "\n";
    }
}
