// Virtual memory is lazy; fork gives a separate address space, threads share one.
#include <cstdio>
#include <cstdlib>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <thread>
#include <unistd.h>

static long faults() { rusage ru{}; getrusage(RUSAGE_SELF, &ru); return ru.ru_minflt; }
static long rss_mb() { rusage ru{}; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / (1024 * 1024); }   // bytes on macOS

int main() {
    const std::size_t size = 512UL << 20;                         // 512 MB of address space
    const std::size_t page = static_cast<std::size_t>(sysconf(_SC_PAGESIZE));
    long f0 = faults();
    char* p = static_cast<char*>(mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0));
    long f1 = faults();
    std::printf("after mmap(512 MB): page faults +%ld, max RSS %ld MB\n", f1 - f0, rss_mb());
    for (std::size_t i = 0; i < size; i += page) p[i] = 1;        // touch one byte per page
    long f2 = faults();
    std::printf("after touching every page: page faults +%ld (= %zu pages), max RSS %ld MB\n", f2 - f1, size / page, rss_mb());

    int value = 1;
    pid_t pid = fork();
    if (pid == 0) { value = 99; _exit(value == 99 ? 0 : 1); }     // child changes its own copy
    int status = 0; waitpid(pid, &status, 0);
    std::printf("after fork+child write: parent value = %d (separate address space)\n", value);
    std::thread t([&] { value = 42; });
    t.join();
    std::printf("after thread write    : value = %d (shared address space)\n", value);
    std::printf("page size = %zu bytes\n", page);
    munmap(p, size);
}
