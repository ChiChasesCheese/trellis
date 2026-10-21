// EXPECT: run-fail
// C11: memcpy of a non-trivially-copyable type: both objects now "own" the same heap buffer.
#include <cstring>
#include <iostream>
#include <string>
#include <new>

int main() {
    std::string a(100, 'x');                       // too long for SSO: heap-allocated buffer
    alignas(std::string) unsigned char raw[sizeof(std::string)];
    std::memcpy(raw, &a, sizeof a);                // bitwise copy: raw holds the same pointer as a
    std::string* b = std::launder(reinterpret_cast<std::string*>(raw));
    std::cout << "copy sees " << b->size() << " chars\n";
    b->~basic_string();                            // frees the buffer ...
}                                                  // ... and a's destructor frees it again: double free
