#!Python 2.6
# Filename: AE_Game.py
# Copyright 2011 by Joe Mortillaro
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Description:
#   Add Edge Game Evaluator v1.11
#   Finds the value of a game of the Forbidden Graph Game.
#   Can find path and complete graph solutions over a range.
#   Backs up data to files for k and p graphs.
#   1.12 will add the fast isomorphic graph generator


version_number = '1.12'

import copy
__metaclass__ = type


# The program makes lists out of a matrix as follows . . .
#
#       a   b   c   d   e   f
#    a      0   1   3   6  10
#    b          2   4   7  11
#    c              5   8  12
#    d                  9  13
#    e                     14
#    f
#
# Where if, for example, the 4th element (indexed at 0) in 
# the string was 1, it would indicate 1 edge between 
# nodes b and d.
#
# Also, the program assumes a standard graph, with no
# loops and no multi-edges.

def gmatrix_row(number):
    #Given the string index _number_, finds the row on the matrix.
    z = 0
    x = 0
    while x >= 0:
        for y in range(x):
            if z == number:
                return y
            z += 1
        x += 1


def gmatrix_row_list_to_n(number):
    #Returns a list of row values for string indexes up to _number_.
    temp = []
    x = 0
    for x in range(number+1):
        for y in range(x):
            temp.append(y)
        x += 1
    temp.append(number)
    return temp


def gmatrix_column(number):
    #Given the string index _number_, finds the column on the matrix.
    z = 0
    x = 0
    while x >= 0:
        for y in range(x):
            if z == number:
                return x
            z += 1
        x += 1


def gmatrix_column_list_to_n(number):
    #Returns a list of column values for indexes up to _number_.
    temp = []
    x = 0
    for x in range(number+1):
        for y in range(x):
            temp.append(x)
        x += 1
    return temp


def make_all_binlists(digits):
# list of list of ints = make_all_binlist(int)
# returns a list of list of ints of all possible binary
#   strings of length digits
    temp = []
    for x in range(2**digits, 2**(digits+1)):
        temp.append(string_to_intlist(bin(x)[3:]))
    return temp


def make_path_graph(number, nodes):
# list of list of ints = make_path_graph(int, int)
# returns the greatest P_number graph with nodes nodes
#   binary as a list if ints.
    temp = [0]*choose_two(nodes)
    z = 0
    for x in range(number):
        for y in range(x):
            if y == x-1:
                temp[z] = 1
            z += 1
    return temp


def make_cycle_graph(number, nodes):
# list of list of ints = make_path_graph(int, int)
# returns the greatest P_number graph with nodes nodes
#   binary as a list if ints.
    temp = [0]*choose_two(nodes)
    z = 0
    for x in range(number):
        for y in range(x):
            if y == x-1:
                temp[z] = 1
            z += 1
    temp[z-x] = 1
    return temp


def make_wheel_graph(number, nodes):
# list of list of ints = make_path_graph(int, int)
# returns the greatest P_number graph with nodes nodes
#   binary as a list if ints.
    temp = [0]*choose_two(nodes)
    z = 0
    for x in range(number):
        for y in range(x):
            if y == 0:
                temp[z] = 1
            z += 1
    return temp


def make_complete_graph(number, nodes):
# list of list of ints = make_complete_graph(int)
# returns the greatest K_number graph binary with nodes nodes
#   as a list if ints.
    temp = [0]*choose_two(nodes)
    z = 0
    for x in range(number):
        for y in range(x):
            temp[z] = 1
            z += 1
    return temp


def cstring_to_intlists(string):
# list of lists of ints = string_to_intlist(commastring)
# returns a list of lists of ints given a string separated by commas.
    temp = string.replace(' ','')
    temp = temp.split(',')
    for x in range(len(temp)):
        temp[x] = list(temp[x])
        for y in range(len(temp[x])):
            temp[x][y] = int(temp[x][y])
    return temp


def string_to_intlist(string):
# list of ints = string_to_intlist(string)
# returns a list of ints given a string.
#    if 
    temp = []
    for x in range(len(string)):
        temp.append(int(string[x]))
    return temp

def intlist_to_string(intlist):
    return str(intlist).replace('[','').replace(',','')\
               .replace(' ','').replace(']','')

