// The ABA problem on a lock-free free list, replayed step by step on ONE thread so that the interleaving is exactly the unlucky one.
// Thread A starts a pop and is suspended; thread B pops two slots and pushes the first one back; thread A resumes.
#include <cstdint>
#include <iostream>
#include <vector>

constexpr std::uint32_t EMPTY = 0xFFFFFFFFu;

struct Stack {
    std::vector<std::uint32_t> next;
    std::uint64_t head;  // high 32 bits: tag, low 32 bits: top slot
    bool use_tag;

    static std::uint64_t pack(std::uint32_t tag, std::uint32_t index) { return (static_cast<std::uint64_t>(tag) << 32) | index; }
    std::uint32_t top() const { return static_cast<std::uint32_t>(head); }
    std::uint32_t tag() const { return static_cast<std::uint32_t>(head >> 32); }
    std::uint64_t next_head(std::uint32_t index) const { return pack(use_tag ? tag() + 1 : 0, index); }

    explicit Stack(bool tagged) : next{1, 2, EMPTY}, head(pack(0, 0)), use_tag(tagged) {}  // list: 0 -> 1 -> 2

    std::uint32_t pop() {
        const std::uint32_t i = top();
        head = next_head(next[i]);
        return i;
    }
    void push(std::uint32_t i) {
        next[i] = top();
        head = next_head(i);
    }
    // compare-and-swap, written out
    bool cas(std::uint64_t expected, std::uint64_t desired) {
        if (head != expected) return false;
        head = desired;
        return true;
    }
};

void replay(bool tagged) {
    Stack s(tagged);
    // Thread A: begins pop().  Reads head (slot 0) and next[0] (= 1).  Then it is suspended before the CAS.
    const std::uint64_t seen_head = s.head;
    const std::uint32_t a_slot = s.top(), a_below = s.next[a_slot];

    // Thread B: pop() -> slot 0, pop() -> slot 1 (B now owns both), then push(0) back.
    const std::uint32_t b0 = s.pop(), b1 = s.pop();
    s.push(b0);
    std::cout << (tagged ? "with tag   " : "without tag") << ": B owns slot " << b1 << "; free list top is slot " << s.top() << ", next[0] = " << s.next[0] << "\n";

    // Thread A resumes: CAS(head: seen -> slot a_below).  Looks unchanged if the head is only the slot number.
    const bool ok = s.cas(seen_head, Stack::pack(tagged ? s.tag() + 1 : 0, a_below));
    if (ok)
        std::cout << "   A's CAS SUCCEEDED -> head = slot " << s.top() << ", which B still owns: the next allocate hands slot " << s.top() << " out twice\n";
    else
        std::cout << "   A's CAS failed (the tag moved from " << (seen_head >> 32) << " to " << s.tag() << "): A re-reads and retries\n";
}

int main() {
    replay(false);
    replay(true);
}
