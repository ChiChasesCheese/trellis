// minitest.hpp — a tiny self-contained test harness for the C++ problem sets (no external libraries).
//
//   TEST(name, "part1,edge") { CHECK_EQ(f(1), 2); }
//   MT_MAIN()                                   // at the bottom of test.cpp
//
// Command line of the produced binary:
//   --tag T            run only tests carrying tag T (repeatable, any-of)
//   --exclude-tag T    skip tests carrying tag T (repeatable)
//   --require-tag T    run only tests that ALSO carry tag T (repeatable, all-of)
//   --name S           run only tests whose name contains S
//   --list             print "name tags" and exit
//   --allow-empty      exit 0 when no test matched (default: exit 2)
//   -q                 print failures and the summary only
// Exit code: 0 all passed, 1 some test failed, 2 nothing matched.  The last line is always
//   SUMMARY total=N passed=P failed=F checks=C
//
// CHECK_* are non-fatal (the test goes on), REQUIRE_* abort the current test.  An exception that escapes a test
// body is a failure (that is how the starter's `throw std::logic_error("TODO")` turns the suite red).
#pragma once

// clang -fsanitize=undefined lowers a checked signed __int128 multiplication to compiler-rt's __muloti4, which libgcc (the
// default runtime on Linux, clang or g++) does not have: the link fails.  Provide it (only when the runtime lacks it, an
// archive member is never pulled in over a definition in the executable).
#if defined(__clang__) && defined(__linux__) && defined(__SIZEOF_INT128__)
extern "C" __int128 __muloti4(__int128 a, __int128 b, int* overflow) {
    using U = unsigned __int128;
    const U ua = a < 0 ? U(0) - U(a) : U(a);
    const U ub = b < 0 ? U(0) - U(b) : U(b);
    const bool negative = (a < 0) != (b < 0);
    const U product = ua * ub;  // unsigned: wraps, never UB
    const U limit = U(1) << 127;  // |INT128_MIN|
    *overflow = (ua != 0 && ub > ~U(0) / ua) || (negative ? product > limit : product >= limit);
    return static_cast<__int128>(negative ? U(0) - product : product);
}
#endif

#include <cerrno>
#include <chrono>
#include <cmath>
#include <stdexcept>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <exception>
#include <fcntl.h>
#include <functional>
#include <iostream>
#include <optional>
#include <mutex>
#include <pthread.h>
#include <thread>
#include <sstream>
#include <string>
#include <string_view>
#include <sys/wait.h>
#include <type_traits>
#include <typeinfo>
#include <unistd.h>
#include <utility>
#include <variant>
#include <vector>

