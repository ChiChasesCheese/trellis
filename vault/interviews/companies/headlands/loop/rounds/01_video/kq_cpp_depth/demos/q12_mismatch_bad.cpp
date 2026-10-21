// EXPECTED TO FAIL under ASan: new[] released with delete (and the converse with malloc/delete).
int main() {
    int* a = new int[10];
    delete a;            // must be delete[]
}