def possible(g):
# list of lists of ints = possible(list of ints)
# generates a list of possible game intlists given
#   an intlist.  Optimized to ignore isomorphic options.

    #finds the rightmost 1 in the intlist
    rightmost1 = -1
    for x in range(len(g)):
        if g[x] == 1:
            rightmost1 = x

    #takes care of the null graph
    if rightmost1 == -1: 
        P = [0]*len(g)
        P[0] = 1
        return [P]
    
    #sets a stopping point
    stop_point_temp = gmatrix_column(rightmost1)
    column_list = gmatrix_column_list_to_n(stop_point_temp+2)
    stop_point = copy.copy(len(column_list))

    #finds possible graphs up to the stopping point    
    x = 0
    P = []
    if stop_point > len(g):
            stop_point = len(g)
    for x in range(stop_point):
        if g[x] == 0:
            g[x] = 1
            P.append(copy.copy(g))
            g[x] = 0
    return P


def all_possible(g):
# list of lists of ints = possible(list of ints)
# generates a list of possible game intlists given
#   an intlist.
    x = 0
    P = []
    while x < len(g):
        if g[x] == 0:
            g[x] = 1
            P.append(copy.copy(g))
            g[x] = 0
        x += 1
    return P


def factorial(number):
# int = factorial(int)
# computes the numberth factorial.
    if number == 1:
        return 1
    else:
        return number * factorial(number - 1)


def choose_two(number):
# int = choose_two(int)
# computes the combinatorial number choose two.
    return int(factorial(number) / (factorial(number - 2) * 2))


def mex(mex_numbers_list):
# int = mex(list of ints)
# returns the minimal-excluded number in a list of integers
    x = 0
    for x in range(len(mex_numbers_list)+1):
        if not x in mex_numbers_list:
            return x
    return 'MEX NOT FOUND'


def forbidden(g):
# int = forbidden(list of ints)
# given an intlist, returns 1 if a list has a forbidden list
#   as a sublist, and returns 0 if it does not.
    global forbidden_graph_list
    j = 0
    k = 0
    is_forbidden = 0
    while j < len(forbidden_graph_list):
        is_forbidden = 1
        while k < len(forbidden_graph_list[j]):
            if forbidden_graph_list[j][k] == 1:
                if g[k] == 0:
                    is_forbidden = 0
            k += 1
        k = 0
        j += 1
        if is_forbidden == 1:
            return 1
    return 0


def permute(original_list):
# list of lists of ints = permute(list of ints)
# returns a list of lists of permutations of a list
    if not original_list:
        return [original_list] # takes care of empty strings/lists
    else:
        temp = []
        for k in range(len(original_list)):
            part = original_list[:k] + original_list[k+1:]
            for m in permute(part):
                temp.append(original_list[k:k+1] + m)
        return temp


def make_iso(g_binary):
#list of lists of ints = make_iso(list of lists of ints)
#this function returns a list of graph lists that are
#   isomorphic to a list of graph lists
    iso_graph_list = []

    #recursively takes care of non-singleton sets
    for j in range(1, len(g_binary)):
        iso_temp = []
        iso_temp.append(copy.copy(make_iso([g_binary[j]])))
        for k in range(len(iso_temp[0])):
            iso_graph_list.append(copy.copy(iso_temp[0][k]))

    #makes new in"dex" to map edges to the graph binary
    dex = []
    x = y = z = number_nodes = 0
    number_edges = len(g_binary[0])
    while z < number_edges:
        x += 1
        for x in range(y):
            z+=1        
            dex.append((x,y))
        y+=1
        x+=1
    number_nodes = y

    #makes permuted indexes
    p = permute(list(range(number_nodes)))
    p_dex = []
    for n in range(len(p)):
        p_dex_temp = []
        p_dex_temp2 = []
        for x in range(number_edges):
            x_temp = p[n][dex[x][0]]
            y_temp = p[n][dex[x][1]]
            if x_temp < y_temp:
                p_dex_temp.append((x_temp, y_temp))
            if y_temp < x_temp:
                p_dex_temp.append((y_temp, x_temp))
        for x in range(number_edges):
            p_dex_temp2.append(dex.index(p_dex_temp[x] ))
        p_dex.append(p_dex_temp2)

    #permutes graphs
    for x in range(len(p_dex)):
        p_dex_temp = [0]*number_edges
        for y in range(number_edges):
            if g_binary[0][y] == 1:
                p_dex_temp[p_dex[x][y]] = 1
        iso_graph_list.append(p_dex_temp)
        
    #gets rid of duplicates in the list
    x_range = len(iso_graph_list)
    x = 0
    while x < x_range:
        y_range = len(iso_graph_list)
        y = x+1
        while y < y_range:
            if iso_graph_list[x] == iso_graph_list[y]:
                del iso_graph_list[y]
                y_range += -1
                x_range += -1
            else:
                y += 1
        x += 1            
    return iso_graph_list



