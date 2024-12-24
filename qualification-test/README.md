# Description for the qualification test

The following class, i.e., Lift.java, contains a functional bug. Please, write a test case that exposes the bug.

# Changes w.r.t. the original `Lift` class

We injected a functional bug in the `call` method, and we asked the developers to write a test case that exposes it. In the `if` statement (Line 67), the second condition should be `floor < topFloor`, instead of a strict inequality; the bug prevents the subsequent while loop from being executed when the `call` function is called with `floor = topFloor`, leaving the lift at `currentFloor`. We also injected two additional changes w.r.t. the original class to mitigate the potential use of LLMs when completing the task (Line 22 is `capacity = maxRiders + numRiders` but originally it was `maxRiders`; Line 49 is `if (numRiders + numEntering < capacity)` but originally it was `if (numRiders + numEntering <= capacity)`). Although both changes do not impact the functionalities of the class in an observable way, they mislead LLMs (we tested this with `gpt-4o` by [OpenAI](https://chatgpt.com/) and `Command R+` by [Cohere](https://cohere.com/chat) via their respective chat interfaces), effectively masking the functional bug at Line 67. 