namespace mt {

// ---------------------------------------------------------------------------------------------- 128-bit helpers
// libc++ has no operator<< for __int128, so the harness prints it itself.
inline std::string to_string(unsigned __int128 v) {
    if (v == 0) return "0";
    std::string s;
    while (v != 0) { s.push_back(static_cast<char>('0' + static_cast<int>(v % 10))); v /= 10; }
    return {s.rbegin(), s.rend()};
}
inline std::string to_string(__int128 v) {
    if (v >= 0) return to_string(static_cast<unsigned __int128>(v));
    return "-" + to_string(static_cast<unsigned __int128>(0) - static_cast<unsigned __int128>(v));
}
/// Parse a decimal literal such as "-42535295865117307937533511947398414336" (test expectations are written as strings).
inline __int128 i128(std::string_view s) {
    bool neg = !s.empty() && s.front() == '-';
    if (neg) s.remove_prefix(1);
    unsigned __int128 v = 0;
    for (char c : s) v = v * 10 + static_cast<unsigned>(c - '0');
    return neg ? static_cast<__int128>(0 - v) : static_cast<__int128>(v);
}

// ---------------------------------------------------------------------------------------------- printing values
template <class T, class = void> struct streamable : std::false_type {};
template <class T>
struct streamable<T, std::void_t<decltype(std::declval<std::ostream&>() << std::declval<const T&>())>> : std::true_type {};

template <class T> std::string show(const T& v);

template <class T> std::string show_seq(const T& v) {
    std::string s = "[";
    size_t n = 0;
    for (const auto& x : v) {
        if (n++ == 20) { s += ", ... (" + std::to_string(v.size()) + " items)"; break; }
        if (n > 1) s += ", ";
        s += show(x);
    }
    return s + "]";
}

template <class T> struct is_vector : std::false_type {};
template <class T, class A> struct is_vector<std::vector<T, A>> : std::true_type {};
template <class T> struct is_optional : std::false_type {};
template <class T> struct is_optional<std::optional<T>> : std::true_type {};
template <class T> struct is_variant : std::false_type {};
template <class... Ts> struct is_variant<std::variant<Ts...>> : std::true_type {};

template <class T> std::string show(const T& v) {
    if constexpr (std::is_same_v<T, bool>) return v ? "true" : "false";
    else if constexpr (std::is_same_v<T, __int128> || std::is_same_v<T, unsigned __int128>) return to_string(v);
    else if constexpr (std::is_floating_point_v<T>) { std::ostringstream os; os.precision(17); os << v; return os.str(); }
    else if constexpr (std::is_same_v<T, std::string>) return "\"" + v + "\"";
    else if constexpr (std::is_same_v<T, std::nullopt_t>) return "nullopt";
    else if constexpr (is_vector<T>::value) return show_seq(v);
    else if constexpr (is_optional<T>::value) return v ? "Some(" + show(*v) + ")" : "nullopt";
    else if constexpr (is_variant<T>::value) return std::visit([](const auto& x) { return show(x); }, v);
    else if constexpr (std::is_enum_v<T>) return std::to_string(static_cast<long long>(v));
    else if constexpr (streamable<T>::value) { std::ostringstream os; os << v; return os.str(); }
    else return std::string("<") + typeid(T).name() + ">";
}

// ---------------------------------------------------------------------------------------------- comparison
// std::cmp_equal & co. avoid -Wsign-compare noise and the silent -1 == 4294967295u trap for integer pairs.
template <class T> inline constexpr bool plain_int_v = std::is_integral_v<T> && !std::is_same_v<T, bool> && sizeof(T) <= 8;
template <class A, class B> bool eq(const A& a, const B& b) {
    if constexpr (plain_int_v<A> && plain_int_v<B>) return std::cmp_equal(a, b);
    else return a == b;
}
template <class A, class B> bool lt(const A& a, const B& b) {
    if constexpr (plain_int_v<A> && plain_int_v<B>) return std::cmp_less(a, b);
    else return a < b;
}

// ---------------------------------------------------------------------------------------------- registry
struct TestCase { const char* name; const char* tags; void (*fn)(); const char* file; int line; };
inline std::vector<TestCase>& registry() { static std::vector<TestCase> r; return r; }
struct Registrar {
    Registrar(const char* name, const char* tags, void (*fn)(), const char* file, int line) {
        registry().push_back({name, tags, fn, file, line});
    }
};
struct AbortTest {};

struct Ctx {
    long long checks = 0;
    int failed_checks = 0;
    std::vector<std::string> messages;
};
inline Ctx& ctx() { static Ctx c; return c; }

inline void fail(const char* file, int line, const std::string& msg) {
    auto& c = ctx();
    ++c.failed_checks;
    if (c.messages.size() < 8) {
        std::string f = file;
        auto slash = f.rfind('/');
        c.messages.push_back((slash == std::string::npos ? f : f.substr(slash + 1)) + ":" + std::to_string(line) + "  " + msg);
    }
}

inline bool has_tag(const char* tags, const std::string& t) {
    std::string_view v = tags;
    size_t pos = 0;
    while (pos <= v.size()) {
        size_t comma = v.find(',', pos);
        if (comma == std::string_view::npos) comma = v.size();
        if (v.substr(pos, comma - pos) == t) return true;
        pos = comma + 1;
    }
    return false;
}

// ---------------------------------------------------------------------------------------------- POSIX helpers
/// Run fn on a fresh thread with exactly `bytes` of stack (std::thread cannot choose its stack size).  Exceptions propagate.
inline void run_on_stack(size_t bytes, std::function<void()> fn) {
    struct Box { std::function<void()> fn; std::exception_ptr err; } box{std::move(fn), nullptr};
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    const size_t page = static_cast<size_t>(sysconf(_SC_PAGESIZE));
    pthread_attr_setstacksize(&attr, (bytes + page - 1) / page * page);
    pthread_t th;
    int rc = pthread_create(&th, &attr, [](void* p) -> void* {
        auto* b = static_cast<Box*>(p);
        try { b->fn(); } catch (...) { b->err = std::current_exception(); }
        return nullptr;
    }, &box);
    pthread_attr_destroy(&attr);
    if (rc != 0) throw std::runtime_error("pthread_create failed: " + std::to_string(rc));
    pthread_join(th, nullptr);
    if (box.err) std::rethrow_exception(box.err);
}

/// Death test: run fn in a forked child.  Returns true when the child finished normally (fn returned), false when it
/// crashed, was killed by a signal (stack overflow = SIGSEGV/SIGBUS), exited non-zero or timed out.
inline bool child_survives(const std::function<void()>& fn, unsigned timeout_seconds = 20) {
    std::cout.flush();
    std::cerr.flush();
    pid_t pid = fork();
    if (pid < 0) throw std::runtime_error("fork failed");
    if (pid == 0) {
        int devnull = open("/dev/null", O_WRONLY);
        if (devnull >= 0) { dup2(devnull, 1); dup2(devnull, 2); }
        alarm(timeout_seconds);
        try { fn(); } catch (...) { _exit(43); }
        _exit(42);
    }
    int status = 0;
    while (waitpid(pid, &status, 0) < 0 && errno == EINTR) {}
    return WIFEXITED(status) && WEXITSTATUS(status) == 42;
}

/// An exception escaping a std::thread body calls std::terminate and kills the whole test binary.  Spawn test threads
/// through ThreadErrors::spawn: exceptions are recorded and reported by CHECK_NO_THREAD_ERRORS after the join.
class ThreadErrors {
public:
    template <class F> std::thread spawn(F f) {
        return std::thread([this, f = std::move(f)]() mutable {
            try { f(); }
            catch (const std::exception& e) { record(e.what()); }
            catch (...) { record("non-std exception"); }
        });
    }
    void record(const std::string& what) { std::lock_guard<std::mutex> g(m_); msgs_.push_back(what); }
    std::string first() const { std::lock_guard<std::mutex> g(m_); return msgs_.empty() ? std::string() : msgs_.front(); }
    bool empty() const { std::lock_guard<std::mutex> g(m_); return msgs_.empty(); }
private:
    mutable std::mutex m_;
    std::vector<std::string> msgs_;
};

// ---------------------------------------------------------------------------------------------- runner
struct Options {
    std::vector<std::string> tags, exclude, require;
    std::string name;
    bool list = false, allow_empty = false, quiet = false;
};

inline bool selected(const TestCase& t, const Options& o) {
    if (!o.name.empty() && std::string_view(t.name).find(o.name) == std::string_view::npos) return false;
    for (const auto& x : o.exclude) if (has_tag(t.tags, x)) return false;
    for (const auto& x : o.require) if (!has_tag(t.tags, x)) return false;
    if (o.tags.empty()) return true;
    for (const auto& x : o.tags) if (has_tag(t.tags, x)) return true;
    return false;
}

inline int run_main(int argc, char** argv) {
    Options o;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        auto next = [&]() -> std::string { return i + 1 < argc ? argv[++i] : std::string(); };
        if (a == "--tag") o.tags.push_back(next());
        else if (a == "--exclude-tag") o.exclude.push_back(next());
        else if (a == "--require-tag") o.require.push_back(next());
        else if (a == "--name") o.name = next();
        else if (a == "--list") o.list = true;
        else if (a == "--allow-empty") o.allow_empty = true;
        else if (a == "-q") o.quiet = true;
        else { std::cerr << "unknown argument " << a << "\n"; return 64; }
    }
    int total = 0, passed = 0;
    long long checks = 0;
    for (const auto& t : registry()) {
        if (!selected(t, o)) continue;
        if (o.list) { std::cout << t.name << " " << t.tags << "\n"; continue; }
        ++total;
        ctx() = Ctx{};
        auto t0 = std::chrono::steady_clock::now();
        try { t.fn(); }
        catch (const AbortTest&) {}
        catch (const std::exception& e) { fail(t.file, t.line, std::string("uncaught exception: ") + e.what()); }
        catch (...) { fail(t.file, t.line, "uncaught non-std exception"); }
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - t0).count();
        checks += ctx().checks;
        bool ok = ctx().failed_checks == 0;
        passed += ok;
        if (!ok || !o.quiet) std::cout << (ok ? "  PASS " : "  FAIL ") << t.name << " [" << t.tags << "] " << ms << " ms\n";
        for (const auto& m : ctx().messages) std::cout << "      " << m << "\n";
        if (ctx().failed_checks > static_cast<int>(ctx().messages.size()))
            std::cout << "      ... and " << ctx().failed_checks - static_cast<int>(ctx().messages.size()) << " more failed checks\n";
    }
    if (o.list) return 0;
    std::cout << "SUMMARY total=" << total << " passed=" << passed << " failed=" << total - passed << " checks=" << checks << "\n";
    if (total == 0) return o.allow_empty ? 0 : 2;
    return total == passed ? 0 : 1;
}

}  // namespace mt

