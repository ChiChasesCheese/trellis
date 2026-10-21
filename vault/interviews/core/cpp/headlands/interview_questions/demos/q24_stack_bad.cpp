// EXPECTED TO FAIL under ASan: stack buffer overflow and returning the address of a local.
#include <cstdio>
#include <cstring>
int main(int argc, char**) {
    char name[8];
    std::strcpy(name, argc == 1 ? "much too long for eight bytes" : "ok");
    std::printf("%s\n", name);
}
