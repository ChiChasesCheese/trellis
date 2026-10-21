// Not an error by default - a warning. Falling off the end of a non-void function is undefined behaviour.
int sign(int x) {
    if (x > 0) return 1;
    if (x < 0) return -1;
}
int main() { return sign(0); }
