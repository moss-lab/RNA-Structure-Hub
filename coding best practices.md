Moss Lab Style Guidelines v0.1

The following document describes good practices to ensure code is legible, easily maintained by future students, and accessible to the wider scientific community.

Underlying reasons why we should write code in this way are given with each guideline, and if in light of that you have a good reason to break one, then do it. These are not absolute rules, just a set of practices that will make your life easier in the long run. Adjustments to these guidelines should be made over time- this is intended to be a living document maintained by and for the entire lab. Language specific requirements/style should take precedence, there isn't a one-sized-fits-all solution.

It should always be assumed that you are writing code that someone else will read, so you should write code for the reader rather than yourself. Even if you don't think this is true, the unexpected can always happen. Writing clean code is also a habit/skill that needs to constantly be practiced to be maintained; don't let yourself fall into bad habits in personal code, they will leak into everything you write!

Resources outside of this guide exist, and provide more in-depth information. Here are a few examples:
Clean code : a handbook of agile software craftsmanship 
Martin, Robert C.; Feathers, Michael C.]
https://quicksearch.lib.iastate.edu/permalink/01IASU_INST/1s27pim/alma9920508983102756
Implementing Effective Code Reviews: How to Build and Maintain Clean Code
Carullo, Giuliana
https://quicksearch.lib.iastate.edu/permalink/01IASU_INST/tuvqkh/cdi_safari_books_v2_9781484261620


1. Comment everything
As a rule of thumb, any line of code beyond trivial arithmetic should have a comment adjacent to it describing what it does, and why it was written that way.
Keep lines short, ideally <100 characters wide. Comments should be on a different line if they can't be fit within that limit, and split up lines if possible if they're too long.
Whenever a line of code is updated, the associated comment should be adjusted at the same time. Comments that are not maintained alongside code are worse than useless. This is part of why it's important to keep comments adjacent to the code they describe.
Carefully document any changes to any code that has documentation written up already so that the associated documentation can be updated as well. When updating a shared repository, give a description of what was changed in that update, even if it's small. Ideally, include the reasoning behind it.

