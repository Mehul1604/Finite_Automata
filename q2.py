import sys
import json

arg_list = []
arg_list[:] = sys.argv[1:]

if not (len(arg_list) == 2):
    print("Incorrect arguments!")
    exit(0)

input_file = arg_list[0]
output_file = arg_list[1]

try:
    f_inp = open(input_file , 'r')
    input_nfa = json.load(f_inp)
    f_inp.close()
except:
    print('Error in finding/reading file')
    exit(0)

def get_all_subsets(S):
    output = []
    # `N` stores the total number of subsets
    N = int(pow(2, len(S)))
    s = set()
 
    # generate each subset one by one
    for i in range(N):
        # check every bit of `i`
        for j in range(len(S)):
            # if j'th bit of `i` is set, print `S[j]`
            if i & (1 << j):
                s.add(S[j])
 
        output.append(list(s))
        s.clear()
    
    return output

def E(state , transition_function , all_states):
    output = []
    visited = {}
    for s in all_states:
        visited[s] = False
    
    queue = []
    queue.append(state)
    visited[state] = True
    while queue:
        head = queue.pop(0)
        output.append(head)

        for t in transition_function:
            if t[0] == head and t[1] == '$':
                nbr = t[2]
                if visited[nbr] == False:
                    visited[nbr] = True
                    queue.append(nbr)
    
    return output



output_dfa = {}
output_dfa["start_states"] = [E(input_nfa["start_states"][0] , input_nfa["transition_function"] , input_nfa["states"])]



P_Q = get_all_subsets(input_nfa["states"])
output_dfa["states"] = P_Q

output_dfa["final_states"] = []
for st in output_dfa["states"]:
    for q in st:
        if (q in input_nfa["final_states"]):
            output_dfa["final_states"].append(st)
            break


output_dfa["letters"] = input_nfa["letters"]

output_dfa["transition_function"] = []
# print('Making transition')
for st in output_dfa["states"]:
    for letter in output_dfa["letters"]:
        # print('At (' , st , ',', letter , ')')
        all_nbrs = []
        for individual_st in st:
            for t in input_nfa["transition_function"]:
                if t[0] == individual_st and t[1] == letter:
                    all_nbrs.extend(E(t[2] , input_nfa["transition_function"] , input_nfa["states"]))
        
        # print('All reachable were: ' , all_nbrs)
        
        output_dfa["transition_function"].append([st , letter , list(set(all_nbrs))])




f_out  = open(output_file , 'w')
json.dump(output_dfa , f_out , indent=1)
f_out.close()