#define MT_MAIN() int main(int argc, char** argv) { return ::mt::run_main(argc, argv); }

#define TEST(name, tags)                                                                  \
    static void name();                                                                   \
    static ::mt::Registrar mt_registrar_##name{#name, tags, &name, __FILE__, __LINE__};   \
    static void name()

#define MT_MSG(...) (std::string() __VA_OPT__(+ std::string(__VA_ARGS__)))

#define CHECK(cond, ...)                                                                              \
    do {                                                                                              \
        ++::mt::ctx().checks;                                                                         \
        if (!(cond)) ::mt::fail(__FILE__, __LINE__, "CHECK(" #cond ") " + MT_MSG(__VA_ARGS__));       \
    } while (0)

#define REQUIRE(cond, ...)                                                                            \
    do {                                                                                              \
        ++::mt::ctx().checks;                                                                         \
        if (!(cond)) {                                                                                \
            ::mt::fail(__FILE__, __LINE__, "REQUIRE(" #cond ") " + MT_MSG(__VA_ARGS__));              \
            throw ::mt::AbortTest{};                                                                  \
        }                                                                                             \
    } while (0)

#define MT_BINARY(opname, pred, a, b, ...)                                                            \
    do {                                                                                              \
        ++::mt::ctx().checks;                                                                         \
        const auto mt_a = (a); /* by value: `f()[0].x` would dangle if bound to a reference */      \
        const auto mt_b = (b);                                                                        \
        if (!(pred(mt_a, mt_b)))                                                                      \
            ::mt::fail(__FILE__, __LINE__,                                                            \
                       std::string(opname " ") + #a " vs " #b "\n        left:  " + ::mt::show(mt_a)  \
                           + "\n        right: " + ::mt::show(mt_b) + " " + MT_MSG(__VA_ARGS__));     \
    } while (0)

#define MT_EQ(x, y) ::mt::eq((x), (y))
#define MT_NE(x, y) (!::mt::eq((x), (y)))
#define MT_LT(x, y) ::mt::lt((x), (y))
#define MT_LE(x, y) (!::mt::lt((y), (x)))
#define MT_GT(x, y) ::mt::lt((y), (x))
#define MT_GE(x, y) (!::mt::lt((x), (y)))

#define CHECK_EQ(a, b, ...) MT_BINARY("expected ==", MT_EQ, a, b, __VA_ARGS__)
#define CHECK_NE(a, b, ...) MT_BINARY("expected !=", MT_NE, a, b, __VA_ARGS__)
#define CHECK_LT(a, b, ...) MT_BINARY("expected <", MT_LT, a, b, __VA_ARGS__)
#define CHECK_LE(a, b, ...) MT_BINARY("expected <=", MT_LE, a, b, __VA_ARGS__)
#define CHECK_GT(a, b, ...) MT_BINARY("expected >", MT_GT, a, b, __VA_ARGS__)
#define CHECK_GE(a, b, ...) MT_BINARY("expected >=", MT_GE, a, b, __VA_ARGS__)

#define REQUIRE_EQ(a, b, ...)                                                                         \
    do {                                                                                              \
        const int mt_before = ::mt::ctx().failed_checks;                                              \
        CHECK_EQ(a, b, __VA_ARGS__);                                                                  \
        if (::mt::ctx().failed_checks != mt_before) throw ::mt::AbortTest{};                          \
    } while (0)

#define CHECK_NEAR(a, b, eps)                                                                         \
    do {                                                                                              \
        ++::mt::ctx().checks;                                                                         \
        const double mt_a = (a), mt_b = (b);                                                          \
        if (!(std::fabs(mt_a - mt_b) <= (eps)))                                                       \
            ::mt::fail(__FILE__, __LINE__, std::string("expected |") + #a " - " #b "| <= " #eps       \
                       + ", got " + std::to_string(mt_a) + " vs " + std::to_string(mt_b));            \
    } while (0)

#define CHECK_THROWS_AS(expr, ExType, ...)                                                            \
    do {                                                                                              \
        ++::mt::ctx().checks;                                                                         \
        try {                                                                                         \
            (void)(expr);                                                                             \
            ::mt::fail(__FILE__, __LINE__, "expected " #ExType " from " #expr ", nothing thrown "     \
                       + MT_MSG(__VA_ARGS__));                                                        \
        } catch (const ExType&) {                                                                     \
        } catch (const std::exception& mt_e) {                                                        \
            ::mt::fail(__FILE__, __LINE__, "expected " #ExType " from " #expr ", got "                \
                       + std::string(typeid(mt_e).name()) + ": " + mt_e.what());                      \
        } catch (...) {                                                                               \
            ::mt::fail(__FILE__, __LINE__, "expected " #ExType " from " #expr ", got a non-std exception"); \
        }                                                                                             \
    } while (0)

#define CHECK_NOTHROW(expr)                                                                           \
    do {                                                                                              \
        ++::mt::ctx().checks;                                                                         \
        try { (void)(expr); }                                                                         \
        catch (const std::exception& mt_e) {                                                          \
            ::mt::fail(__FILE__, __LINE__, "unexpected exception from " #expr ": " + std::string(mt_e.what())); \
        } catch (...) { ::mt::fail(__FILE__, __LINE__, "unexpected non-std exception from " #expr); } \
    } while (0)

#define CHECK_NO_THREAD_ERRORS(errs) CHECK((errs).empty(), "exception in a test thread: " + (errs).first())

/// CHECK_WITHIN_MS(2000, stmt; stmt;) — fail when the statements take longer than the limit.  Only meaningful in the
/// optimised, sanitizer-free binary; tests tagged `perf` are run there by tools/cpptest.py.
#define CHECK_WITHIN_MS(limit_ms, ...)                                                                \
    do {                                                                                              \
        ++::mt::ctx().checks;                                                                         \
        const auto mt_t0 = std::chrono::steady_clock::now();                                          \
        __VA_ARGS__                                                                                   \
        const auto mt_ms = std::chrono::duration_cast<std::chrono::milliseconds>(                     \
                               std::chrono::steady_clock::now() - mt_t0).count();                     \
        if (mt_ms > (limit_ms))                                                                       \
            ::mt::fail(__FILE__, __LINE__, "took " + std::to_string(mt_ms) + " ms, limit "            \
                       + std::to_string(limit_ms) + " ms");                                           \
    } while (0)
