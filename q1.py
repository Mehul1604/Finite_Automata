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
    input_regex = json.load(f_inp)
    f_inp.close()
except:
    print('Error in finding/reading file')
    exit(0)


PRECEDENCE = {
    '*': 1,
    '.': 2,
    '+': 3
}

OPERATORS = ['.' , '+' , '*']
CUR_STATE = 0

def make_state(state_num):
    state_string = "Q{}".format(state_num)
    return state_string

class NFA:
    def __init__(self , states ,  starting_state , finishing_states):
        self.states = []
        self.states[:] = states
        self.starting_state = starting_state
        self.finishing_states = []
        self.finishing_states[:] = finishing_states
        self.transition_function = []
    
    def set_states(self , new_states):
        self.states[:] = new_states
    
    def set_starting_states(self , new_starting_state):
        self.starting_state = new_starting_state
    
    def set_finishing_states(self , new_finishing_states):
        self.finishing_states[:] = new_finishing_states
    
    def append_transition(self , from_state , symbol , to_state):
        self.transition_function.append([from_state , symbol , to_state])
    
    def set_transition(self , new_transition_function):
        self.transition_function[:] = new_transition_function
    
    def display(self):
        print('Nfa')
        print('states: ' , self.states)
        print('transition: ' , self.transition_function)
        print('starting: ' , self.starting_state)
        print('finishing: ' , self.finishing_states)

    

def union(nfa1 , nfa2):
    global CUR_STATE
    new_start = make_state(CUR_STATE)
    CUR_STATE += 1

    new_finishing_states = []
    new_finishing_states.extend(nfa1.finishing_states)
    new_finishing_states.extend(nfa2.finishing_states)

    combined_states = []
    combined_states.extend(nfa1.states)
    combined_states.extend(nfa2.states)
    combined_states.append(new_start)

    union_nfa = NFA(combined_states , new_start , new_finishing_states)
    combined_transition = []
    combined_transition.extend(nfa1.transition_function)
    combined_transition.extend(nfa2.transition_function)
    union_nfa.set_transition(combined_transition)

    union_nfa.append_transition(union_nfa.starting_state , '$' , nfa1.starting_state)
    union_nfa.append_transition(union_nfa.starting_state , '$' , nfa2.starting_state)
    return union_nfa

def concatenation(nfa1 , nfa2):
    combined_states = []
    combined_states.extend(nfa1.states)
    combined_states.extend(nfa2.states)

    combined_transition = []
    combined_transition.extend(nfa1.transition_function)
    combined_transition.extend(nfa2.transition_function)

    concat_nfa = NFA(combined_states , nfa1.starting_state , nfa2.finishing_states)
    concat_nfa.set_transition(combined_transition)
    for fin in nfa1.finishing_states:
        concat_nfa.append_transition(fin , '$' , nfa2.starting_state)
    
    return concat_nfa

def star(nfa):
    global CUR_STATE
    new_start = make_state(CUR_STATE)
    CUR_STATE += 1
    new_states = []
    new_states[:] = nfa.states
    new_states.append(new_start)

    new_finishing_states = []
    new_finishing_states[:] = nfa.finishing_states
    new_finishing_states.append(new_start)

    new_transition = []
    new_transition[:] = nfa.transition_function
    starred_nfa = NFA(new_states , new_start , new_finishing_states)
    starred_nfa.set_transition(new_transition)
    starred_nfa.append_transition(new_start , '$' , nfa.starting_state)
    for fin in nfa.finishing_states:
        starred_nfa.append_transition(fin , '$' , nfa.starting_state)
    
    return starred_nfa

    


