// Which language standard is the compiler using? Compile once per -std and compare.
#include <cstdio>
int main() {
    std::printf("__cplusplus = %ldL\n", static_cast<long>(__cplusplus));
#if __cplusplus >= 202002L
    std::printf("concepts: %s\n", "yes");
#endif
#if defined(__cpp_generic_lambdas)
    std::printf("generic lambdas (14): yes\n");
#endif
#if defined(__cpp_structured_bindings)
    std::printf("structured bindings (17): yes\n");
#endif
#if defined(__cpp_concepts)
    std::printf("__cpp_concepts = %ld\n", static_cast<long>(__cpp_concepts));
#endif
#if defined(__cpp_deduction_guides)
    std::printf("CTAD (17): yes\n");
#endif
}
