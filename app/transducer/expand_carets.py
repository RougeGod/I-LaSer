#this file makes long regular expressions easier to write, by allowing their expansion. 
#entering a caret character (^) followed by a number will cause the previous expression, 
#whether bracketed or a symbol, to be repeated the number of times specified by what's 
#on the right of the caret. For example, 0(0+1)^3 will become 0(0+1)(0+1)(0+1), while
#(0^4)1 will become (0000)1 and 1^4 will become 1111


def expand_carets(aut_str):
    while True: #search through all of the carets in the string. When there are none, the first condition gets us out of the loop
        #it's possible that this recurses with carets creating more carets, which is why we cannot go through each character individually
        caret_position = aut_str.find("^")
        if (caret_position == -1): #no carets in the string
            return aut_str #the only way to exit the program
        else:
            if (aut_str[caret_position - 1] == ')'): #the expression to expand is bracketed, search for the matching bracket
                left_bracket_pos = find_matching_left_bracket(aut_str, caret_position - 1)
                positions_to_replicate = (left_bracket_pos, caret_position)
            else:
                positions_to_replicate = (caret_position - 1, caret_position) #just the last symbol, since there was no bracketed expression
        reps, number_length = find_number(aut_str, caret_position + 1)
        aut_str = aut_str[:positions_to_replicate[0]] + (aut_str[positions_to_replicate[0]:positions_to_replicate[1]] * reps) + aut_str[positions_to_replicate[1] + number_length:]


#when given a string and the position of a right bracket, finds the matching left bracket
#this even works when brackets are nested, as in (a(9+99))^4
def find_matching_left_bracket(input_string, right_bracket_pos):
    right_brackets = 0
    left_brackets = 0
    position = right_bracket_pos
    for position in range(right_bracket_pos, -1, -1): 
        #stop point has to be -1 because the stop point is not evaluated. 
        #if it were 0, a matching bracket at the start of the string would not be found
        if (input_string[position] == ")"):
            right_brackets += 1
        elif (input_string[position] == "("):
            left_brackets += 1
        if (left_brackets == right_brackets):
            return position
    raise ValueError("There was no matching left bracket.")

#finds the largest legal number starting from a certain position in the string

def find_number(input_string, start):
    if (start < 0):
        raise ValueError("Start position cannot be negative.")
    for position in range(len(input_string), start, -1): 
        #search backwards, from the end of the string all the way down to the original starting position
        #return the first legal integer
        try:
            return int(input_string[start:position]), (position + 1 - start)
            #also return the length of the number so that it can be properly removed
        except ValueError: #not legal integer
            continue #go back to the start of the loop
    raise ValueError("Could not find the number of repititions.") 
    #we got all the way back to the caret without a legal number