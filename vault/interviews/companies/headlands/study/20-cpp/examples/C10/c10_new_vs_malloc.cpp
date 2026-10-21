// RUN: ASAN_OPTIONS=allocator_may_return_null=1 $BIN
// C10: new/delete vs malloc/free. malloc hands out raw bytes; new = operator new (raw bytes) + constructor call.
#include <cstdlib>
#include <iostream>
#include <new>
#include <string>

// [[snip:replace]]
// operator new is an ordinary replaceable function. Here: refuse absurd sizes the way a real out-of-memory would
// (the sanitizer's own allocator would abort instead of throwing, and we want to show the standard behaviour).
void* operator new(std::size_t n) {
    if (n > (static_cast<std::size_t>(1) << 40)) throw std::bad_alloc();
    if (void* p = std::malloc(n)) return p;
    throw std::bad_alloc();
}
void* operator new[](std::size_t n) { return operator new(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
// [[/snip]]

struct Widget {
    std::string name = "default-name-longer-than-sso-buffer";
    Widget() { std::cout << "  Widget ctor\n"; }
    ~Widget() { std::cout << "  Widget dtor\n"; }
};

int main() {
    // [[snip:malloc]]
    std::cout << "[malloc]\n";
    void* raw = std::malloc(sizeof(Widget));        // raw bytes only: NO constructor ran
    std::cout << "  malloc returned " << (raw ? "non-null" : "null") << ", no ctor message above\n";
    // Widget* bad = static_cast<Widget*>(raw); bad->name.size();   // UB: no Widget exists there, name is garbage
    std::free(raw);                                 // no destructor either
    // [[/snip]]

    // [[snip:new]]
    std::cout << "[new / delete]\n";
    Widget* w = new Widget;                         // operator new(sizeof(Widget)), then Widget::Widget()
    std::cout << "  name length " << w->name.size() << "\n";
    delete w;                                       // Widget::~Widget(), then operator delete
    // [[/snip]]

    // [[snip:array]]
    std::cout << "[new[] / delete[]]\n";
    Widget* arr = new Widget[2];                    // two constructors; the count is remembered for delete[]
    delete[] arr;                                   // two destructors (plain delete here would be UB)
    // [[/snip]]

    // [[snip:failure]]
    std::cout << "[failure behaviour]\n";
    std::size_t huge = static_cast<std::size_t>(-1) / 2;          // about 8 EiB: no machine has it
    void* volatile sink = nullptr;                  // storing into a volatile stops the optimiser from deleting the allocation
    void* m = std::malloc(huge);
    sink = m;
    std::cout << "  malloc(8 EiB) -> " << (m ? "non-null" : "NULL (you must check)") << "\n";
    try { char* c = new char[huge]; sink = c; delete[] c; std::cout << "  new succeeded?\n"; }
    catch (const std::bad_alloc&) { std::cout << "  new char[8 EiB] -> threw std::bad_alloc\n"; }
    char* nt = new (std::nothrow) char[huge];                     // nothrow form: returns nullptr like malloc
    sink = nt;
    void* seen = sink;                                            // read it back so the volatile is used
    (void)seen;
    std::cout << "  new(std::nothrow) -> " << (nt ? "non-null" : "nullptr") << "\n";
    // [[/snip]]
}
