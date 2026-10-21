// C01: RAII. Acquire in the constructor, release in the destructor; Java's try-with-resources, but for EVERYTHING
// and the compiler applies it automatically at every exit path.
#include <cstdio>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <string>

// [[snip:file]]
class File {
    std::FILE* f_;
public:
    File(const char* path, const char* mode) : f_(std::fopen(path, mode)) {
        if (!f_) throw std::runtime_error(std::string("cannot open ") + path);
    }
    ~File() { if (f_) { std::fclose(f_); std::cout << "  file closed\n"; } }
    File(const File&) = delete;                 // two owners of one FILE* would double-close
    File& operator=(const File&) = delete;
    std::FILE* get() const { return f_; }
};
// [[/snip]]

// [[snip:guard]]
template <class F>
class ScopeGuard {                              // run an arbitrary cleanup at scope exit (Go: defer)
    F fn_;
    bool active_ = true;
public:
    explicit ScopeGuard(F fn) : fn_(std::move(fn)) {}
    ~ScopeGuard() { if (active_) fn_(); }
    void dismiss() { active_ = false; }         // "commit": cancel the cleanup
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};
// [[/snip]]

// [[snip:use]]
int read_first_line_length(const char* path) {
    File file(path, "r");                       // throws if missing: nothing to clean up yet
    char buf[256];
    if (!std::fgets(buf, sizeof buf, file.get())) throw std::runtime_error("empty file");
    return static_cast<int>(std::string(buf).size());
}                                               // every return and every throw closes the file

std::mutex m;
int counter = 0;

void locked_increment() {
    std::lock_guard<std::mutex> lock(m);        // Java: synchronized (m) { ... }
    ++counter;
    if (counter > 100) throw std::runtime_error("too big");   // the mutex is still released
}
// [[/snip]]

int main() {
    try { read_first_line_length("/definitely/not/here"); }
    catch (const std::exception& e) { std::cout << "error: " << e.what() << "\n"; }

    std::FILE* tmp = std::fopen("/tmp/c01_raii_demo.txt", "w");
    std::fputs("hello raii\n", tmp);
    std::fclose(tmp);
    int len = read_first_line_length("/tmp/c01_raii_demo.txt");
    std::cout << "length = " << len << "\n";

    {
        bool committed = false;
        ScopeGuard g([&] { std::cout << "  rollback (guard fired)\n"; });
        if (committed) g.dismiss();
    }
    {
        ScopeGuard g([&] { std::cout << "  rollback (should not print)\n"; });
        g.dismiss();
        std::cout << "  committed, guard dismissed\n";
    }
    locked_increment();
    std::cout << "counter = " << counter << "\n";
}