2. Always use clear, unambiguous names
The names of variables, functions, and classes are the first thing a reader sees when trying to figure out what code is doing. It is important that these names clearly reflect the function of what they describe. Ideally the code should describe itself without needing comments (add comments anyway, though, since you can't be sure how clear it will be to the reader).
Names should also be unique to avoid cluttering up the namespace and to reduce ambiguity. You can ignore this when naming methods for a class that perform analagous functions (ie, "append()")
Make names as long as necessary to ensure descriptiveness and uniqueness, but no longer.
Names should be consistent. Keep the same names when using wrappers to expose code to other languages, for example.

3. Prioritise legibility over efficiency
Sometimes you will have the choice between efficient/elegant code, and easy to parse code. In these situations, always make your code as easy to read as possible. For example, if you have a long sequence of if/else-if statements that could be condensed into a few, more complicated ones, leave them in the longer form (but in their own function to avoid cluttering up the screen).
If the performance improvement is significant then this guideline should be broken- this one is the most context dependent.

4. Naming conventions
Different naming conventions should be used for different things, to more easily distinguish them. Here are the conventions I currently use:
Objects/variables are named using snake_case
Functions/methods are named using camelCase
Classes are named using PascalCase

5. Code should be short and encapsulated
Avoid large blocks of code wherever possible. This is hard to read and often leads to objects sticking around when they're no longer used. Instead, decompose large blocks of code into small functions and classes, which are used where that block would have been. This will help you find errors when debugging, help prevent name conflicts (and let you use shorter names), and improve efficiency by ensuring objects do not stick around for longer than they need to.
It will also help with collaborative projects, since one block in the code can be split into more that multiple people can each work on.
In general, functions should be less than 12 lines, not counting comments. Longer blocks can and should usually be decomposed into smaller functions. Keep these smaller functions directly below the function in which they are called to make them easy for the reader to find- spreading a function out over multiple files or different places in a single file makes the code less legible.
Functions should only adjust their behavior based on their arguments, never any state outside of the function. Any function should be fully usable and testable independent of the rest of the program, to make behavior clearer and allow for incremental testing.

6. Most problems have already been solved; don't reinvent the wheel
Very smart people have been developing algorithms to solve problems for decades. Chances are, whatever you need to do can be done through a known and optimized algorithm or heuristic, though you may need to do some thinking to reframe the problem in a way that's already been solved.
Implementing existing algorithms is a useful learning exercise, but should be avoided in actual projects without good reason to do so as there are open-source implementations for almost anything out there already (remember to cite them properly).
Take time to learn about the history of computer science, what tools people have developed and what problems they were trying to solve. It will save more time than you spend on it, and will greatly increase the performance of your code.

7. Use the right tool for the job
Wherever the data structurees that come with the language don't exactly fit with the data you're trying to store, create your own. Within this class, use all tools the language comes with (they will generally have superior performance than any alternative), but ensure that the outwards-facing part of the class follows the structure of what you're trying to store without reflecting the complexity required to finagle it into built-in structures.
Be aware of what you need a data structure to do most often, and what the best choice for that is. For example, any position in an array can be accessed in O(1) but resizing the array requires O(n), whereas linked lists are the opposite. If you expect to search through something often and rarely update it then it's probably better to sort it, if the opposite is the case then leave it unsorted. Familiarize yourself with data structures and search algorithms if you haven't already.

8. Do not split a single datum across multiple objects without good reason
When storing/processing data, each datum should be represented with at most a single object if it's feasible to do so (underlying implementations of a class to do this will be more complex). If the language doesn't come with one that fits it, create your own. IE, do not use multiple dictionaries with shared keys to store data that can't fit in one. Create a new class with a format matching what you want to store and put it in that. In the example given, you could create one dictionary where the values are custom objects.

9. Functions should have well-defined inputs and outputs
Functions should not modify their arguments, or anything besides what they explicitly return. Functions modifying something other than what they return leads to spaghetti code and confusing behavior.
There are exceptions for certain languages, ie how C handles dynamic memory allocation means that it's often better to pass an empty object to a function to store the output in, but these are exceptions to the rule.

10. Do not use global variables
All objects should exist only within the scope they were defined in, or are explicitly sent to. They should only be inherited or passed between scopes in the form of an argument or return value that is clear to the reader.

11. Functions should take and/or return at most 3 arguments
This is to keep code legible. If you feel the need to go above this number use some sort of list, and carefully consider whether this is something that should be done by one function, or if you should break it down into more.

12. Reuse code via functions and inheritance, as long as they're close together
Code that's called in more than one place should be turned into a function to avoid needless repetition.
Make use of class inheritance if the language allows to keep each class definition short and simple. This also helps find errors when debugging, and makes modifying or extending code easier. Ideally most of your code should consist of logic for deciding which other parts of your code to use, until you get down to the most basic level of the hierarchy.
The exception is if you're reusing code used for another distinct functionality of the program. Try to keep programs modular, conceptually different things should have redundant code or rely on shared libraries distinct from either to ensure that changes to one part of the program don't cause far-reaching bugs. See #21 and #23

13. Write for Python
Python is easy to learn and widely used by the wider scientific community. Therefore all code should have some sort of high-level wrapper to allow it to be callable in Python.
However, most of the code itself should remain hidden, this wrapper should only be for the highest level classes, methods and functions. These will be called within Python, and themselves call the rest of your code. These wrappers often require copying data into or out of a PyObject, so keep what they take and return as simple as possible.

14. Don't write in Python
Python is excellent for combining libraries written in other languages. It is terrible for low-level implementation, due to being very slow and memory intensive. All computationally intensive tasks should be written in another language, then made callable in Python, rather than being written in Python. C is the easiest language to do this with, but any language should be able to do it.
Know Python and at least one other language. Learn languages that are the best for what you want to do- for example, if you want to work on molecular dynamics, learn Fortran.

15. Don't put everything in one file
Split code over several smaller files rather than putting everything in one big file. If the language requires some sort of header, put it in a different file. This makes it easier to find a specific thing in your code, helps isolate bugs, and encourages good encapsulation.
These files should only be dependent on other files if those others implement code that is called in the file. You should not rely on inheriting objects, import/includes, etc between files.
Files (and any other files decomposed from them) should be oriented around one and only one part of the program if at all possible.

16. Include what you use
Include and import statements should always be included in a file (or associeted header file) where they are used, even if this leads to redundancy. Chances are that any library will have some sort of header guard so importing something more than once is rarely an issue. Transitive inclusions can cause code in one file to unexpectedly break when another is changed.
Headers should be self-contained, and include/import whatever they need to compile. They should also have header guards to avoid issues from multiple inclusions.

17. Use namespaces where possible
This is related to splitting code over multiple classes, though many languages have explicit definition of namespaces as well. By doing this you can have multiple methods with the same name without conflicts, which helps in avoiding bugs and can help with legibility.

18. Avoid unnecessary copying; move instead
Copying objects when you don't need to slows down code (for deep copies) and can cause issues where one object has multiple references, leading to unclear behavior (for shallow copies). These behaviors are language dependent, familiarize yourself with how your language deals with memory management. Where possible, move (hand off an object to a new reference and delete the old) instead of copy. Many languages have this sort of behavior built in (ie RVO in C++, Java in general).

19. Avoid cyclic dependency
Two pieces of code should not depend on each other. When code is split there should be a clear hierarchy, where one portion of code calls on the other and not vice versa. The "lower" (called/imported) level in that hierarchy should not require any of the "higher" levels to compile.

20. Keep feature intensity low; functions should do one thing
Each portion of the code should do as little as possible to do the one thing it's meant for. Functions should do exactly one thing, classes should contain as few members and methods and be as narrow in scope as possible, files should be responsible for only one feature of the program.

21. Don't split up code too much
This is the opposite problem of what has been desrcibed earlier, but it is a problem. When code is split too widely it can be hard for the reader to track what is going on. When a block of code is decomposed, keep the code that it's decomposed into nearby- in the same file, or at least the same directory (if there aren't too many files in that directory).
When building for one functionality, keep all required components near each other, even if split across files. When split across files, these files should only be part of that functionality, and not others.