def get_database(file_name):
    global forbidden_graph_list
    global graph_nim_values
    try:
        f = open(str(file_name),'r')
    except IOError:
        return 0
    print "Database Found."
    while True:
        line = f.readline()
        if not line: break
        index_temp = line.index(']')
        graph_temp = list(line[1:index_temp])
        for x in range(len(graph_temp)):
            graph_temp[x] = int(graph_temp[x])
        mex_temp = int(line[index_temp+1:].replace('\n',''))
        if mex_temp == -2:
            forbidden_graph_list.append(graph_temp)
        else: 
            graph_nim_values[tuple(graph_temp)] = copy.copy(mex_temp)
    print "Database loaded."
    return 1



def value(switches, g):
# num = value(list)
# returns the value of a position, uses recursion
# switches == bin 1 to optimize, bin 0 to use all possible moves
# switches == bin 10 to use backup files, bin 00 to not

    if not not graph_nim_values.get(tuple(g)):
        return graph_nim_values.get(tuple(g))
    if forbidden(g) == 1:
        graph_nim_values[tuple(g)] = \
                        copy.copy(-1)
        if (switches & 2) == 2:
            f = open(str(backup_file_name),'a')
            f.write(str(g).replace(' ','')\
                    .replace(',','') + str(-1) + '\n')
            f.close()
        return -1
    else:
        value_numbers = []
        if (switches & 1) == 0 :
            p = all_possible(g)
        else:
            p = possible(g)

        k = 0
        while k < len(p):
            value_numbers.append(value(switches ,p[k]))
            k += 1
        mex_number = mex(value_numbers)
        graph_nim_values[tuple(g)] = \
                        copy.copy(mex_number)
        if (switches & 2) == 2:
            f = open(str(backup_file_name),'a')
            f.write(str(g).replace(' ','')\
                    .replace(',','') + str(mex_number) + '\n')
            f.close()
        return mex_number
    

def evaluate_game(value_switches, iso, forbidden_graph_list0, start_graph):
# num evaluate_game(num, list of intlists, intlist)
# returns the value of the game of gnim for the game
#   position start_graph, with a forbidden graph set
#   forbidden_graph_list. iso = 1 will include graphs
#   isomorphic to the forbidden_graph_list as forbidden
#   graphs. find_all_possible = 1 will not optimize the
#   list of possible moves.

    import time
    global forbidden_graph_list
    graph_nim_values.clear()
    graph_size = int(len(forbidden_graph_list0[0]))
    start_time = copy.copy(time.time())
    if (value_switches & 2) == 2:
        db_ok = get_database(backup_file_name)
    if db_ok == 0:
        
        if iso == 1:
            forbidden_graph_list = make_iso(forbidden_graph_list0)
            if (value_switches & 2) == 2:
                f = open(str(backup_file_name),'a')
                for x in range(len(forbidden_graph_list)):
                    graph_nim_values[tuple(forbidden_graph_list[x])] = \
                            copy.copy(-2)
                    f.write(str(forbidden_graph_list[x]).replace(' ','')\
                        .replace(',','') + str(-2) + '\n')
                f.close()

        if iso == 0:
            forbidden_graph_list = forbidden_graph_list0
            
            if (value_switches & 2) == 2:
                f = open(str(backup_file_name),'a')
                for x in range(len(forbidden_graph_list)):
                    graph_nim_values[tuple(forbidden_graph_list[x])] = \
                            copy.copy(-2)
                    f.write(str(forbidden_graph_list[x]).replace(' ','')\
                        .replace(',','') + str(-2) + '\n')
                f.close()

    Nim_value = value(value_switches,start_graph)
    print "Benchmark time: ", (time.time() - start_time)
    return Nim_value

