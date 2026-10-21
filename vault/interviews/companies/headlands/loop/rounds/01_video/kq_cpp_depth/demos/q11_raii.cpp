// RAII: constructor acquires, destructor releases - on every exit path, in reverse order.
#include <cstdio>
#include <mutex>
#include <stdexcept>

class FileHandle {
    std::FILE* f_;
public:
    explicit FileHandle(const char* path) : f_(std::fopen(path, "w")) {
        if (!f_) throw std::runtime_error("open failed");
        std::printf("  open %s\n", path);
    }
    ~FileHandle() { if (f_) { std::fclose(f_); std::printf("  close\n"); } }
    FileHandle(const FileHandle&) = delete;                   // one owner
    FileHandle& operator=(const FileHandle&) = delete;
    void write(const char* s) { std::fputs(s, f_); }
};

struct Noisy {
    const char* name;
    explicit Noisy(const char* n) : name(n) { std::printf("  ctor %s\n", name); }
    ~Noisy() { std::printf("  dtor %s\n", name); }
};

std::mutex m;
void work(bool fail) {
    Noisy a("a");
    std::lock_guard<std::mutex> g(m);                         // unlocks on every path
    Noisy b("b");
    FileHandle fh("/tmp/kq_raii.txt");
    fh.write("hello\n");
    if (fail) throw std::runtime_error("boom");
    std::printf("  normal return\n");
}

int main() {
    std::printf("normal path:\n");
    work(false);
    std::printf("exception path:\n");
    try { work(true); } catch (const std::exception& e) { std::printf("caught %s\n", e.what()); }
    std::printf("mutex is free again: %s\n", m.try_lock() ? "yes" : "no");
    m.unlock();
}