def convert_posfix(expression):
    operator_stack = []
    output_queue = []
    proper_regex = ""
    for i in range(len(expression)):
        sym = expression[i]
        proper_regex += sym
        if i < (len(expression) - 1):
            next_sym = expression[i+1]
            if (sym.isalnum()) or sym == "$" or (sym == '*') or (sym == ')'):
                if (next_sym.isalnum()) or next_sym == "$" or (next_sym == '('):
                    proper_regex += '.'
    
    # print('proper is ' , proper_regex)
    
    for reg_sym in proper_regex:
        # print('\n\nAt {}'.format(reg_sym))
        # print('stack ' , operator_stack)
        # print('queue ' , output_queue)
        if reg_sym.isalnum() or reg_sym == "$" :
            # print('issa letter so push')
            output_queue.append(reg_sym)
        
        elif reg_sym in OPERATORS:
            # print('issa operator')
            while operator_stack and (operator_stack[len(operator_stack) - 1] in OPERATORS) and (PRECEDENCE[operator_stack[len(operator_stack) - 1]] <= PRECEDENCE[reg_sym]):
                top_head = operator_stack.pop()
                # print('removing {} from top and pushing'.format(top_head))
                output_queue.append(top_head)

            # print('finally pushed {} on stack'.format(reg_sym))
            operator_stack.append(reg_sym)

        elif reg_sym == '(':
            # print('opening bracket so just push')
            operator_stack.append(reg_sym)
        
        elif reg_sym == ')':
            # print('closing bracket')
            while not operator_stack[len(operator_stack) - 1] == '(':
                top_head = operator_stack.pop()
                # print('removing {} from top and pushing'.format(top_head))
                output_queue.append(top_head)
            
            # print('found closing')
            operator_stack.pop()
        
        # print('done')
        # print('stack ' , operator_stack)
        # print('queue ' , output_queue)

    
    while operator_stack:
        top_head = operator_stack.pop()
        output_queue.append(top_head)
    
    

    postfix_expression = ""
    for post_sym in output_queue:
        postfix_expression += post_sym

    return postfix_expression


def thompson_construction(postfix_regex):
    global CUR_STATE
    nfa_stack = []
    for sym in postfix_regex:
        # print('\n\nAt ' , sym)
        # print('starting stack is')
        # for n in nfa_stack:
        #     n.display()
        # print('\n')
           
        if sym.isalnum() or sym == "$":
            # print('letter so just putting')
            if sym == "$":
                n = NFA([make_state(CUR_STATE)] , make_state(CUR_STATE) , [make_state(CUR_STATE)])
                CUR_STATE += 1
                nfa_stack.append(n)
            else:
                n = NFA([make_state(CUR_STATE) , make_state(CUR_STATE+1)] , make_state(CUR_STATE) , [make_state(CUR_STATE+1)])
                CUR_STATE += 2
                n.append_transition(n.starting_state , sym , n.finishing_states[0])
                nfa_stack.append(n)
        
        elif sym == '*':
            # print('star so starring')
            n = nfa_stack.pop()
            n_star = star(n)
            nfa_stack.append(n_star)
        
        elif sym == '.':
            # print('concat so concatting')
            n2 = nfa_stack.pop()
            n1 = nfa_stack.pop()
            concat_nfa = concatenation(n1 , n2)
            nfa_stack.append(concat_nfa)
        
        elif sym == '+':
            # print('union so unioning')
            n2 = nfa_stack.pop()
            n1 = nfa_stack.pop()
            union_nfa = union(n1 , n2)
            nfa_stack.append(union_nfa)
        
        # print('\n')
        
        # print('done ending stack is')
        # for n in nfa_stack:
        #     n.display()
    
    answer = nfa_stack.pop()
    return answer
        
        





regex = input_regex["regex"]
regex = regex.replace(" " , "")

postfix_regular_expression = convert_posfix(regex)
if len(postfix_regular_expression) == 0:
    output_nfa = {}
    output_nfa["states"] = []
    output_nfa["states"][:] = [make_state(CUR_STATE)]
    output_nfa["letters"] = []
    for i in range(97,123):
        output_nfa["letters"].append(chr(i))

    for i in range(10):
        output_nfa["letters"].append(str(i))

    output_nfa["transition_function"] = []
    output_nfa["start_states"] = [make_state(CUR_STATE)]
    output_nfa["final_states"] = []

    f_out = open(output_file , 'w')
    json.dump(output_nfa , f_out , indent=1)
    f_out.close()

else:
    # print(postfix_regular_expression)

    nfa_made = thompson_construction(postfix_regular_expression)
    # print('\nSO answer is ')
    # nfa_made.display()

    output_nfa = {}
    output_nfa["states"] = []
    output_nfa["states"][:] = nfa_made.states
    output_nfa["letters"] = []
    for i in range(97,123):
        output_nfa["letters"].append(chr(i))

    for i in range(10):
        output_nfa["letters"].append(str(i))

    output_nfa["transition_function"] = []
    output_nfa["transition_function"][:] = nfa_made.transition_function
    output_nfa["start_states"] = [nfa_made.starting_state]
    output_nfa["final_states"] = []
    output_nfa["final_states"][:] = nfa_made.finishing_states

    f_out = open(output_file , 'w')
    json.dump(output_nfa , f_out , indent=1)
    f_out.close()