22. Keep interfaces clear
APIs should be simple and descriptive. Complexity should be buried deeper in the code, where someone using the API doesn't have to worry about it. Expose as little of your code as possible for the API to work.
This is especially important for code that is imported into Python- try to make that code something that a person with absolutely no experience in coding can easily grasp.

23. Don't "mesh" code
Each component of the code should be oriented around one and only one thing the program does. One file should not be related to several distinct features. In the case that multiple features are calling on the same code, this code should be kept distinct from either in some sort of shared library that is delineated as such and does not itself rely on either of them.
Different functinalities of a program should be split across different files (generally called by a single binary), which themselves have code split off into "lower level" files. There should be no crossover between these file hierarchies except through accessing shared libraries, even if it leads to redundant code. Shared libraries should only be used by other files in your program, never reliant on them (see #19).

24. Keep components simple
Related to #23. Avoid feature creep. Think carefully on whether adding a new feature to the program should be done by extending existing code or adding new code- if unsure favor the latter, even if it's less efficient, because it makes the program easier to understand and helps avoid code becoming too interdependent.

25. Don't make components too simple
Related to #21. Code that delegates too much can be difficult to parse. By all means delegate, but make it easy for the reader to find whatever code has been spun off of a given block of code when they're looking at that block- ie in the same file, just below it. Keep files used for the same part of the program together if possible.

26. Review regularly, increment slowly
Large, sweeping changes to code will tend to cause issues to arise. Make small changes and have others look over them to ensure you're not cluttering up the code too much. What's obvious to you is likely confusing to others, since you are the one who wrote the code.

27. Clearly define problems before starting
Don't just sit down and start writing, expecting to solve problems as they arise. Just taking a few minutes to come up with a plan will save you hours debugging later! The first step of every project should be writing down the problem you want to solve and the general approach you want to take to solve it. Then pull out a piece of paper and sketch out a flowchart to describe what you want the code to do. After that, write it up as pseudocode. Once you're done all that, you're ready to start actually writing it.

28. Use a top-down approach
It can be helpful to write code from a top-down level, using classes and functions that have been defined but not written and implementing them once you get to the level where they can't be decomposed any more. This keeps code modular, lets more people work on a project at once, and makes it easier to write very long programs. It's easier to make encapsulated code this way than to try to work from the bottom up since you have a sense of what each piece needs to do.

29. Test as you go
Once you're split up code into small, independent pieces, come up with some sample input for each of those pieces and test how they work with various inputs. This makes it easier to find bugs, since you're only looking through 12 lines instead of 1,200.
Use pre-configured test states for consistency. Don't have a test that relies on a previous state of the program, or one that will be different each time you test.
Keep tests independent of each other- don't chain together multiple functions and test them all at once.
Test performance (time and memory) as well as behavior. Writing efficient code is almost as important as writing correct code! This is most important for any portion of your program that scales with input.
Capture all output from a test, but limit that behavior to a debug mode (don't just write stuff to the console whenever you run a program unless there's a reason to).
Keep test cases small. This makes testing easier to understand and set up.
When adding new functionality, write test cases for that functionality and see how existing code fails. This tells you what you need to add. Continue this process with each new error until it works, then refactor the code.

30. Know when to stop
Related to #27. Decide ahead of time any features you want and ensure the code is fully functional for those features until adding anything new.
Have a timeline on what parts of the code you're going to complete before which deadlines. Split the project into smaller parts and don't try to do too much at once.
Avoid feature creep.
Define a minimum viable product and get it working before adding anything more, but ensure you've left room for the code to be expanded without rewriting too much (ie, use class inheritance as described earlier to more easily create new classes similar to what you already have).
Have a concrete timeline on when you're going to release the project and what it needs to do by then. It's better to not get in everything you want than to constantly push back the release date and never get anything out to the public.
