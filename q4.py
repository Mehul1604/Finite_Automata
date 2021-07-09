import sys
import json
from pprint import pprint

arg_list = []
arg_list[:] = sys.argv[1:]

if not (len(arg_list) == 2):
    print("Incorrect arguments!")
    exit(0)

input_file = arg_list[0]
output_file = arg_list[1]

try:
    f_inp = open(input_file , 'r')
    input_dfa = json.load(f_inp)
    f_inp.close()
except:
    print('Error in finding/reading file')
    exit(0)

DISTINCT = {}
for i in range(len(input_dfa["states"])):
    first_state = input_dfa["states"][i]
    for j in range(i+1 , len(input_dfa["states"])):
        second_state = input_dfa["states"][j]
        l = sorted([first_state , second_state])
        DISTINCT[(l[0] , l[1])] = False

# Marking F and not F
for i in range(len(input_dfa["states"])):
    first_state = input_dfa["states"][i]
    for j in range(i+1 , len(input_dfa["states"])):
        second_state = input_dfa["states"][j]
        l = sorted([first_state , second_state])
        if not ((l[0] in input_dfa["final_states"]) == (l[1] in input_dfa["final_states"])):
            DISTINCT[(l[0] , l[1])] = True



while 1:
    change = False
    marks = []
    for i in range(len(input_dfa["states"])):
        first_state = input_dfa["states"][i]
        for j in range(i+1 , len(input_dfa["states"])):
            second_state = input_dfa["states"][j]
            l = sorted([first_state , second_state])
            if DISTINCT[(l[0] , l[1])] == False:
                for letter in input_dfa["letters"]:
                    to_1 = None
                    to_2 = None
                    for t in input_dfa["transition_function"]:
                        if t[0] == l[0] and t[1] == letter:
                            to_1 = t[2]
                            break
                    
                    for t in input_dfa["transition_function"]:
                        if t[0] == l[1] and t[1] == letter:
                            to_2 = t[2]
                            break
                    if to_1 == to_2:
                        continue
                    
                    l2 = sorted([to_1 , to_2])
                    if DISTINCT[(l2[0] , l2[1])] == True:
                        change = True
                        marks.append((l[0] , l[1]))
                        break
    
    
    if not change:
        break
    else:
        for m in marks:
            DISTINCT[m] = True

# pprint(DISTINCT)
# print('\n')

min_states = []
done_states = []
for i in range(len(input_dfa["states"])):
    first_state = input_dfa["states"][i]
    if (first_state not in done_states): 
        st = [first_state]
        done_states.append(first_state)
        for j in range(i+1 , len(input_dfa["states"])):
            second_state = input_dfa["states"][j]
            l = sorted([first_state , second_state])
            if DISTINCT[(l[0] , l[1])] == False:
                st.append(second_state)
                done_states.append(second_state)
        
        min_states.append(st)

# print('MIN STATES: ' , min_states)

min_dfa = {}
min_dfa["states"] = []
min_dfa["states"][:] = min_states
min_dfa["letters"] = []
min_dfa["letters"][:] = input_dfa["letters"]

min_dfa["start_states"] = []

for st in min_dfa["states"]:
    if (input_dfa["start_states"][0] in st):
        min_dfa["start_states"][:] = [st]
        break

min_dfa["final_states"] = []
one_final_state = input_dfa["final_states"][0]
for st in min_dfa["states"]:
    if (one_final_state in st):
        min_dfa["final_states"][:] = [st]
        break

min_dfa["transition_function"] = []
for st in min_dfa["states"]:
    one_from_state = st[0]
    for letter in min_dfa["letters"]:
        one_to_state = None
        for t in input_dfa["transition_function"]:
            if t[0] == one_from_state and t[1] == letter:
                one_to_state = t[2]
                break
        
        to_state = None
        for to_st in min_dfa["states"]:
            if one_to_state in to_st:
                to_state = to_st
                break
        
        min_dfa["transition_function"].append([st , letter , to_state])

# print('\nMIN DFA')
# pprint(min_dfa)

f_out  = open(output_file , 'w')
json.dump(min_dfa , f_out , indent=1)
f_out.close()