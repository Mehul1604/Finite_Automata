# README

# Automata Theory- Programming Assignment
#### Mehul Mathur
2019101046

### Q1 - Regex to NFA

A language is regular only if some regular expression describes it
The approach used here was :

- Period (.) symbols were first inserted wehrever there was a concatenation in the regex
- Then the expression was converted in the **Post fix notation**
- Then Thompson's Construction was used:
    - Each alphanumeric symbol of the language (a-z0-9) is described by an NFA with 2 states - The starting state and accepting state with a single transition of that letter taking the machine from start to accept. This NFA was then pushed in a stack
    - Each empty string (epsilon) was converted to an NFA with a single state (its both the start and accept state). This NFA was then pushed in a stack
    - Each union operation (+) was coverted by popping out top 2 NFAs from the stack and then creating a new NFA which had an extra start state other than the ones in the 2 popped out which had epsilon transitions to both the previous start states. This new NFA was then pushed
    - Each concatenation was converted by popping out the 2 NFAS and making a new NFA by joining the Accept states of the left expression NFA to the start states of the right side NFA
    - Each * operation was converted by popping out the NFA and then creating a new one with an extra state which is now another accept state that joins to the start state of the original NFA by epsilon. And a transition of epsilon was also added from the original accept states to the original start state
    - At the end the last remaining NFA was the answer

### Q2 - NFA to DFA

Here the equivalence of NFAs and DFAs is used

- The states of the DFA is the set of all subsets of the NFA
- The states of the DFA for this question is an array itself of a subset of the states of the NFA
- A function E(S) tells us all the states reachable from the state S through epsilon transitions (A BFS like approach was used)
- For a subset R $\epsilon$ P(Q) , the transition function is the union of E(S) of all the states S for each r $\epsilon$ R , such that Transition_Function$_{NFA}$(r) = S.
- The start state is E(Start state of NFA)
- The accept states are all those subsets which have atleast one accept state of the NFA

### Q3 - DFA to Regex

Here the concept of a *generalized non-deterministic finite automata* (GNFA) is used

- The DFA given is converted to a GNFA (by adding a start state which has epsilon transition to the original start state and an accept state which is reachable by a single epsilon from the original accept states)
- The GNFA is then reduced till it has 2 states (start and accept) by a recursive function
- At each step a state is ripped off the transitions between the other states are updated by the rule:
    - If the R1 is a transition from some q$_{i}$ to q$_{ripped}$ , R2 is from q$_{ripped}$ to q$_{ripped}$ and R3 is from q$_{j}$ and R4 is from q$_{i}$ to q$_{j}$. Then the new transition between q$_{i}$ and q$_{j}$ is        (R1.R2*.R3) U R4
- When number of states is 2 , the recursion stops and the label between the start and accept state of this 2 state GNFA is the regular expression

### Q4 - Minimize DFA

The Myhill-Nerode was utilized in this question

The procedure used was:

- A lower triangular table was created in which the rows and columns were the states of the DFA
- Initially the cells where one state is an accepting state and the other is not were marked as true
- Then the following was repeated until no change was observed
    - For states a and b , if Table(a,b) is marked false and Transition_Function(a) and Transition_Function(b) is marked true , then mark cell (a,b) as true

- The final combination of states where the cell was false were grouped together
- The transition function was:
    - If in a grouped state 1 , a state s of that group reaches a satte s' of a group 2 , the transition(group1) = group 2