# the main function
# I should not use global variables.
def main():
    global forbidden_graph_list
    global graph_size
    global graph_nim_values
    global backup_file_name

    forbidden_graph_list = []
    graph_nim_values = {}

    print "AddEdge version",version_number
    print "Find value for (K)oimplete graphs."
    print "Find value for (P)ath graphs."
    print "Find value for (W)heel graphs."
    print "Find value for (C)ycle graphs."
    print "Find value for a given (S)tart position, with isomorphic forbidden graphs."
    print "Find value for a game with (N)o isomorphic graphs."
    print "Game with (N2)o isomorphic graphs and a given starting graph."
    print "Find value for a (G)ame with isomorphic forbidden graphs."
    print "or (Q)uit."
    menu_choice = raw_input()

    # quit
    if menu_choice.lower() == 'q':
        return 0

    # complete graphs
    if menu_choice.lower() == 'k':
        k_number_of_nodes = int(raw_input("How many nodes in the k graph?"))
        g_number_of_nodes = int(raw_input("How many nodes in game?"))
        backup_file_name = 'AE(K' + str(k_number_of_nodes) + ",N" \
                + str(g_number_of_nodes) + ")_Backup.txt"
        Nim_value = evaluate_game(3,1,[make_complete_graph(k_number_of_nodes,\
                g_number_of_nodes)],[0]*choose_two(g_number_of_nodes))
        print "AE(K" + str(k_number_of_nodes) + ",N" + str(g_number_of_nodes) \
                  + ") =", Nim_value
        F_graph = []


    # wheel graphs
    if menu_choice.lower() == 'w':
        w_number_of_nodes = int(raw_input("How many nodes in the w graph?"))
        g_number_of_nodes = int(raw_input("How many nodes in game?"))
        backup_file_name = 'AE(W' + str(w_number_of_nodes) + ",N" \
                + str(g_number_of_nodes) + ")_Backup.txt"
        Nim_value = evaluate_game(3,1,[make_wheel_graph(w_number_of_nodes,\
                g_number_of_nodes)],[0]*choose_two(g_number_of_nodes))
        print "AE(W" + str(w_number_of_nodes) + ",N" + str(g_number_of_nodes) \
                  + ") =", Nim_value
        F_graph = []


    # cycle graphs
    if menu_choice.lower() == 'c':
        c_number_of_nodes = int(raw_input("How many nodes in the c graph?"))
        g_number_of_nodes = int(raw_input("How many nodes in game?"))
        backup_file_name = 'AE(C' + str(c_number_of_nodes) + ",N" \
                + str(g_number_of_nodes) + ")_Backup.txt"
        Nim_value = evaluate_game(3,1,[make_cycle_graph(c_number_of_nodes,\
                g_number_of_nodes)],[0]*choose_two(g_number_of_nodes))
        print "AE(C" + str(c_number_of_nodes) + ",N" + str(g_number_of_nodes) \
                  + ") =", Nim_value
        F_graph = []


    # path graphs
    if menu_choice.lower() == 'p':
        p_number_of_nodes = int(raw_input("How many nodes in the p graph?"))
        g_number_of_nodes = int(raw_input("How many nodes in game?"))
        backup_file_name = 'AE(P' + str(p_number_of_nodes) + ",N" \
                + str(g_number_of_nodes) + ")_Backup.txt"
        Nim_value = evaluate_game(3,1,[make_path_graph(p_number_of_nodes,\
                g_number_of_nodes)],[0]*choose_two(g_number_of_nodes))
        print "AE(P" + str(p_number_of_nodes) + ",N" + str(g_number_of_nodes) \
                  + ") =", Nim_value
        F_graph = []

            
    # manually inputed graphs with isomorphic graphs
    if menu_choice.lower() == 'g':
        F_graph = raw_input('Input forbidden binary graphs, separated by commas:')
        forbidden_graph_list = cstring_to_intlists(F_graph)
        Nim_value = evaluate_game(1,1, forbidden_graph_list,[0]*len(forbidden_graph_list[0]))
        print "For graphs ", forbidden_graph_list, "Nim value = ", Nim_value
        F_graph = []


    # manually inputed graphs with isomorphic graphs for selected start positions.
    if menu_choice.lower() == 's':
        F_graph = input('Input forbidden binary graphs, separated by commas:')
        forbidden_graph_list = cstring_to_intlists(F_graph)
        start_position = raw_input("Input start position:")
        start_position = string_to_intlist(start_position)
        Nim_value = evaluate_game(1,1, forbidden_graph_list,start_position)
        print "For graphs ", forbidden_graph_list, "Nim value = ", Nim_value
        F_graph = []


    # manually inputed graphs without isomorphic graphs
    if menu_choice.lower() == 'n':
        F_graph = raw_input('No isomorphic graphs: Input forbidden binary graphs, separated by commas:')
        forbidden_graph_list = cstring_to_intlists(F_graph)
        Nim_value = evaluate_game(1,0, forbidden_graph_list,[0]*len(forbidden_graph_list[0]))
        print "For graphs ", forbidden_graph_list, "Nim value = ", Nim_value
        F_graph = []


    # manually inputed graphs without isomorphic graphs for a given start position.
    if menu_choice.lower() == 'n2':
        F_graph = raw_input('No isomorphic graphs: Input forbidden binary graphs, separated by commas:')
        forbidden_graph_list = cstring_to_intlists(F_graph)
        start_position = raw_input("Input start position:")
        start_position = string_to_intlist(start_position)
        Nim_value = evaluate_game(1,0, forbidden_graph_list,start_position)
        print("For graphs ", forbidden_graph_list, "Nim value = ", Nim_value)
        F_graph = []


    menu_choice = ""
    main()
    

main()
