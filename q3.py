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

def dfa_to_gnfa(dfa):
    gnfa = {}
    gnfa["states"] = []
    gnfa["states"][:] = dfa["states"]
    gnfa["letters"] = []
    gnfa["letters"][:] = dfa["letters"]
    
    gnfa["start_state"] = "S"
    gnfa["final_state"] = "A"
    gnfa["states"].append(gnfa["start_state"])
    gnfa["states"].append(gnfa["final_state"])

    gnfa["transition_function"] = {}
    for from_st in gnfa["states"]:
        for to_st in gnfa["states"]:
            gnfa["transition_function"][(from_st , to_st)] = ""
    
    for t in dfa["transition_function"]:
        from_state = t[0]
        to_state = t[2]
        letter = t[1]
        cur_exp = gnfa["transition_function"][(from_state , to_state)]
        if cur_exp == "":
            new_exp = cur_exp + letter
        else:
            new_exp = "("
            new_exp += cur_exp
            new_exp += "+"
            new_exp += letter
            new_exp += ")"
        
        gnfa["transition_function"][(from_state , to_state)] = new_exp
    
    gnfa["transition_function"][(gnfa["start_state"] , dfa["start_states"][0])] = "$"
    for f in dfa["final_states"]:
        gnfa["transition_function"][(f , gnfa["final_state"])] = "$"
    
    return gnfa

try:
    f_inp = open(input_file , 'r')
    input_dfa = json.load(f_inp)
    f_inp.close()
except:
    print('Error in finding/reading file')
    exit(0)

def get_regex(gnfa):
    n = len(gnfa["states"])
    if n == 2:
        regex = gnfa["transition_function"][(gnfa["start_state"] , gnfa["final_state"])]
        return regex
    
    smaller_gnfa = {}
    smaller_gnfa["start_state"] = gnfa["start_state"]
    smaller_gnfa["final_state"] = gnfa["final_state"]
    smaller_gnfa["letters"] = gnfa["letters"]
    smaller_gnfa["states"] = []
    rip_state = None
    for st in gnfa["states"]:
        if st != gnfa["start_state"] and st != gnfa["final_state"]:
            rip_state = st
            break
    
    smaller_gnfa["states"][:] = [st for st in gnfa["states"] if st != rip_state]

    smaller_gnfa["transition_function"] = {}
    for qi in smaller_gnfa["states"]:
        for qj in smaller_gnfa["states"]:
            smaller_gnfa["transition_function"][(qi , qj)] = ""

    for qi in smaller_gnfa["states"]:
        for qj in smaller_gnfa["states"]:
            if qi != smaller_gnfa["final_state"] and qj != smaller_gnfa["start_state"]:
                new_exp = ""
                lhs = ""
                r1 = gnfa["transition_function"][(qi , rip_state)]
                r2 = gnfa["transition_function"][(rip_state , rip_state)]
                r3 = gnfa["transition_function"][(rip_state , qj)]
                r4 = gnfa["transition_function"][(qi , qj)]
                if r1 == "" or r3 == "":
                    new_exp = r4
                else:
                    lhs += "("
                    if r1 != "$":
                        lhs += r1
                    if r2 != "" and r2 != "$":
                        # lhs += "?"
                        lhs += (r2 + "*")
                    
                    # lhs += "?"
                    if r3 != "$":
                        lhs += r3
                    lhs += ")"
                    if len(lhs) == 2:
                        lhs = "$"
                    elif len(lhs) == 3:
                        lhs = lhs[1]
                    if r4 == "":
                        new_exp = lhs
                    else:
                        new_exp += "("
                        new_exp += lhs
                        new_exp += "+"
                        new_exp += r4
                        new_exp += ")"
                
                smaller_gnfa["transition_function"][(qi , qj)] = new_exp
                
    # print('REDUCED TO ')
    # print('start ' , smaller_gnfa["start_state"])
    # print('final ' , smaller_gnfa["final_state"])
    # print('states ' , smaller_gnfa["states"])
    # print('transition: ')
    # pprint(smaller_gnfa["transition_function"])
    # print('\n')


    return get_regex(smaller_gnfa)


GNFA = dfa_to_gnfa(input_dfa)

# pprint(GNFA)

answer = get_regex(GNFA)

# print('REGEX: ' , answer)

output = {"regex": answer}

f_out  = open(output_file , 'w')
json.dump(output , f_out , indent=1)
f_out.close()
