import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

/**
 * J17 例 3：调用 C 函数（downcall）。不写 JNI、不写 C 代码，直接调 libc 的 strlen 和 getpid。
 * 运行（JDK 21）：java --enable-preview --enable-native-access=ALL-UNNAMED J17Ex3
 * 不带 --enable-native-access 会打印警告；JDK 24 起默认就会警告，更晚版本可能直接拒绝。
 */
public class J17Ex3 {
    public static void main(String[] args) throws Throwable {
        Linker linker = Linker.nativeLinker();
        SymbolLookup libc = linker.defaultLookup();                 // 平台的标准 C 库

        MethodHandle strlen = linker.downcallHandle(
                libc.find("strlen").orElseThrow(),
                FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));   // size_t strlen(const char*)
        MethodHandle getpid = linker.downcallHandle(
                libc.find("getpid").orElseThrow(),
                FunctionDescriptor.of(ValueLayout.JAVA_INT));                         // pid_t getpid(void)

        try (Arena arena = Arena.ofConfined()) {
            MemorySegment cStr = arena.allocateUtf8String("AAPL.O");  // JDK 21 的名字；JDK 22 起改名 allocateFrom
            long len = (long) strlen.invokeExact(cStr);
            System.out.println("strlen(\"AAPL.O\") = " + len);
        }
        int pid = (int) getpid.invokeExact();
        System.out.println("getpid() == ProcessHandle.current().pid() ? " + (pid == ProcessHandle.current().pid()));
    }
}
