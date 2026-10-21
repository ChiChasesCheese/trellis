// The C++11 core: auto, range-for, lambdas, move, smart pointers, constexpr, enum class, threads, variadic templates.
#include <algorithm>
#include <cstdio>
#include <memory>
#include <string>
#include <thread>
#include <utility>
#include <vector>

enum class Side : char { Buy = 'B', Sell = 'S' };           // scoped enum: no implicit int conversion

constexpr int square(int x) { return x * x; }               // evaluated at compile time when it can be
static_assert(square(12) == 144, "constexpr works in static_assert");

template <class... Args>                                    // variadic template
void log_all(const char* tag, const Args&... args) {
    std::printf("%s:", tag);
    int dummy[] = {0, ((void)(std::printf(" %s", std::to_string(args).c_str())), 0)...};
    (void)dummy;
    std::printf("\n");
}

int main() {
    std::vector<int> v{5, 3, 9, 1};                          // brace init
    int threshold = 4;
    auto big = [threshold](int x) { return x > threshold; }; // lambda with capture
    std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
    for (auto x : v) std::printf("%d%s", x, big(x) ? "* " : "  ");   // range-for + auto
    std::printf("\n");

    std::unique_ptr<std::string> p(new std::string("owned"));  // C++11: unique_ptr yes, make_unique no (14)
    std::unique_ptr<std::string> q = std::move(p);             // ownership moves
    std::printf("p is %s, q holds \"%s\"\n", p ? "set" : "null", q->c_str());

    int* np = nullptr;                                       // nullptr, not 0/NULL
    std::printf("nullptr is %s\n", np == nullptr ? "null" : "set");
    std::printf("Side::Buy = %c\n", static_cast<char>(Side::Buy));

    int counter = 0;
    std::thread t([&counter] { counter = 42; });             // std::thread
    t.join();
    std::printf("thread wrote %d\n", counter);
    log_all("vals", 1, 2.5, 3L);
}
