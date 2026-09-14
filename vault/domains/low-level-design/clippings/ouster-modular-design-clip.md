---
title: Modular Design
source: https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign
published: '2000-01-01'
site: web.stanford.edu
clipped: '2026-08-15'
---

# Modular Design

# Modular Design

  Lecture Notes for CS 190

  Winter 2018

  John Ousterhout

- Reading: Chapters 4-7, 14 of book

- How to minimize dependencies?

## Modular Design 

- Divide system into *modules* that are relatively independent
- Ideal: each module completely independent of the others
  
  - System complexity = complexity of worst module
  
- In reality, modules are not completely independent
  
  - Some modules must invoke facilities in other modules
  
  - Design decisions in one module must sometimes be known to other
    modules
  
  - Can't change one module without understanding parts of
    other modules
  
- Divide each module into two parts:
  
  - *Interface* : anything about the module that
    must be known to other modules
    - Formal aspects (in the code): method signatures, public variables,
      etc.
    
    - Informal aspects: overall behavior, side effects, constraints
      on usage, etc.
    
    - Informal aspects can only be described with comments
    
  - *Implementation* : code that carries out the promises made
    by the interface
- Goal: interface should be much simpler than the implementation
  
  - If a change affects only a module's implementation, but not
    its interface, then it will not affect any other module
  

## Abstraction

- A simplified view of something that omits unimportant details
- Interface: abstraction of a module
- Goal: define simple abstractions that provide rich functionality

## Classes Should be Deep

- Deep class: small interface, lots of functionality
  
  - Lots of information hidden
  
- Example: Unix system calls for file I/O
- Shallow class
  
  - Complex interface and/or not much functionality
  
  - Invoking a method isn't much easier than just typing in the code
    of the method.
  
  - Shallow classes don't hide much information
  
  - Example: linked list
  
   - Also see [User.java](downloads/User.java)
  - Every class and method introduces complexity with its
    interface
  
  - Goal: get a lot of functionality for that complexity
  
  - If a class is shallow, you have to spend a lot of time
    learning the interface, compared to how much time the
    class saves you.
  
- Many courses teach students that "classes should be small":
  results in shallow classes.
- Classitis: small classes taken to the extreme
  
  - Each class adds the least possible amount of functionality to
    existing classes
  
  - Bad example: Java libraries
  
- Size doesn't really matter that much
  
  - Classes in the range of 200-2000 lines are fine
  
  - The most important thing is depth: the power of the abstraction
  
- It's more important for a class to have a simple interface than
  a simple implementation

## Information Hiding

- First proposed by David Parnas in a classic paper
  "[On
    the Criteria To Be Used in Decomposing Systems into Modules](https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf) "
  - More than 40 years old, but still one of the most important papers
    in all of systems.
  
- Each module (class) should encapsulate certain knowledge or design
  decisions:
- The knowledge/design decisions are only known to the one module
- The interface does not reflect this information (much)
- Benefits:
  
  - Simpler interface (deeper class)
  
  - Can modify the implementation without impacting other classes
  
- This is the single most important idea in software design; will revisit
  it over and over.
- Information leakage: opposite of information hiding
  
  - Implementation details exposed, other classes depend on them
  
  - Anything in the interface is leaked
  
  - Back-door leakage: not visible in the interface
  
- Temporal decomposition: one of the most common causes of information
  leakage
  
  - Code structure reflects the *order* in which operations execute
- Using classes does not necessarily guarantee information hiding!
  
  - Example: private variables can still be leaked
  
- When you see information leakage, look for a way to bring all the
  information together in one place
- Making classes a bit larger often creates opportunities for better
  information hiding

- Questions to ask yourself:
  
  - What is the unique value provided by this class (something this class
    does, but no other class)?
  
  - What is the key knowledge that the class uses to provide
    that value?
  
  - What's the least possible amount of that knowledge that must be
    exposed through the interface?
  

## Generic Classes are Deeper

- Should new classes be general-purpose or special-purpose?
  
  - Special-purpose: just do exactly what's needed today
  
  - General-purpose: solve a range of problems that may in the future
  
- My advice: make classes *somewhat generic* :
  - Overall capabilities reflect current needs
  
  - Design an interface that is generic enough to be used for other
    purposes besides today's needs
  
  - Result: simpler and deeper interface than special-purpose approach
  
- Example from text editor project
- Questions to ask yourself:
  
  - What is the simplest API that will cover all of my current needs?
  
  - In how many situations will this method be used?
  
  - Is this API convenient to use for my current needs?
  

## New Layer, New Abstraction

- Each layer's abstraction should be different from the layer above it and
  the layer below it.
- Red flag: pass-through methods
  
  - Decide *what's important* , design the interface around that
    - Focus on the things that are done most frequently
    
    - Technique #1: if a particular task is invoked repeatedly,
      design an API around that task (even better, do it automatically,
      without having to be invoked).
    
    - Technique #2: if a collection of tasks are not identical,
      look for common features shared by all of them; design
      APIs for the common features.
    
    - It's OK to provide APIs for infrequently-used features,
      but design them in a way that you don't need to be
      aware of them when using the common features.
    
- Bad example: Java I/O
- Good example: device-independent I/O in UNIX/Linux:
  
  - Before UNIX: different kernel calls for opening and accessing
    files vs. devices.
    
    - Different kernel calls for each device: terminal, tape, etc.
    
    - Different naming mechanisms for each device
    
  - UNIX emphasized commonality across devices:
    
    - Devices have names in the file system: special device files
    
    - All devices have same basic access structure: open, read,
      write, seek, close
    
    - Handle device-specific operations with one additional kernel
      call:
      ```
int result = ioctl(int fd, int request,
        void* inBuffer, int inputSize,
        void* outBuffer, int outputSize);
```

- How much to plan ahead?
  
  - "Should I implement extra features beyond those that I need today?
  
  - Design facilities that are general-purpose when possible
    (but don't get carried away)
  
  - Don't create a lot of specific features that aren't needed now;
    you can always add them later.
  
  - When you discover that new features or a more general architecture
    are needed, do it right away: don't hack around it.
  
- **The Martyr Principle**  - Module writers should embrace suffering:
    
    - Take on hard problems
    
    - Solve completely
    
    - Make solution easy for others to use
    
    - Take more challenges for yourself, so that others have
      fewer issues to deal with
    
  - Pull complexity down into modules:
    
    - Let a few module developers suffer, rather than thousands
      of users
    
    - Simple APIs are more important than a simple implementation
    
  - Solve, don't punt:
    
    - Handle error conditions rather than throwing exceptions
    
    - Minimize "voodoo constants" (configuration parameters)
      
      - If you don't know the right value, how will a user or
        administrator ever figure it out?
      
- Are long methods OK?
  
  - Sometimes: see [TransportDispatcher.cc](downloads/TransportDispatcher.cc) (method consists of relatively independent pieces).
  - Shorter is generally better, but only decompose if it can
    be done cleanly (are there dependencies between the parts?).
  
- Applying These Ideas
  
  - May be hard initially to apply these ideas when writing code.
  
  - Make 2 designs and compare
  
  - Pick one and write some code
  
  - Watch for red flags
  
  - Revise code
  
  - Take advantage of code reviews
