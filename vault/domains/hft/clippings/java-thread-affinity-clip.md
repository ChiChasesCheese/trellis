---
title: 'GitHub - OpenHFT/Java-Thread-Affinity: Bind a java thread to a given core'
source: https://github.com/OpenHFT/Java-Thread-Affinity
published: '2013-09-20'
site: GitHub
clipped: '2026-10-23'
---

# GitHub - OpenHFT/Java-Thread-Affinity: Bind a java thread to a given core

Lets you bind a thread to a given core, this can improve performance (this library works best on linux).

OpenHFT Java Thread Affinity library

See [affinity/src/test/java](https://github.com/OpenHFT/Java-Thread-Affinity/tree/develop/affinity/src/test/java)
for working examples of how to use this library.

The library detects the running platform in `Affinity.java` and selects an implementation for that OS.
Features differ between systems:

- 
**Linux** - full affinity control via JNA.
The implementation can get and set thread affinity, query the current CPU, and obtain process and thread IDs.
- 
**Windows** - thread affinity is managed through the kernel API.
Process and thread IDs are available, while`getCpu()` returns`-1` .
- 
**macOS** - provides process and thread IDs but does not modify affinity and reports the CPU id as`-1` .
- 
**Solaris** - mirrors the macOS implementation: only process and thread IDs are returned with no affinity or CPU querying support.

For detailed release notes and upgrade impact for tagged releases since the start of 2020, see [RELEASE_NOTES.adoc](/OpenHFT/Java-Thread-Affinity/blob/ea/RELEASE_NOTES.adoc).

Java-Thread-Affinity will try to use [JNA](https://github.com/java-native-access/jna)
to provide access to native thread-handling functions.
JNA should be installed on your system to get the most from this library.

Java-Thread-Affinity currently depends on JNA version 4.4.0, which in turn depends on a version of GLIBC >= 2.14. If your operating system is an old one, with a version of GLIBC released before 2011, this library will not be able to invoke native functions.

To work around this problem, fork the repository, and override the `<version>` tag for the artifacts `jna` and `jna-platform` in the project’s `pom` file.

choco install jna

Or download jna.jar and jna-platform.jar from the JNA project and add them to your classpath.

The library will read your `/proc/cpuinfo` if you have one or provide one and it will determine your CPU layout.
If you don’t have one it will assume every CPU is on one CPU socket.

The library looks for isolated CPUs determined by looking at the CPUs you are not running on by default. i.e. if you have 16 CPUs but 8 of them are not available for general use (as determined by the affinity of the process on startup) it will start assigning to those CPUs.

Note: if you have more than one process using this library you need to specify which CPUs the process can use otherwise it will assign the same CPUs to both processes.

To control which CPUs a process can use, add `-Daffinity.reserved={cpu-mask-in-hex}` to the command line of the process.
The mask is a hexadecimal bit mask without the `0x` prefix where bit `0` represents CPU `0`, bit `1` represents CPU `1` and so on.
Multiple CPUs can be specified by setting more than one bit.

For example:

- 
`-Daffinity.reserved=2` reserves only CPU`1` .
- 
`-Daffinity.reserved=6` reserves CPUs`1` and`2` .
- 
`-Daffinity.reserved=10` reserves CPUs`1` and`3` (hexadecimal`a` ).

Use an appropriate mask when starting each process to avoid reserving the same cores for multiple JVMs.

Note: the CPU 0 is reserved for the Operating System, it has to run somewhere.

Java-Thread-Affinity requires that you first isolate some CPU’s.

Once a CPU core is isolated, the Linux scheduler will not use the CPU core to run any user-space processes. The isolated CPUs will not participate in load balancing, and will not have tasks running on them unless explicitly assigned.

To isolate the 1st and 3rd CPU cores (CPU numbers start from 0) on your system, add the following to the kernel command line during boot:

isolcpus=1,3

```
sudo sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="isolcpus=1,3 /' /etc/default/grub
sudo update-grub
sudo reboot
```
```
sudo sed -i 's/^options \(.*\)/options \1 isolcpus=1,3/' /boot/loader/entries/*.conf
sudo reboot
```
You can acquire a lock for a CPU in the following way:

```
AffinityLock al = AffinityLock.acquireLock();
try {
     // do some work locked to a CPU.
} finally {
     al.release();
}
```
```
try (AffinityLock al = AffinityLock.acquireLock()) {
    // do some work while locked to a CPU.
}
```
You have further options such as

You can reserve a whole core. If you have hyper-threading enabled, this will use one CPU and leave it’s twin CPU unused.

```
try (AffinityLock al = AffinityLock.acquireCore()) {
    // do some work while locked to a CPU.
}
```
You can chose a layout relative to an existing lock.

```
try (final AffinityLock al = AffinityLock.acquireLock()) {
    System.out.println("Main locked");
    Thread t = new Thread(new Runnable() {
        @Override
        public void run() {
            try (AffinityLock al2 = al.acquireLock(AffinityStrategies.SAME_SOCKET,
                                                   AffinityStrategies.ANY)) {
                 System.out.println("Thread-0 locked");
            }
        }
    });
    t.start();
}
```
In this example, the library will prefer a free CPU on the same Socket as the first thread, otherwise it will pick any free CPU.

The `AffinityStrategies` enum defines hints for selecting a CPU relative to an existing lock.

| Strategy | Meaning | 
|---|---|
| `ANY` | Use any available CPU. | 
| `SAME_CORE` | Select a CPU on the same core. | 
| `SAME_SOCKET` | Select a CPU on the same socket but a different core. | 
| `DIFFERENT_CORE` | Select a CPU on another core (possibly another socket). | 
| `DIFFERENT_SOCKET` | Select a CPU on a different socket. | 

You can get the current thread id using

`int threadId = AffinitySupport.getThreadId();`
You can get the current CPU being used by

`int cpuId = AffinitySupport.getCpu();`
The affinity of the process on start up is

`long baseAffinity = AffinityLock.BASE_AFFINITY;`
The available CPU for reservation is

`long reservedAffinity = AffinityLock.RESERVED_AFFINITY;`
If you want to get/set the affinity directly you can do

```
long currentAffinity = AffinitySupport.getAffinity();
AffinitySupport.setAffinity(1L << 5); // lock to CPU 5.
```
Several examples print the current CPU assignments using `AffinityLock.dumpLocks()`.
Each line of the output begins with the zero based CPU id followed by the status of that CPU.
Example output might look like:

```
0: Reserved for this application
1: Thread[reader,5,main] alive=true
2: General use CPU
3: CPU not available
```
The number on each line is the logical CPU index as recognised by the library.
The text after the colon describes whether that CPU is free, reserved or already bound to a thread.
Use these indices when calling `AffinityLock.acquireLock(n)`
or when constructing explicit affinity masks.

AffinityLock stores a small lock file for each CPU.
These files are placed in the directory specified by the `java.io.tmpdir` system property, which by default points to your system’s temporary directory (usually `/tmp` on Linux).

If you want to keep the lock files elsewhere, set this property before using any affinity APIs:

`java -Djava.io.tmpdir=/path/to/dir ...`
or in code

`System.setProperty("java.io.tmpdir", "/path/to/dir");`
For a detailed of view of the current affinity state (as seen by the library), execute the following script on Linux systems:

```
# change to the affinity lock-file directory (defaults to system property java.io.tmpdir)
$ cd /tmp
# dump affinity state
$ for i in "$(ls cpu-*)";
      do PID="$(cat $i | head -n1)"; TIMESTAMP="$(cat $i | tail -n1)";
      echo "pid $PID locked at $TIMESTAMP in $i"; taskset -cp $PID;
      cat "/proc/$PID/cmdline"; echo; echo
  done
  pid 14584 locked at 2017.10.30 at 10:33:24 GMT in cpu-3.lock
  pid 14584's current affinity list: 3
  /opt/jdk1.8.0_141/bin/java ...
```
`AffinityThreadFactory` binds each thread it creates according to a set of `AffinityStrategy` rules.
This allows executors to automatically run tasks on cores selected by the library.

```
ExecutorService es = Executors.newFixedThreadPool(4,
        new AffinityThreadFactory("worker",
                AffinityStrategies.SAME_CORE,
                AffinityStrategies.DIFFERENT_SOCKET,
                AffinityStrategies.ANY));
es.submit(() -> {
    // your task here
});
System.out.println("\nThe assignment of CPUs is\n" + AffinityLock.dumpLocks());
```
For an article on how much difference affinity can make and how to use it [https://blog.vanillajava.blog/2013/07/micro-jitter-busy-waiting-and-binding.html](https://blog.vanillajava.blog/2013/07/micro-jitter-busy-waiting-and-binding.html)

I am currently working on a project related to deadlock detection in multithreaded programs in java.
We are trying to run threads on different processors and thus came across your github posts regarding the same. [https://github.com/OpenHFT/Java-Thread-Affinity/wiki/Getting-started](https://github.com/OpenHFT/Java-Thread-Affinity/wiki/Getting-started)
Being a beginner, I have little knowledge and thus need your assistance.
We need to know how to run threads on specified cpu number and then switch threads when one is waiting.

```
// lock a cpuId
try (AffinityLock lock = AffinityLock.acquireLock(n)) {
}
```
where n is the cpu you want to run the thread on.

OR

```
// lock one of the last CPUs
try (AffinityLock lock = AffinityLock.acquireLockLastMinus(n)) {
}
```
I have the cpuId in a configuration file, how can I set it using a string?

```
try (AffinityLock lock = AffinityLock.acquireLock("last")) {
    assertEquals(PROCESSORS - 1, Affinity.getCpu());
}
try (AffinityLock lock = AffinityLock.acquireLock("last-1")) {
    assertEquals(PROCESSORS - 2, Affinity.getCpu());
}
try (AffinityLock lock = AffinityLock.acquireLock("1")) {
    assertEquals(1, Affinity.getCpu());
}
try (AffinityLock lock = AffinityLock.acquireLock("any")) {
    assertTrue(lock.bound);
}
try (AffinityLock lock = AffinityLock.acquireLock("none")) {
    assertFalse(lock.bound);
}
try (AffinityLock lock = AffinityLock.acquireLock((String) null)) {
    assertFalse(lock.bound);
}
try (AffinityLock lock = AffinityLock.acquireLock("0")) { // prints a warning
    assertFalse(lock.bound);
}
```
