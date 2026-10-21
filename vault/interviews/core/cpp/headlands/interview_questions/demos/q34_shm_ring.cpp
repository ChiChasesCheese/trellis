// Shared memory between two processes: shm_open + mmap, with a lock-free SPSC ring inside.
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <fcntl.h>
#include <new>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

struct Ring {                                         // only plain data + atomics: no pointers, no std::string
    static constexpr std::uint32_t N = 1024;          // power of two
    alignas(64) std::atomic<std::uint32_t> head{0};   // written by consumer
    alignas(64) std::atomic<std::uint32_t> tail{0};   // written by producer
    alignas(64) std::int64_t slots[N];
};
static_assert(std::atomic<std::uint32_t>::is_always_lock_free, "must be lock-free to work across processes");

int main() {
    const char* name = "/kq_ring_demo";
    shm_unlink(name);
    int fd = shm_open(name, O_CREAT | O_RDWR, 0600);
    if (fd < 0 || ftruncate(fd, sizeof(Ring)) != 0) { std::perror("shm"); return 1; }
    void* mem = mmap(nullptr, sizeof(Ring), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    Ring* r = new (mem) Ring;                          // construct the atomics in shared memory
    const int COUNT = 1'000'000;

    pid_t pid = fork();
    if (pid == 0) {                                    // child = producer
        for (std::int64_t i = 1; i <= COUNT; ++i) {
            std::uint32_t t = r->tail.load(std::memory_order_relaxed);
            while (t - r->head.load(std::memory_order_acquire) == Ring::N) {}      // full: spin
            r->slots[t & (Ring::N - 1)] = i;
            r->tail.store(t + 1, std::memory_order_release);                       // publish
        }
        _exit(0);
    }
    std::int64_t sum = 0;                              // parent = consumer
    for (int got = 0; got < COUNT; ) {
        std::uint32_t h = r->head.load(std::memory_order_relaxed);
        if (h == r->tail.load(std::memory_order_acquire)) continue;                // empty: spin
        sum += r->slots[h & (Ring::N - 1)];
        r->head.store(h + 1, std::memory_order_release);
        ++got;
    }
    waitpid(pid, nullptr, 0);
    std::printf("consumer summed %lld (expected %lld)\n", static_cast<long long>(sum), static_cast<long long>(COUNT) * (COUNT + 1) / 2);
    munmap(mem, sizeof(Ring));
    close(fd);
    shm_unlink(name);
}
