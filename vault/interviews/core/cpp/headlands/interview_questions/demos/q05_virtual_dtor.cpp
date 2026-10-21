// A base class used polymorphically needs a virtual destructor.
// (Deleting through the non-virtual base is undefined behaviour; this shows what typically happens.)
#include <cstdio>

struct BadBase { ~BadBase() { std::printf("  ~BadBase\n"); } };
struct BadDerived : BadBase { ~BadDerived() { std::printf("  ~BadDerived\n"); } };

struct GoodBase { virtual ~GoodBase() { std::printf("  ~GoodBase\n"); } };
struct GoodDerived : GoodBase { ~GoodDerived() override { std::printf("  ~GoodDerived\n"); } };

int main() {
    std::printf("non-virtual destructor, delete via Base*:\n");
    BadBase* b = new BadDerived;
    delete b;
    std::printf("virtual destructor, delete via Base*:\n");
    GoodBase* g = new GoodDerived;
    delete g;
}
