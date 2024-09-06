# Island hopper

Run the program from the command line providing a file as argument:
```
python src/island_hopper.py tests/examples/input1
```
Or with input from stdin:
```
cat tests/examples/input2 | python src/island_hopper.py
```

### Problem
The problem consists of finding an optimal itinerary choosing between two transportation modes, `by-sea` or `airborne`, for a given number of hops H subjected to the requerements of a given number of customers C.
An optimal itinerary, if it exists, **minimizes** the number of `airborne` hops and satisfies **at least** one requirement per customer. 

### Solution
This problem is an example of constrained optimization, where an objective function needs to be (in this case) minimized, while its variables are subjected to constraints.
Since each of the hops can either be `by-sea` or `airborne`, we can encode each hop as a binary variable, corresponding to:

- `by-sea`: 0
- `airborne`: 1

Furthermore, each customer requrement can be cast into constraint on these variables that is satisfied whenever at least one of the specified preferences is met.
For example the requirement `0 by-sea, 5 airborn`, translates into the following constraint on the binary variables `h_0` and `h_5`:

$$
\bar{h_0} \lor h_5
$$

The objective function is a minimization of the sum of all variables, as in:

$$
\min \sum_i h_i
$$

We are therefore dealing with an optimization problem on boolean satisfiability clauses. In order to solve it we can use the CP-SAT solver of the OR-Tools library. An example can be seen [here](https://developers.google.com/optimization/cp/cp_solver)
For our problem, the model is consists of H binary variables subjected to C constraints.
The objective function is simply the sum of all the binary variables as shown above.

Note that if multiple solutions are possible, the program will only return the first one.

### Tests
Since we talked a bit about tests in our converations I experimented a bit and implemented a couple of simple tests for the provided input-output examples :)

They can be run invoking `pytest` in the project folder.

PS: It is by no meanss an extensive testing, especially for input validation.
