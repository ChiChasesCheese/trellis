// sizeof, alignof, padding, reordering fields, cache-line alignment.
#include <cstddef>
#include <cstdint>
#include <cstdio>

struct Bad  { char a; double b; char c; int d; };             // padding between and after
struct Good { double b; int d; char a; char c; };             // largest first
struct Packed4 { std::uint8_t side : 1; std::uint8_t kind : 3; std::uint8_t pad : 4; };
struct alignas(64) Line { std::int64_t v; };                  // one value per 64-byte line
struct Empty {};

int main() {
    std::printf("Bad : size=%zu align=%zu  offsets a=%zu b=%zu c=%zu d=%zu\n", sizeof(Bad), alignof(Bad),
                offsetof(Bad, a), offsetof(Bad, b), offsetof(Bad, c), offsetof(Bad, d));
    std::printf("Good: size=%zu align=%zu  offsets b=%zu d=%zu a=%zu c=%zu\n", sizeof(Good), alignof(Good),
                offsetof(Good, b), offsetof(Good, d), offsetof(Good, a), offsetof(Good, c));
    std::printf("bitfield struct: %zu byte\n", sizeof(Packed4));
    std::printf("alignas(64) Line: size=%zu align=%zu\n", sizeof(Line), alignof(Line));
    std::printf("Empty: %zu, long: %zu, void*: %zu, long double: %zu, bool: %zu\n", sizeof(Empty), sizeof(long), sizeof(void*), sizeof(long double), sizeof(bool));
    Line arr[2];
    std::printf("arr[1]-arr[0] = %td bytes\n", reinterpret_cast<char*>(&arr[1]) - reinterpret_cast<char*>(&arr[0]));
}
